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
from datetime import datetime as dt
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

# Layout - BiciRuta
def alfonsoreyes_1():

    return html.Div([

        dbc.Row([

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
                ), width = 8

            ),

            dbc.Col(

                dcc.DatePickerRange(
                    id = 'calendario',
                    min_date_allowed = dt(2021, 6, 21),
                    max_date_allowed = dt(2021, 7, 19),
                    start_date = dt(2021, 6, 21),
                    end_date = dt(2021, 7, 19),
                    first_day_of_week = 1,
                    style = {'float': 'right'}         
                ), width = 4)

        ]),

        html.Br(),

        dbc.Row(

            dbc.Col(

                dcc.Dropdown(
                    id='my_dropdown',
                    options=[],
                    value = 'bicycle',
                    multi=False,
                    clearable=False,
                    style={"width": "50%"}
                ), width = 8

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
                        {'label': 'Semana', 'value': 'semana'}
                    ],
                    value = 'hora',
                    multi=False,
                    clearable=False,
                    style={"width": "50%"}
                ), width = 8

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
                                'modeBarButtonsToRemove':
                                ['zoom2d', 'lasso2d', 'pan2d',
                                'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                'resetScale2d', 'hoverClosestCartesian',
                                'hoverCompareCartesian', 'toggleSpikelines',
                                'select2d', 'toImage'],
                                'displaylogo': False
                            }
                        )
                    ])
                ])

            )
        )

    ])

#----------

# OPCIONES

def render_opciones(my_dropdown_0):

    if my_dropdown_0 == 'conteo':

        return [
            {'label': 'Bicicletas', 'value': 'bicycle'},
            {'label': 'Peatones', 'value': 'peatones'},
            {'label': 'Motocicletas', 'value': 'motorcycle'},
            {'label': 'Autobuses', 'value': 'bus'},
            {'label': 'Autos', 'value': 'autos'}
        ]   

    elif my_dropdown_0 == 'velocidad_promedio':

        return [
            {'label': 'Autos', 'value': 'avg_vel_car'},
            {'label': 'Motocicletas', 'value': 'avg_vel_motorcycle'},
            {'label': 'Autobuses', 'value': 'avg_vel_bus'}
        ]


# CONTEO Y VELOCIDADES

