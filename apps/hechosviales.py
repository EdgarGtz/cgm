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
from dash_extensions import Download
from dash_extensions.snippets import send_file
import base64

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
                            dbc.Tab(label='Datos Generales', tab_id='', disabled=True),
                            dbc.Tab(label='Intersecciones', tab_id='hv_vasconcelos'),
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
        dbc.Row([
            dbc.Col(
                html.H6('Instituto Municipal de Planeación y Gestión Urbana')),
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México',
                    style = {'textAlign': 'right'}))
        ], className='px-3 py-4', style={'background-color': 'black','color': 'white'})

    ])

#----------

# Connect to Google Drive
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('plasma-galaxy-271714-fa7f2076caca.json', scope)
gc = gspread.authorize(credentials)

#----------

# Intersecciones

# Map

#-- Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

#----------

# Layout - Intersecciones
def hv_vasconcelos():

    return html.Div([

        # Controles
        dbc.Row(
            dbc.Col([
                 dbc.Row([

                        dbc.Col([

                            dbc.Card([
                                dbc.CardHeader('Calendario', style={'text-align':'center'}),
                                dbc.CardBody([

                                    dcc.DatePickerRange(
                                        id = 'calendario',
                                        min_date_allowed = dt(2015, 1, 1),
                                        max_date_allowed = dt(2020, 12, 31),
                                        start_date = dt(2015, 1, 1),
                                        end_date = dt(2020, 12, 31),
                                        first_day_of_week = 1,
                                        className="d-flex justify-content-center"
                                    ),
                                ], style={'height':'90px'}, className='d-flex align-items-center justify-content-center')
                            ])

                        ], lg=4, md=4),
                       
                        dbc.Col([

                            dbc.Card([
                                dbc.CardHeader('Día de la Semana', style={'text-align':'center'}),
                                dbc.CardBody([
                                
                                    dcc.Checklist(
                                        id='checklist_dias',
                                        className="d-flex justify-content-center btn-group ",
                                        options=[
                                            {'label': 'LU', 'value': 'Lunes'},
                                            {'label': 'MA', 'value': 'Martes'},
                                            {'label': 'MI', 'value': 'Miércoles'},
                                            {'label': 'JU', 'value': 'Jueves'},
                                            {'label': 'VI', 'value': 'Viernes'},
                                            {'label': 'SA', 'value': 'Sábado'},
                                            {'label': 'DO', 'value': 'Domingo'},
                                        ],
                                        value=['Lunes', 'Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
                                        inputClassName='form-check-input ',
                                        labelClassName="btn btn-secondary ",
                                        inputStyle={'background-color:':'#767c85!important;'},
                                        style={'display':'inline-block'}
                                    ),

                                ], style={'height':'90px'}, className='pt-4')
                            ])
 
                        ],lg=4, md=4),

                        dbc.Col([
                            dbc.Card([
                            dbc.CardHeader('Horario', style={'text-align':'center'}),
                                dbc.CardBody([
                                   
                                    html.Div(
                                        dcc.RangeSlider(
                                            id='slider_hora',
                                            min=0,
                                            max=23,
                                            value=[0, 23],
                                            marks={
                                                0: {'label': '0'},
                                                3: {'label': '3'},
                                                6: {'label': '6'},
                                                9: {'label': '9'},
                                                12: {'label': '12'},
                                                15: {'label': '15'},
                                                18: {'label': '18'},
                                                21: {'label': '21'},
                                                23: {'label': '23'}
                                            },
                                            allowCross=False,
                                            dots=True,
                                            tooltip={'always_visible': False , "placement":"bottom"},
                                            updatemode='drag'
                                        ),
                                    ),
                                ], style={'height':'90px'}, className='pt-4')
                            ])
                            
                        ], lg=4, md=4),

                    ], className="d-flex justify-content-between ",),

                html.Br(),

            ])
        ),

        # Mapa y principales indicadores
        dbc.Row([
            # Mapa
            dbc.Col([

                dbc.Card([

                    # Nombre Intersección
                    dbc.CardHeader([
                        
                        ],id='interseccion_nombre',
                        style={'textAlign': 'center','color':'black'},
                        ),

                    dbc.CardBody(
                        dcc.Graph(
                            id = 'mapa',
                            figure = {},
                            config={
                            'displayModeBar': False
                            },
                            style={'height':'80vh'}
                        ),
                    style={'padding':'0px'},
                    )
                ]), 

                html.Br(),
                
                dbc.Card([
                    dbc.CardHeader('Tipos de hechos viales'),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'tabla',
                            figure = {},
                            config={'displaylogo': False}
                            ),
                    style={'padding':'0px'}
                    )
                ])

            ],lg=6, md=6),

            dbc.Col([

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
                            dbc.CardHeader([
                                dbc.Tabs([
                                    dbc.Tab(label='Día', tab_id='dia',
                                        disabled = False),
                                    dbc.Tab(label = 'Mes', tab_id = 'mes',
                                        disabled = False),
                                    dbc.Tab(label = 'Año', tab_id = 'año',
                                        disabled = False),
                                ],
                                id='periodo_hv',
                                active_tab="mes",
                                card=True
                                )
                            ]),
                            dbc.CardBody([
                                dcc.Graph(
                                    id = 'interseccion_hv_tiempo',
                                    figure = {},
                                    config={
                                    'modeBarButtonsToRemove': ['zoom2d', 'lasso2d', 'pan2d',
                                    'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian',
                                    'toggleSpikelines', 'select2d'], 'displaylogo': False
                                    },
                                )
                            ],style={'padding':'0'}),
                        ])
                    )
                ),

                html.Br(),
                
                dbc.Card([
                    dbc.CardHeader([

                        html.Div([
                            'Hechos Viales por Tipo y Causa',
                            ],
                            className="mt-1", 
                            style={'width':'90%','display':'inline-block'}),

                        html.Span(
                            dbc.Button(
                                html.B('i'), 
                                id="open1", 
                                n_clicks=0, 
                                className="btn btn-success rounded-pill", 
                                style={'display':'inline-block',
                                        'float':'right',
                                        'background-color':'#636EFA','margin':'0px','width':'4%'}
                                ),

                            id="tooltip-target",
                            style={"textDecoration": "underline", "cursor": "pointer"},
                        ),

                        dbc.Tooltip(
                            "Más información",
                            target="tooltip-target",
                        ),
                            
                        dbc.Modal([

                            dbc.ModalHeader(html.H4("Tipos de Hechos Viales")),

                            dbc.ModalBody([
                                html.Ul([
                                    html.Li([html.B('Alcance:'),' Sucede cuando un conductor impacta con su vehículo en la parte trasera de otro.']),
                                    html.Li([html.B('Atropello:'),' Ocurre cuando un vehículo en movimiento impacta con una persona. La persona puede estar estática o en movimiento ya sea caminando, corriendo o montando en patines, patinetas, o cualquier juguete similar, o trasladándose asistiéndose de aparatos o de vehículos no regulados por este reglamento, esto en el caso de las personas con discapacidad.']),
                                    html.Li([html.B('Caída de persona:'),' Ocurre cuando una persona cae hacia fuera o dentro de un vehículo en movimiento, comúnmente dentro de un autobús de transporte público. ']),
                                    html.Li([html.B('Choque de crucero:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación que convergen o se cruzan, invadiendo un vehículo parcial o totalmente el arroyo de circulación de otro. ']),
                                    html.Li([html.B('Choque de Frente:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación opuestos, los cuales chocan cuando uno de ellos invade parcial o totalmente el carril, arroyo de circulación o trayectoria contraria. ']),
                                    html.Li([html.B('Choque Diverso:'),' En esta clasificación queda cualquier hecho de tránsito no especificado en los puntos anteriores. ']),
                                    html.Li([html.B('Choque Lateral:'),' Ocurre entre dos o más vehículos cuyos conductores circulan en carriles o con trayectorias paralelas, en el mismo sentido chocando los vehículos entre sí, cuando uno de ellos invada parcial o totalmente el carril o trayectoria donde circula el otro.']),
                                    html.Li([html.B('Estrellamiento:'),' Ocurre cuando un vehículo en movimiento en cualquier sentido choca con algo que se encuentra provisional o permanentemente estático.'])

                                ], style={'list-style-type':'none'}, className="p-1")

                            ],style={"textAlign":"justify",'font-size':'120%'}),

                            dbc.ModalFooter([
                                
                                dbc.Button(
                                    "Cerrar", 
                                    id="close1", 
                                    className="ml-auto btn btn-secondary", 
                                    n_clicks=0
                                )
                            ]),

                            ],
                            id="modal",
                            centered=True,
                            size="lg",
                            is_open=False,
                        ),

                    ]),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'treemap',
                            figure = {},
                            style={'padding':'0px'},
                            config={'displaylogo': False}
                            ), style={'height':'550px'}
                    )
                ]),

                

            ], lg=6, md=6),

        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Datos Completos'),
                    dbc.CardBody(
                        dbc.Row([
                            dbc.Col('La información que aquí se muestra representa los datos de los hechos viales de los últimos 6 años (2015 - 2020) proporcionados por la Secretaría de Seguridad Pública procesados por el IMPLANG.', style={'display':'inline-block'},lg=6, md=6),
                            dbc.Col(
                                html.Div([
                                    html.Button(
                                        html.B("Descarga la base de datos completa"), 
                                        id="btn_csv",
                                        className="btn btn-success",
                                        n_clicks=None,
                                        style={'float':'right'}
                                    ),
                                    Download(id="download-dataframe-csv")
                                ]), lg=6, md=6, style={'display':'inline-block'}
                            )
                        ])

                    )
                ])
            ])
        ], className="pt-4")

    ])

