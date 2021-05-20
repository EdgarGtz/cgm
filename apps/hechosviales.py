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

hv_ano.update_layout(yaxis_title="Hechos Viales")


# José Vasconcelos
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

#-- Map
vasconcelos_map = px.scatter_mapbox(vasconcelos, lat="lat", lon="lon", size = 'hechosviales',
    size_max=15, zoom=13, hover_name='interseccion',
    custom_data=['2015', '2016', '2017', '2018', '2019', '2020', 'lesionados', 'fallecidos',
    'tipo_alcance', 'tipo_atropello', 'tipo_caida_persona', 'tipo_choque_crucero',
    'tipo_choque_frente', 'tipo_choque_reversa', 'tipo_choque_diverso', 'tipo_choque_lateral',
    'tipo_estrellamiento', 'tipo_incendio', 'tipo_volcadura', 'distraccion',
    'dormitando', 'estado_alcoholico', 'exceso_dimensiones', 'exceso_velocidad',
    'invadir_carril', 'mal_estacionado', 'no_guardo_dist', 'no_resp_alto', 'no_resp_sem',
    'otros', 'viro_indevidamente'],
    hover_data={'lat':False, 'lon':False, 'hechosviales':False})


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

        # Mapa y principales indicadores

        dbc.Row([

            dbc.Col([

                dbc.Card(
                    dbc.CardHeader(id='interseccion_nombre'),
                    style={'textAlign':'center'}
                ),

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Hechos Viales'),
                    dbc.CardBody(
                        html.H2(id = 'interseccion_hv')
                    )
                ], color="info", outline=True, style={'textAlign':'center'}), 

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Lesionados'),
                    dbc.CardBody(
                        html.H2(id = 'interseccion_les')
                    )
                ], color="warning", outline=True, style={'textAlign':'center'}),

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Fallecidos'),
                    dbc.CardBody(
                        html.H2(id = 'interseccion_fal')
                    )
                ], color="danger", outline=True, style={'textAlign':'center'})             

            ]),

            # Mapa

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader("Da click en cualquier intersección para conocer más",
                        style={'textAlign': 'center'}),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'vasconcelos_map',
                            figure = vasconcelos_map,
                            config={
                            'displayModeBar': False
                            },
                            style={'height':'100vh'}
                        ),
                    style={'padding':'0px'}
                    )
                ]), lg=10

            )

        ]),

        html.Br(),

        # Hechos viales por año

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Hechos viales por año'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'vasconcelos_hv_ano',
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

        # Hechos viales por tipo

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Hechos viales por tipo'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'vasconcelos_hv_tipo',
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

        # Hechos viales por causa

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Hechos viales por causa'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'vasconcelos_hv_causa',
                            figure = {},
                            config={
                            'displayModeBar': False
                            }
                        )
                    ])
                ])

            )

        ),

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

# Render interseccion - lesionados
def render_interseccion_les(clickData):
    return clickData['points'][0]['customdata'][6]

# Render interseccion - lesionados
def render_interseccion_fal(clickData):
    return clickData['points'][0]['customdata'][7]

# Render hechos viales por año

def render_vasconcelos_hv_ano(clickData):
    ano_2015 = clickData['points'][0]['customdata'][0]
    ano_2016 = clickData['points'][0]['customdata'][1]
    ano_2017 = clickData['points'][0]['customdata'][2]
    ano_2018 = clickData['points'][0]['customdata'][3]
    ano_2019 = clickData['points'][0]['customdata'][4]
    ano_2020 = clickData['points'][0]['customdata'][5]

    vasconcelos_hv_ano = px.histogram(y=[ano_2015,ano_2016,ano_2017,ano_2018,ano_2019,ano_2020],
        x=['2015', '2016', '2017', '2018', '2019', '2020'],
        labels = {'x': ''}) 

    vasconcelos_hv_ano.update_layout(yaxis_title="Hechos Viales")   

    return vasconcelos_hv_ano

# Render hechos viales por tipo

def render_vasconcelos_hv_tipo(clickData):
    tipo_alcance = clickData['points'][0]['customdata'][8]
    tipo_atropello = clickData['points'][0]['customdata'][9]
    tipo_caida_persona = clickData['points'][0]['customdata'][10]
    tipo_choque_crucero = clickData['points'][0]['customdata'][11]
    tipo_choque_frente = clickData['points'][0]['customdata'][12]
    tipo_choque_reversa = clickData['points'][0]['customdata'][13]
    tipo_choque_diverso = clickData['points'][0]['customdata'][14]
    tipo_choque_lateral = clickData['points'][0]['customdata'][15]
    tipo_estrellamiento = clickData['points'][0]['customdata'][16]
    tipo_incendio = clickData['points'][0]['customdata'][17]
    tipo_volcadura = clickData['points'][0]['customdata'][18]

    vasconcelos_hv_tipo = px.histogram(y=[tipo_alcance, tipo_atropello, tipo_caida_persona,
        tipo_choque_crucero, tipo_choque_frente, tipo_choque_reversa, tipo_choque_diverso,
        tipo_choque_lateral, tipo_estrellamiento, tipo_incendio, tipo_volcadura],
        x=['Alcance', 'Atropello', 'Caída de Persona', 'Choque de Crucero',
        'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral',
        'Estrellamiento', 'Incendio', 'Volcadura'],
        labels = {'x': ''}) 

    vasconcelos_hv_tipo.update_layout(yaxis_title="Hechos Viales")   

    return vasconcelos_hv_tipo


# Render hechos viales por causa

def render_vasconcelos_hv_causa(clickData):
    distraccion = clickData['points'][0]['customdata'][19]
    dormitando = clickData['points'][0]['customdata'][20]
    estado_aloholico = clickData['points'][0]['customdata'][21]
    exceso_dimensiones = clickData['points'][0]['customdata'][22]
    exceso_velocidad = clickData['points'][0]['customdata'][23]
    invadir_carril = clickData['points'][0]['customdata'][24]
    mal_estacionado = clickData['points'][0]['customdata'][25]
    no_guardo_dist = clickData['points'][0]['customdata'][26]
    no_resp_alto = clickData['points'][0]['customdata'][27]
    no_resp_sem = clickData['points'][0]['customdata'][28]
    otros = clickData['points'][0]['customdata'][29]
    viro_indevidamente = clickData['points'][0]['customdata'][30]

    vasconcelos_hv_causa = px.histogram(y=[distraccion, dormitando, estado_aloholico,
        exceso_dimensiones, exceso_velocidad, invadir_carril, mal_estacionado,
        no_guardo_dist, no_resp_alto, no_resp_sem, otros, viro_indevidamente],
        x=['Distracción', 'Dormitando', 'Estado Alcohólico', 'Exceso de Dimensiones',
        'Exceso de Velocidad', 'Invadir Carril', 'Mal Estacionado', 'No Guardo Distancia',
        'No Respeto el Alto', 'No Respeto el Semáforo', 'Otros', 'Viro Idevidamente'],
        labels = {'x': ''}) 

    vasconcelos_hv_causa.update_layout(yaxis_title="Hechos Viales")   

    return vasconcelos_hv_causa

























