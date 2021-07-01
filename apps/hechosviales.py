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
                            dbc.Tab(label='General', tab_id='hv_general', disabled=True),
                            dbc.Tab(label='Intersecciones', tab_id='hv_vasconcelos'),
                            dbc.Tab(label='Peatón', tab_id='hv_peaton',
                                disabled = True),
                            dbc.Tab(label = 'Ciclista', tab_id = 'hv_ciclista',
                                disabled = True),
                            dbc.Tab(label = 'Motociclista', tab_id = 'hv_motociclista',
                                disabled = True)
                        ],
                        id='tabs',
                        active_tab="hv_vasconcelos",
                        card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="hechosviales_content"))
                ]), lg=12
            ), justify = 'center'
        ),

        # html.Br(),
        
        # dbc.Row(
        #     dbc.Col(

        #         dbc.Card([
        #             dbc.CardHeader("Datos de hechos viales"),
        #             dbc.CardBody("Datos")
        #         ])

        #     )
        # ),

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

# Hechos Viales por Año

#-- Connect to the spreadsheet
spreadsheet_key = '1NoDDBG09EkE2RR6urkC0FBUWw3hro_u7cqgEPYF98DA'
book = gc.open_by_key(spreadsheet_key)

hechos_viales = book.worksheet('hechosviales')
hechos_viales = hechos_viales.get_all_values()
hechos_viales = pd.DataFrame(hechos_viales[1:], columns = hechos_viales[0])

# Count hv por año
hv_ano = pd.DataFrame(hechos_viales['año'].value_counts())
hv_ano = hv_ano.reset_index()

# Rename columns and change hv to numeric
hv_ano.columns = ['Año', 'Hechos Viales']
hv_ano['Hechos Viales'] = pd.to_numeric(hv_ano['Hechos Viales'])

# Graph
hv_ano = px.bar(hv_ano, x='Año', y='Hechos Viales',
    labels = {'Año': ''}, text='Hechos Viales',
    hover_data={'Año':False, 'Hechos Viales':False})


# Layout - General
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
vasconcelos['Hechos Viales'] = pd.to_numeric(vasconcelos['Hechos Viales'])

#-- Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#-- Graph
vasconcelos_map = px.scatter_mapbox(vasconcelos, lat="lat", lon="lon",
    size = 'Hechos Viales',
    size_max=15, zoom=12.5, hover_name='interseccion', color='Hechos Viales',
    custom_data=['lesionados', 'fallecidos'],
    hover_data={'lat':False, 'lon':False, 'Hechos Viales':False},
    color_continuous_scale=px.colors.sequential.Sunset)

vasconcelos_map.update_layout(clickmode='event+select')



