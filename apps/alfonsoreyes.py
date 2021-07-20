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
                                disabled = False)
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

# CONTEO

# BICICLETAS

# BICICLETAS POR HORA

# Create dataframe
bicicletas_hora = pd.read_csv('assets/camaras_viales.csv', header = [3])
bicicletas_hora = bicicletas_hora.iloc[57:]

# Change variable types
bicicletas_hora['hora'] = bicicletas_hora['hora'].astype(str)
bicicletas_hora['dia'] = bicicletas_hora['dia'].astype(str)

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
bicicletas_dia = pd.read_csv('assets/camaras_viales.csv', header = [3])
bicicletas_dia = bicicletas_dia.iloc[57:]

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
bicicletas_semana = pd.read_csv('assets/camaras_viales.csv', header = [3])
bicicletas_semana = bicicletas_semana.iloc[57:]

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

#----------

# VELOCIDAD PROMEDIO

# AUTOS (CAR)

# AUTOS POR HORA

# Create dataframe
autos_vel_hora = pd.read_csv('assets/camaras_viales.csv', header = [3])
autos_vel_hora = autos_vel_hora.iloc[57:]

# Change variable types
autos_vel_hora['hora'] = autos_vel_hora['hora'].astype(str)
autos_vel_hora['dia'] = autos_vel_hora['dia'].astype(str)

# Create datetime variable
autos_vel_hora['datetime'] = autos_vel_hora['dia'] + ' ' + autos_vel_hora['hora']

# Change variable types
autos_vel_hora['datetime'] = pd.to_datetime(autos_vel_hora['datetime'],
    dayfirst = True, format = '%d/%m/%Y %H')

# Graph
autos_vel_hora = px.scatter(autos_vel_hora, x = 'datetime', y = 'avg_vel_car',
    labels = {'datetime': '', 'avg_vel_autos': ''}, template = 'plotly_white',
    hover_data = ['dia_semana'])

autos_vel_hora.update_traces(mode = 'lines', fill='tozeroy')
autos_vel_hora.update_xaxes(showgrid = False, showline = True)
autos_vel_hora.update_layout(dragmode = False, hovermode = 'x',
    hoverlabel = dict(font_size = 16))













#----------

# Layout - BiciRuta
def alfonsoreyes_1():

    return html.Div([

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='my_dropdown_0',
                    options=[
                             {'label': 'Conteo', 'value': 'conteo'},
                             {'label': 'Velocidad Promedio', 
                                'value': 'velocidad_promedio'}
                    ],
                    value='conteo',
                    multi=False,
                    clearable=False,
                    style={"width": "50%"}
                )

            )

        ),

        html.Br(),

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='my_dropdown',
                    options=[],
                    value='bicycle',
                    multi=False,
                    clearable=False,
                    style={"width": "50%"}
                )

            )

        ),

        html.Br(),

        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='my_dropdown_1',
                    options=[
                             {'label': 'Hora', 'value': 'hora'},
                             {'label': 'Día', 'value': 'dia'},
                             {'label': 'Semana', 'value': 'semana'}                    ],
                    value='dia',
                    multi=False,
                    clearable=False,
                    style={"width": "50%"}
                )

            )

        ),


        html.Br(),

        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader(''),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'conteo2',
                            figure = {},
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
                    dbc.CardHeader('Hola'),
                    dbc.CardBody([
                        dcc.Graph(
                            id = 'autos_vel_hora',
                            figure = {},
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

# VARIABLES

# def render_opciones(my_dropdown_0):

#     if my_dropdown_0 == 'conteo':

#         return [{'label': 'Peatones', 'value': 'peatones'}]

#     elif my_dropdown_0 == 'velocidad_promedio':

#         return [{'label': 'Autos', 'value': 'autos'}]


# CONTEO

def render_conteo(my_dropdown_1, my_dropdown, my_dropdown_0):

    if my_dropdown_0 == 'conteo' and my_dropdown_1 == 'hora':

        # Create dataframe
        conteo_hora = pd.read_csv('assets/camaras_viales.csv', header = [3])
        conteo_hora = conteo_hora.iloc[57:]

        # Change variable types
        conteo_hora['hora'] = conteo_hora['hora'].astype(str)
        conteo_hora['dia'] = conteo_hora['dia'].astype(str)

        # Create datetime variable
        conteo_hora['datetime'] = conteo_hora['dia'] + ' ' + conteo_hora['hora']

        # Change variable types
        conteo_hora['datetime'] = pd.to_datetime(conteo_hora['datetime'], 
            dayfirst = True, format = '%d/%m/%Y %H')

        # Graph
        conteo2 = px.scatter(conteo_hora, x = 'datetime', y = my_dropdown,
            labels = {'datetime': '', my_dropdown: ''}, template = 'plotly_white',
            hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    elif my_dropdown_0 == 'conteo' and my_dropdown_1 == 'dia':

        # Create dataframe
        conteo_dia = pd.read_csv('assets/camaras_viales.csv', header = [3])
        conteo_dia = conteo_dia.iloc[57:]

        # Change dia to datetime
        conteo_dia['dia'] = pd.to_datetime(conteo_dia['dia'],
            dayfirst = True)

        # Create dataframe
        conteo2 = pd.pivot_table(conteo_dia, index = ['dia', 'dia_semana'],
            values = my_dropdown, aggfunc = 'sum')
        conteo2 = conteo2.reset_index()

        # Graph
        conteo2 = px.scatter(conteo2, x = 'dia', y = my_dropdown,
            labels = {'datetime': '', my_dropdown: ''}, template = 'plotly_white',
            hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    elif my_dropdown_0 == 'conteo' and my_dropdown_1 == 'semana':

        # Create dataframe
        conteo_semana = pd.read_csv('assets/camaras_viales.csv', header = [3])
        conteo_semana = conteo_semana.iloc[57:]

        conteo_semana['dia'] = pd.to_datetime(conteo_semana['dia'],
            dayfirst = True)

        # Create dataframe
        conteo2 = pd.pivot_table(conteo_semana, index = ['dia'],
            values = my_dropdown, aggfunc = 'sum')
        conteo2 = conteo2.resample('W').sum()
        conteo2 = conteo2.reset_index()

        # Graph
        conteo2 = px.scatter(conteo2, x = 'dia', y = my_dropdown,
            labels = {'dia': '', my_dropdown: ''}, template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines', marker_size = 10,
            fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    else:
        return autos_vel_hora

#----------

# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()










