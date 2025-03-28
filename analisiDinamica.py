import spacy
import pandas as pd


# Carica il modello di spaCy con word embeddings
nlp = spacy.load("it_core_news_lg")

def carica_dati_excel(percorso_file):
    """Carica il file Excel e restituisce i nomi delle colonne e i dati."""
    df = pd.read_excel(percorso_file)
    return df.columns.tolist(), df

def trova_colonna_corrispondente(testo, colonne):
    """Trova la colonna più simile al testo in base alla similarità semantica."""
    doc_input = nlp(testo.lower())
    similarita_max = 0
    colonna_selezionata = "Nessuna corrispondenza"
    
    for colonna in colonne:
        doc_colonna = nlp(colonna.lower())
        similarita = doc_input.similarity(doc_colonna)
        
        if similarita > similarita_max:
            similarita_max = similarita
            colonna_selezionata = colonna
    
    return colonna_selezionata

# Esempio di utilizzo
percorso_excel = "GENERALE_CASO_TOILETTE_FUORI_SERVIZIO.xlsx"  # Sostituisci con il tuo file Excel
colonne, df = carica_dati_excel(percorso_excel)

testo_input = "Il bagno è fuori servizio e nessuno lo sta riparando."
colonna_trovata = trova_colonna_corrispondente(testo_input, colonne)

print(f"Colonna identificata: {colonna_trovata}")
