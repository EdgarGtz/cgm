import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


# Connect to Google Drive

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

# Connect to the spreadsheet

spreadsheet_key = '1zFm8XDU2DpinjzZHCFK-S9T9sHVEwF6Km2iOpYqbGgg'
book = gc.open_by_key(spreadsheet_key)


# Hechos Viales por Año

hv_ano = book.worksheet('hv_ano')

hv_ano = hv_ano.get_all_values()

hv_ano = pd.DataFrame(hv_ano[2:], columns = hv_ano[0])

hv_ano = px.bar(hv_ano, x = 'año', y = 'hechosviales',
            labels = {
            'año': '',
            'hechosviales': 'Hechos Viales'
            })


# Layout

def hechosviales():

    return html.Div([

        # Tabs

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs(
                            dbc.Tab(label='Hechos Viales', tab_id='datos_hechosviales'),
                            id='tabs',
                            active_tab="datos_hechosviales",
                            card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="hechosviales_content"))
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


# Hechos Viales

def datos_hechosviales():

    return html.Div([

        # Header

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        html.H4('Hechos Viales', 
                            style={'text-align':'left'})
                    )
                )
            ),

            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        html.P('01 de enero del 2015 al 31 de diciembre del 2020', 
                            style={'text-align':'center'})
                    )
                ), lg=4
            )

        ]),

        html.Br(),

        # Hechos Viales por Año

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Hechos Viales por Año"),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'hv_ano',
                            figure = hv_ano,
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

def render_hechosviales(tab):
    if tab == 'datos_hechosviales':
        return datos_hechosviales()










