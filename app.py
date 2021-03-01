import dash
import pandas as pd
from dash.dependencies import Input, Output, State
import datetime as date
import yfinance as yf

# defined modules
import dash_layout as dashf
import help_time_series_analysis as htsa

# Input Parameters
file_name = 'symbols'
folder = 'data'
path_file = folder + '/' + file_name + '.csv'
testing = False

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
    stock_options = stock_options[0:10]

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
app.config.suppress_callback_exceptions = True

# create layout of the app
dashf.app_layout(app, stock_options, initial_value)

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

@app.callback(Output('intermediate-value_dec', 'children'),
              Input('stockselector_fcst', 'value'))
def create_decomposed(input_value):
    """ update decomposed series dataframe """
    # decompose series using additive model
    df_dec = htsa.deco_series(df[input_value])

    return df_dec.to_json(date_format='iso', orient='split')


@app.callback(Output('tsa_season', 'figure'),
              Input('intermediate-value_dec', 'children'))
def update_seasonal(json_data):
    """ update seasonal component figure"""
    df_season = pd.read_json(json_data, orient='split')

    trace1 = []

    # append plotly object
    trace1.append(dashf.go_scatter(x=df_season.index, y=df_season['seasonal'], name='seasonal'))

    # update figure
    figure = dashf.scatter_figure(trace1, min_range=df_season.index.min(), max_range=df_season.index.max(),
                                  text_title='Seasonal Component')

    return figure


@app.callback(Output('tsa_trend', 'figure'),
              Input('intermediate-value_dec', 'children'))
def update_trend(json_data):
    """ update trned component figure"""
    df_season = pd.read_json(json_data, orient='split')

    trace1 = []

    # append plotly object
    trace1.append(dashf.go_scatter(x=df_season.index, y=df_season['trend'], name='trend'))

    # update figure
    figure = dashf.scatter_figure(trace1, min_range=df_season.index.min(), max_range=df_season.index.max(), text_title='Trend Component')

    return figure


@app.callback(Output('tsa_resid', 'figure'),
              Input('intermediate-value_dec', 'children'))
def update_residual(json_data):
    """ update residual figure"""
    df_season = pd.read_json(json_data, orient='split')

    trace1 = []

    # append plotly object
    trace1.append(dashf.go_scatter(x=df_season.index, y=df_season['resid'], name='residuals'))

    # update figure
    figure = dashf.scatter_figure(trace1, min_range=df_season.index.min(), max_range=df_season.index.max(),
                                  text_title='Residuals')

    return figure


##### TAB 3
@app.callback(Output('intermediate-value', 'children'),
              Input('stockselector_fcst', 'value'))
def create_forecast(input_value):
    """ update forecast dataframe"""
    list_df = []

    # create 100 step ahed forecast
    df_fcst = htsa.forecast_stock(x=df[input_value], n=n, xreg=xreg)['df']

    # return json file
    return df_fcst.to_json(date_format='iso', orient='split')


@app.callback(Output('forecast', 'figure'),
              [Input('intermediate-value', 'children')])
def update_forecast(json_data):
    """ update forecast figure"""
    df_fcst = pd.read_json(json_data, orient='split')
    trace_f = []
    selected_stocks = df_fcst.columns.tolist()
    selected_stocks = [stock for stock in selected_stocks if stock != 'type_obs']
    type_obs = df_fcst['type_obs'].unique().tolist()

    for stock in selected_stocks:
        # loop over types to differentiate forecast vs observed
        for observed_type in type_obs:
            x = df_fcst[df_fcst['type_obs'] == observed_type][stock].index
            y = df_fcst[df_fcst['type_obs'] == observed_type][stock]
            tmp_name = observed_type + ' ' + stock
            # append Plotly object
            trace_f.append(dashf.go_scatter(x=x, y=y, name=tmp_name))

    figure = dashf.scatter_figure(trace=trace_f, min_range=df_fcst.index.min(), max_range=df_fcst.index.max(),
                                  text_title='Stock Prices Forecast')

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
