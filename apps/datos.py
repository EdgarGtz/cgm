import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd




# Connect to to data

    # Connect to Google Drive

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

    # Connect to the spreadsheet

spreadsheet_key = '1BgqV1yRoBot-EcGNySlkUA2PjwU56HP7mekxXDMt3qA'
book = gc.open_by_key(spreadsheet_key)

    # Connect to the tabs

monitoreo = book.worksheet('reportes_dia')
monitoreo = monitoreo.get_all_values()


# Reportes por fuente - stacked bar

monitoreo = pd.DataFrame(monitoreo[1:], columns = monitoreo[0])

monitoreo = px.histogram(monitoreo, x = 'fecha', y = 'reportes', color='Fuente',
                labels={
                    'fecha':'',
                    'reportes':'reportes' 
                },
                color_discrete_map={
                'Waze': '#00CC96',
                '#911 (C5)': '#EF553B',
                'Agentes de Tránsito': '#636EFA',
                'CIAC':'#FECB52'
                }
            )


# Layout

def datos():

    return html.Div([

        # Tabs

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Monitoreo de Tráfico', tab_id='datos_monitoreo'),
                            dbc.Tab(label='Cerrar Vialidades', tab_id="datos_vialidades",
                                disabled=True)],
                            id='tabs',
                            active_tab="datos_monitoreo",
                            card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="datos_content"))
                ], style={'min-height': '100vh'})
            ), justify = 'center'
        ),

        #Footer 

        dbc.Row(
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México')
            ), className='px-3 py-4', style={'background-color': 'black','color': 'white'}
        )

    ])


# Monitoreo de Tráfico

def datos_monitoreo():

    return html.Div([

        # Header

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        html.H4('Reportes Totales', 
                            style={'text-align':'left'})
                    )
                )
            ),

            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        html.P('12 de abril al 18 de abril 2021', 
                            style={'text-align':'center'})
                    )
                ), lg=4
            )

        ]),

        html.Br(),


        # Reportes por fuente - tarjetas

        dbc.Row([

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Todos"),
                    dbc.CardBody([
                        html.H1("300", className="card-text",
                            style={'display':'inline-block'}),
                        html.P("(100%)", style={'display':'inline-block'},
                            className='pl-2')
                    ])  
                ])
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("#911 (C5)"),
                    dbc.CardBody([
                        html.H1("90", className="card-text",
                            style={'display':'inline-block'}),
                        html.P("(30%)", style={'display':'inline-block'},
                            className='pl-2')
                    ]) 
                ], color='danger', outline='true')
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Agentes de Tránsito"),
                    dbc.CardBody([
                        html.H1("165", className="card-text",
                            style={'display':'inline-block'}),
                        html.P("(55%)", style={'display':'inline-block'},
                            className='pl-2')
                    ]) 
                ], color='primary', outline='True')
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("CIAC"),
                    dbc.CardBody([
                        html.H1("33", className="card-text",
                            style={'display':'inline-block'}),
                        html.P("(11%)", style={'display':'inline-block'},
                            className='pl-2')
                    ]) 
                ], color='warning', outline='True')
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Waze"),
                    dbc.CardBody([
                        html.H1("12", className="card-text",
                            style={'display':'inline-block'}),
                        html.P("(4%)", style={'display':'inline-block'},
                            className='pl-2')
                    ]) 
                ], color='success', outline='True')
            )

        ]),


        html.Br(),

        # Reportes por fuente - stacked bar

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Reportes por Día"),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'monitoreo',
                            figure = monitoreo,
                            config={
                            'displayModeBar': False
                            }
                        ) 
                    )  
                ])
            )
        ),

        html.Br()


    ])


# Render página

def render_datos(tab):
    if tab == 'datos_monitoreo':
        return datos_monitoreo()





















