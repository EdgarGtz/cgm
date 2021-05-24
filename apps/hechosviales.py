import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

#----------

# Layout
def hechosviales():

    return html.Div([

        # Tabs
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='General', tab_id='hv_general'),
                            dbc.Tab(label='Intersecciones', tab_id='hv_vasconcelos')
                        ],
                        id='tabs',
                        active_tab="hv_general",
                        card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="hechosviales_content"))
                ]), lg=12
            ), justify = 'center'
        ),

        #Footer 
        dbc.Row(
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México')
            ), className='px-3 py-4', style={'background-color': 'black','color': 'white'}
        )

    ])

#----------

# Connect to Google Drive
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

#----------

# General

# Siniestros Viales por Año

#-- Connect to data
spreadsheet_key = '1NoDDBG09EkE2RR6urkC0FBUWw3hro_u7cqgEPYF98DA'
book = gc.open_by_key(spreadsheet_key)

siniestros_viales = book.worksheet('siniestrosviales')
siniestros_viales = siniestros_viales.get_all_values()
siniestros_viales = pd.DataFrame(siniestros_viales[1:], columns = siniestros_viales[0])

# Count sv por año
sv_ano = pd.DataFrame(siniestros_viales['año'].value_counts())
sv_ano = sv_ano.reset_index()

# Rename columns and change sv to numeric
sv_ano.columns = ['Año', 'Siniestros Viales']
sv_ano['Siniestros Viales'] = pd.to_numeric(sv_ano['Siniestros Viales'])

# Graph
sv_ano = px.bar(sv_ano, x='Año', y='Siniestros Viales',
    labels = {'Año': ''}, text='Siniestros Viales',
    hover_data={'Año':False, 'Siniestros Viales':False})


# Layout
def hv_general():

    return html.Div([

        # Hechos Viales por Año

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Siniestros Viales por Año"),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'hv_ano',
                            figure = sv_ano,
                            config={
                            'displayModeBar': False
                            }
                        ) 
                    )  
                ])
            )
        ),

    ])

#----------

# Intersecciones

# Map

#-- Connect to data
spreadsheet_key = '1NoDDBG09EkE2RR6urkC0FBUWw3hro_u7cqgEPYF98DA'
book = gc.open_by_key(spreadsheet_key)

vasconcelos = book.worksheet('vasconcelos')
vasconcelos = vasconcelos.get_all_values()
vasconcelos = pd.DataFrame(vasconcelos[1:], columns = vasconcelos[0])

#-- Convert to numeric
vasconcelos['lat'] = pd.to_numeric(vasconcelos['lat'])
vasconcelos['lon'] = pd.to_numeric(vasconcelos['lon'])
vasconcelos['hechosviales'] = pd.to_numeric(vasconcelos['hechosviales'])

#-- Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#-- Graph
vasconcelos_map = px.scatter_mapbox(vasconcelos, lat="lat", lon="lon", size = 'hechosviales',
    size_max=15, zoom=13, hover_name='interseccion', color='hechosviales',
    custom_data=['lesionados', 'fallecidos'],
    hover_data={'lat':False, 'lon':False, 'hechosviales':False})


# Layout
def hv_vasconcelos():

    return html.Div([

        # Mapa y principales indicadores
        dbc.Row([

            dbc.Col([

                dbc.Card(
                    dbc.CardHeader(id='interseccion_nombre'),
                    style={'textAlign':'center'}
                ),

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Siniestros Viales'),
                    dbc.CardBody(
                        html.H3(id = 'interseccion_hv')
                    )
                ], color="info", outline=True, style={'textAlign':'center'}), 

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Lesionados'),
                    dbc.CardBody(
                        html.H3(id = 'interseccion_les')
                    )
                ], color="warning", outline=True, style={'textAlign':'center'}),

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Fallecidos'),
                    dbc.CardBody(
                        html.H3(id = 'interseccion_fal')
                    )
                ], color="danger", outline=True, style={'textAlign':'center'})             

            ]),

            # Mapa
            dbc.Col(

                dbc.Card([
                    dbc.CardHeader("Da click en una intersección y desliza la página para conocer más.",
                        style={'textAlign': 'center'}),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'vasconcelos_map',
                            figure = vasconcelos_map,
                            config={
                            'displayModeBar': False
                            },
                            style={'height':'80vh'}
                        ),
                    style={'padding':'0px'}
                    )
                ]), lg=10

            )

        ]),

        html.Br(),

        # Siniestros viales por año
        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Siniestros Viales por Año'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_sv_ano',
                            figure = {},
                            config={
                            'displayModeBar': False
                            }
                        )
                    ])
                ])

            )

        ),

        html.Br(),

        # Causa y Tipo de Siniestros Viales
        dbc.Row([

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Tipos de Siniestros Viales'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_sv_tipo',
                            figure = {},
                            config={
                            'displayModeBar': False
                            }
                        )
                    ])
                ])

            ),

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Causas de Siniestros Viales'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_sv_causa',
                            figure = {},
                            config={
                            'displayModeBar': False
                            }
                        )
                    ])
                ])

            )            

        ])

    ])

