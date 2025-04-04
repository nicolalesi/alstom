import spacy
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os


# Carica il modello di linguaggio di Spacy
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
    #similarita_max = 0
    colonna_selezionata = set()

    for colonna, parole_chiave in categorie.items():
        for parola in parole_chiave:
            doc_parola = nlp(parola.lower())
            if doc_parola.has_vector:  # Evita parole senza embedding
                similarita = doc_input.similarity(doc_parola)
                if similarita >= soglia:
                    #similarita_max = similarita
                    colonna_selezionata.add(colonna)

    return colonna_selezionata

def checkErrors(df, colonne):
    """Controlla se almeno una delle colonne ha il valore 1 e avvia 'analisiDettaglio.py' se necessario."""
    df.columns = df.columns.str.strip().str.lower()
    colonne_norm = [col.strip().lower() for col in colonne]

    errore_trovato = False

    for colonna_norm in colonne_norm:
        if colonna_norm in df.columns:
            df[colonna_norm] = pd.to_numeric(df[colonna_norm], errors='coerce')

            if (df[colonna_norm] == 1).any():
                errore_trovato = True

    if errore_trovato:
        print("Eseguo analisiDettaglio.py...")
        os.system("python analisiDettaglioRaffinata.py")

# Funzione per gestire il caricamento del file Excel tramite la GUI
def carica_file():
    percorso_file = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if percorso_file:
        colonne, df = carica_dati_excel(percorso_file)
        return df, colonne
    else:
        messagebox.showerror("Errore", "Nessun file selezionato!")
        return None, None

# Funzione per eseguire l'elaborazione quando l'utente invia il testo
def esegui_analisi():
    testo_input = testo_entry.get()
    if not testo_input:
        messagebox.showerror("Errore", "Inserisci un testo!")
        return

    # Carica il file Excel e trova la colonna corrispondente
    df, colonne = carica_file()
    if df is None:
        return

    colonna_trovata = trova_colonna_corrispondente(testo_input, categorie)
    if colonna_trovata:
        messagebox.showinfo("Analisi completata", f"Colonna identificata: {colonna_trovata}")
        checkErrors(df, colonna_trovata)
    else:
        messagebox.showerror("Errore", "Nessuna corrispondenza trovata nel testo.")

# Creazione dell'interfaccia grafica con Tkinter
root = tk.Tk()
root.title("Analisi Dati WC Fuori Servizio")

# Creazione del frame principale
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Label e Entry per il testo
testo_label = tk.Label(frame, text="Inserisci il testo:")
testo_label.grid(row=0, column=0, padx=10, pady=10)

testo_entry = tk.Entry(frame, width=40)
testo_entry.grid(row=0, column=1, padx=10, pady=10)

# Bottone per eseguire l'analisi
analizza_button = tk.Button(frame, text="Esegui Analisi", command=esegui_analisi)
analizza_button.grid(row=1, columnspan=2, pady=20)

# Avvia l'interfaccia grafica
root.mainloop()
