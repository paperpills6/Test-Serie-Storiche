# ANALISI SERIE STORICHE

Questo repository contiene un esempio di analisi su dati storici di mercato.
Il notebook `Average_Open_Close_Difference.ipynb` calcola la differenza media
tra i prezzi di apertura e di chiusura e produce un grafico dell'andamento nel
tempo utilizzando Matplotlib.

## Come esplorare il notebook

1. Assicurati di avere Python 3, Jupyter Notebook e le dipendenze necessarie
   (`pandas` e `matplotlib`).
2. Avvia l'ambiente Jupyter dalla cartella del progetto:

   ```bash
   jupyter notebook
   ```

3. Apri il file `Average_Open_Close_Difference.ipynb` e segui le celle per
   eseguire l'analisi e visualizzare il grafico interattivamente.

Il notebook legge il file `HistoricalData_1760090934890.csv`, calcola la
variazione giornaliera (Close - Open), aggrega i risultati a livello mensile e
mostra un grafico che permette di osservare come la differenza media tra i
prezzi di apertura e chiusura si è evoluta nel tempo.
