import dash
import pandas as pd
from dash.dependencies import Input, Output, State
import datetime as date
import yfinance as yf

# defined modules
import dash_layout as dashf
import help_time_series_analysis as htsa
from callbacks import callback_manager

# Input Parameters
file_name = 'symbols'
folder = 'data'
path_file = folder + '/' + file_name + '.csv'
# if true, download only 5 stocks.
testing = True

# time of the analysis
start_date = date.date(2019, 1, 1)
end_date = date.date.today()

# forecast step ahead
n: int = 100

# Load stock symbols
df_syms = pd.read_csv(path_file, index_col=0)

# Clean Data: Keep only main columns
df_syms = df_syms[['name', 'symbol', 'country', 'industries']]

# extract symbols
stock_options = df_syms['symbol'].unique().tolist()

# small list for testing
if testing:
    stock_options = stock_options[0:5]

# Download static dataframe from yf
df = yf.download(stock_options, start=start_date, end=end_date, progress=True)

# drop stock with all NA
df = df.dropna(axis=1, how='all')

# Consider Open price
df = df.Open

# Redefine stock options: show only the one for which you have data
stock_options = list(df.columns)
initial_value = stock_options[0]

# add xregressors: dummy for days of the week (and months?)
df['dow'] = df.index.to_series().dt.dayofweek
xreg = df['dow']

# Initialize the app
app = dash.Dash(__name__)
server = app.server

# create layout of the app
dashf.app_layout(app, stock_options, initial_value)

#### CALLBACKS decorator that use GLOBAL variables df
#### TAB 1
# Callback for past timeseries price visualization
@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    """update stock price figure """
    trace1 = []
    df_sub = df

    for stock in selected_dropdown_value:
        # append Plotly Scatter object
        trace1.append(dashf.go_scatter(x=df_sub.index, y=df_sub[stock], name=stock))

    # Update figure
    figure = dashf.scatter_figure(trace1, min_range=df_sub.index.min(), max_range=df_sub.index.max(),
                                  text_title='Stock Prices')

    return figure


#### TAB2

@app.callback(Output(component_id='intermediate-value_dec', component_property='children'),
              [Input('button', 'n_clicks'),
               State(component_id='stockselector_fcst', component_property='value')])
def create_decomposed(n_clicks, input_value):
    """ update decomposed series dataframe """
    # decompose series using additive model
    df_dec = htsa.deco_series(df[input_value])

    return df_dec.to_json(date_format='iso', orient='split')


##### TAB 3
@app.callback(Output('intermediate-value', 'children'),
              [Input('button', 'n_clicks'),
               State(component_id='stockselector_fcst', component_property='value')])
def create_forecast(n_clicks, input_value):
    """ update forecast dataframe"""
    list_df = []

    # create 100 step ahed forecast
    df_fcst = htsa.forecast_stock(x=df[input_value], n=n, xreg=xreg)['df']

    # return json file
    return df_fcst.to_json(date_format='iso', orient='split')


# attachetd outside defined callbacks. They only use reactive values
callback_manager.attach_to_app(app=app)

if __name__ == '__main__':
    app.run_server(debug=True)
