import spacy
import pandas as pd

nlp = spacy.load("it_core_news_lg")

# Dizionario che associa le colonne del file Excel a parole chiave
categorie = {
    "TO1:WC Fuori Servizio": ["bagno", "wc", "toilette", "gabinetto", "latrina", "servizi", "water", "restroom", "lavatory", "servizi igienici"],
    "TO2:WC Fuori Servizio": ["bagno", "wc", "toilette", "gabinetto", "latrina", "servizi", "water", "restroom", "lavatory", "servizi igienici"]
}

def carica_dati_excel(percorso_file):
    """Carica il file Excel e restituisce i nomi delle colonne e i dati."""
    df = pd.read_excel(percorso_file)
    return df.columns.tolist(), df

def trova_colonna_corrispondente(testo, categorie,soglia=0.2):
    """Trova la colonna più simile al testo in base alla similarità semantica."""
    doc_input = nlp(testo.lower())
    similarita_max = 0
    colonna_selezionata = set()

    for colonna, parole_chiave in categorie.items():
        for parola in parole_chiave:
            doc_parola = nlp(parola.lower())
            if doc_parola.has_vector:  # Evita parole senza embedding
                similarita = doc_input.similarity(doc_parola)
                #print(f"Similarità tra '{testo}' e '{parola}': {similarita:.2f}")  # Debug: visualizza la similarità
                if similarita >= similarita_max:
                    similarita_max = similarita
                    colonna_selezionata.add(colonna)

    return colonna_selezionata

# Esempio di utilizzo
percorso_excel = "dati/DETTAGLIO_CASO_TOILETTE_FUOR_SERVIZIO.xlsx"  # Sostituisci con il tuo file Excel
colonne, df = carica_dati_excel(percorso_excel)

testo_input = "Il bagno è fuori servizio e nessuno lo sta riparando."
colonna_trovata = trova_colonna_corrispondente(testo_input, categorie)

print(f"Colonna identificata: {colonna_trovata}")
#Se il testo è generico e non troviamo un matching controlliamo tutte le colonne che potrebbero avere degli errori (stabilite a prescindere)
#Altrimenti si dà priorità al testo

