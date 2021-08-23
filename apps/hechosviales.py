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
                        active_tab="hv_general",
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
    zoom=12.8, 
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

       

        html.Br(),

        # Mapa y filtros
        dbc.Row([

            # Controles
            dbc.Col([

                dbc.Card([
                   dbc.CardHeader(['Usa los filtros para hacer una búsqueda'])
                ], className='bg-dark', style={'text-align':'center','color':'white'}),

                html.Br(),

                # ¿Cuándo?
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "¿Cuándo?",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_cal",
                                    className='btn btn-light btn-lg btn-block',
                                    color="primary",
                                    n_clicks=0,
                                    style={'font-size':'16px'},
                                ),

                            ], style={'text-align':'center'}, className='p-0'),

                            dbc.Collapse(

                                dbc.CardBody([

                                    html.Div([

                                        dcc.DatePickerRange(
                                            id = 'calendario',
                                            min_date_allowed = dt(2015, 1, 1),
                                            max_date_allowed = dt(2020, 12, 31),
                                            start_date = dt(2015, 1, 1),
                                            end_date = dt(2020, 12, 31),
                                            first_day_of_week = 1,
                                            className="d-flex justify-content-center"
                                        ),

                                    ], className='d-flex align-items-center justify-content-center'),

                                    html.Br(),

                                    dcc.Checklist(
                                        id='checklist_dias',
                                        className="d-flex justify-content-center btn-group ",
                                        options=[
                                            {'label': ' LU', 'value': 'Lunes'},
                                            {'label': ' MA', 'value': 'Martes'},
                                            {'label': ' MI', 'value': 'Miércoles'},
                                            {'label': ' JU', 'value': 'Jueves'},
                                            {'label': ' VI', 'value': 'Viernes'},
                                            {'label': ' SA', 'value': 'Sábado'},
                                            {'label': ' DO', 'value': 'Domingo'},
                                        ],
                                        value=['Lunes', 'Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'],
                                        inputClassName='form-check-input custom-input-check',
                                        labelClassName="btn btn-secondary ",
                                        style={'display':'inline-block'}
                                    ),

                                    html.Br(),

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

                                ]),
                                id="collapse_cal",
                                is_open=False,
                            ),

                        ])

                    ], lg=12, md=12),

                ], className="d-flex justify-content-between ",),

                html.Br(),

                # ¿Qué buscas?
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "¿Qué buscas?",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_dsem",
                                    className='btn btn-light btn-lg btn-block',
                                    color="primary",
                                    n_clicks=0,
                                    style={'font-size':'16px'},
                                ),

                            ], style={'text-align':'center'}, className='p-0'),

                            dbc.Collapse(
                                dbc.CardBody([

                                    html.Div([
                                        
                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_sev", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'5%','background-color':'transparent',
                                                        'border-color':'transparent',},
                                                className='rounded-circle pt-1'

                                                ),

                                            id="tooltip-target-sev",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-sev",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Severidad de Hechos Viales")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Todos:'),' Hechos viales graves y no graves.']),
                                                    html.Li([html.B('Graves:'),' Hechos viales en los que resultaron personas lesionadas o fallecidas.']),
                                                    html.Li([html.B('Lesionados:'),' Hechos viales en los que resultaron personas lesionadas.']),
                                                    html.Li([html.B('Fallecidos:'),' Hechos viales en los que resultaron personas fallecidas.']),
                                                    html.Br(),
                                                    html.Li([
                                                        html.P([html.B('Nota:'), 
                                                            ' Es importante destacar que, de acuerdo con la información proporcionada por la Secretaría de Seguridad Pública, es posible identificar la cantidad de personas lesionadas o fallecidas para cada hecho vial, pero no se puede reconocer si esta cantidad corresponde al responsable o al afectado.',
                                                            html.Br(),html.Br(), 'De la misma manera, en el caso de que en un hecho vial resulte más de una persona lesionada y que además también ocurran decesos, no es posible identificar de manera digital a cada involucrado.']),
                                                            ])
                                                ], style={'list-style-type':'none'}, className="p-1"),

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_sev", 
                                                    className="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_sev",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                        ),

                                        html.P(' Severidad de hecho vial:',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.RadioItems(
                                        id = 'hv_graves_opciones',
                                        className = 'radio-group btn-group',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
                                        value = 'todos',
                                        options = [
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': 'Graves', 'value': 'graves'},
                                            {'label': 'Lesionados', 'value': 'lesionados'},
                                            {'label': 'Fallecidos', 'value': 'fallecidos'},
                                        ]
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.Div([

                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_usaf", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'5%','background-color':'transparent',
                                                        'border-color':'transparent',},
                                                className='rounded-circle pt-1'

                                                ),

                                            id="tooltip-target-usaf",
                                            style={"textDecoration": "underline", "cursor": "pointer"},
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-usaf"
                                        ),
                                    
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Usuarios afectados")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Todos:'),' Personas peatonas ciclistas, motociclistas y demás conductores de otros vehículos motorizados.']),
                                                    html.Li([html.B('Peatón:'),' Personas que caminan.']),
                                                    html.Li([html.B('Ciclista:'),' Personas que utilizan la bicicleta como modo de transporte.']),
                                                    html.Li([html.B('Motociclista:'),' Personas que utilizan la motocicleta como modo de transporte.']),
                                                ], style={'list-style-type':'none'}, className="p-1")

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_usaf", 
                                                    className="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_usaf",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                        ),

                                        html.P('Usuarios afectados:', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),   

                                    dbc.RadioItems(
                                        id = 'hv_usvuln_opciones',
                                        className = 'radio-group btn-group',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
                                        value = 'todos',
                                        options = [
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': 'Peatón', 'value': 'Peaton'},
                                            {'label': 'Ciclista', 'value': 'Bicicleta'},
                                            {'label': 'Motociclista', 'value': 'Motocicleta'}
                                        ]
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.Div([

                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_thv", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'5%','background-color':'transparent',
                                                        'border-color':'transparent',},
                                                className='rounded-circle pt-1'

                                                ),

                                            id="tooltip-target-thv",
                                            style={"textDecoration": "underline", "cursor": "pointer"},
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-thv",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Tipos de Hechos Viales")),

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

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_thv", 
                                                    className="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_thv",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                        ),

                                        html.P('Tipo de hecho vial:', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.Checklist(
                                        id = 'checklist_tipo_hv',
                                        className="btn-group",
                                        labelClassName="btn btn-secondary",
                                        style={'display':'inline-block'},
                                        value = [],
                                        options = [],
                                    ),

                                ]),
                                id="collapse_dsem",
                                is_open=True,
                            ),

                        ])

                    ],lg=12, md=12),

                ]),

                html.Br(),
                
                # Búsqueda avanzada
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "Búsqueda avanzada",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_hora",
                                    className='btn btn-light btn-lg btn-block',
                                    color="primary",
                                    n_clicks=0,
                                    style={'font-size':'16px'},
                                ),



                            ], style={'text-align':'center'}, className='p-0'),

                            dbc.Collapse(
                                dbc.CardBody([

                                    html.Div([
                                        
                                        html.Span(
                                            dbc.Button(
                                                html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                                        style={'float':'right'},
                                                        className="p-0 img-fluid"), 
                                                id="open1_sev", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'5%','background-color':'transparent',
                                                        'border-color':'transparent',},
                                                className='rounded-circle pt-1'

                                                ),

                                            id="tooltip-target-sev",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-sev",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Severidad de Hechos Viales")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Afectado:'),' Sujeto perjudicado del siniestro vial.']),
                                                    html.Li([html.B('Responsable:'),' Sujeto causante del siniestro vial.']),
                                                    html.Br(),
                                                    html.Li([
                                                        html.P([html.B('Nota:'), 
                                                            ' Es importante destacar que, para el caso de los atropellos al momento de registrar la información sólo se captura de manera digital la información sobre el contexto del hecho vial y de los vehículos, mientras que la información del perfil de las personas que no transitan en un vehículo (peatonas) sólo se registra de manera física en el parte vial y no digital, por lo que actualmente no es posible conocer el perfil demográfico (edad, sexo) de las personas atropelladas.',]),
                                                            ])
                                                ], style={'list-style-type':'none'}, className="p-1"),

                                            ],style={"textAlign":"justify",'font-size':'100%'}),

                                            dbc.ModalFooter([
                                                
                                                dbc.Button(
                                                    "Cerrar", 
                                                    id="close1_sev", 
                                                    className="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_sev",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                        ),

                                        html.P(' Afectado o responsable:',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.RadioItems(
                                        id = 'hv_afres_opciones',
                                        className = 'radio-group btn-group',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
                                        value = 'todos',
                                        options = [
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': 'Afectados', 'value': 'afectados'},
                                            {'label': 'Responsables', 'value': 'responsables'},
                                        ]
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.P(' Sexo:',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    dbc.RadioItems(
                                        id = 'hv_sexo_opciones',
                                        className = 'radio-group btn-group',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
                                        value = 'todos',
                                        options = [
                                            {'label': 'Todos', 'value': 'todos'},
                                            {'label': 'Masculino', 'value': 'Masculino'},
                                            {'label': 'Femenino', 'value': 'Femenino'},
                                        ],
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.P(' Edad:',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    html.Br(),

                                    dcc.RangeSlider(
                                        id='slider_edad',
                                        min=0,
                                        max=85,
                                        value=[0,85],
                                        step=5,
                                        marks={
                                            1: {'label': '0'},
                                            5: {'label': '5'},
                                            10: {'label': '10'},
                                            15: {'label': '15'},
                                            20: {'label': '20'},
                                            25: {'label': '25'},
                                            30: {'label': '30'},
                                            35: {'label': '35'},
                                            40: {'label': '40'},
                                            45: {'label': '45'},
                                            50: {'label': '50'},
                                            55: {'label': '55'},
                                            60: {'label': '60'},
                                            65: {'label': '65'},
                                            70: {'label': '70'},
                                            75: {'label': '75'},
                                            80: {'label': '80'},
                                            85: {'label': '85+'},
                                        },
                                        allowCross=False,
                                        dots=True,
                                        tooltip={'always_visible': False , "placement":"bottom"},
                                        updatemode='drag',
                                        className='px-2 pt-2',
                                    ),

                                    html.Br(),

                                    html.P(' Tipo de vehículo:',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    dcc.Checklist(
                                        id='checklist_tipo_veh',
                                        className="btn-group ",
                                        options=[
                                            {'label': ' Auto', 'value': 'Auto'},
                                            {'label': ' Bicicleta', 'value': 'Bicicleta'},
                                            {'label': ' Camión de pasajeros', 'value': 'Camión de pasajeros'},
                                            {'label': ' Camioneta', 'value': 'Camioneta'},
                                            {'label': ' Carga pesada', 'value': 'Carga pesada'},
                                            {'label': ' Mini Van', 'value': 'Mini Van'},
                                            {'label': ' Motocicleta', 'value': 'Motocicleta'},
                                            {'label': ' Pick Up', 'value': 'Pick Up'},
                                            {'label': ' Tracción animal', 'value': 'Tracción animal'},
                                            {'label': ' Trailer', 'value': 'Trailer'},
                                            {'label': ' Tren', 'value': 'Tren'},
                                        ],
                                        value=['Auto', 'Bicicleta','Camión de pasajeros','Camioneta','Carga pesada','Mini Van','Motocicleta','Pick Up','Tracción animal','Trailer','Tren'],
                                        labelClassName="btn btn-secondary ",
                                        style={'display':'inline-block'}
                                    ),

                                ]),
                                id="collapse_hora",
                                is_open=False,
                            ),

                        ])
                        
                    ], lg=12, md=12),

                ])


            ],lg=4, md=4),
            
            # Mapa
            dbc.Col([

                dbc.Card([

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

            ],lg=8, md=8),

        ]),

        # Inner Footer info extra
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Datos'),
                    dbc.CardBody(
                        dbc.Row([
                            dbc.Col('Datos de hechos viales de los últimos 6 años (2015 - 2020) proporcionados por la Secretaría de Seguridad Pública y procesados por el IMPLANG.', style={'display':'inline-block'},lg=9, md=9),
                            dbc.Col(
                                html.Div([
                                    html.Button(
                                        html.B("Descarga la base de datos completa"), 
                                        id="btn_csv",
                                        className="btn",
                                        n_clicks=None,
                                        style={'float':'right','background-color':'#636EFA','color':'white'}
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
                            style={'font-size':'16px'},
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
                            style={'font-size':'16px'},
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
                            style={'font-size':'16px'},
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
                            style={'height':'100%'}
                        ),
                    style={'padding':'0px'},
                    )
                ], style={'height':'96%'} ,className="text-white bg-dark"), 

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
                                active_tab="año",
                                card=True
                                )
                            ]),
                            dbc.CardBody([

                                dcc.Graph(
                                    id = 'interseccion_hv_tiempo',
                                    figure = {},
                                    config={
                                        'modeBarButtonsToRemove':
                                        ['lasso2d', 'pan2d',
                                        'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                        'resetScale2d', 'hoverClosestCartesian',
                                        'hoverCompareCartesian', 'toggleSpikelines',
                                        'select2d',],
                                        'displaylogo': False
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
                                        'border-color':'transparent',},
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

                            dbc.ModalHeader(html.B("Tipos de Hechos Viales")),

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

                            ],style={"textAlign":"justify",'font-size':'100%'}),

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
                            dbc.Col('Datos de hechos viales de los últimos 6 años (2015 - 2020) proporcionados por la Secretaría de Seguridad Pública y procesados por el IMPLANG.', style={'display':'inline-block'},lg=9, md=9),
                            dbc.Col(
                                html.Div([
                                    html.Button(
                                        html.B("Descarga la base de datos completa"), 
                                        id="btn_csv",
                                        className="btn",
                                        n_clicks=None,
                                        style={'float':'right','background-color':'#636EFA','color':'white'}
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

# Checklist de tipos de hechos viales dependiendo de los usuarios afectados opciones
def render_opciones_dos(hv_usvuln_opciones, hv_graves_opciones):

    # Todos

    if hv_usvuln_opciones == 'todos' and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caída de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif hv_usvuln_opciones == 'Peaton' and hv_graves_opciones == 'todos':

       return [
            {'label': 'Atropello', 'value': 'Atropello'}
        ]

    elif hv_usvuln_opciones == 'Bicicleta' and hv_graves_opciones == 'todos':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': 'Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': 'Choque de Frente', 'value': 'Choque de Frente'},
            {'label': 'Choque Diverso', 'value': 'Choque Diverso'},
            {'label': 'Choque Lateral', 'value': 'Choque Lateral'},
        ]

    elif hv_usvuln_opciones == 'Motocicleta' and hv_graves_opciones == 'todos':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': 'Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': 'Choque de Frente', 'value': 'Choque de Frente'},
            {'label': 'Choque Diverso', 'value': 'Choque Diverso'},
            {'label': 'Choque Lateral', 'value': 'Choque Lateral'},
            {'label': 'Estrellamiento', 'value': 'Estrellamiento'},
        ]

    # Graves

    elif hv_usvuln_opciones == 'todos' and hv_graves_opciones == 'graves':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caída de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif hv_usvuln_opciones == 'Peaton' and hv_graves_opciones == 'graves':

       return [
            {'label': 'Atropello', 'value': 'Atropello'}
        ]

    elif hv_usvuln_opciones == 'Bicicleta' and hv_graves_opciones == 'graves':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': 'Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': 'Choque de Frente', 'value': 'Choque de Frente'},
            {'label': 'Choque Diverso', 'value': 'Choque Diverso'},
            {'label': 'Choque Lateral', 'value': 'Choque Lateral'},
        ]

    elif hv_usvuln_opciones == 'Motocicleta' and hv_graves_opciones == 'graves':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': 'Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': 'Choque de Frente', 'value': 'Choque de Frente'},
            {'label': 'Choque Diverso', 'value': 'Choque Diverso'},
            {'label': 'Choque Lateral', 'value': 'Choque Lateral'},
        ]

    # Lesionados

    elif hv_usvuln_opciones == 'todos' and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caída de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif hv_usvuln_opciones == 'Peaton' and hv_graves_opciones == 'lesionados':

       return [
            {'label': 'Atropello', 'value': 'Atropello'}
        ]

    elif hv_usvuln_opciones == 'Bicicleta' and hv_graves_opciones == 'lesionados':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': 'Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': 'Choque Lateral', 'value': 'Choque Lateral'},
        ]

    elif hv_usvuln_opciones == 'Motocicleta' and hv_graves_opciones == 'lesionados':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': 'Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': 'Choque de Frente', 'value': 'Choque de Frente'},
            {'label': 'Choque Diverso', 'value': 'Choque Diverso'},
            {'label': 'Choque Lateral', 'value': 'Choque Lateral'},
        ]

    # Fallecidos

    elif hv_usvuln_opciones == 'todos' and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif hv_usvuln_opciones == 'Peaton' and hv_graves_opciones == 'fallecidos':

       return [
            {'label': 'Atropello', 'value': 'Atropello'}
        ]

    elif hv_usvuln_opciones == 'Bicicleta' and hv_graves_opciones == 'fallecidos':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]

    elif hv_usvuln_opciones == 'Motocicleta' and hv_graves_opciones == 'fallecidos':

        return [
            {'label': 'Alcance', 'value': 'Alcance'},
            {'label': 'Choque de Crucero', 'value': 'Choque de Crucero'},
        ]

