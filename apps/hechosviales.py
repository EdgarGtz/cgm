import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
from datetime import datetime as dt

#----------

# Layout General
def hechosviales():

    return html.Div([

        # Tabs
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Hechos viales', tab_id='hv_vasconcelos')
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

        #Footer 
        dbc.Row(
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México')
            ), className='px-3 py-4',
            style={'background-color': 'black','color': 'white'}
        )

    ])

#----------

# Connect to Google Drive
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

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
vasconcelos['Hechos Viales'] = pd.to_numeric(vasconcelos['Hechos Viales'])+100 #el 100 está sólo para que los puntos en el mapa se vean más grandes

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

vasconcelos_map.update_layout(clickmode='event+select', mapbox=dict(center=dict(lat=25.6572,lon=-100.3689)))


#----------

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
                ]), lg=7

            ),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.DatePickerRange(
                            id = 'calendario',
                            min_date_allowed = dt(2015, 1, 1),
                            max_date_allowed = dt(2020, 12, 31),
                            start_date = dt(2015, 1, 1),
                            end_date = dt(2020, 12, 31),
                            first_day_of_week = 1
                        ),
                        dcc.Dropdown(
                            id='periodo_hv',
                            options=[
                                #{'label': 'Hora', 'value': 'hora'},
                                {'label': 'Día', 'value': 'dia'},
                                #{'label': 'Semana', 'value': 'semana'},
                                {'label': 'Mes', 'value': 'mes'},
                                #{'label': 'Año', 'value': 'año'}
                            ],
                            value = 'dia',
                            multi = False,
                            clearable = False,
                            style={"width": "50%"},
                            className="py-2 px-3"
                        ),
                    ],className="d-flex justify-content-center"),
                ]),

                html.Br(),

                # Nombre Intersección
                dbc.Card(
                        dbc.CardHeader(id='interseccion_nombre'),
                        style={'textAlign':'center'}, inverse=False, outline = False),

                html.Br(),

                # Tarjetas Indicadores
                dbc.Row([
                        dbc.Col(
                            
                            dbc.Card([
                                dbc.CardHeader('Hechos Viales'),
                                dbc.CardBody(
                                    html.H3(id = 'interseccion_hv')
                                )
                            ], style={'textAlign':'center'}),
                        ),

                        dbc.Col(
                             dbc.Card([
                                dbc.CardHeader('Lesionados'),
                                dbc.CardBody(
                                    html.H3(id = 'interseccion_les')
                                )
                            ], style={'textAlign':'center'}),
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader('Fallecidos'),
                                dbc.CardBody(
                                    html.H3(id = 'interseccion_fal')
                                )
                            ], style={'textAlign':'center'})
                        )
                ]),

                html.Br(),

                # Hechos viales por año
                dbc.Row(
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader('Hechos Viales por'),
                            dbc.CardBody([
                                dcc.Graph(
                                    id = 'interseccion_hv_tiempo',
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
                )
            ])

            

        ]),

    ])

#----------

# Datos de Intersecciones

# Nombre
def render_interseccion_nombre(clickData):
    if clickData is None:
        return 'Intersección'
    else:
        return clickData['points'][0]['hovertext']

# Hechos Viales
def render_interseccion_hv(clickData):
    return clickData['points'][0]['marker.size']-100

# Lesionados
def render_interseccion_les(clickData):
    return clickData['points'][0]['customdata'][0]

# Fallecidos
def render_interseccion_fal(clickData):
    return clickData['points'][0]['customdata'][1]

# Hechos Viales por Año
def render_interseccion_hv_tiempo(clickData, periodo_hv, start_date, end_date):

    # Diferencia en días entre fecha de inicio y fecha final
    start_date_tiempo = pd.to_datetime(start_date)
    end_date_tiempo = pd.to_datetime(end_date)
    dif_tiempo = end_date_tiempo - start_date_tiempo
    dif_tiempo = dif_tiempo / np.timedelta64(1, 'D')

    # Diferencia para el loop de semana
    dif_tiempo_loop = dif_tiempo

    # Conteo por hora
    if periodo_hv == 'dia':

        # Leer csv
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

        # Filter interseccion
        hvi = hvi[hvi['interseccion'] == 
        clickData['points'][0]['hovertext']]
        
        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)
        #hvi["hora"] = hvi["hora"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        # +" - "+ hvi["hora"]                # - %H
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y')

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        # Filtro por calendario
        interseccion_hv_tiempo_data = hvi.loc[start_date:end_date]
        
        # Graph
        interseccion_hv_tiempo = px.line(interseccion_hv_tiempo_data, x='fecha2',y='hechos_viales', labels = {'fecha2': ''}, template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="markers+lines", fill='tozeroy', hovertemplate="") 
        interseccion_hv_tiempo.update_xaxes(showgrid = False, showline = True, type="date", rangemode="normal",rangebreaks=[dict(pattern="day of week")])
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales', tick0 = 0, dtick = 1, range=[0,2])
        interseccion_hv_tiempo.update_layout(dragmode = False, hovermode = 'x unified', hoverlabel = dict(font_size = 16))

        return interseccion_hv_tiempo

    elif periodo_hv == 'mes':
    
        # Leer csv
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

        # Filter interseccion
        hvi = hvi[hvi['interseccion'] == 
        clickData['points'][0]['hovertext']]
        
        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)
        #hvi["hora"] = hvi["hora"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        # +" - "+ hvi["hora"]                # - %H
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y')

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        # Filtro por calendario
        interseccion_hv_tiempo_data = hvi.loc[start_date:end_date]
        interseccion_hv_tiempo_data["hv_mes"] = interseccion_hv_tiempo_data["hechos_viales"].resample("M").sum()

        # Graph
        interseccion_hv_tiempo = px.scatter(interseccion_hv_tiempo_data, x='fecha2',y='hv_mes', labels = {'fecha2': ''}, template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="markers+lines", fill='tozeroy', hovertemplate="") 
        interseccion_hv_tiempo.update_xaxes(showgrid = False, showline = True)
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales')
        interseccion_hv_tiempo.update_layout(dragmode = False, hovermode = 'x', hoverlabel = dict(font_size = 16))

        return interseccion_hv_tiempo

    elif periodo_hv == 'año':
    
        # Leer csv
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

        # Filter interseccion
        hvi = hvi[hvi['interseccion'] == 
        clickData['points'][0]['hovertext']]
        
        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)
        #hvi["hora"] = hvi["hora"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        # +" - "+ hvi["hora"]                # - %H
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y')

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        # Filtro por calendario
        interseccion_hv_tiempo_data = hvi.loc[start_date:end_date]
        interseccion_hv_tiempo_data["hv_año"] = interseccion_hv_tiempo_data["hechos_viales"].resample("M").sum()

        # Graph
        interseccion_hv_tiempo = px.scatter(interseccion_hv_tiempo_data, x='fecha2',y='hv_año', labels = {'fecha2': ''}, template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="markers+lines", fill='tozeroy', hovertemplate="") 
        interseccion_hv_tiempo.update_xaxes(showgrid = False, showline = True)
        interseccion_hv_tiempo.update_layout(dragmode = False, hovermode = 'x', hoverlabel = dict(font_size = 16))

        return interseccion_hv_tiempo


#----------

# Display tabs
def render_hechosviales(tab):
    if tab == 'hv_vasconcelos':
        return hv_vasconcelos()





















