import pandas as pd
import ollama

def estrai_dati(file_path):
    """Estrae e rielabora gli eventi dal file Excel."""
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name="Scarico REGISTRAZIONI")
    
    accensione = df.iloc[2, 0]  # Supponiamo che il primo orario valido sia qui
    data_analisi = accensione[:5]
    ora_accensione = accensione[-5:]
    
    eventi = []
    for index, row in df.iterrows():
        if isinstance(row.iloc[1], str):
            eventi.append(f"{row.iloc[0]} - {row.iloc[1]}")
    
    return data_analisi, ora_accensione, eventi

def genera_report_con_llm(data_analisi, ora_accensione, eventi):
    """Genera il report utilizzando un LLM locale tramite Ollama."""
    prompt = f"""
    Sei un tecnico esperti di treni, stai leggendo un report dettagliato di un treno,
    Genera un report in linguaggio naturale basato sui seguenti eventi:

    Data: {data_analisi}
    Ora di accensione: {ora_accensione}
    Eventi registrati:
    """
    
    for evento in eventi:
        prompt += f"- {evento}\n"
    
    prompt += """
    
    Il report deve essere strutturato come segue:
    1.Introduzione con data e ora di accensione.
    2.Descrizione chiara e fluida degli eventi.
    3.Conclusione che riassume la situazione generale.
    4. Riassunto che scriva semplicemente se alla fine del file gli impianti in esame sono in funzione o meno.
    
    Scrivi il report basandoti unicamente sugli eventi presenti nel file.

    """
    #Per quanto riguarda i contatori dovremmo passargli i dati come già facciamo negli eventi e poi farglieli elaborare come nel reoprt
    risposta = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': prompt}])
    return risposta['message']['content']

# Percorso del file
file_path = "dati/DETTAGLIO_CASO_TOILETTE_FUOR_SERVIZIO.xlsx"
data_analisi, ora_accensione, eventi = estrai_dati(file_path)
report = genera_report_con_llm(data_analisi, ora_accensione, eventi)
print(report)
