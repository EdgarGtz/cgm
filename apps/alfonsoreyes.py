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

#----------

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

# CONTEO

# Connect to Google Drive
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

# Connect to the spreadsheet
spreadsheet_key = '18mtg-QZ0sCF-_7u643LTGGBoEekV7fGW3S_jaePmQQY'
book = gc.open_by_key(spreadsheet_key)


# BICICLETAS

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

bicicletas_hora.update_traces(mode = 'lines', fill='tozeroy')
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

bicicletas_dia.update_traces(mode = 'markers+lines', marker_size = 10,
    fill='tozeroy')
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

bicicletas_semana.update_traces(mode = 'markers+lines', marker_size = 10,
    fill='tozeroy')
bicicletas_semana.update_xaxes(showgrid = False, showline = True)
bicicletas_semana.update_yaxes(range = [0, max_bicicletas_semana])
bicicletas_semana.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


# PEATONES

# PEATONES POR HORA

# Connect to database
peatones_hora = book.worksheet('camaras_viales')
peatones_hora = peatones_hora.get_all_values()
peatones_hora = pd.DataFrame(peatones_hora[61:],
    columns = peatones_hora[3])

# Create datetime variable
peatones_hora['datetime'] = peatones_hora['dia'] + ' ' + peatones_hora['hora']

# Change variable types
peatones_hora['datetime'] = pd.to_datetime(peatones_hora['datetime'],
    dayfirst = True, format = '%d/%m/%Y %H')
peatones_hora['peatones'] = pd.to_numeric(peatones_hora['peatones'])

# Maximo de peatones
max_peatones_hora = peatones_hora.peatones.max() + 100

