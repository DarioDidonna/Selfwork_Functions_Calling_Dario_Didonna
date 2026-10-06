import os
import json
import chainlit as cl
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS_DEFINITIONS, AVAILABLE_TOOLS

# Carica le variabili d'ambiente (.env)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("⚠️ OPENAI_API_KEY non trovata nel file .env!")

# Client OpenAI nativo
client = OpenAI(api_key=api_key)
MODEL_NAME = "gpt-4o-mini"

SYSTEM_PROMPT = """
Sei l'assistente virtuale ufficiale del 'Baricentro Sport & Wellness', un centro sportivo situato a Bari.
Il tuo compito e aiutare gli utenti fornendo informazioni accurate su orari, corsi, lezioni e permettere loro di prenotare appuntamenti.

REGOLE IMPORTANTI:
1. Per rispondere a domande su orari, indirizzo, corsi o prenotazioni, DEVI SEMPRE utilizzare i tool forniti.
2. Sii cordiale, accogliente e professionale.
"""


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("messages", [{"role": "system", "content": SYSTEM_PROMPT}])
    
    await cl.Message(
        content="🏋️‍♂️ **Benvenuto al Baricentro Sport & Wellness di Bari!**\n\nCome posso aiutarti oggi? Puoi chiedermi informazioni su corsi, orari di apertura o prenotare una lezione."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    messages = cl.user_session.get("messages")
    if not messages:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    messages.append({"role": "user", "content": message.content})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS_DEFINITIONS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            messages.append({
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in response_message.tool_calls
                ]
            })

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                async with cl.Step(name=f"🛠️ Esecuzione Tool: {function_name}") as step:
                    step.input = function_args
                    
                    if function_name in AVAILABLE_TOOLS:
                        function_to_call = AVAILABLE_TOOLS[function_name]
                        tool_output = function_to_call(**function_args)
                    else:
                        tool_output = json.dumps({"error": f"Tool {function_name} non trovato."})
                    
                    step.output = tool_output

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_output
                })

            final_response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages
            )
            final_content = final_response.choices[0].message.content or "Operazione completata."
            messages.append({"role": "assistant", "content": final_content})
            
            await cl.Message(content=final_content).send()

        else:
            final_content = response_message.content or "Spiacente, non ho compreso la richiesta."
            messages.append({"role": "assistant", "content": final_content})
            
            await cl.Message(content=final_content).send()

    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        await cl.Message(content=f"⚠️ **Si è verificato un errore:** {e}").send()

    cl.user_session.set("messages", messages)
