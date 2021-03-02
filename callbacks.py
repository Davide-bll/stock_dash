from dash.dependencies import Input, Output, State
import dash_layout as dashf
import pandas as pd
from callback_manager import CallbackManager

callback_manager = CallbackManager()

# callback updating seasonal figure, TAB2
@callback_manager.callback(Output('tsa_season', 'figure'),
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

# callback for updating residual figure, TAB 2
@callback_manager.callback(Output('tsa_resid', 'figure'),
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

# callback for updating trend figure, TAB 2
@callback_manager.callback(Output('tsa_trend', 'figure'),
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

# callback for updating forecast figure, TAB 3
@callback_manager.callback(Output('forecast', 'figure'),
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
