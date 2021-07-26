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
import numpy as np
from datetime import timedelta

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
                    dbc.CardBody(
                        html.Div(id="alfonsoreyes_content")
                    )
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

        # Dropdown de variables y calendario
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
                    end_date = dt(2021, 7, 18),
                    first_day_of_week = 1,
                    minimum_nights = 0,
                    updatemode = 'bothdates',
                    style = {'float': 'right'}         
                ), width = 4)

        ]),

        html.Br(),

        # Dropdown de modo de transporte
        dbc.Row(

            dbc.Col(

                dcc.Dropdown(
                    id='my_dropdown',
                    options=[],
                    value = 'bicycle',
                    multi = False,
                    clearable = False,
                    style={"width": "50%"}
                ), width = 8

            )

        ),

        html.Br(),

        # # Dropdown de periodo de tiempo
        # dbc.Row(

        #     dbc.Col(

        #         dcc.Dropdown(
        #             id='my_dropdown_1',
        #             options=[
        #                 {'label': 'Hora', 'value': 'hora'},
        #                 {'label': 'Día', 'value': 'dia'},
        #                 {'label': 'Semana', 'value': 'semana'}
        #             ],
        #             value = 'hora',
        #             multi = False,
        #             clearable = False,
        #             style={"width": "50%"}
        #         ), width = 8

        #     )

        # ),

        # html.Br(),

        # # Gráfica de línea
        # dbc.Row(

        #     dbc.Col(

        #         dbc.Card([
        #             dbc.CardBody([
        #                 dcc.Graph(
        #                     id = 'conteo2',
        #                     figure = {},
        #                     config={
        #                         'modeBarButtonsToRemove':
        #                         ['zoom2d', 'lasso2d', 'pan2d',
        #                         'zoomIn2d', 'zoomOut2d', 'autoScale2d',
        #                         'resetScale2d', 'hoverClosestCartesian',
        #                         'hoverCompareCartesian', 'toggleSpikelines',
        #                         'select2d', 'toImage'],
        #                         'displaylogo': False
        #                     }
        #                 )
        #             ])
        #         ])

        #     )
        # ),

        html.Br(),

        # Gráfica de línea con tabs
        dbc.Row(

            dbc.Col(

                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Hora', tab_id='hora',
                                disabled = False),
                            dbc.Tab(label = 'Día', tab_id = 'dia',
                                disabled = False),
                            dbc.Tab(label = 'Semana', tab_id = 'semana',
                                disabled = False)
                        ],
                        id='periodo',
                        active_tab="hora",
                        card=True
                        )
                    ),
                    dbc.CardBody(
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
                    )
                ]), lg=12

            ), justify = 'center'

        )

    ])

#----------

# Conexión entre dropdown de variables y dropdown de modo de transporte
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

#----------