# Layout - Intersecciones
def hv_vasconcelos():

    return html.Div([

        # Mapa y principales indicadores
        dbc.Row([

            # Mapa
            dbc.Col(

                dbc.Card([
                    dbc.CardHeader("Da click en una intersección y desliza la página para conocer más",
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

            ),

            dbc.Col([

                dbc.Card(
                    dbc.CardHeader(id='interseccion_nombre'),
                    style={'textAlign':'center'}, inverse=False, outline = False
                ),

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Hechos Viales'),
                    dbc.CardBody(
                        html.H3(id = 'interseccion_hv')
                    )
                ], style={'textAlign':'center'}),

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Lesionados'),
                    dbc.CardBody(
                        html.H3(id = 'interseccion_les')
                    )
                ], style={'textAlign':'center'}),

                html.Br(),

                dbc.Card([
                    dbc.CardHeader('Fallecidos'),
                    dbc.CardBody(
                        html.H3(id = 'interseccion_fal')
                    )
                ], style={'textAlign':'center'})            

            ])

        ]),

        html.Br(),

        # Hechos viales por año
        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Hechos Viales por Año'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_hv_ano',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d'], 'displaylogo': False
                            }
                        )
                    ])
                ])

            )

        ),

        html.Br(),

        # Causa y Tipo de Hechos Viales
        dbc.Row([

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Tipos de Hechos Viales'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_hv_tipo',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d'], 'displaylogo': False
                            }
                        )
                    ])
                ])

            ),

            html.Br(),

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Causas de Hechos Viales'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_hv_causa',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d'], 'displaylogo': False
                            }
                        )
                    ])
                ])

            )          

        ]),

        html.Br(),

        # Edad de Responsables y Afectados
        dbc.Row([

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Edad de Responsables'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_resp_edad',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d'], 'displaylogo': False
                            }
                        )
                    ])
                ])

            ),

            html.Br(),

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Edad de Afectados'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_afec_edad',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d'], 'displaylogo': False
                            }
                        )
                    ])
                ])

            )          

        ]),

        html.Br(),

        # Género de Responsables y Afectados
        dbc.Row([

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Género de Responsables'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_resp_genero',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d', 'hoverClosestPie'],
                            'displaylogo': False
                            }
                        )
                    ])
                ])

            ),

            html.Br(),

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Género de Afectados'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_afec_genero',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d', 'hoverClosestPie'],
                            'displaylogo': False
                            }
                        )
                    ])
                ])

            )          

        ]),

        html.Br(),

        # Vehículo de Responsables y Afectados
        dbc.Row([

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Vehículo del Responsable'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_resp_vehiculo',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d', 'hoverClosestPie'],
                            'displaylogo': False
                            }
                        )
                    ])
                ])

            ),

            html.Br(),

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Vehículo del Afectado'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'interseccion_afec_vehiculo',
                            figure = {},
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d', 'hoverClosestPie'],
                            'displaylogo': False
                            }
                        )
                    ])
                ])

            )          

        ])

    ])

#----------

# Layout - Atropellos
def hv_atropellos():

    return html.Div([

        # Atropellos
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Atropellos a Peatones (2015 - 2020)"),
                    dbc.CardBody(
                        html.Iframe(width='100%', height='560', 
                           src='https://edgargtzgzz.carto.com/builder/981d5d24-9fd7-4f8f-b1ca-47dc0e8658c7/embed')
                    )  
                ])
            )
        )

    ])

#----------

# Datos de Intersección

# Nombre
def render_interseccion_nombre(clickData):
    if clickData is None:
        return 'Intersección'
    else:
        return clickData['points'][0]['hovertext']

# Hechos Viales
def render_interseccion_hv(clickData):
    return clickData['points'][0]['marker.size']

# Lesionados
def render_interseccion_les(clickData):
    return clickData['points'][0]['customdata'][0]

# Fallecidos
def render_interseccion_fal(clickData):
    return clickData['points'][0]['customdata'][1]