#----------

# Datos de Intersecciones

# Nombre
def render_interseccion_nombre(clickData):
    if clickData is None:
        return 'Da click en una intersección para saber más información'
    else:
        return clickData['points'][0]['hovertext']

# Hechos Viales
def render_interseccion_hv(clickData, start_date, end_date, slider_hora, checklist_dias):

    if clickData is None:
        
        return '0'

    elif clickData is not None:
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
        hv_tiempo_data_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hv_tiempo_data_cal_dsm = hv_tiempo_data_cal[hv_tiempo_data_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hv_tiempo_data_cal_dsm_hora = hv_tiempo_data_cal_dsm[(hv_tiempo_data_cal_dsm['hora']>=slider_hora[0])&(hv_tiempo_data_cal_dsm['hora']<=slider_hora[1])]
        
        #Sumo los hechos viales
        interseccion_hv = hv_tiempo_data_cal_dsm_hora["hechos_viales"].sum()

        return interseccion_hv

# Lesionados
def render_interseccion_les(clickData, start_date, end_date, slider_hora, checklist_dias):

    if clickData is None:
        
        return '0'

    elif clickData is not None:

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
        hv_tiempo_data_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hv_tiempo_data_cal_dsm = hv_tiempo_data_cal[hv_tiempo_data_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hv_tiempo_data_cal_dsm_hora = hv_tiempo_data_cal_dsm[(hv_tiempo_data_cal_dsm['hora']>=slider_hora[0])&(hv_tiempo_data_cal_dsm['hora']<=slider_hora[1])]

        #Sumo los lesionados
        interseccion_les = hv_tiempo_data_cal_dsm_hora["lesionados"].sum()

        return interseccion_les

# Fallecidos
def render_interseccion_fal(clickData, start_date, end_date, slider_hora, checklist_dias):

    if clickData is None:
        
        return '0'

    elif clickData is not None:
    
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
        hv_tiempo_data_cal = hvi.loc[start_date:end_date]
        
        #Filtro por día de la semana
        hv_tiempo_data_cal_dsm = hv_tiempo_data_cal[hv_tiempo_data_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hv_tiempo_data_cal_dsm_hora = hv_tiempo_data_cal_dsm[(hv_tiempo_data_cal_dsm['hora']>=slider_hora[0])&(hv_tiempo_data_cal_dsm['hora']<=slider_hora[1])]

        #Sumo los fallecidos
        interseccion_fal = hv_tiempo_data_cal_dsm_hora["fallecidos"].sum()

        return interseccion_fal


# Mapa
def render_mapa(start_date, end_date, slider_hora, checklist_dias):
    
    if checklist_dias == []:
    
        mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data = pd.DataFrame(mapa_data)

        #-- Graph
        mapa = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=1, 
            zoom=12.2, 
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=0.9))

        mapa.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            )
        )
        mapa.update_traces(marker_color="#c6cc14",
            selected_marker_color="#636EFA",
            unselected_marker_opacity=.5)
    
        return mapa

    elif checklist_dias != []:

        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        
        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        #Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        coords = hvi_cal_dsm_hora.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)
        hechosviales = hvi_cal_dsm_hora.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        les_fall = hvi_cal_dsm_hora.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        mapa_data = join_hv_lf

        #-- Graph
        mapa = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=13, 
            hover_name='interseccion', 
            custom_data=['lesionados', 'fallecidos'],
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=1))

        mapa.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa.update_traces(marker_color="#c6cc14",
            selected_marker_color="#636EFA",
            selected_marker_size=28,
            unselected_marker_opacity=.5)

        return mapa


