import pandas as pd
import spacy

# Carica il modello linguistico italiano di spaCy
nlp = spacy.load("it_core_news_lg")

def elabora_evento(evento):
    """
    Riformula l'evento tecnico in un linguaggio più naturale.
    """
    doc = nlp(evento)
    
    # Regole per interpretare gli eventi
    if "SW in blocco" in evento:
        return "Il software di gestione della toilette ha subito un blocco."
    elif "WC Libero" in evento:
        return "Il WC è ora disponibile per l'uso."
    elif "Serbatoio acque scure > 80%" in evento:
        return "Il serbatoio delle acque scure ha superato l'80% della capacità."
    elif "Porta chiusa" in evento:
        return "La porta della toilette è stata chiusa."
    elif "WC Fuori servizio" in evento:
        return "Il WC è attualmente fuori servizio."
    elif "Bassa pressione alimentazione aria" in evento:
        return "C'è un problema di bassa pressione nell'alimentazione dell'aria."
    elif "Avaria sistema scarico tazza" in evento:
        return "Si è verificato un guasto al sistema di scarico della toilette."
    elif "Comando svuotamento tubazioni WC" in evento:
        return "È stato attivato il comando di svuotamento delle tubazioni del WC."
    elif "WC occupato" in evento:
        return "Il WC è attualmente occupato."
    else:
        return f"Evento rilevato: {doc.text}"  # Se l'evento non è riconosciuto, lo restituisce così com'è.

def genera_spiegazioni(file_path):
    # Leggi il file Excel senza intestazioni automatiche
    df = pd.read_excel(file_path, header=None)

    # Imposta la seconda riga come intestazione
    df.columns = df.iloc[1]  
    df = df[2:].reset_index(drop=True)

    # Trova la colonna "EVENTO"
    colonna_evento = "EVENTO" if "EVENTO" in df.columns else df.columns[1]

    # Filtra solo le righe con eventi validi
    df_filtrato = df.dropna(subset=[colonna_evento])

    spiegazioni = []
    for _, row in df_filtrato.iterrows():
        evento = str(row[colonna_evento])  # Converti in stringa per sicurezza
        spiegazione = elabora_evento(evento)
        spiegazioni.append(spiegazione)

    return spiegazioni

# Percorso del file Excel
file_path = "dati/DETTAGLIO_CASO_TOILETTE_FUOR_SERVIZIO.xlsx"

# Genera spiegazioni
spiegazioni = genera_spiegazioni(file_path)

# Stampa le prime 10 spiegazioni
for spiegazione in spiegazioni[:10]:
    print(spiegazione)