#----------

# Datos de Intersección

# Nombre
def render_interseccion_nombre(clickData):
    if clickData is None:
        return 'Intersección'
    else:
        return clickData['points'][0]['hovertext']

# Siniestros Viales
def render_interseccion_hv(clickData):
    return clickData['points'][0]['marker.size']

# Lesionados
def render_interseccion_les(clickData):
    return clickData['points'][0]['customdata'][0]

# Fallecidos
def render_interseccion_fal(clickData):
    return clickData['points'][0]['customdata'][1]

# Siniestros Viales por Año
def render_interseccion_sv_ano(clickData):

    # Filter interseccion
    interseccion_sv_ano = vasconcelos[vasconcelos['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Filter columns
    interseccion_sv_ano = interseccion_sv_ano[interseccion_sv_ano.columns[6:12]]

    # Transpose
    interseccion_sv_ano = interseccion_sv_ano.T
    interseccion_sv_ano = interseccion_sv_ano.reset_index()

    # Rename columns and change to numeric
    interseccion_sv_ano.columns = ['Años', 'Siniestros Viales']
    interseccion_sv_ano['Siniestros Viales'] = pd.to_numeric(
        interseccion_sv_ano['Siniestros Viales'])

    # Graph
    interseccion_sv_ano = px.bar(interseccion_sv_ano, x='Años', y='Siniestros Viales',
            labels = {'Años': ''}, text='Siniestros Viales',
            hover_data={'Años':False, 'Siniestros Viales':False})

    interseccion_sv_ano.update_layout(yaxis={'categoryorder':'total ascending'})

    return interseccion_sv_ano

# Tipo de Siniestros Viales
def render_interseccion_sv_tipo(clickData):

    # Filter interseccion
    interseccion_sv_tipo = vasconcelos[vasconcelos['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Filter and Rename columns
    interseccion_sv_tipo = interseccion_sv_tipo[interseccion_sv_tipo.columns[12:23]]
    interseccion_sv_tipo.columns = ['Alcance', 'Atropello', 'Caida de Persona',
        'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso',
        'Choque Lateral', 'Estrellamiento', 'Incendio', 'Volcadura']

    # Transpose
    interseccion_sv_tipo = interseccion_sv_tipo.T
    interseccion_sv_tipo = interseccion_sv_tipo.reset_index()

    # Rename columns and change to numeric
    interseccion_sv_tipo.columns = ['Tipo', 'Siniestros Viales']
    interseccion_sv_tipo['Siniestros Viales'] = pd.to_numeric(
        interseccion_sv_tipo['Siniestros Viales'])

    # Graph
    interseccion_sv_tipo = px.bar(interseccion_sv_tipo, x='Siniestros Viales', y='Tipo',
            labels = {'Tipo': ''}, text='Siniestros Viales',
            hover_data={'Tipo':False, 'Siniestros Viales':False})

    interseccion_sv_tipo.update_layout(yaxis={'categoryorder':'total ascending'})

    return interseccion_sv_tipo

# Causa de Siniestros Viales
def render_interseccion_sv_causa(clickData):

    # Filter interseccion
    interseccion_sv_causa = vasconcelos[vasconcelos['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Filter and Rename columns
    interseccion_sv_causa = interseccion_sv_causa[interseccion_sv_causa.columns[24:36]]
    interseccion_sv_causa.columns = ['Distracción', 'Dormitando', 'Estado alcohólico',
        'Exceso de Dimensiones', 'Exceso de Velocidad', 'Invadir Carril', 'Mal Estacionado',
        'No Guardó Distancia', 'No Respetó Alto', 'No Respetó Semáforo', 'Viró Indevidamente',
        'Otros']

    # Transpose
    interseccion_sv_causa = interseccion_sv_causa.T
    interseccion_sv_causa = interseccion_sv_causa.reset_index()

    # Rename columns and change to numeric
    interseccion_sv_causa.columns = ['Causa', 'Siniestros Viales']
    interseccion_sv_causa['Siniestros Viales'] = pd.to_numeric(
        interseccion_sv_causa['Siniestros Viales'])

    # Graph
    interseccion_sv_causa = px.bar(interseccion_sv_causa, x='Siniestros Viales', y='Causa',
            labels = {'Causa': ''}, text='Siniestros Viales')

    interseccion_sv_causa.update_layout(yaxis={'categoryorder':'total ascending'})

    return interseccion_sv_causa

#----------

# Display tabs
def render_hechosviales(tab):
    if tab == 'hv_general':
        return hv_general()
    elif tab == 'hv_vasconcelos':
        return hv_vasconcelos()



















