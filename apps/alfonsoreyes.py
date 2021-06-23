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
import geopandas as pdg



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

inegi = pdg.read_file("assets/geojson/inegi_2020_sp_manzanas_ar_datos.geojson")

#-- Graph


# Layout - General
def alfonsoreyes_1():

    return html.Div([

        # Hechos Viales por Año

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Alfonso Reyes"),
                    dbc.CardBody(
						html.Iframe(width='100%', height='560', 
                           src='https://edgargtzgzz.carto.com/builder/d1005d51-e3de-4e56-a6be-274465006ebd/embed')
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