def render_conteo(my_dropdown_1, my_dropdown, my_dropdown_0, start_date, end_date):

    if my_dropdown_0 == 'conteo' and my_dropdown_1 == 'hora':

        # Create dataframe
        conteo_hora = pd.read_csv('assets/camaras_viales_hora.csv', header = [3])
        conteo_hora = conteo_hora.iloc[57:]

        # Change variable types
        conteo_hora['hora'] = conteo_hora['hora'].astype(str)
        conteo_hora['dia'] = conteo_hora['dia'].astype(str)

        # Create datetime variable
        conteo_hora['datetime'] = conteo_hora['dia'] + ' ' + conteo_hora['hora']

        # Change variable types
        conteo_hora['datetime'] = pd.to_datetime(conteo_hora['datetime'], 
            dayfirst = True, format = '%d/%m/%Y %H')

        conteo_hora['datetime1'] = conteo_hora['datetime']

        # Filter on calendario
        conteo_hora = conteo_hora.set_index('datetime')
        conteo_hora = conteo_hora.loc[start_date:end_date]

        # Graph
        conteo2 = px.scatter(conteo_hora, x = 'datetime1', y = my_dropdown,
            labels = {'datetime1': ''}, template = 'plotly_white',
            hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    elif my_dropdown_0 == 'conteo' and my_dropdown_1 == 'dia':

        # Create dataframe
        conteo_dia = pd.read_csv('assets/camaras_viales_dia.csv')
        conteo_dia = conteo_dia.iloc[3:]

        # Change dia to datetime
        conteo_dia['dia'] = pd.to_datetime(conteo_dia['dia'],
            dayfirst = True)

        conteo_dia['dia1'] = conteo_dia['dia']
        conteo_dia = conteo_dia.set_index('dia')
        conteo_dia = conteo_dia.loc[start_date:end_date]


        # Graph
        conteo2 = px.scatter(conteo_dia, x = 'dia1', y = my_dropdown,
            labels = {'dia1': ''}, template = 'plotly_white',
            hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    elif my_dropdown_0 == 'conteo' and my_dropdown_1 == 'semana':

        # Create dataframe
        conteo_semana = pd.read_csv('assets/camaras_viales_semana.csv')
        conteo_semana = conteo_semana.iloc[1:]

        conteo_semana['semana_fecha'] = pd.to_datetime(conteo_semana['semana_fecha'],
            dayfirst = True)

        conteo_semana['semana_fecha1'] = conteo_semana['semana_fecha']
        conteo_semana = conteo_semana.set_index('semana_fecha')
        conteo_semana = conteo_semana.loc[start_date:end_date]

        # Graph
        conteo2 = px.scatter(conteo_semana, x = 'semana_fecha1', y = my_dropdown,
            labels = {'semana_fecha1': ''}, template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines', marker_size = 10,
            fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    elif my_dropdown_0 == 'velocidad_promedio' and my_dropdown_1 == 'hora':

        # Create dataframe
        vel_hora = pd.read_csv('assets/camaras_viales_hora.csv', header = [3])
        vel_hora = vel_hora.iloc[57:]

        # Change variable types
        vel_hora['hora'] = vel_hora['hora'].astype(str)
        vel_hora['dia'] = vel_hora['dia'].astype(str)

        # Create datetime variable
        vel_hora['datetime'] = vel_hora['dia'] + ' ' + vel_hora['hora']

        # Change variable types
        vel_hora['datetime'] = pd.to_datetime(vel_hora['datetime'],
            dayfirst = True, format = '%d/%m/%Y %H')

        vel_hora['datetime1'] = vel_hora['datetime']

        # Filter on calendario
        vel_hora = vel_hora.set_index('datetime')
        vel_hora = vel_hora.loc[start_date:end_date]

        # Graph
        conteo2 = px.scatter(vel_hora, x = 'datetime1', y = my_dropdown,
            labels = {'datetime1': ''}, template = 'plotly_white',
            hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    elif my_dropdown_0 == 'velocidad_promedio' and my_dropdown_1 == 'dia':

        # Create dataframe
        vel_dia = pd.read_csv('assets/camaras_viales_dia.csv')
        vel_dia = vel_dia.iloc[3:]

        # Change dia to datetime
        vel_dia['dia'] = pd.to_datetime(vel_dia['dia'],
            dayfirst = True)

        vel_dia['dia1'] = vel_dia['dia']
        vel_dia = vel_dia.set_index('dia')
        vel_dia = vel_dia.loc[start_date:end_date]

        # Graph
        conteo2 = px.scatter(vel_dia, x = 'dia1', y = my_dropdown,
            labels = {'dia1': ''}, template = 'plotly_white',
            hover_data = ['dia_semana'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    elif my_dropdown_0 == 'velocidad_promedio' and my_dropdown_1 == 'semana':

        # Create dataframe
        vel_semana = pd.read_csv('assets/camaras_viales_semana.csv')
        vel_semana = vel_semana.iloc[1:]

        vel_semana['semana_fecha'] = pd.to_datetime(vel_semana['semana_fecha'],
            dayfirst = True)

        vel_semana['semana_fecha1'] = vel_semana['semana_fecha']
        vel_semana = vel_semana.set_index('semana_fecha')
        vel_semana = vel_semana.loc[start_date:end_date]

        # Graph
        conteo2 = px.scatter(vel_semana, x = 'semana_fecha1', y = my_dropdown,
            labels = {'semana_fecha1': ''}, template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines', marker_size = 10,
            fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2


#----------

# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()










