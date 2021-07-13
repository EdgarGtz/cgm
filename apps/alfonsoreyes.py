import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import geopandas as gpd


# Layout General
def alfonsoreyes():

    return html.Div([

        # Tabs
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='BiciRuta', tab_id='alfonsoreyes_1',
                                disabled = False),
                            dbc.Tab(label='Mapa', tab_id='alfonsoreyes_2',
                                disabled = True),
                        ],
                        id='tabs',
                        active_tab="alfonsoreyes_1",
                        card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="alfonsoreyes_content"))
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

#-- Connect to data
juntasv = gpd.read_file("assets/juntas_vecinos_ar_f1.geojson")
camaras = gpd.read_file("assets/camaras_viales_fase1_ar.geojson")
biciracks = gpd.read_file("assets/biciracks_ar.geojson")
#denue = pd.read_csv("assets/mapa/denue.csv")

# Mapa Juntas
juntasv_map = px.choropleth_mapbox(juntasv, geojson=juntasv.geometry,locations=juntasv.index,color="seccion",
                                        center={"lat": 25.645682, "lon": -100.380236}, 
                                        mapbox_style="carto-positron", zoom=13)
juntasv_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Mapa Cámaras
camaras_map = px.scatter_mapbox(camaras, lat=camaras.geometry.y, lon=camaras.geometry.x, color_discrete_sequence=["fuchsia"], zoom=13.5, height=800)
camaras_map.update_layout(mapbox_style="carto-positron")
camaras_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Mapa Biciracks
biciracks_map = px.scatter_mapbox(biciracks, lat=biciracks.geometry.y, lon=biciracks.geometry.x, color_discrete_sequence=["fuchsia"], zoom=13.5, height=800)
biciracks_map.update_layout(mapbox_style="carto-positron")
biciracks_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#mapa_denue = px.scatter_mapbox(denue, lat="latitud", lon="longitud", color_discrete_sequence=["fuchsia"], zoom=13.5, height=300)
#mapa_denue.update_layout(mapbox_style="carto-positron")
#mapa_denue.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


#----------

# Connect to Google Drive
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

#----------

# BICICLETAS

# Connect to the spreadsheet
spreadsheet_key = '18mtg-QZ0sCF-_7u643LTGGBoEekV7fGW3S_jaePmQQY'
book = gc.open_by_key(spreadsheet_key)


# BICICLETAS POR HORA

# Create dataframe
bicicletas_hora = book.worksheet('camaras_viales')
bicicletas_hora = bicicletas_hora.get_all_values()
bicicletas_hora = pd.DataFrame(bicicletas_hora[61:], columns = bicicletas_hora[3])

# Create datetime variable
bicicletas_hora['datetime'] = bicicletas_hora['dia'] + ' ' + bicicletas_hora['hora']

# Change variable types
bicicletas_hora['datetime'] = pd.to_datetime(bicicletas_hora['datetime'],
    dayfirst = True, format = '%d/%m/%Y %H')
bicicletas_hora['bicycle'] = pd.to_numeric(bicicletas_hora['bicycle'])

# Maximo de bicicletas
max_bicicletas_hora = bicicletas_hora.bicycle.max() + 100

# Graph
bicicletas_hora = px.scatter(bicicletas_hora, x = 'datetime', y = 'bicycle',
    labels = {'datetime': '', 'bicycle': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

bicicletas_hora.update_traces(mode = 'lines')
bicicletas_hora.update_xaxes(showgrid = False, showline = True)
bicicletas_hora.update_yaxes(range = [0, max_bicicletas_hora])
bicicletas_hora.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


# BICICLETAS POR DÍA

# Create dataframe
bicicletas_dia = book.worksheet('camaras_viales')
bicicletas_dia = bicicletas_dia.get_all_values()
bicicletas_dia = pd.DataFrame(bicicletas_dia[61:], columns = bicicletas_dia[3])

# Change variable types
bicicletas_dia['dia'] = pd.to_datetime(bicicletas_dia['dia'],
    dayfirst = True)
bicicletas_dia['bicycle'] = pd.to_numeric(bicicletas_dia['bicycle'])

# Bicycles per day
bicicletas_dia = pd.pivot_table(bicicletas_dia, index = ['dia', 'dia_semana'],
    values = 'bicycle', aggfunc = 'sum')
bicicletas_dia = bicicletas_dia.reset_index()

# Maximo de bicicletas
max_bicicletas_dia = bicicletas_dia.bicycle.max() + 200

# Graph
bicicletas_dia = px.scatter(bicicletas_dia, x = 'dia', y = 'bicycle',
    labels = {'dia': '', 'bicycle': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

bicicletas_dia.update_traces(mode = 'markers+lines', marker_size = 10)
bicicletas_dia.update_xaxes(showgrid = False, showline = True)
bicicletas_dia.update_yaxes(range = [0, max_bicicletas_dia])
bicicletas_dia.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


# BICICLETAS POR SEMANA

# Create dataframe
bicicletas_semana = book.worksheet('camaras_viales')
bicicletas_semana = bicicletas_semana.get_all_values()
bicicletas_semana = pd.DataFrame(bicicletas_semana[61:], columns = bicicletas_semana[3])

#Change variable types
bicicletas_semana['dia'] = pd.to_datetime(bicicletas_semana['dia'], dayfirst = True)
bicicletas_semana['bicycle'] = pd.to_numeric(bicicletas_semana['bicycle'])

# Bicycles per week
bicicletas_semana = pd.pivot_table(bicicletas_semana, index = ['dia'],
    values = 'bicycle', aggfunc = 'sum')
bicicletas_semana = bicicletas_semana.resample('W').sum()
bicicletas_semana = bicicletas_semana.reset_index()

# Maximo de bicicletas
max_bicicletas_semana = bicicletas_semana.bicycle.max() + 1000

# Graph
bicicletas_semana = px.scatter(bicicletas_semana, x = 'dia', y = 'bicycle',
    labels = {'dia': '', 'bicycle': ''}, template = 'plotly_white')

bicicletas_semana.update_traces(mode = 'markers+lines', marker_size = 10)
bicicletas_semana.update_xaxes(showgrid = False, showline = True)
bicicletas_semana.update_yaxes(range = [0, max_bicicletas_semana])
bicicletas_semana.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


#----------

# Layout - BiciRuta
def alfonsoreyes_1():

    return html.Div([

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Bicicletas por Hora'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'bicicletas_hora',
                            figure = bicicletas_hora,
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

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Bicicletas por Día'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'bicicletas_dia',
                            figure = bicicletas_dia,
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

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Bicicletas por Semana'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'bicicletas_semana',
                            figure = bicicletas_semana,
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
        )

    ])

#----------

# Layout - Mapa
def alfonsoreyes_2():

    return html.Div([

        # Hechos Viales por Año

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("BiciRuta"),
                    dbc.CardBody(
                           dcc.Graph(
                           id = 'juntasv_map',
                           figure = juntasv_map,
                           style={'height':'80vh'}
                        )
                    ),
                    dbc.CardBody(
                           dcc.Graph(
                           id = 'camaras_map',
                           figure = camaras_map,
                           style={'height':'80vh'}
                        )
                    ),
                    dbc.CardBody(
                           dcc.Graph(
                           id = 'biciracks_map',
                           figure = biciracks_map,
                           style={'height':'80vh'}
                        )
                    ),
                ])
            )
        )

    ])


#----------


# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()
    elif tab == 'alfonsoreyes_2':
        return alfonsoreyes_2()









