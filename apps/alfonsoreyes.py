import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


# Layout General
def alfonsoreyes():

    return html.Div([

        # Tabs
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Datos Generales', tab_id='alfonsoreyes_1'),
                            dbc.Tab(label='Ciclistas', tab_id='alfonsoreyes_2',
                            	disabled = True),
                            dbc.Tab(label='Hechos Viales', tab_id='alfonsoreyes_3',
                            	disabled = True)
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

#-- Connect to data
#inegi = gpd.read_file("assets/geojson/inegi_2020_sp_manzanas_ar_datos.geojson")
#inegi_df = inegi[["CVEGEO","POBTOT"]]

#-- Graph
#alfonsoreyes_map = px.choropleth(inegi_df, geojson=inegi.geometry,locations="CVEGEO",color="POBTOT",projection="mercator")

denue = pd.read_csv("assets/denue.csv")
mapa_denue = px.scatter_mapbox(denue, lat="latitud", lon="longitud", color_discrete_sequence=["fuchsia"], zoom=3, height=300)
mapa_denue.update_layout(mapbox_style="open-street-map")
mapa_denue.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Layout - General
def alfonsoreyes_1():

    return html.Div([

        # Hechos Viales por Año

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Alfonso Reyes"),
                    dbc.CardBody(
						#html.Iframe(width='100%', height='560', 
                           #src='https://edgargtzgzz.carto.com/builder/d1005d51-e3de-4e56-a6be-274465006ebd/embed')
                           dcc.Graph(
                           id = 'mapa_denue',
                           figure = mapa_denue,
                           style={'height':'80vh'}
                        )
                    ),
                ])
            )
        ),

    ])

# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()
    elif tab == 'alfonsoreyes_2':
        return alfonsoreyes_2()
    elif tab == 'alfonsoreyes_3':
        return alfonsoreyes_3()








