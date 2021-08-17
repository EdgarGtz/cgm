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
                            dbc.Tab(label='Datos Generales', tab_id='hv_general'), #, disabled=True
                            dbc.Tab(label='Intersecciones', tab_id='hv_intersecciones'),
                        ],
                        id='tabs',
                        active_tab="hv_intersecciones",
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

# Intersecciones

# Map

# Mapbox Access Token
mapbox_access_token = 'pk.eyJ1IjoiZWRnYXJndHpnenoiLCJhIjoiY2s4aHRoZTBjMDE4azNoanlxbmhqNjB3aiJ9.PI_g5CMTCSYw0UM016lKPw'
px.set_mapbox_access_token(mapbox_access_token)

# Tabla de intersecciones con coordenadas mapeadas
hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
coords = hvi.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)
coords['hechos_viales'] = ['1']*coords['interseccion'].count()
coords['hechos_viales'] = coords['hechos_viales'].astype(int)
mapa_data = coords

# Graph
mapa = go.Figure(
    px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
    size = 'hechos_viales',
    size_max=5, 
    zoom=13, 
    hover_name='interseccion', 
    #custom_data=['lesionados', 'fallecidos'],
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

# Imágenes
img1 = 'assets/down-arrow.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/info.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

#----------

# Layout - General
def hv_general():

    return html.Div([

        # Controles
         dbc.Row([

            # Calendario
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
            
            # Día de la Semana
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

            # Horario
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
                            id = 'mapa_interac',
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

            ],lg=6, md=6),

            # Principales Indicadores
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

            ], lg=6, md=6),

        ]),



    ])

# Layout - Intersecciones
def hv_intersecciones():

    return html.Div([

        # Controles
         dbc.Row([

            # Calendario
            dbc.Col([

                dbc.Card([
                    dbc.CardHeader([
                        dbc.Button([
                            "Calendario",
                            html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                        style={'width':'3%','float':'right'},
                                        className="pt-1")
                            ],
                            id="collapse_button_cal",
                            className='btn btn-light btn-lg btn-block',
                            color="primary",
                            n_clicks=0,
                            style={'font-size':'17px'},
                        ),

                    ], style={'text-align':'center'}, className='p-0'),

                    dbc.Collapse(
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
                        ], style={'height':'90px'}, className='d-flex align-items-center justify-content-center'),
                        id="collapse_cal",
                        is_open=False,
                    ),

                ])

            ], lg=4, md=4),
            
            # Día de la Semana
            dbc.Col([

                dbc.Card([
                    dbc.CardHeader([
                        dbc.Button([
                            "Día de la Semana",
                            html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                        style={'width':'3%','float':'right'},
                                        className="pt-1")
                            ],
                            id="collapse_button_dsem",
                            className='btn btn-light btn-lg btn-block',
                            color="primary",
                            n_clicks=0,
                            style={'font-size':'17px'},
                        ),

                    ], style={'text-align':'center'}, className='p-0'),

                    dbc.Collapse(
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

                        ], style={'height':'90px'}),
                        id="collapse_dsem",
                        is_open=False,
                    ),

                ])

            ],lg=4, md=4),

            # Horario
            dbc.Col([

                dbc.Card([
                    dbc.CardHeader([
                        dbc.Button([
                            "Horario",
                            html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                        style={'width':'3%','float':'right'},
                                        className="pt-1")
                            ],
                            id="collapse_button_hora",
                            className='btn btn-light btn-lg btn-block',
                            color="primary",
                            n_clicks=0,
                            style={'font-size':'17px'},
                        ),



                    ], style={'text-align':'center'}, className='p-0'),

                    dbc.Collapse(
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
                                ), className='pt-2'
                            ),

                        ], style={'height':'90px'}),
                        id="collapse_hora",
                        is_open=False,
                    ),

                ])
                
            ], lg=4, md=4),

        ], className="d-flex justify-content-between ",),

        html.Br(),

        # Mapa y principales indicadores
        dbc.Row([
            
            # Mapa
            dbc.Col([

                dbc.Card([

                    # Nombre Intersección
                    dbc.CardHeader([
                        
                        ],id='interseccion_nombre',
                        style={'textAlign': 'center'},
                        ),

                    dbc.CardBody(
                        dcc.Graph(
                            id = 'mapa',
                            figure = mapa,
                            config={
                            'displayModeBar': False
                            },
                            style={'height':'80vh'}
                        ),
                    style={'padding':'0px'},
                    )
                ], className="text-white bg-dark"), 

                html.Br(),

            ],lg=6, md=6),

            # Principales Indicadores
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

            ], lg=6, md=6),

        ]),

        # Gráficas Tipos / Tipo y Causa
        dbc.Row([
            
            # Tipos de Hechos Viales
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Tipos de Hechos Viales'),
                    dbc.CardBody(
                        dcc.Graph(
                            id = 'tabla',
                            figure = {},
                            config={'displaylogo': False}
                            ),
                    style={'padding':'0px'}
                    )
                ], style={'height':'550px'})
            ]),
            
            # Hechos viales por Tipo y Causa
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([

                        html.Div([
                            'Hechos Viales por Tipo y Causa',
                            ],
                            className="mt-1", 
                            style={'width':'90%','display':'inline-block'}),

                        html.Span(
                            dbc.Button(
                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                        style={'float':'right'},
                                        className="p-0 img-fluid"), 
                                id="open1", 
                                n_clicks=0, 
                                style={'display':'inline-block',
                                        'float':'right','padding':'0', 
                                        'width':'3%','background-color':'transparent',
                                        'border-color':'transparent',
                                        'margin':'0'},
                                className='rounded-circle'

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
                            )
                    )
                ], style={'height':'550px'}),
            ])
        ]),

        # Inner Footer info extra
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Datos'),
                    dbc.CardBody(
                        dbc.Row([
                            dbc.Col('La información que aquí se muestra representa los datos de los hechos viales de los últimos 6 años (2015 - 2020) y proporcionados por la Secretaría de Seguridad Pública procesados por el IMPLANG.', style={'display':'inline-block'},lg=9, md=9),
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
                                ], className='d-flex justify-content-center'), lg=3, md=3, style={'display':'inline-block'}, className='align-self-center',
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
        return 'Da click en una intersección para conocer más'
    else:
        return clickData['points'][0]['hovertext']

# Hechos Viales
def render_interseccion_hv(clickData, start_date, end_date, slider_hora, checklist_dias):

    # Si no se ha hecho click a una intersección en el mapa pon un cero
    if clickData is None:
        
        return '0'

    # Si le ha hecho click a una intersección en el mapa pon lo siguiente:
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

    # Si no se ha hecho click a una intersección en el mapa pon un cero
    if clickData is None:
        
        return '0'

    # Si le ha hecho click a una intersección en el mapa pon lo siguiente:
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

    # Si no se ha hecho click a una intersección en el mapa pon un cero
    if clickData is None:
        
        return '0'

    # Si le ha hecho click a una intersección en el mapa pon lo siguiente:
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
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)
        coords['hechos_viales'] = ['1']*coords['interseccion'].count()
        coords['hechos_viales'] = coords['hechos_viales'].astype(int)

        # Cambiar nombre
        mapa_data = coords

        #-- Graph
        mapa = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=5, 
            zoom=13, 
            hover_name='interseccion', 
            #custom_data=['lesionados', 'fallecidos'],
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

