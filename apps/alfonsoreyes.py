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
                            dbc.Tab(label='Ciclistas', tab_id='alfonsoreyes_2'),
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


#----------

# Connect to Google Drive
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

#----------

# Cámaras Viales

# Bicicletas por Día

# Connect to the spreadsheet
spreadsheet_key = '18mtg-QZ0sCF-_7u643LTGGBoEekV7fGW3S_jaePmQQY'
book = gc.open_by_key(spreadsheet_key)

# Create dataframe
camaras_viales = book.worksheet('camaras_viales')
camaras_viales = camaras_viales.get_all_values()
camaras_viales = pd.DataFrame(camaras_viales[1:], columns = camaras_viales[0])
 
camaras_viales['bicycle'] = pd.to_numeric(camaras_viales['bicycle'])

bicicletas_dia = pd.pivot_table(camaras_viales, index = ['dia','dia_semana'], values = 'bicycle', aggfunc = 'sum')

bicicletas_dia = bicicletas_dia.reset_index()

# Graph
bicicletas_dia = px.bar(bicicletas_dia, x='dia_semana', y='bicycle',
    labels = {'dia_semana': '', 'bicycle': ''}, text='bicycle',
    hover_data={'dia_semana':False, 'bicycle':False}, opacity = .9, template = 'plotly_white')

bicicletas_dia.update_xaxes(showline=True, showgrid=False)
bicicletas_dia.update_yaxes(showline=False, showgrid=False, showticklabels = False)
bicicletas_dia.update_traces(hoverlabel_bgcolor='white', textfont_size=14,
    hoverlabel_bordercolor='white')
bicicletas_dia.update(layout_coloraxis_showscale=False)
bicicletas_dia.update_layout(hovermode = False, dragmode=False)

#----------


# Layout - Mapa
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
        )

    ])

#----------

# Layout - Camaras Viales
def alfonsoreyes_2():

    return html.Div([

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Bicicletas por Semana'),
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
        )

    ])






# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()
    elif tab == 'alfonsoreyes_2':
        return alfonsoreyes_2()
    elif tab == 'alfonsoreyes_3':
        return alfonsoreyes_3()