# Hechos Viales por 
def render_interseccion_hv_tiempo(clickData, periodo_hv, start_date, end_date, slider_hora, checklist_dias):

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
        hv_tiempo_data_cal = hvi

        # Filtro por calendario
        hv_tiempo_data_cal = hv_tiempo_data_cal.loc[start_date:end_date]

        #Filtro por día de la semana
        hv_tiempo_data_cal_dsm = hv_tiempo_data_cal[hv_tiempo_data_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hv_tiempo_data_cal_dsm_hora = hv_tiempo_data_cal_dsm[(hv_tiempo_data_cal_dsm['hora']>=slider_hora[0])&(hv_tiempo_data_cal_dsm['hora']<=slider_hora[1])]
        
        #Transformar datos en dias
        hv_tiempo_data_cal_dsm_hora_res = hv_tiempo_data_cal_dsm_hora.resample("D").sum()
        
        #Agregar fecha
        hv_tiempo_data_cal_dsm_hora_res["fecha_dos"] = hv_tiempo_data_cal_dsm_hora_res.index

        # Graph
        interseccion_hv_tiempo = px.scatter(hv_tiempo_data_cal_dsm_hora_res, 
            x='fecha_dos',
            y='hechos_viales', 
            labels = {'fecha_dos': ''}, 
            template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="markers", 
            fill='tozeroy', 
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br> %{y} hechos viales") #+lines
        interseccion_hv_tiempo.update_xaxes(showgrid = False, 
            showline = True, 
            type="date", 
            spikemode="toaxis+across+marker", 
            spikesnap="data", 
            spikecolor="gray", 
            spikethickness=2,
            tickmode="auto") #, rangemode="normal",rangebreaks=[dict(pattern="day of week")]
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales', 
            tick0 = 0, 
            dtick = 1,
            autorange=True, 
            rangemode="normal")
        interseccion_hv_tiempo.update_layout(dragmode = False, 
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right'
        )

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
        hv_tiempo_data_cal = hvi

        # Filtro por calendario
        hv_tiempo_data_cal = hv_tiempo_data_cal.loc[start_date:end_date]

        #Filtro por día de la semana
        hv_tiempo_data_cal_dsm = hv_tiempo_data_cal[hv_tiempo_data_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hv_tiempo_data_cal_dsm_hora = hv_tiempo_data_cal_dsm[(hv_tiempo_data_cal_dsm['hora']>=slider_hora[0])&(hv_tiempo_data_cal_dsm['hora']<=slider_hora[1])]

        #Transformar datos en meses
        hv_tiempo_data_cal_dsm_hora_res = hv_tiempo_data_cal_dsm_hora.resample("M").sum()
        
        #Agregar fecha
        hv_tiempo_data_cal_dsm_hora_res["fecha_2"] = hv_tiempo_data_cal_dsm_hora_res.index

        # Graph
        interseccion_hv_tiempo = px.scatter(hv_tiempo_data_cal_dsm_hora_res, 
            x='fecha_2',
            y='hechos_viales', 
            labels = {'fecha2': ''}, 
            template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="markers+lines", 
            fill='tozeroy', 
            hovertemplate="<b>%{x|%m/%Y}</b><br> %{y} hechos viales")
        interseccion_hv_tiempo.update_xaxes(showgrid = False, 
            showline = True, 
            title_text='', 
            type="date", 
            spikemode="toaxis+across+marker", 
            spikesnap="data", 
            spikecolor="gray", 
            spikethickness=2,
            tickmode="auto")
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales')
        interseccion_hv_tiempo.update_layout(dragmode = False, 
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right'
        )

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
        hv_tiempo_data_cal = hvi

         # Filtro por calendario
        hv_tiempo_data_cal = hv_tiempo_data_cal.loc[start_date:end_date]

        #Filtro por día de la semana
        hv_tiempo_data_cal_dsm = hv_tiempo_data_cal[hv_tiempo_data_cal["dia_semana"].isin(checklist_dias)]

        #Filtro por hora
        hv_tiempo_data_cal_dsm_hora = hv_tiempo_data_cal_dsm[(hv_tiempo_data_cal_dsm['hora']>=slider_hora[0])&(hv_tiempo_data_cal_dsm['hora']<=slider_hora[1])]

        #Transformar datos en años
        hv_tiempo_data_cal_dsm_hora_res = hv_tiempo_data_cal_dsm_hora.resample("Y").sum()
        
        #Agregar fecha
        hv_tiempo_data_cal_dsm_hora_res["fecha_2"] = hv_tiempo_data_cal_dsm_hora_res.index

        # Graph
        interseccion_hv_tiempo = px.scatter(hv_tiempo_data_cal_dsm_hora_res, 
            x='fecha_2',
            y='hechos_viales', 
            labels = {'fecha2': ''}, 
            template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="markers+lines", 
            fill='tozeroy', hovertemplate="<b>%{x|%Y}</b><br> %{y} hechos viales")
        interseccion_hv_tiempo.update_xaxes(showgrid = False, 
            showline = True, title_text='', 
            type="date", 
            spikemode="toaxis+across+marker", 
            spikesnap="data", 
            spikecolor="gray", 
            spikethickness=2,
            tickmode="auto")
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales')
        interseccion_hv_tiempo.update_layout(dragmode = False, 
            hoverlabel = dict(font_size = 16),
            hoverlabel_align = 'right')

        return interseccion_hv_tiempo

def render_down_data(n_clicks):
    down_data = send_file("assets/hechosviales_sp.xlsx")
    return down_data

def toggle_modal(open1, close1, modal):
    if open1 or close1:
        return not modal
    return modal

def render_tabla(clickData, start_date, end_date, slider_hora, checklist_dias):
    
    # Leer csv
    hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
    
    # Filter interseccion
    hvi = hvi[hvi['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Cambiar variables a string
    hvi["año"] = hvi["año"].astype(str)
    hvi["mes"] = hvi["mes"].astype(str)
    hvi["dia"] = hvi["dia"].astype(str)

    # Crear variable datetime
    hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
    hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

    # Duplicar columna de fecha y set index
    hvi["fecha2"] = hvi["fecha"]
    hvi = hvi.set_index("fecha")
    hvi = hvi.sort_index()

    # Filtro por calendario
    hvi_cal = hvi.loc[start_date:end_date]

    #Filtro por día de la semana
    hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

    #Filtro por hora
    hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

    tipo_acc = hvi_cal_dsm_hora.pivot_table(index="tipo_accidente", values=["hechos_viales","lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1).sort_values(by=['hechos_viales'], ascending=[0])

    tabla = go.Figure(
        [go.Table(
                header=dict(values=list(['Tipo de accidente','Hechos viales','Fallecidos','Lesionados']),
                    fill_color='#343332',
                    font=dict(color='white'),
                    align='center'),
                cells=dict(values=[tipo_acc.tipo_accidente, tipo_acc.hechos_viales, tipo_acc.lesionados, tipo_acc.fallecidos],
                   fill_color='#F7F7F7',
                   align='center',
                   height=35))
        ])
    tabla.update_layout(margin = dict(t=20, l=20, r=20, b=10))
    
    return tabla

def render_treemap(clickData, start_date, end_date, slider_hora, checklist_dias):

    # Leer csv
    hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
    
    # Filter interseccion
    hvi = hvi[hvi['interseccion'] == 
    clickData['points'][0]['hovertext']]

    # Cambiar variables a string
    hvi["año"] = hvi["año"].astype(str)
    hvi["mes"] = hvi["mes"].astype(str)
    hvi["dia"] = hvi["dia"].astype(str)

    # Crear variable datetime
    hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
    hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

    # Duplicar columna de fecha y set index
    hvi["fecha2"] = hvi["fecha"]
    hvi = hvi.set_index("fecha")
    hvi = hvi.sort_index()

    # Filtro por calendario
    hvi_cal = hvi.loc[start_date:end_date]

    #Filtro por día de la semana
    hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

    #Filtro por hora
    hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]
                        
    causa_acc = hvi_cal_dsm_hora.pivot_table(index="tipo_accidente", columns=["causa_accidente"], values=["hechos_viales"], aggfunc=np.sum)
    causa_acc = causa_acc.fillna(0)

    st_causas = causa_acc['hechos_viales'].stack()
    df_causas = pd.DataFrame(st_causas, columns=['hechos_viales']).reset_index()

    treemap = px.treemap(df_causas, 
                    path=['tipo_accidente', 'causa_accidente'], 
                    values='hechos_viales',
                    color='causa_accidente',
                    )

    #treemap.update_traces(root_color="lightgrey")
    treemap.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    treemap.data[0].hovertemplate = '%{label}<br>%{value}'


    return treemap

#----------

# Display tabs
def render_hechosviales(tab):
    if tab == 'hv_vasconcelos':
        return hv_vasconcelos()