# Checklist de tipos de hechos viales dependiendo de los usuarios afectados valores
def render_opciones_dos_dos(hv_usvuln_opciones):

    # Todos

    if hv_usvuln_opciones == 'todos':

       return ['Alcance','Atropello','Caída de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif hv_usvuln_opciones == 'Peaton':

        return ['Atropello']

    elif hv_usvuln_opciones == 'Bicicleta':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral']

    elif hv_usvuln_opciones == 'Motocicleta':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']

    # Graves

    elif hv_usvuln_opciones == 'todos' and hv_graves_opciones == 'graves':

        return ['Alcance','Atropello','Caída de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif hv_usvuln_opciones == 'Peaton' and hv_graves_opciones == 'graves':

        return ['Atropello']

    elif hv_usvuln_opciones == 'Bicicleta' and hv_graves_opciones == 'graves':

        return ['Alcance','Choque de Crucero', 'Choque de Frente','Choque Diverso', 'Choque Lateral']

    elif hv_usvuln_opciones == 'Motocicleta' and hv_graves_opciones == 'graves':

        return ['Alcance','Choque de Crucero', 'Choque de Frente','Choque Diverso', 'Choque Lateral']

    # Lesionados

    elif hv_usvuln_opciones == 'todos' and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caída de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif hv_usvuln_opciones == 'Peaton' and hv_graves_opciones == 'lesionados':

       return ['Atropello']

    elif hv_usvuln_opciones == 'Bicicleta' and hv_graves_opciones == 'lesionados':

        return ['Alcance','Choque de Crucero', 'Choque Lateral']

    elif hv_usvuln_opciones == 'Motocicleta' and hv_graves_opciones == 'lesionados':

        return ['Alcance','Choque de Crucero', 'Choque de Frente','Choque Diverso', 'Choque Lateral']

    # Fallecidos

    elif hv_usvuln_opciones == 'todos' and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Caída de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif hv_usvuln_opciones == 'Peaton' and hv_graves_opciones == 'fallecidos':

       return ['Atropello']

    elif hv_usvuln_opciones == 'Bicicleta' and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque Diverso']

    elif hv_usvuln_opciones == 'Motocicleta' and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero']

# Mapa interactivo
def render_mapa_interac(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usvuln_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == []:
    
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
            zoom=13,
            hover_data={'Lat':False, 'Lon':False, 'hechos_viales':False},
            opacity=0.9))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
        margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=.5)
    
        return mapa_interac

    
    # -------------------------------------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            zoom=12.5, 
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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuarios vulnerables afectados
        us_vuln = hvi_cal_dsm_hora[hvi_cal_dsm_hora.us_vuln != 0]
        hvi_cal_dsm_hora_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv_usvuln = hvi_cal_dsm_hora_usvuln[(hvi_cal_dsm_hora_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usvuln.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usvuln.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usvuln.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_thv_afect = hvi_cal_dsm_hora_thv[hvi_cal_dsm_hora_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_thv_afect_edad = hvi_cal_dsm_hora_thv_afect[(hvi_cal_dsm_hora_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_thv_afect_edad_tveh = hvi_cal_dsm_hora_thv_afect_edad[hvi_cal_dsm_hora_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuarios vulnerables afectados
        us_vuln = hvi_cal_dsm_hora[hvi_cal_dsm_hora.us_vuln != 0]
        hvi_cal_dsm_hora_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv_usvuln = hvi_cal_dsm_hora_usvuln[(hvi_cal_dsm_hora_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_thv_usvuln_afect = hvi_cal_dsm_hora_thv_usvuln[hvi_cal_dsm_hora_thv_usvuln.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_thv_usvuln_afect_edad = hvi_cal_dsm_hora_thv_usvuln_afect[(hvi_cal_dsm_hora_thv_usvuln_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_thv_usvuln_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_thv_usvuln_afect_edad_tveh = hvi_cal_dsm_hora_thv_usvuln_afect_edad[hvi_cal_dsm_hora_thv_usvuln_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usvuln_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usvuln_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usvuln_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    
    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_thv_resp = hvi_cal_dsm_hora_thv[hvi_cal_dsm_hora_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_thv_resp_edad = hvi_cal_dsm_hora_thv_resp[(hvi_cal_dsm_hora_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_thv_resp_edad_tveh = hvi_cal_dsm_hora_thv_resp_edad[hvi_cal_dsm_hora_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuarios vulnerables afectados
        us_vuln = hvi_cal_dsm_hora[hvi_cal_dsm_hora.us_vuln != 0]
        hvi_cal_dsm_hora_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv_usvuln = hvi_cal_dsm_hora_usvuln[(hvi_cal_dsm_hora_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_thv_usvuln_resp = hvi_cal_dsm_hora_thv_usvuln[hvi_cal_dsm_hora_thv_usvuln.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_thv_usvuln_resp_edad = hvi_cal_dsm_hora_thv_usvuln_resp[(hvi_cal_dsm_hora_thv_usvuln_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_thv_usvuln_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_thv_usvuln_resp_edad_tveh = hvi_cal_dsm_hora_thv_usvuln_resp_edad[hvi_cal_dsm_hora_thv_usvuln_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usvuln_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usvuln_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usvuln_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuarios vulnerables afectados
        us_vuln = hvi_cal_dsm_hora[hvi_cal_dsm_hora.us_vuln != 0]
        hvi_cal_dsm_hora_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv_usvuln = hvi_cal_dsm_hora_usvuln[(hvi_cal_dsm_hora_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usvuln.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usvuln.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usvuln.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_thv_afect = hvi_cal_dsm_hora_thv[hvi_cal_dsm_hora_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_afect_sexo = hvi_cal_dsm_hora_thv_afect[hvi_cal_dsm_hora_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_afect_sexo_edad = hvi_cal_dsm_hora_afect_sexo[(hvi_cal_dsm_hora_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_afect_sexo_edad_tveh = hvi_cal_dsm_hora_afect_sexo_edad[hvi_cal_dsm_hora_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuarios vulnerables afectados
        us_vuln = hvi_cal_dsm_hora[hvi_cal_dsm_hora.us_vuln != 0]
        hvi_cal_dsm_hora_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv_usvuln = hvi_cal_dsm_hora_usvuln[(hvi_cal_dsm_hora_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_thv_usvuln_afect = hvi_cal_dsm_hora_thv_usvuln[hvi_cal_dsm_hora_thv_usvuln.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_thv_usvuln_afect_sexo = hvi_cal_dsm_hora_thv_usvuln_afect[hvi_cal_dsm_hora_thv_usvuln_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_thv_usvuln_afect_sexo_edad = hvi_cal_dsm_hora_thv_usvuln_afect_sexo[(hvi_cal_dsm_hora_thv_usvuln_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_thv_usvuln_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_thv_usvuln_afect_sexo_edad_tveh = hvi_cal_dsm_hora_thv_usvuln_afect_sexo_edad[hvi_cal_dsm_hora_thv_usvuln_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usvuln_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usvuln_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usvuln_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_thv_resp = hvi_cal_dsm_hora_thv[hvi_cal_dsm_hora_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_thv_resp_sexo = hvi_cal_dsm_hora_thv_resp[hvi_cal_dsm_hora_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_thv_resp_sexo_edad = hvi_cal_dsm_hora_thv_resp_sexo[(hvi_cal_dsm_hora_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_thv_resp_sexo_edad[hvi_cal_dsm_hora_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuarios vulnerables afectados
        us_vuln = hvi_cal_dsm_hora[hvi_cal_dsm_hora.us_vuln != 0]
        hvi_cal_dsm_hora_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_thv_usvuln = hvi_cal_dsm_hora_usvuln[(hvi_cal_dsm_hora_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_thv_usvuln_resp = hvi_cal_dsm_hora_thv_usvuln[hvi_cal_dsm_hora_thv_usvuln.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_thv_usvuln_resp_sexo = hvi_cal_dsm_hora_thv_usvuln_resp[hvi_cal_dsm_hora_thv_usvuln_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_thv_usvuln_resp_sexo_edad = hvi_cal_dsm_hora_thv_usvuln_resp_sexo[(hvi_cal_dsm_hora_thv_usvuln_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_thv_usvuln_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_thv_usvuln_resp_sexo_edad_tveh = hvi_cal_dsm_hora_thv_usvuln_resp_sexo_edad[hvi_cal_dsm_hora_thv_usvuln_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usvuln_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usvuln_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usvuln_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # -------------------------------------------


    # HECHOS VIALES GRAVES -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales graves seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por tipo de hecho vial
        hv_graves_thv = hv_graves[(hv_graves['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales graves seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_graves[hv_graves.us_vuln != 0]
        hv_graves_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_graves_usvuln_thv = hv_graves_usvuln[(hv_graves_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_usvuln_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_usvuln_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_usvuln_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # HECHOS VIALES GRAVES -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por tipo de hecho vial
        hv_graves_thv = hv_graves[(hv_graves['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_graves_thv_afect = hv_graves_thv[hv_graves_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_graves_thv_afect_edad = hv_graves_thv_afect[(hv_graves_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_graves_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_graves_thv_afect_edad_tveh = hv_graves_thv_afect_edad[hv_graves_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_graves[hv_graves.us_vuln != 0]
        hv_graves_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_graves_usvuln_thv = hv_graves_usvuln[(hv_graves_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_graves_usvuln_thv_afect = hv_graves_usvuln_thv[hv_graves_usvuln_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_graves_usvuln_thv_afect_edad = hv_graves_usvuln_thv_afect[(hv_graves_usvuln_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_graves_usvuln_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_graves_usvuln_thv_afect_edad_tveh = hv_graves_usvuln_thv_afect_edad[hv_graves_usvuln_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # HECHOS VIALES GRAVES -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por tipo de hecho vial
        hv_graves_thv = hv_graves[(hv_graves['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_graves_thv_resp = hv_graves_thv[hv_graves_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_graves_thv_resp_edad = hv_graves_thv_resp[(hv_graves_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_graves_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_graves_thv_resp_edad_tveh = hv_graves_thv_resp_edad[hv_graves_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_graves[hv_graves.us_vuln != 0]
        hv_graves_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_graves_usvuln_thv = hv_graves_usvuln[(hv_graves_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_graves_usvuln_thv_resp = hv_graves_usvuln_thv[hv_graves_usvuln_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_graves_usvuln_thv_resp_edad = hv_graves_usvuln_thv_resp[(hv_graves_usvuln_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_graves_usvuln_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_graves_usvuln_thv_resp_edad_tveh = hv_graves_usvuln_thv_resp_edad[hv_graves_usvuln_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac
    

    # ----------------


    # HECHOS VIALES GRAVES -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales graves seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por tipo de hecho vial
        hv_graves_thv = hv_graves[(hv_graves['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales graves seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_graves[hv_graves.us_vuln != 0]
        hv_graves_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_graves_usvuln_thv = hv_graves_usvuln[(hv_graves_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_usvuln_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_usvuln_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_usvuln_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    
    # HECHOS VIALES GRAVES -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por tipo de hecho vial
        hv_graves_thv = hv_graves[(hv_graves['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_graves_thv_afect = hv_graves_thv[hv_graves_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_graves_thv_afect_edad = hv_graves_thv_afect[(hv_graves_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_graves_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_graves_thv_afect_edad_sexo = hv_graves_thv_afect_edad[hv_graves_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_graves_thv_afect_edad_sexo_tveh = hv_graves_thv_afect_edad_sexo[hv_graves_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_graves[hv_graves.us_vuln != 0]
        hv_graves_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_graves_usvuln_thv = hv_graves_usvuln[(hv_graves_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_graves_usvuln_thv_afect = hv_graves_usvuln_thv[hv_graves_usvuln_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_graves_usvuln_thv_afect_edad = hv_graves_usvuln_thv_afect[(hv_graves_usvuln_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_graves_usvuln_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_graves_usvuln_thv_afect_edad_sexo = hv_graves_usvuln_thv_afect_edad[hv_graves_usvuln_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_graves_usvuln_thv_afect_edad_sexo_tveh = hv_graves_usvuln_thv_afect_edad_sexo[hv_graves_usvuln_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac



    # HECHOS VIALES GRAVES -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por tipo de hecho vial
        hv_graves_thv = hv_graves[(hv_graves['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_graves_thv_resp = hv_graves_thv[hv_graves_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_graves_thv_resp_edad = hv_graves_thv_resp[(hv_graves_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_graves_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_graves_thv_resp_edad_sexo = hv_graves_thv_resp_edad[hv_graves_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_graves_thv_resp_edad_sexo_tveh = hv_graves_thv_resp_edad_sexo[hv_graves_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'graves' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Filtro por hechos viales graves
        hv_graves = hvi_cal_dsm_hora[hvi_cal_dsm_hora.les_fall != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_graves[hv_graves.us_vuln != 0]
        hv_graves_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_graves_usvuln_thv = hv_graves_usvuln[(hv_graves_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_graves_usvuln_thv_resp = hv_graves_usvuln_thv[hv_graves_usvuln_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_graves_usvuln_thv_resp_edad = hv_graves_usvuln_thv_resp[(hv_graves_usvuln_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_graves_usvuln_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_graves_usvuln_thv_resp_edad_sexo = hv_graves_usvuln_thv_resp_edad[hv_graves_usvuln_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_graves_usvuln_thv_resp_edad_sexo_tveh = hv_graves_usvuln_thv_resp_edad_sexo[hv_graves_usvuln_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_graves_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_graves_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_graves_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac



    # -------------------------------------------



    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_les[hv_les.us_vuln != 0]
        hv_les_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_les_usvuln_thv = hv_les_usvuln[(hv_les_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usvuln_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usvuln_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usvuln_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_thv_afect_edad = hv_les_thv_afect[(hv_les_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_edad_tveh = hv_les_thv_afect_edad[hv_les_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_les[hv_les.us_vuln != 0]
        hv_les_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_les_usvuln_thv = hv_les_usvuln[(hv_les_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usvuln_thv_afect = hv_les_usvuln_thv[hv_les_usvuln_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usvuln_thv_afect_edad = hv_les_usvuln_thv_afect[(hv_les_usvuln_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usvuln_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usvuln_thv_afect_edad_tveh = hv_les_usvuln_thv_afect_edad[hv_les_usvuln_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_thv_resp_edad = hv_les_thv_resp[(hv_les_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_edad_tveh = hv_les_thv_resp_edad[hv_les_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_les[hv_les.us_vuln != 0]
        hv_les_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_les_usvuln_thv = hv_les_usvuln[(hv_les_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usvuln_thv_resp = hv_les_usvuln_thv[hv_les_usvuln_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usvuln_thv_resp_edad = hv_les_usvuln_thv_resp[(hv_les_usvuln_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usvuln_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usvuln_thv_resp_edad_tveh = hv_les_usvuln_thv_resp_edad[hv_les_usvuln_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_les[hv_les.us_vuln != 0]
        hv_les_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_les_usvuln_thv = hv_les_usvuln[(hv_les_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usvuln_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usvuln_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usvuln_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_thv_afect = hv_les_thv[hv_les_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_thv_afect_edad = hv_les_thv_afect[(hv_les_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_afect_edad_sexo = hv_les_thv_afect_edad[hv_les_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_edad_sexo_tveh = hv_les_thv_afect_edad_sexo[hv_les_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_les[hv_les.us_vuln != 0]
        hv_les_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_les_usvuln_thv = hv_les_usvuln[(hv_les_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usvuln_thv_afect = hv_les_usvuln_thv[hv_les_usvuln_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usvuln_thv_afect_edad = hv_les_usvuln_thv_afect[(hv_les_usvuln_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usvuln_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usvuln_thv_afect_edad_sexo = hv_les_usvuln_thv_afect_edad[hv_les_usvuln_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usvuln_thv_afect_edad_sexo_tveh = hv_les_usvuln_thv_afect_edad_sexo[hv_les_usvuln_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por tipo de hecho vial
        hv_les_thv = hv_les[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_thv_resp = hv_les_thv[hv_les_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_thv_resp_edad = hv_les_thv_resp[(hv_les_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_resp_edad_sexo = hv_les_thv_resp_edad[hv_les_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_edad_sexo_tveh = hv_les_thv_resp_edad_sexo[hv_les_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_les[hv_les.us_vuln != 0]
        hv_les_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_les_usvuln_thv = hv_les_usvuln[(hv_les_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usvuln_thv_resp = hv_les_usvuln_thv[hv_les_usvuln_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usvuln_thv_resp_edad = hv_les_usvuln_thv_resp[(hv_les_usvuln_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usvuln_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usvuln_thv_resp_edad_sexo = hv_les_usvuln_thv_resp_edad[hv_les_usvuln_thv_resp_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usvuln_thv_resp_edad_sexo_tveh = hv_les_usvuln_thv_resp_edad_sexo[hv_les_usvuln_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac


    # -------------------------------------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales fallecidos seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_fall[hv_fall.us_vuln != 0]
        hv_fall_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_fall_usvuln_thv = hv_fall_usvuln[(hv_fall_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usvuln_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usvuln_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usvuln_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac   

    
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_thv_afect_edad = hv_fall_thv_afect[(hv_fall_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_edad_tveh = hv_fall_thv_afect_edad[hv_fall_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales fallecidos seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_fall[hv_fall.us_vuln != 0]
        hv_fall_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_fall_usvuln_thv = hv_fall_usvuln[(hv_fall_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usvuln_thv_afect = hv_fall_usvuln_thv[hv_fall_usvuln_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_fall_usvuln_thv_afect_edad = hv_fall_usvuln_thv_afect[(hv_fall_usvuln_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usvuln_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usvuln_thv_afect_edad_tveh = hv_fall_usvuln_thv_afect_edad[hv_fall_usvuln_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usvuln_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac   

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_thv_resp_edad = hv_fall_thv_resp[(hv_fall_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_edad_tveh = hv_fall_thv_resp_edad[hv_fall_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales fallecidos seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_fall[hv_fall.us_vuln != 0]
        hv_fall_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_fall_usvuln_thv = hv_fall_usvuln[(hv_fall_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usvuln_thv_resp = hv_fall_usvuln_thv[hv_fall_usvuln_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_fall_usvuln_thv_resp_edad = hv_fall_usvuln_thv_resp[(hv_fall_usvuln_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usvuln_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usvuln_thv_resp_edad_tveh = hv_fall_usvuln_thv_resp_edad[hv_fall_usvuln_thv_resp_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usvuln_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac   


    # ----------------

    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales fallecidos seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_fall[hv_fall.us_vuln != 0]
        hv_fall_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_fall_usvuln_thv = hv_fall_usvuln[(hv_fall_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usvuln_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usvuln_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usvuln_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac   


    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_thv_afect = hv_fall_thv[hv_fall_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_thv_afect_edad = hv_fall_thv_afect[(hv_fall_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hvi_cal_dsm_hora_afect_sexo = hv_fall_thv_afect_edad[hv_fall_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_afect_sexo_tveh = hvi_cal_dsm_hora_afect_sexo[hvi_cal_dsm_hora_afect_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_afect_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_afect_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_afect_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales fallecidos seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_fall[hv_fall.us_vuln != 0]
        hv_fall_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_fall_usvuln_thv = hv_fall_usvuln[(hv_fall_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usvuln_thv_afect = hv_fall_usvuln_thv[hv_fall_usvuln_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_fall_usvuln_thv_afect_edad = hv_fall_usvuln_thv_afect[(hv_fall_usvuln_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usvuln_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usvuln_thv_afect_edad_sexo = hv_fall_usvuln_thv_afect_edad[hv_fall_usvuln_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usvuln_thv_afect_edad_sexo_tveh = hv_fall_usvuln_thv_afect_edad_sexo[hv_fall_usvuln_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usvuln_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac   

    
    # HECHOS VIALES FALLECIDOS -- Responsables

     # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hv_fall_thv = hv_fall[(hv_fall['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_thv_resp = hv_fall_thv[hv_fall_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_thv_resp_edad = hv_fall_thv_resp[(hv_fall_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_resp_edad_sexo = hv_fall_thv_resp_edad[hv_fall_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_edad_sexo_tveh = hv_fall_thv_resp_edad_sexo[hv_fall_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac

    # Si hay algún día seleccionado, los hechos viales fallecidos seleccionados, con cualquier usuario vulnerable
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_usvuln_opciones != 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por hechos viales con fallecidos
        hv_fall = hvi_cal_dsm_hora[hvi_cal_dsm_hora.fallecidos != 0]

        # Filtro por usuarios vulnerables afectados
        us_vuln = hv_fall[hv_fall.us_vuln != 0]
        hv_fall_usvuln = us_vuln[(us_vuln['tipo_v_afec']==hv_usvuln_opciones)]

        # Filtro por tipo de hecho vial
        hv_fall_usvuln_thv = hv_fall_usvuln[(hv_fall_usvuln['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usvuln_thv_resp = hv_fall_usvuln_thv[hv_fall_usvuln_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_fall_usvuln_thv_resp_edad = hv_fall_usvuln_thv_resp[(hv_fall_usvuln_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usvuln_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usvuln_thv_resp_edad_sexo = hv_fall_usvuln_thv_resp_edad[hv_fall_usvuln_thv_resp_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usvuln_thv_resp_edad_sexo_tveh = hv_fall_usvuln_thv_resp_edad_sexo[hv_fall_usvuln_thv_resp_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usvuln_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            unselected_marker_opacity=.5)

        return mapa_interac   

    # -------------------------------------------

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
            showline = False, 
            title_text='', 
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
            showline = False, 
            title_text='', 
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
            showline = False, 
            title_text='', 
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

# Cerrar la ventana de información de la severidad de hechos viales
def toggle_modal_sev(open1_sev, close1_sev, modal_sev):
    if open1_sev or close1_sev:
        return not modal_sev
    return modal_sev

# Cerrar la ventana de información de los usuarios afectados
def toggle_modal_usaf(open1_usaf, close1_usaf, modal_usaf):
    if open1_usaf or close1_usaf:
        return not modal_usaf
    return modal_usaf

# Cerrar la ventana de información de los tipos de hechos viales
def toggle_modal_thv(open1_thv, close1_thv, modal_thv):
    if open1_thv or close1_thv:
        return not modal_thv
    return modal_thv

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

# Tarjeta colapsable calendario
def render_collapse_button_cal(n, is_open):
    if n:
        return not is_open
    return collapse_button

# Tarjeta colapsable días de la semana
def render_collapse_button_dsem(n, is_open):
    if n:
        return not is_open
    return collapse_button_dsem

# Tarjeta colapsable hora
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