# Graph
peatones_hora = px.scatter(peatones_hora, x = 'datetime', y = 'peatones',
    labels = {'datetime': '', 'peatones': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

peatones_hora.update_traces(mode = 'lines', fill='tozeroy')
peatones_hora.update_xaxes(showgrid = False, showline = True)
peatones_hora.update_yaxes(range = [0, max_peatones_hora])
peatones_hora.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# PEATONES POR DIA

# Connect to database
peatones_dia = book.worksheet('camaras_viales')
peatones_dia = peatones_dia.get_all_values()
peatones_dia = pd.DataFrame(peatones_dia[61:], columns = peatones_dia[3])

# Change variable types
peatones_dia['dia'] = pd.to_datetime(peatones_dia['dia'],
    dayfirst = True)
peatones_dia['peatones'] = pd.to_numeric(peatones_dia['peatones'])

# Peatones per day
peatones_dia = pd.pivot_table(peatones_dia, index = ['dia', 'dia_semana'],
    values = 'peatones', aggfunc = 'sum')
peatones_dia = peatones_dia.reset_index()

# Maximo de peatones
max_peatones_dia = peatones_dia.peatones.max() + 500

# Graph
peatones_dia = px.scatter(peatones_dia, x = 'dia', y = 'peatones',
    labels = {'dia': '', 'peatones': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

peatones_dia.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
peatones_dia.update_xaxes(showgrid = False, showline = True)
peatones_dia.update_yaxes(range = [0, max_peatones_dia])
peatones_dia.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# PEATONES POR SEMANA

# Connect to database
peatones_semana = book.worksheet('camaras_viales')
peatones_semana = peatones_semana.get_all_values()
peatones_semana = pd.DataFrame(peatones_semana[61:],
    columns = peatones_semana[3])

#Change variable types
peatones_semana['dia'] = pd.to_datetime(peatones_semana['dia'],
    dayfirst = True)
peatones_semana['peatones'] = pd.to_numeric(peatones_semana['peatones'])

# Peatones per week
peatones_semana = pd.pivot_table(peatones_semana, index = ['dia'],
    values = 'peatones', aggfunc = 'sum')
peatones_semana = peatones_semana.resample('W').sum()
peatones_semana = peatones_semana.reset_index()

# Maximo de peatones
max_peatones_semana = peatones_semana.peatones.max() + 5000

# Graph
peatones_semana = px.scatter(peatones_semana, x = 'dia', y = 'peatones',
    labels = {'dia': '', 'peatones': ''}, template = 'plotly_white')

peatones_semana.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
peatones_semana.update_xaxes(showgrid = False, showline = True)
peatones_semana.update_yaxes(range = [0, max_peatones_semana])
peatones_semana.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


# MOTOCICLETAS

# MOTOCICLETAS POR HORA

# Connect to database
motocicletas_hora = book.worksheet('camaras_viales')
motocicletas_hora = motocicletas_hora.get_all_values()
motocicletas_hora = pd.DataFrame(motocicletas_hora[61:],
    columns = motocicletas_hora[3])

# Create datetime variable
motocicletas_hora['datetime'] = motocicletas_hora['dia'] + ' ' + motocicletas_hora['hora']

# Change variable types
motocicletas_hora['datetime'] = pd.to_datetime(motocicletas_hora['datetime'],
    dayfirst = True, format = '%d/%m/%Y %H')
motocicletas_hora['motorcycle'] = pd.to_numeric(motocicletas_hora['motorcycle'])

# Maximo de motocicletas
max_motocicletas_hora = motocicletas_hora.motorcycle.max() + 100

# Graph
motocicletas_hora = px.scatter(motocicletas_hora, x = 'datetime', y = 'motorcycle',
    labels = {'datetime': '', 'motorcycle': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

motocicletas_hora.update_traces(mode = 'lines', fill='tozeroy')
motocicletas_hora.update_xaxes(showgrid = False, showline = True)
motocicletas_hora.update_yaxes(range = [0, max_motocicletas_hora])
motocicletas_hora.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# MOTOCICLETAS POR DIA

# Connect to database
motocicletas_dia = book.worksheet('camaras_viales')
motocicletas_dia = motocicletas_dia.get_all_values()
motocicletas_dia = pd.DataFrame(motocicletas_dia[61:], columns = motocicletas_dia[3])

# Change variable types
motocicletas_dia['dia'] = pd.to_datetime(motocicletas_dia['dia'],
    dayfirst = True)
motocicletas_dia['motorcycle'] = pd.to_numeric(motocicletas_dia['motorcycle'])

# Motorcycles per day
motocicletas_dia = pd.pivot_table(motocicletas_dia, index = ['dia', 'dia_semana'],
    values = 'motorcycle', aggfunc = 'sum')
motocicletas_dia = motocicletas_dia.reset_index()

# Maximo de motocicletas
max_motocicletas_dia = motocicletas_dia.motorcycle.max() + 500

# Graph
motocicletas_dia = px.scatter(motocicletas_dia, x = 'dia', y = 'motorcycle',
    labels = {'dia': '', 'motorcycle': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

motocicletas_dia.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
motocicletas_dia.update_xaxes(showgrid = False, showline = True)
motocicletas_dia.update_yaxes(range = [0, max_motocicletas_dia])
motocicletas_dia.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# MOTOCICLETAS POR SEMANA

# Connect to database
motocicletas_semana = book.worksheet('camaras_viales')
motocicletas_semana = motocicletas_semana.get_all_values()
motocicletas_semana = pd.DataFrame(motocicletas_semana[61:],
    columns = motocicletas_semana[3])

#Change variable types
motocicletas_semana['dia'] = pd.to_datetime(motocicletas_semana['dia'],
    dayfirst = True)
motocicletas_semana['motorcycle'] = pd.to_numeric(motocicletas_semana['motorcycle'])

# Motorcycles per week
motocicletas_semana = pd.pivot_table(motocicletas_semana, index = ['dia'],
    values = 'motorcycle', aggfunc = 'sum')
motocicletas_semana = motocicletas_semana.resample('W').sum()
motocicletas_semana = motocicletas_semana.reset_index()

# Maximo de motocicletas
max_motocicletas_semana = motocicletas_semana.motorcycle.max() + 5000

# Graph
motocicletas_semana = px.scatter(motocicletas_semana, x = 'dia', y = 'motorcycle',
    labels = {'dia': '', 'motorcycle': ''}, template = 'plotly_white')

motocicletas_semana.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
motocicletas_semana.update_xaxes(showgrid = False, showline = True)
motocicletas_semana.update_yaxes(range = [0, max_motocicletas_semana])
motocicletas_semana.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


# AUTOBUSES

# AUTOBUSES POR HORA

# Connect to database
autobuses_hora = book.worksheet('camaras_viales')
autobuses_hora = autobuses_hora.get_all_values()
autobuses_hora = pd.DataFrame(autobuses_hora[61:],
    columns = autobuses_hora[3])

# Create datetime variable
autobuses_hora['datetime'] = autobuses_hora['dia'] + ' ' + autobuses_hora['hora']

# Change variable types
autobuses_hora['datetime'] = pd.to_datetime(autobuses_hora['datetime'],
    dayfirst = True, format = '%d/%m/%Y %H')
autobuses_hora['bus'] = pd.to_numeric(autobuses_hora['bus'])

# Maximo de autobuses
max_autobuses_hora = autobuses_hora.bus.max() + 50

# Graph
autobuses_hora = px.scatter(autobuses_hora, x = 'datetime', y = 'bus',
    labels = {'datetime': '', 'bus': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

autobuses_hora.update_traces(mode = 'lines', fill='tozeroy')
autobuses_hora.update_xaxes(showgrid = False, showline = True)
autobuses_hora.update_yaxes(range = [0, max_autobuses_hora])
autobuses_hora.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# AUTOBUSES POR DIA

# Connect to database
autobuses_dia = book.worksheet('camaras_viales')
autobuses_dia = autobuses_dia.get_all_values()
autobuses_dia = pd.DataFrame(autobuses_dia[61:], columns = autobuses_dia[3])

# Change variable types
autobuses_dia['dia'] = pd.to_datetime(autobuses_dia['dia'],
    dayfirst = True)
autobuses_dia['bus'] = pd.to_numeric(autobuses_dia['bus'])

# Buses per day
autobuses_dia = pd.pivot_table(autobuses_dia, index = ['dia', 'dia_semana'],
    values = 'bus', aggfunc = 'sum')
autobuses_dia = autobuses_dia.reset_index()

# Maximo de motocicletas
max_autobuses_dia = autobuses_dia.bus.max() + 500

# Graph
autobuses_dia = px.scatter(autobuses_dia, x = 'dia', y = 'bus',
    labels = {'dia': '', 'bus': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

autobuses_dia.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
autobuses_dia.update_xaxes(showgrid = False, showline = True)
autobuses_dia.update_yaxes(range = [0, max_autobuses_dia])
autobuses_dia.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# AUTOBUSES POR SEMANA

# Connect to database
autobuses_semana = book.worksheet('camaras_viales')
autobuses_semana = autobuses_semana.get_all_values()
autobuses_semana = pd.DataFrame(autobuses_semana[61:],
    columns = autobuses_semana[3])

#Change variable types
autobuses_semana['dia'] = pd.to_datetime(autobuses_semana['dia'],
    dayfirst = True)
autobuses_semana['bus'] = pd.to_numeric(autobuses_semana['bus'])

# Buses per week
autobuses_semana = pd.pivot_table(autobuses_semana, index = ['dia'],
    values = 'bus', aggfunc = 'sum')
autobuses_semana = autobuses_semana.resample('W').sum()
autobuses_semana = autobuses_semana.reset_index()

# Maximo de autobuses
max_autobuses_semana = autobuses_semana.bus.max() + 5000

# Graph
autobuses_semana = px.scatter(autobuses_semana, x = 'dia', y = 'bus',
    labels = {'dia': '', 'bus': ''}, template = 'plotly_white')

autobuses_semana.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
autobuses_semana.update_xaxes(showgrid = False, showline = True)
autobuses_semana.update_yaxes(range = [0, max_autobuses_semana])
autobuses_semana.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))


# AUTOS

# AUTOS POR HORA

# Connect to database
autos_hora = book.worksheet('camaras_viales')
autos_hora = autos_hora.get_all_values()
autos_hora = pd.DataFrame(autos_hora[61:],
    columns = autos_hora[3])

# Create datetime variable
autos_hora['datetime'] = autos_hora['dia'] + ' ' + autos_hora['hora']

# Change variable types
autos_hora['datetime'] = pd.to_datetime(autos_hora['datetime'],
    dayfirst = True, format = '%d/%m/%Y %H')
autos_hora['autos'] = pd.to_numeric(autos_hora['autos'])

# Maximo de autos
max_autos_hora = autos_hora.autos.max() + 50

# Graph
autos_hora = px.scatter(autos_hora, x = 'datetime', y = 'autos',
    labels = {'datetime': '', 'autos': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

autos_hora.update_traces(mode = 'lines', fill='tozeroy')
autos_hora.update_xaxes(showgrid = False, showline = True)
autos_hora.update_yaxes(range = [0, max_autos_hora])
autos_hora.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# AUTOS POR DIA

# Connect to database
autos_dia = book.worksheet('camaras_viales')
autos_dia = autos_dia.get_all_values()
autos_dia = pd.DataFrame(autos_dia[61:], columns = autos_dia[3])

# Change variable types
autos_dia['dia'] = pd.to_datetime(autos_dia['dia'],
    dayfirst = True)
autos_dia['autos'] = pd.to_numeric(autos_dia['autos'])

# Buses per day
autos_dia = pd.pivot_table(autos_dia, index = ['dia', 'dia_semana'],
    values = 'autos', aggfunc = 'sum')
autos_dia = autos_dia.reset_index()

# Maximo de motocicletas
max_autos_dia = autos_dia.autos.max() + 20000

# Graph
autos_dia = px.scatter(autos_dia, x = 'dia', y = 'autos',
    labels = {'dia': '', 'autos': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

autos_dia.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
autos_dia.update_xaxes(showgrid = False, showline = True)
autos_dia.update_yaxes(range = [0, max_autos_dia])
autos_dia.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

# AUTOS POR SEMANA

# Connect to database
autos_semana = book.worksheet('camaras_viales')
autos_semana = autos_semana.get_all_values()
autos_semana = pd.DataFrame(autos_semana[61:],
    columns = autos_semana[3])

#Change variable types
autos_semana['dia'] = pd.to_datetime(autos_semana['dia'],
    dayfirst = True)
autos_semana['autos'] = pd.to_numeric(autos_semana['autos'])

# Buses per week
autos_semana = pd.pivot_table(autos_semana, index = ['dia'],
    values = 'autos', aggfunc = 'sum')
autos_semana = autos_semana.resample('W').sum()
autos_semana = autos_semana.reset_index()

# Maximo de autobuses
max_autos_semana = autos_semana.autos.max() + 100000

# Graph
autos_semana = px.scatter(autos_semana, x = 'dia', y = 'autos',
    labels = {'dia': '', 'autos': ''}, template = 'plotly_white')

autos_semana.update_traces(mode = 'markers+lines', marker_size = 10, 
    fill='tozeroy')
autos_semana.update_xaxes(showgrid = False, showline = True)
autos_semana.update_yaxes(range = [0, max_autos_semana])
autos_semana.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))

#----------

# Layout - BiciRuta
def alfonsoreyes_1():

    return html.Div([

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader('Autos por Hora'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'autos_hora',
                            figure = autos_hora,
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d', 'toImage'],
                            'displaylogo': False
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
                    dbc.CardHeader('Autos por Día'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'autos_dia',
                            figure = autos_dia,
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d', 'toImage'],
                            'displaylogo': False
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
                    dbc.CardHeader('Autos por Semana'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'autos_semana',
                            figure = autos_semana,
                            config={
                            'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                            'hoverClosestCartesian', 'hoverCompareCartesian',
                            'toggleSpikelines', 'select2d', 'toImage'],
                            'displaylogo': False
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









