# ANALISI SERIE STORICHE

Questo repository contiene un esempio di analisi su dati storici di mercato.
Lo script `analyze_open_close_diff.py` calcola la differenza media tra i prezzi
di apertura e di chiusura e genera un grafico dell'andamento nel tempo.

## Come generare il grafico

1. Assicurati di avere Python 3 installato.
2. Esegui il comando:

   ```bash
   python analyze_open_close_diff.py
   ```

Lo script legge il file `HistoricalData_1760090934890.csv`, calcola la
variazione giornaliera (Close - Open), aggrega i risultati a livello mensile e
salva un grafico SVG in `plots/average_open_close_difference.svg`.
Il grafico consente di visualizzare come la differenza media tra i prezzi di
apertura e chiusura si è evoluta nel tempo.
