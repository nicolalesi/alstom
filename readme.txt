Requisiti:
pip install spacy
python -m spacy download it_core_news_lg

pip install pandas
install ollama following the online doc

############## Struttura ###########
- analisiTesto.py --> Vengono mappati dei termini relativi alle colonne di errore, in modo che spacy possa riconoscere la similarità semantica tra la frase in input e le colonne 
- analisiDettaglio.py --> Attraverso l'utilizzo di spacy viene generato un input in linguaggio naturale, c'è bisogno di mappature dei dati, quindi in realtà non è così comodo per generare output, ma permette una maggiore manipolazione
- analisiDettaglioRaffinata.py --> Attraverso l'utilizzo di Ollama https://ollama.com/ diamo in input un prompt e il file e facciamo in modo di generare un output simile a quello nel pdf, va ancora affinato, ollama permette la verticalizzazione 
                                    è possibile utilizzare anche le API di GPT4 ma sono a pagamento.
- analisiDinamica.py --> Può essere ignorato