# Mapa interactivo
def render_mapa_interac(start_date, end_date, slider_hora, checklist_dias):
    
    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == []:
    
        mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data = pd.DataFrame(mapa_data)

        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=1, 
            zoom=12.2, 
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=0.9))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            )
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            selected_marker_color="#636EFA",
            unselected_marker_opacity=.5)
    
        return mapa_interac

    # Si hay algún día seleccionado ponme un mapa con sus puntos
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

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con coordenadas y hechos viales
        join_hv = pd.merge(coords, hechosviales, on ='interseccion', how ='left')

        # Tabla de intersecciones con coordenadas, hechos viales y lesionados y fallecidos
        join_hv_lf = pd.merge(join_hv, les_fall, on ='interseccion', how ='left')

        # Cambiar nombre
        mapa_data = join_hv_lf

        #-- Graph
        mapa_interac = go.Figure(
            px.scatter_mapbox(mapa_data, lat="Lat", lon="Lon",
            size = 'hechos_viales',
            size_max=20, 
            zoom=13, 
            hover_name='interseccion', 
            custom_data=['lesionados', 'fallecidos'],
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#42f581",
            selected_marker_color="#636EFA",
            selected_marker_size=28,
            unselected_marker_opacity=.5)

        return mapa_interac

# Hechos Viales por 
def render_interseccion_hv_tiempo(clickData, periodo_hv, start_date, end_date, slider_hora, checklist_dias):

    # Tab de Día
    if periodo_hv == 'dia' and clickData is None:

        # Leer csv
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

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
        hvi_ceros = hvi

        hvi_ceros_res = hvi_ceros.resample("D").sum()
        hvi_ceros_res["fecha_dos"] = hvi_ceros_res.index
        hvi_ceros_res['ceros'] = ['0']*hvi_ceros_res['fecha_dos'].count()
        hvi_ceros_res['ceros'] = hvi_ceros_res['ceros'].astype(int)
        hvi_ceros_res_data = hvi_ceros_res

        # Graph
        interseccion_hv_tiempo = px.scatter(hvi_ceros_res_data, 
            x='fecha_dos',
            y='ceros',  
            template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="lines", 
            )
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales', 
            tick0 = 0, 
            dtick = 1,
            fixedrange = True,
            range = [0,5],
            showgrid = False)
        interseccion_hv_tiempo.update_xaxes(title_text='', )
        interseccion_hv_tiempo.update_layout(dragmode = False, 
            hovermode=False
        )

        return interseccion_hv_tiempo

    elif periodo_hv == 'dia' and clickData is not None:

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

    # Tab de Mes
    if periodo_hv == 'mes' and clickData is None:

        # Leer csv
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')

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
        hvi_ceros = hvi

        hvi_ceros_res = hvi_ceros.resample("M").sum()
        hvi_ceros_res["fecha_dos"] = hvi_ceros_res.index
        hvi_ceros_res['ceros'] = ['0']*hvi_ceros_res['fecha_dos'].count()
        hvi_ceros_res['ceros'] = hvi_ceros_res['ceros'].astype(int)
        hvi_ceros_res_data = hvi_ceros_res

        # Graph
        interseccion_hv_tiempo = px.scatter(hvi_ceros_res_data, 
            x='fecha_dos',
            y='ceros',  
            template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="lines", 
            )
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales', 
            tick0 = 0, 
            dtick = 1,
            fixedrange = True,
            range = [0,5],
            showgrid = False)
        interseccion_hv_tiempo.update_xaxes(title_text='', )
        interseccion_hv_tiempo.update_layout(dragmode = False, 
            hovermode=False
        )

        return interseccion_hv_tiempo

    elif periodo_hv == 'mes' and clickData is not None:
    
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

    # Tab de Año
    if periodo_hv == 'año' and clickData is None:

        # Leer csv
        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
       
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
        hvi_ceros = hvi

        hvi_ceros_res = hvi_ceros.resample("Y").sum()
        hvi_ceros_res["fecha_dos"] = hvi_ceros_res.index
        hvi_ceros_res['ceros'] = ['0']*hvi_ceros_res['fecha_dos'].count()
        hvi_ceros_res['ceros'] = hvi_ceros_res['ceros'].astype(int)
        hvi_ceros_res_data = hvi_ceros_res

        # Graph
        interseccion_hv_tiempo = px.scatter(hvi_ceros_res_data, 
            x='fecha_dos',
            y='ceros',  
            template = 'plotly_white')
        interseccion_hv_tiempo.update_traces(mode="lines", 
            )
        interseccion_hv_tiempo.update_yaxes(title_text='Hechos viales', 
            tick0 = 0, 
            dtick = 1,
            fixedrange = True,
            range = [0,5],
            showgrid = False)
        interseccion_hv_tiempo.update_xaxes(title_text='', )
        interseccion_hv_tiempo.update_layout(dragmode = False, 
            hovermode=False
        )

        return interseccion_hv_tiempo

    elif periodo_hv == 'año' and clickData is not None:
    
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

