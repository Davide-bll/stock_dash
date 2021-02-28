readme file per stock dash


DASHBOARD per FORECAST tempo reale 

### estrazione dati

I dati vengono estratti usando l'API di yahoo finance.
La serie storica parte dal 2019/01/01. 
Vengono considerati circa 100 indici Nasdaq.

# Tab 1) 
Data visualization

Dal pannelllo si possono scegliere uno o piu indici da visualizzare.
I grafici sono interattivi. (Plotly package)

# Tab 2) 

Time series analysis

Dal pannelllo viene selezionato un singolo stock, di cui viene calcolato automaticamente 
il forecast usando la funzione autoArima, che sceglie il modello ARIMA piu appropriato.
La serie viene decomposta usando il modello additivo:
y(t) = trend(t) + seasonality(t) + residual.

Le tre componenti della serie vengono visualizzate.


# Tab 3) 
 Forecast visualization
 
 Viene visualizzato il forecast calcolato Real time.
 
 
TODOS 

1)
Verifica di ipotesi della stazionarietà della serie.
2) 
Divisione train e test dei dati in modo da poter confrontare modelli di forecast diversi.
(ets, tslm ecc.. ) e non solo autoarima.
3)
l'utente non ha la possibilità di scegliere la lunghezza della serie. aggiongere uno slider 
per mettere inizio e fine serie storica come input.