# Visualizar gráficas de línea para conteo y velocidad promedio
def render_conteo(periodo, my_dropdown, my_dropdown_0, start_date, end_date):

    # Diferencia en días entre fecha de inicio y fecha final
    start_date_tiempo = pd.to_datetime(start_date)
    end_date_tiempo = pd.to_datetime(end_date)
    dif_tiempo = end_date_tiempo - start_date_tiempo
    dif_tiempo = dif_tiempo / np.timedelta64(1, 'D')

    # Diferencia para el loop de semana
    dif_tiempo_loop = dif_tiempo

    # Conteo por hora
    if my_dropdown_0 == 'conteo' and periodo == 'hora':

        # Leer csv
        conteo_hora = pd.read_csv('assets/camaras_viales_hora.csv', header = [3])
        conteo_hora = conteo_hora.iloc[57:]

        # Cambiar variables a string
        conteo_hora['hora'] = conteo_hora['hora'].astype(str)
        conteo_hora['dia'] = conteo_hora['dia'].astype(str)

        # Crear variable datetime
        conteo_hora['datetime'] = conteo_hora['dia'] + ' ' + conteo_hora['hora']
        conteo_hora['datetime'] = pd.to_datetime(conteo_hora['datetime'], 
            dayfirst = True, format = '%d/%m/%Y %H')

        # Duplicar columna de fecha y set index
        conteo_hora['datetime1'] = conteo_hora['datetime']
        conteo_hora = conteo_hora.set_index('datetime')

        # Filtro por calendario
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

    # Conteo por día
    elif my_dropdown_0 == 'conteo' and periodo == 'dia':

        # Leer csv
        conteo_dia = pd.read_csv('assets/camaras_viales_dia.csv')
        conteo_dia = conteo_dia.iloc[3:]

        # Cambiar variable a datetime
        conteo_dia['dia'] = pd.to_datetime(conteo_dia['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        conteo_dia['dia1'] = conteo_dia['dia']
        conteo_dia = conteo_dia.set_index('dia')

        # Filtro por calendario
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

    # Conteo por semana - una semana o menos
    elif my_dropdown_0 == 'conteo' and periodo == 'semana' and dif_tiempo < 7:

        # Leer csv
        conteo_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        conteo_semana = conteo_semana.iloc[3:]

        # Cambiar variable a datetime
        conteo_semana['dia'] = pd.to_datetime(conteo_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        conteo_semana['dia1'] = conteo_semana['dia']
        conteo_semana = conteo_semana.set_index('dia')

        # Filtro por calendario
        conteo_semana = conteo_semana.loc[start_date:end_date]

        # Crear df nuevo con suma de selección
        suma = conteo_semana[my_dropdown].sum()
        suma = pd.Series(suma)
        fecha = pd.Series(start_date)
        conteo_semana = pd.DataFrame(dict(fecha = fecha, suma = suma))

        # Graph
        conteo2 = px.scatter(conteo_semana, x = 'fecha', y = 'suma',
            labels = {'fecha': ''}, template = 'plotly_white',
            hover_data = ['fecha'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size =16))

        return conteo2

    # Conteo por semana - más de una semana
    elif my_dropdown_0 == 'conteo' and periodo == 'semana':

        # Leer csv
        conteo_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        conteo_semana = conteo_semana.iloc[3:]

        # Cambiar variable a datetime
        conteo_semana['dia'] = pd.to_datetime(conteo_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        conteo_semana['dia1'] = conteo_semana['dia']
        conteo_semana = conteo_semana.set_index('dia')

        # Filtro por calendario
        conteo_semana = conteo_semana.loc[start_date:end_date]

        # Variables de fecha para el while loop
        dt_start_date = pd.to_datetime(start_date)
        dt_end_date = pd.to_datetime(end_date)

        # DF que se actualiza con el loop y termina graficado
        conteo_semana_graph = pd.DataFrame(columns = ['fecha', 'suma'])

        while dif_tiempo_loop >= 7:

            # Filtra por la primera semana completa
            conteo_semana_nuevo = conteo_semana.loc[
                dt_start_date: dt_start_date + pd.DateOffset(days = 6)]

            # Suma de variable y actualiza df a graficar
            suma = conteo_semana_nuevo[my_dropdown].sum()
            conteo_semana_graph = conteo_semana_graph.append(
                {'fecha' : dt_start_date, 'suma' : suma}, ignore_index = True)

            # Actualizar variables para el loop
            dt_start_date = dt_start_date + pd.DateOffset(days = 7)
            dif_tiempo_loop = dif_tiempo_loop - 7 

        else:

            # Filtra por los días restantes
            conteo_semana_ultimo = conteo_semana.loc[dt_start_date: dt_end_date]
    
            # Suma de variable y actualiza df a graficar
            suma = conteo_semana_ultimo[my_dropdown].sum()
            conteo_semana_graph = conteo_semana_graph.append(
                {'fecha' : dt_start_date, 'suma' : suma}, ignore_index = True)

        # Graph
        conteo2 = px.scatter(conteo_semana_graph, x = 'fecha', y = 'suma',
            labels = {'fecha': ''}, template = 'plotly_white',
            hover_data = ['fecha'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size =16))

        return conteo2

    # Velocidad promedio por hora
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'hora':

        # Leer csv
        vel_hora = pd.read_csv('assets/camaras_viales_hora.csv', header = [3])
        vel_hora = vel_hora.iloc[57:]

        # Cambiar variables a string
        vel_hora['hora'] = vel_hora['hora'].astype(str)
        vel_hora['dia'] = vel_hora['dia'].astype(str)

        # Crear variable datetime
        vel_hora['datetime'] = vel_hora['dia'] + ' ' + vel_hora['hora']
        vel_hora['datetime'] = pd.to_datetime(vel_hora['datetime'],
            dayfirst = True, format = '%d/%m/%Y %H')

        # Duplicar columna de fecha y set index
        vel_hora['datetime1'] = vel_hora['datetime']
        vel_hora = vel_hora.set_index('datetime')

        # Filtro por calendario
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

    # Velocidad promedio por día
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'dia':

        # Leer csv
        vel_dia = pd.read_csv('assets/camaras_viales_dia.csv')
        vel_dia = vel_dia.iloc[3:]

        # Cambiar variable a datetime
        vel_dia['dia'] = pd.to_datetime(vel_dia['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        vel_dia['dia1'] = vel_dia['dia']
        vel_dia = vel_dia.set_index('dia')

        # Filtro por calendario
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

    # Velocidad promedio por semana - una semana o menos
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'semana' and dif_tiempo < 7:

        # Leer csv
        vel_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        vel_semana = vel_semana.iloc[3:]

        # Cambiar variable a datetime
        vel_semana['dia'] = pd.to_datetime(vel_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        vel_semana['dia1'] = vel_semana['dia']
        vel_semana = vel_semana.set_index('dia')

        # Filtro por calendario
        vel_semana = vel_semana.loc[start_date:end_date]

        # Crear df nuevo con suma de selección
        mean = vel_semana[my_dropdown].mean()
        mean = pd.Series(mean)
        fecha = pd.Series(start_date)
        vel_semana = pd.DataFrame(dict(fecha = fecha, mean = mean))

        # Graph
        conteo2 = px.scatter(vel_semana, x = 'fecha', y = 'mean',
            labels = {'fecha': ''}, template = 'plotly_white')

        conteo2.update_traces(mode = 'markers+lines', marker_size = 10,
            fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size = 16))

        return conteo2

    # Velocidad promedio por semana - más de una semana
    elif my_dropdown_0 == 'velocidad_promedio' and periodo == 'semana':

        # Leer csv
        vel_semana = pd.read_csv('assets/camaras_viales_dia.csv')
        vel_semana = vel_semana.iloc[3:]

        # Cambiar variable a datetime
        vel_semana['dia'] = pd.to_datetime(vel_semana['dia'],
            dayfirst = True)

        # Duplicar columna de fecha y set index
        vel_semana['dia1'] = vel_semana['dia']
        vel_semana = vel_semana.set_index('dia')

        # Filtro por calendario
        vel_semana = vel_semana.loc[start_date:end_date]

        # Variables de fecha para el while loop
        dt_start_date = pd.to_datetime(start_date)
        dt_end_date = pd.to_datetime(end_date)

        # DF que se actualiza con el loop y termina graficado
        vel_semana_graph = pd.DataFrame(columns = ['fecha', 'suma'])

        while dif_tiempo_loop >= 7:

            # Filtra por la primera semana completa
            vel_semana_nuevo = vel_semana.loc[
                dt_start_date: dt_start_date + pd.DateOffset(days = 6)]

            # Suma de variable y actualiza df a graficar
            mean = vel_semana_nuevo[my_dropdown].mean()
            vel_semana_graph = vel_semana_graph.append(
                {'fecha' : dt_start_date, 'mean' : mean}, ignore_index = True)

            # Actualizar variables para el loop
            dt_start_date = dt_start_date + pd.DateOffset(days = 7)
            dif_tiempo_loop = dif_tiempo_loop - 7 

        else:

            # Filtra por los días restantes
            vel_semana_ultimo = vel_semana.loc[dt_start_date: dt_end_date]
    
            # Suma de variable y actualiza df a graficar
            mean = vel_semana_ultimo[my_dropdown].mean()
            vel_semana_graph = vel_semana_graph.append(
                {'fecha' : dt_start_date, 'mean' : mean}, ignore_index = True)

        # Graph
        conteo2 = px.scatter(vel_semana_graph, x = 'fecha', y = 'mean',
            labels = {'fecha': ''}, template = 'plotly_white',
            hover_data = ['fecha'])

        conteo2.update_traces(mode = 'markers+lines', fill='tozeroy')
        conteo2.update_xaxes(showgrid = False, showline = True)
        conteo2.update_layout(dragmode = False, hovermode = 'x',
            hoverlabel = dict(font_size =16))

        return conteo2

#----------

# Display tabs
def render_alfonsoreyes(tab):
    if tab == 'alfonsoreyes_1':
        return alfonsoreyes_1()










