
### DASHBOARD per STOCK prices FORECAST real time
La dashboard visualizza e calcola il forecast dei prezzi stock.

### Simboli degli stocks
Per scaricare la lista di simboli, installare il modulo pytickersymbols
e creare una cartella nella directory chiamata "data"

da terminale:
```
python get\_symbols.py
```

### Avvia la dashboard
per avviare la dashboard, da terminale, digitare: 

```
python app.py
```

## Estrazione Dati

I dati vengono estratti usando l'API di yahoo finance. La serie storica
parte dal 2019/01/01. Vengono considerati circa 100 indici Nasdaq.

Tab 1: Data Visualization
======


Dal pannelllo si possono scegliere uno o piu indici da visualizzare.

![Alt text](img_readme/tab1.png?raw=true)

Tab 2: Time series analysis
======


Dal pannelllo viene selezionato un singolo stock, di cui viene calcolato
automaticamente il forecast usando la funzione autoArima, che sceglie il
modello ARIMA piu appropriato. La serie viene decomposta usando il
modello additivo: 
```
y(t) = trend(t) + seasonality(t) + residual.
```
Le tre componenti della serie vengono visualizzate.

![Alt text](img_readme/tab2.png?raw=true)

Tab 3: Forecast results
======

Forecast visualization Viene visualizzato il forecast calcolato Real
time.

Il forecast è calcolato in modo reattivo, quando si seleziona un altro
indice nel secondo TAB, l'immagine viene aggiornata, dopo che il forecast viene ricalcolato

![Alt text](img_readme/tab3.png?raw=true)


### Moduli
moduli utilizzati 
pandas 

datetime 

dash 

yfinance 

pytickersymbols


### Moduli definiti: 

help\_time\_series\_analysis: aiuta a gestire l'analisi
di serie storiche.

dash\_layout: gestisce il layout della dashboard

helpers\_functions: funzioni generiche

### next TODOS 
1) Verifica di ipotesi della stazionarietà della serie. 
2) Divisione train e test dei dati in modo da poter confrontare modelli di
forecast diversi. (ets, tslm ecc.. ) e non solo autoarima. 
3) l'utente non ha la possibilità di scegliere la lunghezza della serie. aggiongere
uno slider per mettere inizio e fine serie storica come input.
