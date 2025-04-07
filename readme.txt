############## Struttura ###########
- analisiTesto.py --> Vengono mappati dei termini relativi alle colonne di errore, in modo che spacy possa riconoscere la similarità semantica tra la frase in input e le colonne 
- analisiDettaglio.py --> Attraverso l'utilizzo di spacy viene generato un input in linguaggio naturale, c'è bisogno di mappature dei dati, quindi in realtà non è così comodo per generare output, ma permette una maggiore manipolazione
- analisiDettaglioRaffinata.py --> Attraverso l'utilizzo di Ollama https://ollama.com/ diamo in input un prompt e il file e facciamo in modo di generare un output simile a quello nel pdf, va ancora affinato, ollama permette la verticalizzazione 
                                    è possibile utilizzare anche le API di GPT4 ma sono a pagamento.
- analisiDinamica.py --> Può essere ignorato


########### HOW TO TEST ############
python analisiTesto.py      or double click

# 🧠 Analisi Eventi Tecnici da File Excel

Questo progetto automatizza l'analisi di eventi tecnici (es. "WC fuori servizio") da file Excel, generando report con AI.

## 📂 Script

- `analisiTesto.py`: GUI che riceve un testo in input, lo confronta semanticamente con le colonne del file Excel e avvia l’analisi dettagliata se trova errori.
- `analisiDettaglioRaffinata.py`: Estrae eventi tecnici dal file, analizza i contatori, genera un report con un LLM locale (via Ollama) e mostra tutto in una GUI.

## ✅ Requisiti

```bash
pip install pandas spacy openpyxl
python -m spacy download it_core_news_lg
pip install ollama

https://ollama.com/ --> Bisogna scaricarlo e poi fare anche
ollama pull mistral


###  Miglioramenti   
- Input parametrico in analisiDettaglioRaffinata.py e non fissa
- Valutazione di utilizzo di un modello diverso (altri modelli ollama o gpt)
- Modellazione e raffinazione del prompt in entrata, ad esempio se ci si vuole soffermare su determinati orari si possono estrarre e passare al prompt solo gli eventi in quel range di tempo
- Aggiungere anche gli orari in cui avvengono gli eventi
