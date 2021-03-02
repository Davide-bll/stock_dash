# modules
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.graph_objects as go
from helpers_functions import get_options
from pandas import read_csv

# syms
df_syms = read_csv('data/symbols.csv')

# Clean Data: Keep only main columns
df_syms = df_syms[['name', 'symbol', 'country', 'industries']]


# create layout of the app
def app_layout(app, options, init_val):
    """Create Layout of the app"""

    app.layout = html.Div(
        dcc.Tabs([
            dcc.Tab(label='Data Visualization',
                    children=[
                        html.Div(className='row',
                                 children=[
                                     html.Div(className='four columns div-user-controls',
                                              children=[
                                                  html.H2('DASH - STOCK PRICES'),
                                                  html.P('Pick one or more stocks from the dropdown below.'),
                                                  html.Div(
                                                      className='div-for-dropdown',
                                                      children=[
                                                          dcc.Dropdown(id='stockselector',
                                                                       options=get_options(options),
                                                                       multi=True,
                                                                       value=[init_val],
                                                                       style={'backgroundColor': '#1E1E1E'},
                                                                       className='stockselector'
                                                                       ),
                                                      ],
                                                      style={'color': '#1E1E1E'})
                                              ]),
                                     html.Div(className='eight columns div-for-charts bg-grey',
                                              children=[
                                                  dcc.Graph(id='timeseries', config={'displayModeBar': False},
                                                            animate=True)
                                              ])
                                 ]),
                        html.Div(
                            dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i} for i in df_syms.columns],
                                data=df_syms.to_dict('records'),
                                page_size=20,
                                fixed_rows={'headers': True},
                                style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                                style_cell={
                                    'minWidth': 95, 'maxWidth': 200, 'width': 95,
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white'

                                }
                            )
                        )

                    ]
                    ),
            dcc.Tab(
                label='Time series modelling',
                children=[
                    html.H2('Time Series Decomposition'),
                    html.P('Choose a single stock to analyze'),
                    html.Div(className='div for dropdown',
                             children=[
                                 dcc.Dropdown(id='stockselector_fcst',
                                              options=get_options(options),
                                              multi=False,  # until fixing the button, compute one forecast at a time
                                              value=init_val,
                                              style={'backgroundColor': '#1E1E1E'},
                                              className='stockselector_fcst'
                                              )
                             ],
                             style={'color': '#1E1E1E'}

                             ),
                    html.Div(
                        id='intermediate-value_dec', style={'display': 'none'}
                    ),
                    html.Div(
                        dcc.Graph(id='tsa_season')
                    ),
                    html.Div(
                        dcc.Graph(id='tsa_trend')
                    ),
                    html.Div(
                        dcc.Graph(id='tsa_resid')
                    )
                ]
            ),
            dcc.Tab(label='Forecast of Stock Prices',
                    children=[
                        html.H2('Real Time ARIMA Forecast - 100 step ahead'),
                        html.Div(
                            id='intermediate-value', style={'display': 'none'}
                        ),
                        html.Div(
                            dcc.Graph(id='forecast', animate=True)
                        )
                    ])

        ]

        )

    )


def scatter_figure(trace, min_range, max_range, text_title):
    """
    Return a figure of the input Scatter trace.
    :param trace: List of plotly graph object go.scatter
    :param min_range:   x min value
    :param max_range:   x max value
    :return: a figure
    """
    figure = {'data': trace,
              'layout': go.Layout(
                  # colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 1)',
                  plot_bgcolor='rgba(0, 0, 0, 1)',
                  margin={'b': 10},
                  hovermode='x',
                  autosize=True,
                  title={'text': text_title, 'font': {'color': 'black'}, 'x': 0.5},
                  xaxis={'range': [min_range, max_range]},
              )
              }

    return figure


def go_scatter(x, y, name, mode='lines', opacity=0.7, textposition='bottom center', showlegend=True):
    """ return a Plotly Scatter object"""
    res = go.Scatter(x=x,
                     y=y,
                     mode=mode,
                     opacity=opacity,
                     name=name,
                     textposition=textposition,
                     showlegend=showlegend
                     )
    return res
