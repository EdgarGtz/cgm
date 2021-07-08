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
                                disabled = True),
                            dbc.Tab(label='Mapa', tab_id='alfonsoreyes_2',
                                disabled = True),
                            dbc.Tab(label='Ciclistas', tab_id='alfonsoreyes_3',
                                disabled = False)
                        ],
                        id='tabs',
                        active_tab="alfonsoreyes_3",
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

# Ciclistas

# Cámaras Viales

# Connect to the spreadsheet
spreadsheet_key = '18mtg-QZ0sCF-_7u643LTGGBoEekV7fGW3S_jaePmQQY'
book = gc.open_by_key(spreadsheet_key)

# Create dataframe
camaras_viales = book.worksheet('camaras_viales')
camaras_viales = camaras_viales.get_all_values()
camaras_viales = pd.DataFrame(camaras_viales[4:], columns = camaras_viales[3])

# Change some variables to numeric
camaras_viales['bicycle'] = pd.to_numeric(camaras_viales['bicycle'])
camaras_viales['hora'] = pd.to_numeric(camaras_viales['hora'])

# Change variables to datetime
camaras_viales['dia'] = pd.to_datetime(camaras_viales['dia'], dayfirst = True)


# Ciclistas por Día
bicicletas_dia = pd.pivot_table(camaras_viales, index = ['dia', 'dia_semana'],
    values = 'bicycle', aggfunc = 'sum')

bicicletas_dia = bicicletas_dia.reset_index()

# Maximo de bicicletas
maximo_bicicletas = bicicletas_dia.bicycle.max() + 200

# Graph
bicicletas_dia_graph = px.line(bicicletas_dia, x = 'dia', y = 'bicycle',
    labels = {'dia': '', 'bicycle': ''},
    template = 'plotly_white')

bicicletas_dia_graph.update_traces(mode = 'lines+markers', marker_size = 10,
    hovertemplate = None)
bicicletas_dia_graph.update_xaxes(showgrid = False, showline = True)
bicicletas_dia_graph.update_yaxes(range = [0,maximo_bicicletas])
bicicletas_dia_graph.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


# Ciclistas por Hora
bicicletas_hora = pd.pivot_table(camaras_viales, index = ['hora'], values = 'bicycle',
    aggfunc = 'sum')
bicicletas_hora = bicicletas_hora.reset_index()
bicicletas_hora = bicicletas_hora.sort_values(by=['hora'])

suma = bicicletas_hora['bicycle'].sum()
bicicletas_hora['porcentaje'] = (bicicletas_hora['bicycle'] / suma) * 100
bicicletas_hora['porcentaje'] = bicicletas_hora['porcentaje'].round(decimals = 1)

# Graph
bicicletas_hora = px.bar(bicicletas_hora, x='hora', y='porcentaje',
    labels = {'hora': '', 'porcentaje': ''}, text='porcentaje',
    hover_data={'hora':False, 'porcentaje':False}, color = 'porcentaje', 
    color_continuous_scale = px.colors.sequential.Blues, template = 'plotly_white',
    opacity = .9)

bicicletas_hora.update(layout_coloraxis_showscale=False)
bicicletas_hora.update_yaxes(showticklabels=False, showgrid=False)
bicicletas_hora.update_traces(texttemplate='%{text:}% ')
bicicletas_hora.layout.yaxis.ticksuffix = ' '
bicicletas_hora.update_layout(hovermode = False, dragmode=False)

#----------


# Layout - BiciRuta
def alfonsoreyes_1():

    return html.Div([

        # Avance del Proyecto

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Avance del Proyecto"),
                    dbc.CardBody(
                        dbc.Progress("25%", value=25)
                    )
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

# Layout - Ciclistas
def alfonsoreyes_3():

    return html.Div([

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Bicicletas por Día'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'bicicletas_dia',
                            figure = bicicletas_dia_graph,
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
        )

    ])

#----------


# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()
    elif tab == 'alfonsoreyes_2':
        return alfonsoreyes_2()
    elif tab == 'alfonsoreyes_3':
        return alfonsoreyes_3()








