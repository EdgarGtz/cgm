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


# Hechos Viales - Generales
spreadsheet_key = '1NoDDBG09EkE2RR6urkC0FBUWw3hro_u7cqgEPYF98DA'
book = gc.open_by_key(spreadsheet_key)

hv_ano = book.worksheet('hv_ano')
hv_ano = hv_ano.get_all_values()
hv_ano = pd.DataFrame(hv_ano[1:7], columns = hv_ano[0])

#-- Graph
hv_ano = px.histogram(hv_ano, x = 'año', y = 'hechosviales',
             labels = {
             'año': '',
             'hechosviales': 'Hechos Viales'
             })


# José Vasconcelos
spreadsheet_key = '1NoDDBG09EkE2RR6urkC0FBUWw3hro_u7cqgEPYF98DA'
book = gc.open_by_key(spreadsheet_key)

vasconcelos = book.worksheet('vasconcelos')
vasconcelos = vasconcelos.get_all_values()
vasconcelos = pd.DataFrame(vasconcelos[2:], columns = vasconcelos[0])

#-- Convert to numeric
vasconcelos['lat'] = pd.to_numeric(vasconcelos['lat'])
vasconcelos['lon'] = pd.to_numeric(vasconcelos['lon'])
vasconcelos['hechosviales'] = pd.to_numeric(vasconcelos['hechosviales'])

#-- Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#-- Map
vasconcelos = px.scatter_mapbox(vasconcelos, lat="lat", lon="lon", size = 'hechosviales',
    size_max=15, zoom=13, hover_name='interseccion')



# Layout

def hechosviales():

    return html.Div([

        # Tabs

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Generales', tab_id='hv_general'),
                            dbc.Tab(label='José Vasconcelos', tab_id='hv_vasconcelos')
                        ],
                        id='tabs',
                        active_tab="hv_general",
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


# Hechos Viales - Generales

def hv_general():

    return html.Div([

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

    ])


# Jose Vasconcelos

def hv_vasconcelos():

    return html.Div([

        # José Vasconcelos

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(""),
                    dbc.CardBody(
                        html.P(id='interseccion_nombre')
                    ),
                    dbc.CardBody(
                        html.P(id='interseccion_hv')
                    )
                ]), lg=3
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(""),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'vasconcelos',
                            figure = vasconcelos,
                            config={
                            'displayModeBar': False
                            },
                            style={'height':'100vh'}
                        ),
                    style={'padding':'0px'}
                    )
                ])
            )
        ]),

    ])


# Render página
def render_hechosviales(tab):
    if tab == 'hv_general':
        return hv_general()
    elif tab == 'hv_vasconcelos':
        return hv_vasconcelos()

# Render interseccion - nombre
def render_interseccion_nombre(clickData):
    return clickData['points'][0]['hovertext']

# Render interseccion - hv
def render_interseccion_hv(clickData):
    return clickData['points'][0]['marker.size']

