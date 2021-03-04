
### DASHBOARD  STOCK prices FORECAST real time
Visualize daily stock prices and forecast them real time.

### Demo
You can find a demo of the App, in the following [link](https://demo-forecast-prices.herokuapp.com/)


In the Demo, the data are considered from 2019-01-01 to 2021-04-03, only a few stocks are considered,  and the forecast is calculated in a static 
dataframe (before deploying the App).

### Stock Symbols
To download a stock symbols list, make sure you have 'pytickersymbols' module installed, 
and you have a folder named 'data' in your directory

digit from the terminal:
```
python get\_symbols.py
```

### Run the Dashboard
To run the dashboard, digit from the terminal: 

```
python app.py
```

## Data download
Data are extracted using yahoof API. The series starts from 2019-01-01. 
About 100 NASDAQ symbols are considered.

Tab 1: Data Visualization
======

From the panel you can select the stock prices you want to visualize

![Alt text](img_readme/tab1.jpg?raw=true)

Tab 2: Time Series Analysis
======

Select a single stock from the panel, and push the button to start the tsa. The series is decomposed using the additive
model:
```
y(t) = trend(t) + seasonality(t) + residual.
```
This is an example of the trend component of AAPL

![Alt text](img_readme/tab2.jpg?raw=true)

Tab 3: Forecast results
======

The autoARIMA forecast is plotted.
The forecast computation is reactive, so if you change the stock selected at TAB2, you should wait some seconds
for seeing the updated forecast

![Alt text](img_readme/tab3.jpg?raw=true)


### Modules
 
```
pandas 
datetime 
dash 
yfinance 
pytickersymbols
typing
dataclasses
```

### Defined Modules: 

help\_time\_series\_analysis: deal time series analysys.

dash\_layout: gestisce deal with the dashboard layout

helpers\_functions: generic functions

callbacks_manager: define callbacks decorators outside the app.py file

### next TODOS 
1) check stationarity of the series. 
2) train/test so that other models can be selected and compared 
3) customize length of the series
