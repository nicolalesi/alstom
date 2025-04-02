import spacy
import pandas as pd

nlp = spacy.load("it_core_news_lg")

# Dizionario che associa le colonne del file Excel a parole chiave
categorie = {
    "TOI1:WC Fuori Servizio": ["bagno", "wc", "toilette", "gabinetto", "latrina", "servizi", "water", "restroom", "lavatory", "servizi igienici"],
    "TOI2:WC Fuori Servizio": ["bagno", "wc", "toilette", "gabinetto", "latrina", "servizi", "water", "restroom", "lavatory", "servizi igienici"]
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

import os

import os
import pandas as pd

def checkErrors(df, colonne):
    """Controlla se almeno una delle colonne ha il valore 1 e avvia 'analisiDettaglio.py' se necessario."""

    # Normalizziamo i nomi delle colonne nel DataFrame
    df.columns = df.columns.str.strip().str.lower()

    # Normalizziamo i nomi delle colonne in input
    colonne_norm = [col.strip().lower() for col in colonne]

    errore_trovato = False  # Flag per verificare se ci sono valori 1

    for colonna_norm in colonne_norm:
        if colonna_norm in df.columns:
            print(f"🔍 Controllando colonna: {colonna_norm}")  # Debug

            # Convertiamo la colonna in numerico (forza '1' stringa -> 1 numero)
            df[colonna_norm] = pd.to_numeric(df[colonna_norm], errors='coerce')

            # Stampiamo un'anteprima dei valori per debugging
            print(f"📊 Valori unici nella colonna {colonna_norm}: {df[colonna_norm].unique()}")

            # Controlliamo se almeno un valore è 1
            if (df[colonna_norm] == 1).any():
                print(f"⚠️ Trovato almeno un '1' nella colonna '{colonna_norm}'")
                errore_trovato = True
            else:
                print(f"✅ Nessun '1' trovato nella colonna '{colonna_norm}'")
        else:
            print(f"❌ La colonna '{colonna_norm}' non esiste nel DataFrame.")

    # Se c'è almeno un '1', esegui lo script "analisiDettaglio.py"
    if errore_trovato:
        print("🚀 Eseguo analisiDettaglio.py...")
        os.system("python analisiDettaglio.py")  # Esegui lo script
        #ora il path di dettaglio è predefinito in analisiDettaglio, ma richiamando lo script può essere passato come parametro


# Esempio di utilizzo

#Questo sarebbe poi da rendere generico per tutti, andrebbe estratta la parte finale del generale e ricavarsi il dettaglio oppure si passano in input
percorso_excel = "dati/GENERALE_CASO_TOILETTE_FUORI_SERVIZIO.xlsx"  # Sostituisci con il tuo file Excel
colonne, df = carica_dati_excel(percorso_excel)

testo_input = "Il bagno è fuori servizio e nessuno lo sta riparando."
colonna_trovata = trova_colonna_corrispondente(testo_input, categorie)

print(f"Colonna identificata: {colonna_trovata}")
#Se il testo è generico e non troviamo un matching controlliamo tutte le colonne che potrebbero avere degli errori (stabilite a prescindere)
#Altrimenti si dà priorità al testo
#print(df.columns.tolist())

checkErrors(df, colonna_trovata)