# Descargar Excel
def render_down_data(n_clicks):
    down_data = send_file("assets/hechosviales_sp.xlsx")
    return down_data

# Cerrar la ventana de información de los tipos de hechos viales
def toggle_modal(open1, close1, modal):
    if open1 or close1:
        return not modal
    return modal

# Tabla de Tipos de hechos viales
def render_tabla(clickData, start_date, end_date, slider_hora, checklist_dias):
    
    # Si no se ha hecho click a una intersección en el mapa pon un cero
    if clickData is None:
        
        # Leer csv
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
        
        # Crear una tabla por tipo de hecho vial con las causas en las columnas y que tenga la suma del número de hechos viales 
        causa_hv = hvi_cal_dsm_hora.pivot_table(index="tipo_accidente", columns=["causa_accidente"], values=["hechos_viales"], aggfunc=np.sum)

        # Reemplazar NAs con ceros
        causa_hv = causa_hv.fillna(0)

        # Hacer una tabla con las causas apiladas
        st_causas = causa_hv['hechos_viales'].stack()

        # Repetir tipo de hecho vial y convertir a DataFrame
        df_causas = pd.DataFrame(st_causas, columns=['hechos_viales']).reset_index()
        df_causas['hechos_viales'] = ['0']*df_causas['hechos_viales'].count()
        df_causas['hechos_viales'] = df_causas['hechos_viales'].astype(int)


        # Treemap
        tabla = px.treemap(df_causas, 
                        path=['tipo_accidente', 'causa_accidente'], 
                        values='hechos_viales',
                        color='causa_accidente',
                        )
        tabla.update_layout(margin = dict(t=0, l=0, r=0, b=0),
            hovermode=False)


        return tabla

    # Si le ha hecho click a una intersección en el mapa pon lo siguiente:
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

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

        # Duplicar columna de fecha y set index
        hvi["fecha2"] = hvi["fecha"]
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Crear una tabla por tipo de accidente que tenga la suma del número de hechos viales, lesionados y fallecidos ordenados de mayor a menor por número de hechos viales
        tipo_hv = hvi_cal_dsm_hora.pivot_table(index="tipo_accidente", values=["hechos_viales","lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1).sort_values(by=['hechos_viales'], ascending=[0]) 

        # Tabla
        tabla = go.Figure(
            [go.Table(
                    header=dict(values=list(['Tipo de accidente','Hechos viales','Fallecidos','Lesionados']),
                        fill_color='#343332',
                        font=dict(color='white'),
                        align='center'),
                    cells=dict(values=[tipo_hv.tipo_accidente, tipo_hv.hechos_viales, tipo_hv.lesionados, tipo_hv.fallecidos],
                       fill_color='#F7F7F7',
                       align='center',
                       height=35))
            ])
        tabla.update_layout(margin = dict(t=20, l=20, r=20, b=10))
    
    return tabla

# Treemap Hechos Viales por Tipo y Causa
def render_treemap(clickData, start_date, end_date, slider_hora, checklist_dias):

    # Si no se ha hecho click a una intersección en el mapa pon un cero
    if clickData is None:
        
        # Leer csv
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
        
        # Crear una tabla por tipo de hecho vial con las causas en las columnas y que tenga la suma del número de hechos viales 
        causa_hv = hvi_cal_dsm_hora.pivot_table(index="tipo_accidente", columns=["causa_accidente"], values=["hechos_viales"], aggfunc=np.sum)

        # Reemplazar NAs con ceros
        causa_hv = causa_hv.fillna(0)

        # Hacer una tabla con las causas apiladas
        st_causas = causa_hv['hechos_viales'].stack()

        # Repetir tipo de hecho vial y convertir a DataFrame
        df_causas = pd.DataFrame(st_causas, columns=['hechos_viales']).reset_index()
        df_causas['hechos_viales'] = ['0']*df_causas['hechos_viales'].count()
        df_causas['hechos_viales'] = df_causas['hechos_viales'].astype(int)


        # Treemap
        treemap = px.treemap(df_causas, 
                        path=['tipo_accidente', 'causa_accidente'], 
                        values='hechos_viales',
                        color='causa_accidente',
                        )
        treemap.update_layout(margin = dict(t=0, l=0, r=0, b=0),
            hovermode=False)


        return treemap

    # Si le ha hecho click a una intersección en el mapa pon lo siguiente:
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
        
        # Crear una tabla por tipo de hecho vial con las causas en las columnas y que tenga la suma del número de hechos viales 
        causa_hv = hvi_cal_dsm_hora.pivot_table(index="tipo_accidente", columns=["causa_accidente"], values=["hechos_viales"], aggfunc=np.sum)

        # Reemplazar NAs con ceros
        causa_hv = causa_hv.fillna(0)

        # Hacer una tabla con las causas apiladas
        st_causas = causa_hv['hechos_viales'].stack()

        # Repetir tipo de hecho vial y convertir a DataFrame
        df_causas = pd.DataFrame(st_causas, columns=['hechos_viales']).reset_index()

        # Treemap
        treemap = px.treemap(df_causas, 
                        path=['tipo_accidente', 'causa_accidente'], 
                        values='hechos_viales',
                        color='causa_accidente',
                        )
        treemap.update_layout(margin = dict(t=0, l=0, r=0, b=0))
        treemap.data[0].hovertemplate = '%{label}<br>%{value}'

        return treemap

def render_collapse_button_cal(n, is_open):
    if n:
        return not is_open
    return collapse_button

def render_collapse_button_dsem(n, is_open):
    if n:
        return not is_open
    return collapse_button_dsem

def render_collapse_button_hora(n, is_open):
    if n:
        return not is_open
    return collapse_button_hora

#----------

# Display tabs
def render_hechosviales(tab):
    if tab == 'hv_intersecciones':
        return hv_intersecciones()

    elif tab == 'hv_general':
        return hv_general()