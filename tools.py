import json

CENTRO_SPORTIVO_DATA = {
    "nome": "Baricentro Sport & Wellness",
    "indirizzo": "Via Bernardo Quartanta 12, Bari",
    "orari": {
        "lunedi_venerdi": "07:00 - 22:30",
        "sabato": "08:30 - 19:00",
        "domenica": "09:00 - 13:00"
    },
    "corsi": [
        {"nome": "Padel Pro", "giorni": "Lun-Mer-Ven", "orario": "18:00", "istruttore": "Marco"},
        {"nome": "CrossFit", "giorni": "Mar-Gio", "orario": "19:00", "istruttore": "Elena"},
        {"nome": "Nuoto Libero & Corsi", "giorni": "Tutti i giorni", "orario": "Vedi orari apertura", "istruttore": "Squadra Nuoto"},
        {"nome": "Yoga Flex", "giorni": "Sabato", "orario": "10:00", "istruttore": "Sara"}
    ]
}


def get_orari_e_info() -> str:
    """Restituisce orari di apertura e indirizzo del centro sportivo."""
    return json.dumps({
        "nome": CENTRO_SPORTIVO_DATA["nome"],
        "indirizzo": CENTRO_SPORTIVO_DATA["indirizzo"],
        "orari": CENTRO_SPORTIVO_DATA["orari"]
    }, ensure_ascii=False)

def get_lista_corsi(categoria: str = None) -> str:
    """Restituisce l'elenco dei corsi disponibili."""
    corsi = CENTRO_SPORTIVO_DATA["corsi"]
    if categoria:
        corsi = [c for c in corsi if categoria.lower() in c["nome"].lower()]
    return json.dumps(corsi, ensure_ascii=False)

def prenota_appuntamento(nome_utente: str, servizio_o_corso: str, giorno: str, ora: str) -> str:
    """Simula la prenotazione di una lezione o appuntamento."""
    return json.dumps({
        "stato": "confermato",
        "messaggio": f"Prenotazione confermata per {nome_utente}!",
        "dettagli": {
            "servizio": servizio_o_corso,
            "giorno": giorno,
            "ora": ora,
            "sede": CENTRO_SPORTIVO_DATA["nome"]
        }
    }, ensure_ascii=False)



TOOLS_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_orari_e_info",
            "description": "Ottieni gli orari di apertura, i giorni di attivita e l'indirizzo del centro sportivo a Bari.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_lista_corsi",
            "description": "Consulta il palinsesto dei corsi sportivi, orari delle lezioni e istruttori del centro.",
            "parameters": {
                "type": "object",
                "properties": {
                    "categoria": {
                        "type": "string",
                        "description": "Filtro opzionale per cercare uno specifico corso (es. Padel, Yoga, Nuoto, CrossFit)."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prenota_appuntamento",
            "description": "Effettua la prenotazione di una lezione, campo o appuntamento presso il centro sportivo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_utente": {"type": "string", "description": "Nome e cognome dell'utente che prenota."},
                    "servizio_o_corso": {"type": "string", "description": "Il corso o campo da prenotare (es. Campo Padel, Lezione Yoga)."},
                    "giorno": {"type": "string", "description": "Giorno richiesto per la prenotazione (es. Lunedi, 15 Ottobre)."},
                    "ora": {"type": "string", "description": "Orario richiesto (es. 18:00)."}
                },
                "required": ["nome_utente", "servizio_o_corso", "giorno", "ora"]
            }
        }
    }
]

AVAILABLE_TOOLS = {
    "get_orari_e_info": get_orari_e_info,
    "get_lista_corsi": get_lista_corsi,
    "prenota_appuntamento": prenota_appuntamento
}