# Hechos Viales por Año
def render_interseccion_hv_ano(clickData):

    # Filter interseccion
    interseccion_hv_ano = vasconcelos[vasconcelos['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Filter columns
    interseccion_hv_ano = interseccion_hv_ano[interseccion_hv_ano.columns[6:12]]

    # Transpose
    interseccion_hv_ano = interseccion_hv_ano.T
    interseccion_hv_ano = interseccion_hv_ano.reset_index()

    # Rename columns and change to numeric
    interseccion_hv_ano.columns = ['Años', 'Hechos Viales']
    interseccion_hv_ano['Hechos Viales'] = pd.to_numeric(
        interseccion_hv_ano['Hechos Viales'])

    maxy = max(interseccion_hv_ano['Hechos Viales'])

    # Graph
    interseccion_hv_ano = px.bar(interseccion_hv_ano, x='Años', y='Hechos Viales',
            labels = {'Años': '', 'Hechos Viales': ''}, text = 'Hechos Viales',
            hover_data={'Años':False, 'Hechos Viales':False}, opacity = .9,
            template = "plotly_white")

    interseccion_hv_ano.update_xaxes(showline=True, showgrid=False)
    interseccion_hv_ano.update_yaxes(showline=False, showgrid=False, showticklabels = False)
    interseccion_hv_ano.update_traces(hoverlabel_bgcolor='white', textfont_size=14,
        hoverlabel_bordercolor='white')
    interseccion_hv_ano.update(layout_coloraxis_showscale=False)
    interseccion_hv_ano.update_layout(hovermode = False, dragmode=False)

    return interseccion_hv_ano

# Tipo de Hechos Viales
def render_interseccion_hv_tipo(clickData):

    # Filter interseccion
    interseccion_hv_tipo = vasconcelos[vasconcelos['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Filter and Rename columns
    interseccion_hv_tipo = interseccion_hv_tipo[interseccion_hv_tipo.columns[12:23]]
    interseccion_hv_tipo.columns = ['Alcance', 'Atropello', 'Caida de Persona',
        'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso',
        'Choque Lateral', 'Estrellamiento', 'Incendio', 'Volcadura']

    # Transpose
    interseccion_hv_tipo = interseccion_hv_tipo.T
    interseccion_hv_tipo = interseccion_hv_tipo.reset_index()

    # Rename columns and change to numeric
    interseccion_hv_tipo.columns = ['Tipo', 'Hechos Viales 2']
    interseccion_hv_tipo['Hechos Viales 2'] = pd.to_numeric(
        interseccion_hv_tipo['Hechos Viales 2'])

    # Create new variable with percentage values
    suma = interseccion_hv_tipo['Hechos Viales 2'].sum()
    interseccion_hv_tipo['Hechos Viales'] = (interseccion_hv_tipo[
        'Hechos Viales 2'] / suma) * 100
    interseccion_hv_tipo['Hechos Viales'] = interseccion_hv_tipo[
        'Hechos Viales'].round(decimals=0)

    # Graph
    interseccion_hv_tipo = px.bar(interseccion_hv_tipo, x='Hechos Viales', y='Tipo',
            labels = {'Tipo': '', 'Hechos Viales': ''}, text='Hechos Viales',
            hover_data={'Tipo':False, 'Hechos Viales':False}, color = 'Hechos Viales',
            color_continuous_scale=px.colors.sequential.Sunset, template = "plotly_white",
            opacity = .9)

    interseccion_hv_tipo.update_layout(yaxis={'categoryorder':'total ascending'},
        hovermode = False, dragmode=False)
    interseccion_hv_tipo.update(layout_coloraxis_showscale=False)
    interseccion_hv_tipo.update_xaxes(showticklabels=False, showgrid=False)
    interseccion_hv_tipo.update_traces(texttemplate='%{text:}% ')
    interseccion_hv_tipo.layout.yaxis.ticksuffix = ' '

    return interseccion_hv_tipo

# Causa de Hechos Viales
def render_interseccion_hv_causa(clickData):

    # Filter interseccion
    interseccion_hv_causa = vasconcelos[vasconcelos['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Filter and Rename columns
    interseccion_hv_causa = interseccion_hv_causa[interseccion_hv_causa.columns[24:36]]
    interseccion_hv_causa.columns = ['Distracción', 'Dormitando', 'Estado alcohólico',
        'Exceso de Dimensiones', 'Exceso de Velocidad', 'Invadir Carril', 'Mal Estacionado',
        'No Guardó Distancia', 'No Respetó Alto', 'No Respetó Semáforo', 'Viró Indevidamente',
        'Otros']

    # Transpose
    interseccion_hv_causa = interseccion_hv_causa.T
    interseccion_hv_causa = interseccion_hv_causa.reset_index()

    # Rename columns and change to numeric
    interseccion_hv_causa.columns = ['Causa', 'Hechos Viales 2']
    interseccion_hv_causa['Hechos Viales 2'] = pd.to_numeric(
        interseccion_hv_causa['Hechos Viales 2'])

    # Create new variable with percentage values
    suma = interseccion_hv_causa['Hechos Viales 2'].sum()
    interseccion_hv_causa['Hechos Viales'] = (interseccion_hv_causa[
        'Hechos Viales 2'] / suma) * 100
    interseccion_hv_causa['Hechos Viales'] = interseccion_hv_causa[
        'Hechos Viales'].round(decimals=0)

    # Graph
    interseccion_hv_causa = px.bar(interseccion_hv_causa, x='Hechos Viales', y='Causa',
            labels = {'Causa': '', 'Hechos Viales': ''}, text='Hechos Viales',
            hover_data={'Causa':False, 'Hechos Viales':False}, color = 'Hechos Viales',
            color_continuous_scale=px.colors.sequential.Sunset, template = "plotly_white",
            opacity = .9)

    interseccion_hv_causa.update_layout(yaxis={'categoryorder':'total ascending'},
        hovermode = False, dragmode=False)
    interseccion_hv_causa.layout.yaxis.ticksuffix = ' '
    interseccion_hv_causa.update(layout_coloraxis_showscale=False)
    interseccion_hv_causa.update_xaxes(showticklabels=False, showgrid=False)
    # interseccion_hv_causa.update_traces(hovertemplate='  %{x}')
    # interseccion_hv_causa.update_layout(margin=dict(r=20))
    interseccion_hv_causa.update_traces(texttemplate='%{text:}% ')

# range=[0, 50], 
    return interseccion_hv_causa

# Edad de Responsables
def render_interseccion_resp_edad(clickData):

    # Connect to database
    interseccion_resp = book.worksheet('vasconcelos_resp')
    interseccion_resp = interseccion_resp.get_all_values()
    interseccion_resp = pd.DataFrame(interseccion_resp[1:], columns = interseccion_resp[0])

    # Filter interseccion and drop NA's
    interseccion_resp_edad = interseccion_resp[interseccion_resp['interseccion'] == 
    clickData['points'][0]['hovertext']]
    interseccion_resp_edad = interseccion_resp_edad[interseccion_resp_edad.edad_grupo != 'NA']

    # Create dataframe
    interseccion_resp_edad = pd.DataFrame(interseccion_resp_edad.edad_grupo.value_counts())
    interseccion_resp_edad = interseccion_resp_edad.reset_index()
    interseccion_resp_edad.columns = ['Edades', 'Hechos Viales 2']
    interseccion_resp_edad['Hechos Viales 2'] = pd.to_numeric(
        interseccion_resp_edad['Hechos Viales 2'])

    # Create new variable with percentage values
    suma = interseccion_resp_edad['Hechos Viales 2'].sum()
    interseccion_resp_edad['Hechos Viales'] = (interseccion_resp_edad[
        'Hechos Viales 2'] / suma) * 100
    interseccion_resp_edad['Hechos Viales'] = interseccion_resp_edad[
        'Hechos Viales'].round(decimals=0)

    # Create edades dataframe
    edades = {'Edades': ['0 - 9', '10 - 19', '20 - 29', '30 - 39', '40 - 49',
        '50 - 59', '60 - 69', '70 - 79', '80 - 89', '90 y más'],
        'Hechos Viales 3': [0,0,0,0,0,0,0,0,0,0]}
    interseccion_edades = pd.DataFrame(data=edades)

    # Join dataframes
    interseccion_resp_edad = interseccion_edades.merge(interseccion_resp_edad, how = 'left')
    interseccion_resp_edad['Hechos Viales'] = interseccion_resp_edad[
        'Hechos Viales'].fillna(0)

    # Graph
    interseccion_resp_edad = px.bar(interseccion_resp_edad, y='Edades',
        x='Hechos Viales',
        labels = {'Edades': '', 'Hechos Viales': ''}, text = 'Hechos Viales',
        hover_data={'Edades':False, 'Hechos Viales':False}, color = 'Hechos Viales',
        color_continuous_scale=px.colors.sequential.Sunset, template = "plotly_white",
        opacity = .9)

    interseccion_resp_edad.update(layout_coloraxis_showscale=False)
    interseccion_resp_edad.layout.yaxis.ticksuffix = ' '
    interseccion_resp_edad.update_xaxes(showticklabels=False, showgrid=False)
    interseccion_resp_edad.update_traces(texttemplate='%{text:}% ')
    interseccion_resp_edad.update_layout(hovermode = False, dragmode=False)

    return interseccion_resp_edad

# Edad de Afectados
def render_interseccion_afec_edad(clickData):

    # Connect to database
    interseccion_afec = book.worksheet('vasconcelos_afec')
    interseccion_afec = interseccion_afec.get_all_values()
    interseccion_afec = pd.DataFrame(interseccion_afec[1:], columns = interseccion_afec[0])

    # Filter interseccion and drop NA's
    interseccion_afec_edad = interseccion_afec[interseccion_afec['interseccion'] == 
    clickData['points'][0]['hovertext']]
    interseccion_afec_edad = interseccion_afec_edad[interseccion_afec_edad.edad_grupo != 'NA']

    # Create dataframe
    interseccion_afec_edad = pd.DataFrame(interseccion_afec_edad.edad_grupo.value_counts())
    interseccion_afec_edad = interseccion_afec_edad.reset_index()
    interseccion_afec_edad.columns = ['Edades', 'Hechos Viales 2']
    interseccion_afec_edad['Hechos Viales 2'] = pd.to_numeric(
        interseccion_afec_edad['Hechos Viales 2'])

    # Create new variable with percentage values
    suma = interseccion_afec_edad['Hechos Viales 2'].sum()
    interseccion_afec_edad['Hechos Viales'] = (interseccion_afec_edad[
        'Hechos Viales 2'] / suma) * 100
    interseccion_afec_edad['Hechos Viales'] = interseccion_afec_edad[
        'Hechos Viales'].round(decimals=0)

    # Create edades dataframe
    edades = {'Edades': ['0 - 9', '10 - 19', '20 - 29', '30 - 39', '40 - 49',
        '50 - 59', '60 - 69', '70 - 79', '80 - 89', '90 y más'],
        'Hechos Viales 3': [0,0,0,0,0,0,0,0,0,0]}
    interseccion_edades = pd.DataFrame(data=edades)

    # Join dataframes
    interseccion_afec_edad = interseccion_edades.merge(interseccion_afec_edad, how = 'left')
    interseccion_afec_edad['Hechos Viales'] = interseccion_afec_edad[
        'Hechos Viales'].fillna(0)

    # Graph
    interseccion_afec_edad = px.bar(interseccion_afec_edad, y='Edades', x='Hechos Viales',
        labels = {'Edades': '', 'Hechos Viales': ''}, text='Hechos Viales',
        hover_data={'Edades':False, 'Hechos Viales':False}, color = 'Hechos Viales',
        color_continuous_scale=px.colors.sequential.Sunset, template = "plotly_white",
        opacity = .9)

    interseccion_afec_edad.update(layout_coloraxis_showscale=False)
    interseccion_afec_edad.layout.yaxis.ticksuffix = ' '
    interseccion_afec_edad.update_xaxes(showticklabels=False, showgrid=False)
    interseccion_afec_edad.update_traces(texttemplate='%{text:}% ')
    interseccion_afec_edad.update_layout(hovermode = False, dragmode=False)

    return interseccion_afec_edad

# Género de Responsables
def render_interseccion_resp_genero(clickData):

    # Connect to the database
    interseccion_resp = book.worksheet('vasconcelos_resp')
    interseccion_resp = interseccion_resp.get_all_values()
    interseccion_resp = pd.DataFrame(interseccion_resp[1:], columns = interseccion_resp[0])

    # Filter interseccion and drop NA's
    interseccion_resp_genero = interseccion_resp[interseccion_resp['interseccion'] == 
    clickData['points'][0]['hovertext']]
    interseccion_resp_genero = interseccion_resp_genero[interseccion_resp_genero.sexo != 'NA']

    # Create df
    interseccion_resp_genero = pd.DataFrame(interseccion_resp_genero.sexo.value_counts())
    interseccion_resp_genero = interseccion_resp_genero.reset_index()
    interseccion_resp_genero.columns = ['Género', 'Hechos Viales 2']
    interseccion_resp_genero['Hechos Viales 2'] = pd.to_numeric(
        interseccion_resp_genero['Hechos Viales 2'])

    # Get percent value
    suma = interseccion_resp_genero['Hechos Viales 2'].sum()
    interseccion_resp_genero['Hechos Viales'] = (interseccion_resp_genero[
        'Hechos Viales 2'] / suma) * 100
    interseccion_resp_genero['Hechos Viales'] = interseccion_resp_genero[
        'Hechos Viales'].round(decimals=0)

    # Graph
    interseccion_resp_genero = px.pie(interseccion_resp_genero,
        labels = interseccion_resp_genero['Género'], values = interseccion_resp_genero[
        'Hechos Viales'], hole = .4, names = interseccion_resp_genero['Género'], opacity = .9,
        hover_data={'Género':False, 'Hechos Viales':False})
    
    interseccion_resp_genero.update_traces(textposition='inside', textinfo='percent+label')
    interseccion_resp_genero.update(layout_showlegend=False)
    interseccion_resp_genero.update_layout(hovermode = False)

    return interseccion_resp_genero

# Género de Afectados
def render_interseccion_afec_genero(clickData):

    # Connect to the database
    interseccion_afec = book.worksheet('vasconcelos_afec')
    interseccion_afec = interseccion_afec.get_all_values()
    interseccion_afec = pd.DataFrame(interseccion_afec[1:], columns = interseccion_afec[0])

    # Filter interseccion and drop NA's
    interseccion_afec_genero = interseccion_afec[interseccion_afec['interseccion'] == 
    clickData['points'][0]['hovertext']]
    interseccion_afec_genero = interseccion_afec_genero[interseccion_afec_genero.sexo != 'NA']

    # Create df
    interseccion_afec_genero = pd.DataFrame(interseccion_afec_genero.sexo.value_counts())
    interseccion_afec_genero = interseccion_afec_genero.reset_index()
    interseccion_afec_genero.columns = ['Género', 'Hechos Viales 2']
    interseccion_afec_genero['Hechos Viales 2'] = pd.to_numeric(
        interseccion_afec_genero['Hechos Viales 2'])

    # Get percent value
    suma = interseccion_afec_genero['Hechos Viales 2'].sum()
    interseccion_afec_genero['Hechos Viales'] = (interseccion_afec_genero[
        'Hechos Viales 2'] / suma) * 100
    interseccion_afec_genero['Hechos Viales'] = interseccion_afec_genero[
        'Hechos Viales'].round(decimals=0)

    # Graph
    interseccion_afec_genero = px.pie(interseccion_afec_genero,
        labels = interseccion_afec_genero['Género'], values = interseccion_afec_genero[
        'Hechos Viales'], hole = .4, names = interseccion_afec_genero['Género'], opacity = .9,
        hover_data={'Género':False, 'Hechos Viales':False},
        color_discrete_map={'Femenino':'#88c55f',
                            'Masculino':'#9eb9f3'})
    
    interseccion_afec_genero.update_traces(textposition='inside', textinfo='percent+label')
    interseccion_afec_genero.update(layout_showlegend=False)
    interseccion_afec_genero.update_layout(hovermode = False)

    return interseccion_afec_genero

# Vehiculo de Responsables
def render_interseccion_resp_vehiculo(clickData):

    # Connect to database
    interseccion_resp = book.worksheet('vasconcelos_resp')
    interseccion_resp = interseccion_resp.get_all_values()
    interseccion_resp = pd.DataFrame(interseccion_resp[1:], columns = interseccion_resp[0])

    # Filter interseccion and drop NA's
    interseccion_resp_vehiculo = interseccion_resp[interseccion_resp['interseccion'] == 
    clickData['points'][0]['hovertext']]
    interseccion_resp_vehiculo = interseccion_resp_vehiculo[
        interseccion_resp_vehiculo.tipo_vehiculo != 'NA']

    # Create dataframe
    interseccion_resp_vehiculo = pd.DataFrame(
        interseccion_resp_vehiculo.tipo_vehiculo.value_counts())
    interseccion_resp_vehiculo = interseccion_resp_vehiculo.reset_index()
    interseccion_resp_vehiculo.columns = ['Vehiculo', 'Hechos Viales 2']
    interseccion_resp_vehiculo['Hechos Viales 2'] = pd.to_numeric(
        interseccion_resp_vehiculo['Hechos Viales 2'])

    # Create new variable with percentage values
    suma = interseccion_resp_vehiculo['Hechos Viales 2'].sum()
    interseccion_resp_vehiculo['Hechos Viales'] = (interseccion_resp_vehiculo[
        'Hechos Viales 2'] / suma) * 100
    interseccion_resp_vehiculo['Hechos Viales'] = interseccion_resp_vehiculo[
        'Hechos Viales'].round(decimals=1)

    # Graph
    interseccion_resp_vehiculo = px.bar(interseccion_resp_vehiculo, y='Vehiculo',
        x='Hechos Viales', labels = {'Vehiculo': '', 'Hechos Viales 2': 'Responsables ',
        'Hechos Viales': ''}, text = 'Hechos Viales',
        hover_data={'Vehiculo':False, 'Hechos Viales 2':True, 'Hechos Viales': False},
        color = 'Hechos Viales', color_continuous_scale=px.colors.sequential.Sunset,
        template = "plotly_white", opacity = .9)

    interseccion_resp_vehiculo.update(layout_coloraxis_showscale=False)
    interseccion_resp_vehiculo.layout.yaxis.ticksuffix = ' '
    interseccion_resp_vehiculo.update_xaxes(showticklabels=False, showgrid=False)
    interseccion_resp_vehiculo.update_traces(texttemplate='%{text:}% ')
    interseccion_resp_vehiculo.update_layout(yaxis={'categoryorder':'total ascending'})

    return interseccion_resp_vehiculo

# Vehiculo de Afectados
def render_interseccion_afec_vehiculo(clickData):

    # Connect to database
    interseccion_afec = book.worksheet('vasconcelos_afec')
    interseccion_afec = interseccion_afec.get_all_values()
    interseccion_afec = pd.DataFrame(interseccion_afec[1:], columns = interseccion_afec[0])

    # Filter interseccion and drop NA's
    interseccion_afec_vehiculo = interseccion_afec[interseccion_afec['interseccion'] == 
    clickData['points'][0]['hovertext']]
    interseccion_afec_vehiculo = interseccion_afec_vehiculo[
        interseccion_afec_vehiculo.tipo_vehiculo != 'NA']

    # Create dataframe
    interseccion_afec_vehiculo = pd.DataFrame(
        interseccion_afec_vehiculo.tipo_vehiculo.value_counts())
    interseccion_afec_vehiculo = interseccion_afec_vehiculo.reset_index()
    interseccion_afec_vehiculo.columns = ['Vehiculo', 'Hechos Viales 2']
    interseccion_afec_vehiculo['Hechos Viales 2'] = pd.to_numeric(
        interseccion_afec_vehiculo['Hechos Viales 2'])

    # Create new variable with percentage values
    suma = interseccion_afec_vehiculo['Hechos Viales 2'].sum()
    interseccion_afec_vehiculo['Hechos Viales'] = (interseccion_afec_vehiculo[
        'Hechos Viales 2'] / suma) * 100
    interseccion_afec_vehiculo['Hechos Viales'] = interseccion_afec_vehiculo[
        'Hechos Viales'].round(decimals=1)

    # Graph
    interseccion_afec_vehiculo = px.bar(interseccion_afec_vehiculo, y='Vehiculo',
        x='Hechos Viales', labels = {'Vehiculo': '', 'Hechos Viales 2': 'Afectados ',
        'Hechos Viales': ''}, text = 'Hechos Viales',
        hover_data={'Vehiculo':False, 'Hechos Viales 2':True, 'Hechos Viales': False},
        color = 'Hechos Viales', color_continuous_scale=px.colors.sequential.Sunset,
        template = "plotly_white", opacity = .9)

    interseccion_afec_vehiculo.update(layout_coloraxis_showscale=False)
    interseccion_afec_vehiculo.layout.yaxis.ticksuffix = ' '
    interseccion_afec_vehiculo.update_xaxes(showticklabels=False, showgrid=False)
    interseccion_afec_vehiculo.update_traces(texttemplate='%{text:}% ')
    interseccion_afec_vehiculo.update_layout(yaxis={'categoryorder':'total ascending'})

    return interseccion_afec_vehiculo

#----------

# Display tabs
def render_hechosviales(tab):
    if tab == 'hv_general':
        return hv_general()
    elif tab == 'hv_vasconcelos':
        return hv_vasconcelos()
    elif tab == 'hv_atropellos':
        return hv_peaton()
    elif tab == 'hv_ciclista':
        return hv_ciclista()
    elif tab == 'hv_motociclista':
        return hv_motociclista()



















