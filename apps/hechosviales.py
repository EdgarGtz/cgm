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
import json as json
from datetime import datetime as dt
from dash_extensions import Download
from dash_extensions.snippets import send_file
from dash_extensions.snippets import send_data_frame

import base64

#----------

app = dash.Dash(__name__, title='Centro de Gestión de Movilidad',
                external_stylesheets = [dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'},])



app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-2FB009N3XV"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-2FB009N3XV');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Layout General
def hechosviales():

    return html.Div([

        # Tabs
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label='Inicio', tab_id='hv_general'), #, disabled=True
                            dbc.Tab(label='Intersecciones', tab_id='hv_intersecciones'),
                            dbc.Tab(label='Datos', tab_id='hv_datos'),
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

# Display tabs
def render_hechosviales(tab):
    if tab == 'hv_intersecciones':
        return hv_intersecciones()

    elif tab == 'hv_general':
        return hv_general()

    elif tab == 'hv_datos':
        return hv_datos()

# Descargar Excel
def render_down_data(n_clicks):
    down_data = send_file("assets/hechosviales_sp.xlsx")
    return down_data

# Imágenes
img1 = 'assets/down-arrow.png' # replace with your own image
encoded_img1 = base64.b64encode(open(img1, 'rb').read()).decode('ascii')

img2 = 'assets/informacion.png' # replace with your own image
encoded_img2 = base64.b64encode(open(img2, 'rb').read()).decode('ascii')

img3 = 'assets/descargar.png' # replace with your own image
encoded_img3 = base64.b64encode(open(img3, 'rb').read()).decode('ascii')

#----------

# Layout - General
def hv_general():

    return html.Div([

       

        html.Br(),

        # Mapa y filtros
        dbc.Row([

            # Controles
            dbc.Col([

                # Fechas
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "Fecha",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_fecha",
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

                                    

                                    dbc.Checklist(
                                        id = 'checklist_dias',
                                        className = 'radio-group btn-group d-flex justify-content-center',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
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
                                        updatemode='mouseup'
                                    ),

                                ]),
                                id="collapse_cal",
                                is_open=True,
                            ),

                        ])

                    ], lg=12, md=12),

                ], className="d-flex justify-content-between ",),

                html.Br(),

                # Hechos Viales
                dbc.Row([

                    dbc.Col([

                        dbc.Card([
                            dbc.CardHeader([
                                dbc.Button([
                                    "Hechos Viales",
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                                style={'width':'3%','float':'right'},
                                                className="pt-1")
                                    ],
                                    id="collapse_button_hv",
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
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                className='rounded-circle'

                                            ),

                                            id="tooltip-target-sev",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-sev",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Gravedad de Hechos Viales")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Todos:'),' Hechos viales con lesionados + hechos viales con fallecidos + hechos viales sin lesionados y fallecidos.']),
                                                    html.Li([html.B('Lesionados:'),' Hechos viales en los que resultaron personas lesionadas.']),
                                                    html.Li([html.B('Fallecidos:'),' Hechos viales en los que resultaron personas fallecidas.']),
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

                                        html.P(' Gravedad',
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
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                className='rounded-circle'

                                            ),

                                            id="tooltip-target-usaf",
                                            style={"textDecoration": "underline", "cursor": "pointer"},
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-usaf"
                                        ),
                                    
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Usuario")),

                                            dbc.ModalBody([
                                                html.Ul([
                                                    html.Li([html.B('Auto:'),' Acumulado de personas que conducen auto, camión de pasajeros, camioneta, carga pesada, mini van, pickup, trailer y tren.']),
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

                                        html.P(' Usuario', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),   

                                    dbc.Checklist(
                                        id = 'hv_usu_opciones',
                                        className = 'radio-group btn-group',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
                                        value = ['Motorizado','Peaton','Bicicleta','Motocicleta'],
                                        options = [
                                            {'label': 'Auto', 'value': 'Motorizado'},
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
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                className='rounded-circle'

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
                                                    html.Li([html.B('Atropello:'),' Ocurre cuando un vehículo en movimiento impacta con una persona. La persona puede estar estática o en movimiento ya sea caminando, corriendo o montando en patines, patinetas, o cualquier juguete similar, o trasladándose asistiéndose de aparatos o de vehículos no regulados por este reglamento, esto en el caso de las personas con discapacidad. Es imporante destacar que este tipo de hevho vial se asocia únicamente con peatones.']),
                                                    html.Li([html.B('Caída de persona:'),' Ocurre cuando una persona cae hacia fuera o dentro de un vehículo en movimiento, comúnmente dentro de un autobús de transporte público. ']),
                                                    html.Li([html.B('Choque de crucero:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación que convergen o se cruzan, invadiendo un vehículo parcial o totalmente el arroyo de circulación de otro. ']),
                                                    html.Li([html.B('Choque de Reversa:'),' Ocurre cuando un vehículo choca con otro al ir de reversa.']),
                                                    html.Li([html.B('Choque de Frente:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación opuestos, los cuales chocan cuando uno de ellos invade parcial o totalmente el carril, arroyo de circulación o trayectoria contraria. ']),
                                                    html.Li([html.B('Choque Diverso:'),' En esta clasificación queda cualquier hecho de tránsito no especificado en los puntos anteriores. ']),
                                                    html.Li([html.B('Choque Lateral:'),' Ocurre entre dos o más vehículos cuyos conductores circulan en carriles o con trayectorias paralelas, en el mismo sentido chocando los vehículos entre sí, cuando uno de ellos invada parcial o totalmente el carril o trayectoria donde circula el otro.']),
                                                    html.Li([html.B('Estrellamiento:'),' Ocurre cuando un vehículo en movimiento en cualquier sentido choca con algo que se encuentra provisional o permanentemente estático.']),
                                                    html.Li([html.B('Incendio:'),' Ocurre cuando existe un incendio por un percance vial.']),
                                                    html.Li([html.B('Volcadura:'),' Ocurre cuando un vehículo pierde completamente el contacto entre llantas y superficie de rodamiento originándose giros verticales o transversales']),

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

                                        html.P(' Tipo de hecho vial', style={'width':'90%','float':'left'}, className='pl-1'),

                                    ]),

                                    dbc.Checklist(
                                        id = 'checklist_tipo_hv',
                                        className = 'radio-group btn-group',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
                                        style={'display':'inline-block'},
                                        value = [],
                                        options = [],
                                    ),

                                ]),
                                id="collapse_dsem",
                                is_open=True,
                            ),

                        ]),

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
                                    id="collapse_button_bavan",
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
                                                id="open1_afres", 
                                                n_clicks=0, 
                                                style={'display':'inline-block',
                                                        'float':'left','padding':'0', 
                                                        'width':'15px','background-color':'transparent',
                                                        'border-color':'transparent','padding-top':'5px'},
                                                className='rounded-circle'

                                                ),

                                            id="tooltip-target-afres",
                                        ),

                                        dbc.Tooltip(
                                            "Más información",
                                            target="tooltip-target-afres",
                                        ),
                                            
                                        dbc.Modal([

                                            dbc.ModalHeader(html.B("Afectado o Responsable")),

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
                                                    id="close1_afres", 
                                                    className="ml-auto btn btn-secondary", 
                                                    n_clicks=0
                                                )
                                            ]),

                                            ],
                                            id="modal_afres",
                                            centered=True,
                                            size="lg",
                                            is_open=False,
                                        ),

                                        html.P(' Afectado o responsable',
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

                                    html.P(' Sexo',
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

                                    html.P(' Edad',
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
                                        updatemode='mouseup',
                                        className='px-2 pt-2',
                                    ),

                                    html.Br(),

                                    html.P(' Tipo de vehículo',
                                            style={'width':'90%','float':'left'}, className='pl-1'),

                                    dbc.Checklist(
                                        id = 'checklist_tipo_veh',
                                        className = 'radio-group btn-group',
                                        labelClassName = 'btn btn-secondary',
                                        labelCheckedClassName = 'active',
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
                                        style={'display':'inline-block'}
                                    ),

                                    html.Br(),
                                    html.Br(),

                                    html.P([
                                        html.I([
                                            html.B('Nota:'),
                                            ' Los filtros de "sexo", "edad" y "tipo de vehículo" se activan al seleccionar "Afectados" o "Responsables".'
                                            ])
                                    ]),

                                ]),
                                id="collapse_hora",
                                is_open=False,
                            ),

                        ]),
                        
                    ], lg=12, md=12),

                ])


            ],lg=4, md=4),
            
            # Mapa
            dbc.Col([

                dbc.Card([
                    dbc.CardHeader([
                        
                        dbc.Row([

                            dbc.Col([

                                html.Table([

                                    html.Tr([
                                        html.Th('Hechos Viales ', style={'font-weight':'normal'}),
                                        html.Th(id = 'hv_totales', style={'font-weight':'normal'}),
                                    ]),

                                ]),

                            ], className='d-flex justify-content-center'),

                            dbc.Col([

                                html.Table([

                                    html.Tr([
                                        html.Th('Lesionados: ', style={'font-weight':'normal'}),
                                        html.Th(id = 'hv_les_totales', style={'font-weight':'normal'}),
                                    ]),

                                ]),

                            ], className='d-flex justify-content-center'),

                            dbc.Col([

                                html.Table([

                                    html.Tr([
                                        html.Th('Fallecidos: ', style={'font-weight':'normal'}),
                                        html.Th(id = 'hv_fall_totales', style={'font-weight':'normal'}),
                                    ]),

                                ]),

                            ], className='d-flex justify-content-center'),
                        ])

                    ], style={'padding':'8px'})
                ], style={'textAlign':'center','color':'white'}, className='bg-dark tarjeta_arriba_map'),

                dbc.Card([

                    dbc.CardBody(

                        dcc.Loading(

                            dcc.Graph(
                                id = 'mapa_interac',
                                figure = {},
                                config={
                                'displayModeBar': False
                                },
                                style={'height':'85vh'}
                            ),

                        color="#42f581", type="cube"),

                    style={'padding':'0px'},),

                    dbc.CardBody([
                        dcc.Store(id='mapa_data'),
                        Download(id="download-personal-csv"),
                        html.Button([
                            #html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                            #        style={'width':'8%','float':'left'},
                            #        className="pt-1"),
                            html.B("Descargar datos en CSV"),
                            ], 
                            id="btn_perso_csv",
                            className="btn btn-block",
                            n_clicks=None,
                            style={'float':'right','background-color':'#00b55b','color':'white'}
                        ),
                    ], className='p-0', style={'background-color':'transparent'}),

                ], className='tarjeta_map'), 

            ],lg=8, md=8),

        ]),

    ])


# Filtro colapsable hechos viales
def render_collapse_button_hv(n, is_open):
    if n:
        return not is_open
    return collapse_button_hv

# Filtro colapsable busqueda avanzada
def render_collapse_button_bavan(n, is_open):
    if n:
        return not is_open
    return collapse_button_bavan

# Mapa interactivo
def render_mapa_interac(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
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
            zoom=12.5,
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
            unselected_marker_opacity=1)
    
        return mapa_interac

    
    # -------------------------------------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_thv_usu = hvi_cal_dsm_hora_thv[(hvi_cal_dsm_hora_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_thv_usu.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
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
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
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
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
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
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
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
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
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
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
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
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos viales Totales: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")

        return mapa_interac



    # -------------------------------------------



    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_les_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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
            zoom=12.5, 
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#c6cc14",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Lesionados: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac



    # -------------------------------------------



    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_tveh = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_afect_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_tveh = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_resp_edad_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_afect_edad_sexo = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_sexo_tveh = hv_fall_usu_thv_afect_edad_sexo[hv_fall_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_afect_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac
    
    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_resp_edad_sexo = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_sexo_tveh = hv_fall_usu_thv_resp_edad_sexo[hv_fall_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Tabla de intersecciones con coordenadas mapeadas
        coords = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["Lat","Lon"]).reset_index().rename_axis(None, axis=1)

        # Tabla de intersecciones con suma de hechos viales
        hechosviales = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["hechos_viales"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)
        
        # Tabla de intersecciones con suma de lesionados y fallecidos
        les_fall = hv_fall_usu_thv_resp_edad_sexo_tveh.pivot_table(index="interseccion", values=["lesionados","fallecidos"], aggfunc=np.sum).reset_index().rename_axis(None, axis=1)

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
            custom_data=['lesionados', 'fallecidos','interseccion'],
            hover_data={'Lat':False, 'Lon':False, 'interseccion':True, 'hechos_viales':True, 'lesionados':True, 'fallecidos':True, },
            opacity=1))

        mapa_interac.update_layout(clickmode='event+select', 
             mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=25.6572, lon=-100.3689),
                style="dark"
            ),
            margin = dict(t=0, l=0, r=0, b=0)
        )
        mapa_interac.update_traces(marker_color="#f54242",
            unselected_marker_opacity=1,
            hovertemplate = "<br><b>%{customdata[2]}</b> <br>Hechos Viales con Fallecidos: %{marker.size}<br>Lesionados: %{customdata[0]} <br>Fallecidos:%{customdata[1]}")
        
        return mapa_interac

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
        zoom=12.5,
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
        unselected_marker_opacity=1)

    return mapa_interac

    # -------------------------------------------

# Descargar CSV
def render_down_data_csv(n_clicks, data):
    
    a_json = json.loads(data)
    df = pd.DataFrame.from_dict(a_json, orient="columns")

    csv = send_data_frame(df.to_csv, "hechos_viales_query.csv", index=False, encoding='ISO-8859-1')

    return csv


# Mapa interactivo
def render_mapa_data(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):
    
    # -------------------------------------------

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        mapa_data = {
           "Lat": pd.Series(25.6572),
           "Lon": pd.Series(-100.3689),
            "hechos_viales" : pd.Series(0),
           }
        mapa_data = pd.DataFrame(mapa_data)

        # Cambiar a JSON
        mapa_data = mapa_data.reset_index()
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    
    # -------------------------------------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

        hvi = pd.read_csv("assets/hechosviales_lite.csv", encoding='ISO-8859-1')
        
        # Cambiar variables a string
        hvi["año"] = hvi["año"].astype(str)
        hvi["mes"] = hvi["mes"].astype(str)
        hvi["dia"] = hvi["dia"].astype(str)

        # Crear variable datetime
        hvi["fecha"] = hvi["dia"] +"/"+ hvi["mes"] + "/"+ hvi["año"]
        hvi["fecha"]  = pd.to_datetime(hvi["fecha"], dayfirst = True, format ='%d/%m/%Y') # - %H

        # Duplicar columna de fecha y set index
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

        # Filtro por usuario
        hvi_cal_dsm_hora_thv_usu = hvi_cal_dsm_hora_thv[(hvi_cal_dsm_hora_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_thv_usu

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data



    # -------------------------------------------



    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_afect_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_resp_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_afect_edad_sexo = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_sexo_tveh = hv_les_usu_thv_afect_edad_sexo[hv_les_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_afect_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_resp_edad_sexo = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_sexo_tveh = hv_les_usu_thv_resp_edad_sexo[hv_les_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Cambiar nombre
        mapa_data = hv_les_usu_thv_resp_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data



    # -------------------------------------------



    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Cambiar nombre
        mapa_data = hv_fall_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_tveh = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_afect_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_tveh = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_resp_edad_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Cambiar nombre
        mapa_data = hv_fall_usu_thv

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_fall_usu_thv_afect = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_afec != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_afect_edad = hv_fall_usu_thv_afect[(hv_fall_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_fall_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_afect_edad_sexo = hv_fall_usu_thv_afect_edad[hv_fall_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_afect_edad_sexo_tveh = hv_fall_usu_thv_afect_edad_sexo[hv_fall_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_afect_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data
    
    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_usu_thv_resp_edad_sexo = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad_sexo_tveh = hv_fall_usu_thv_resp_edad_sexo[hv_fall_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Cambiar nombre
        mapa_data = hv_fall_usu_thv_resp_edad_sexo_tveh

        # Dejar fechas como texto
        mapa_data = mapa_data.reset_index()
        mapa_data['fecha'] = mapa_data['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', '', '', '',],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', 'Gravedad', 'Usuario', 'Tipo hecho vial',], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,hv_graves_opciones,hv_usu_opciones,checklist_tipo_hv,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        mapa_data = pd.concat([mapa_data, filtros], axis=1, join="outer")

        # Cambiar a JSON
        mapa_data = mapa_data.to_json(orient='columns')

        return mapa_data

    # Cambiar a JSON
    mapa_data = mapa_data.reset_index()
    mapa_data = mapa_data.to_json(orient='columns')

    return mapa_data

    # -------------------------------------------


# Número de hechos viales totales
def render_hv_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.tipo_accidente.count()

        return 'Totales: {:,.0f}'.format(hv_totales)



    # -------------------------------------------


    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_afect_edad_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_resp_edad_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_hv_les_usules[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_afect_edad_sexo = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_sexo_tveh = hv_les_usu_thv_afect_edad_sexo[hv_les_usu_thv_afect_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_afect_edad_sexo_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_usu_thv_resp_edad_sexo = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_sexo_tveh = hv_les_usu_thv_resp_edad_sexo[hv_les_usu_thv_resp_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Total de hechos viales
        hv_les_totales = hv_les_usu_thv_resp_edad_sexo_tveh.tipo_accidente.count()

        return 'con Lesionados: {:,.0f}'.format(hv_les_totales)



    # -------------------------------------------

    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_fall_usu_thv_resp = hv_fall_usu_thv[hv_fall_usu_thv.tipo_v_resp != 0]
    
        #Filtro por edad
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp[(hv_fall_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_fall_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_usu_thv_resp_edad = hv_fall_usu_thv_resp_edad[hv_fall_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv_resp_edad.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de hechos viales
        hv_fall_totales = hv_fall_usu_thv.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_afect_usu_edad_sexo = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_sexo_tveh = hv_fall_thv_afect_usu_edad_sexo[hv_fall_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_afect_usu_edad_sexo_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_resp_usu_edad_sexo = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_sexo_tveh = hv_fall_thv_resp_usu_edad_sexo[hv_fall_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de hechos viales
        hv_fall_totales = hv_fall_thv_resp_usu_edad_sexo_tveh.tipo_accidente.count()

        return 'con Fallecidos: {:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------

# Número de lesionados totales
def render_hv_les_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu_thv_usu = hvi_cal_dsm_hora_usu_thv[(hvi_cal_dsm_hora_usu_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_usu.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)



    
    # -------------------------------------------

    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv_afect_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv_resp_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de lesionados
        hv_les_totales = hv_les_usu_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_thv_afect_usu = hv_les_thv_afect[(hv_les_thv_afect['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_afect_usu_edad = hv_les_thv_afect_usu[(hv_les_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_les_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_afect_usu_edad_sexo = hv_les_thv_afect_usu_edad[hv_les_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_usu_edad_sexo_tveh = hv_les_thv_afect_usu_edad_sexo[hv_les_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de lesionados
        hv_les_totales = hv_les_thv_afect_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_thv_resp_usu = hv_les_thv_resp[(hv_les_thv_resp['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_resp_usu_edad = hv_les_thv_resp_usu[(hv_les_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_les_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_resp_usu_edad_sexo = hv_les_thv_resp_usu_edad[hv_les_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_usu_edad_sexo_tveh = hv_les_thv_resp_usu_edad_sexo[hv_les_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Total de lesionados
        hv_les_totales = hv_les_thv_resp_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_les_totales)



    # -------------------------------------------

     # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por hechos viales con fallecidos
        hvi_cal_dsm_hora_usu_fall = hvi_cal_dsm_hora_usu[hvi_cal_dsm_hora_usu.fallecidos != 0]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_fall_thv = hvi_cal_dsm_hora_usu_fall[(hvi_cal_dsm_hora_usu_fall['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_fall_thv.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_tveh = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_thv.hv_fall_usu_thv.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_afect_usu_edad_sexo = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_sexo_tveh = hv_fall_thv_afect_usu_edad_sexo[hv_fall_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_fall_thv_resp_usu_edad_sexo = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_sexo_tveh = hv_fall_thv_resp_usu_edad_sexo[hv_fall_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_sexo_tveh.lesionados.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------

# Número de fallecidos viales totales
def render_hv_fall_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, hv_sexo_opciones, checklist_tipo_veh, slider_edad):

    # NADA

    # Si no hay ningún día seleccionado ponme un mapa sin puntos
    if checklist_dias == [] or checklist_tipo_hv == [] or checklist_tipo_veh == [] or hv_usu_opciones == []:
    
        return 0

    # -------------------------------------------

    # HECHOS VIALES TODOS -- Todos (A/R) -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por usuario
        hvi_cal_dsm_hora_usu_thv_usu = hvi_cal_dsm_hora_usu_thv[(hvi_cal_dsm_hora_usu_thv['tipo_usu'].isin(hv_usu_opciones))]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_usu.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES TODOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]      

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_edad = hvi_cal_dsm_hora_usu_thv_afect[(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_edad[hvi_cal_dsm_hora_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_afect_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_edad = hvi_cal_dsm_hora_usu_thv_resp[(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_edad[hvi_cal_dsm_hora_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_resp_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    
    # ----------------


    # HECHOS VIALES TODOS -- Todos (A/R) -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hvi_cal_dsm_hora_usu_thv_afect = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_afec != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_afect_sexo = hvi_cal_dsm_hora_usu_thv_afect[hvi_cal_dsm_hora_usu_thv_afect.sexo_afect == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad = hvi_cal_dsm_hora_usu_thv_afect_sexo[(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_afect_sexo['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad[hvi_cal_dsm_hora_usu_thv_afect_sexo_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_afect_sexo_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES TODOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, todos los hechos viales seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'todos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hvi_cal_dsm_hora_usu = hvi_cal_dsm_hora[(hvi_cal_dsm_hora['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hvi_cal_dsm_hora_usu_thv = hvi_cal_dsm_hora_usu[(hvi_cal_dsm_hora_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hvi_cal_dsm_hora_usu_thv_resp = hvi_cal_dsm_hora_usu_thv[hvi_cal_dsm_hora_usu_thv.tipo_v_resp != 0]

        # Filtro por sexo
        hvi_cal_dsm_hora_usu_thv_resp_sexo = hvi_cal_dsm_hora_usu_thv_resp[hvi_cal_dsm_hora_usu_thv_resp.sexo_resp == hv_sexo_opciones]

        #Filtro por edad
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad = hvi_cal_dsm_hora_usu_thv_resp_sexo[(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']>=slider_edad[0])&(hvi_cal_dsm_hora_usu_thv_resp_sexo['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad[hvi_cal_dsm_hora_usu_thv_resp_sexo_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_usu_thv_resp_sexo_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)



    # -------------------------------------------


    # HECHOS VIALES LESIONADOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
       
    # HECHOS VIALES LESIONADOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_graves_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por afectado
        hv_les_usu_thv_afect = hv_les_usu_thv[hv_les_usu_thv.tipo_v_afec != 0]

        #Filtro por edad
        hv_les_usu_thv_afect_edad = hv_les_usu_thv_afect[(hv_les_usu_thv_afect['edad_afect_mid']>=slider_edad[0])&(hv_les_usu_thv_afect['edad_afect_mid']<=slider_edad[1])]
    
        # Filtro por tipo de vehículo
        hv_les_usu_thv_afect_edad_tveh = hv_les_usu_thv_afect_edad[hv_les_usu_thv_afect_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv_afect_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por hechos viales lesionados
        hv_les = hvi_cal_dsm_hora[hvi_cal_dsm_hora.lesionados != 0]

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Filtro por responsable
        hv_les_usu_thv_resp = hv_les_usu_thv[hv_les_usu_thv.tipo_v_resp != 0]

        #Filtro por edad
        hv_les_usu_thv_resp_edad = hv_les_usu_thv_resp[(hv_les_usu_thv_resp['edad_resp_mid']>=slider_edad[0])&(hv_les_usu_thv_resp['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_les_usu_thv_resp_edad_tveh = hv_les_usu_thv_resp_edad[hv_les_usu_thv_resp_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv_resp_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------

    
    # HECHOS VIALES LESIONADOS -- Todos -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_usu = hv_les[(hv_les['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_les_usu_thv = hv_les_usu[(hv_les_usu['tipo_accidente'].isin(checklist_tipo_hv))]

        # Total de fallecidos
        hv_fall_totales = hv_les_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Afectados -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_thv_afect_usu = hv_les_thv_afect[(hv_les_thv_afect['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_afect_usu_edad = hv_les_thv_afect_usu[(hv_les_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_les_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_afect_usu_edad_sexo = hv_les_thv_afect_usu_edad[hv_les_thv_afect_usu_edad.sexo_afect == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_afect_usu_edad_sexo_tveh = hv_les_thv_afect_usu_edad_sexo[hv_les_thv_afect_usu_edad_sexo["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_les_thv_afect_usu_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES LESIONADOS -- Responsables -- Masculino o Femenino

    # Si hay algún día seleccionado, los hechos viales con lesionados seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'lesionados' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Filtro por usuario
        hv_les_thv_resp_usu = hv_les_thv_resp[(hv_les_thv_resp['tipo_usu'].isin(hv_usu_opciones))]

        #Filtro por edad
        hv_les_thv_resp_usu_edad = hv_les_thv_resp_usu[(hv_les_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_les_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por sexo
        hv_les_thv_resp_usu_edad_sexo = hv_les_thv_resp_usu_edad[hv_les_thv_resp_usu_edad.sexo_resp == hv_sexo_opciones]

        # Filtro por tipo de vehículo
        hv_les_thv_resp_usu_edad_sexo_tveh = hv_les_thv_resp_usu_edad_sexo[hv_les_thv_resp_usu_edad_sexo["tipo_v_resp"].isin(checklist_tipo_veh)]        

        # Total de fallecidos
        hv_fall_totales = hv_les_thv_resp_usu_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)



    # -------------------------------------------

     # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_usu = hv_fall[(hv_fall['tipo_usu'].isin(hv_usu_opciones))]

        # Filtro por tipo de hecho vial
        hv_fall_usu_thv = hv_fall_usu[(hv_fall_usu['tipo_accidente'].isin(checklist_tipo_hv))]
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_usu_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
   
    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_thv_afect_usu = hv_fall_thv_afect[(hv_fall_thv_afect['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_afect_usu_edad = hv_fall_thv_afect_usu[(hv_fall_thv_afect_usu['edad_afect_mid']>=slider_edad[0])&(hv_fall_thv_afect_usu['edad_afect_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_afect_usu_edad_tveh = hv_fall_thv_afect_usu_edad[hv_fall_thv_afect_usu_edad["tipo_v_afec"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_afect_usu_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Responsables

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones == 'todos':

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

        # Filtro por usuario
        hv_fall_thv_resp_usu = hv_fall_thv_resp[(hv_fall_thv_resp['tipo_usu'].isin(hv_usu_opciones))]
    
        #Filtro por edad
        hv_fall_thv_resp_usu_edad = hv_fall_thv_resp_usu[(hv_fall_thv_resp_usu['edad_resp_mid']>=slider_edad[0])&(hv_fall_thv_resp_usu['edad_resp_mid']<=slider_edad[1])]

        # Filtro por tipo de vehículo
        hv_fall_thv_resp_usu_edad_tveh = hv_fall_thv_resp_usu_edad[hv_fall_thv_resp_usu_edad["tipo_v_resp"].isin(checklist_tipo_veh)]

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_usu_edad_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)


    # ----------------


    # HECHOS VIALES FALLECIDOS -- Todos -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'todos' and hv_sexo_opciones != 'todos':

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
    
        # Total de fallecidos
        hv_fall_totales = hv_fall_thv.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # HECHOS VIALES FALLECIDOS -- Afectados -- Todos (M/F)

    # Si hay algún día seleccionado, los hechos viales con fallecidos seleccionados, con todos los usuarios vulnerables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'afectados' and hv_sexo_opciones != 'todos':

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

        # Total de fallecidos
        hv_fall_totales = hvi_cal_dsm_hora_afect_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)
    
    # HECHOS VIALES FALLECIDOS -- Responsables
    elif checklist_dias != [] and hv_graves_opciones == 'fallecidos' and hv_afres_opciones == 'responsables' and hv_sexo_opciones != 'todos':

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

        # Total de fallecidos
        hv_fall_totales = hv_fall_thv_resp_edad_sexo_tveh.fallecidos.sum()

        return '{:,.0f}'.format(hv_fall_totales)

    # -------------------------------------------

# Checklist de tipos de hechos viales dependiendo de los usuarios afectados opciones
def render_opciones_dos(hv_usu_opciones, hv_graves_opciones):

    # Todos
    
    if hv_usu_opciones == [] and hv_graves_opciones == 'todos':

        return [] 

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Incendio', 'value': 'Incendio'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]    
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

    # Lesionados

    elif hv_usu_opciones == [] and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ] 
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque de Reversa', 'value': 'Choque de Reversa'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},            
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]        
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]  
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Caída de Persona', 'value': 'Caida de Persona'},            
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

    # Fallecidos

    elif hv_usu_opciones == [] and hv_graves_opciones == 'fallecidos':

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
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

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

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

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

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

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

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque de Frente', 'value': 'Choque de Frente'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Choque Lateral', 'value': 'Choque Lateral'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
            {'label': ' Volcadura', 'value': 'Volcadura'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
        ]  
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Atropello', 'value': 'Atropello'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]

    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Alcance', 'value': 'Alcance'},
            {'label': ' Choque de Crucero', 'value': 'Choque de Crucero'},
            {'label': ' Choque Diverso', 'value': 'Choque Diverso'},
            {'label': ' Estrellamiento', 'value': 'Estrellamiento'},
        ]
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return [
            {'label': ' Atropello', 'value': 'Atropello'},
        ]

# Checklist de tipos de hechos viales dependiendo de los usuarios afectados valores
def render_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones):
    
    # Todos

    if hv_usu_opciones == [] and hv_graves_opciones == 'todos':

       return []

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

       return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento','Incendio', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

       return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'todos':

        return ['Atropello']

    # Lesionados

    elif hv_usu_opciones == [] and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque de Reversa', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

       return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento',] 
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque Lateral', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento',]
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Alcance','Caida de Persona', 'Choque de Crucero', 'Choque de Frente','Choque Diverso', 'Choque Lateral', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'lesionados':

        return ['Atropello']

    # Fallecidos

    elif hv_usu_opciones == [] and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']

    elif 'Motorizado' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque de Frente', 'Choque Diverso', 'Choque Lateral', 'Estrellamiento', 'Volcadura']
    
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
        
    elif 'Peaton' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance', 'Atropello', 'Choque Diverso']
    
    elif 'Peaton' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
 
    elif 'Bicicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance', 'Atropello', 'Choque Diverso']

    elif 'Bicicleta' in hv_usu_opciones and 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance', 'Choque Diverso']
    
    elif 'Motocicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Motocicleta' in hv_usu_opciones and 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Atropello','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']

    elif 'Motocicleta' in hv_usu_opciones and 'Bicicleta' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Alcance','Choque de Crucero', 'Choque Diverso', 'Estrellamiento']
    
    elif 'Peaton' in hv_usu_opciones and hv_graves_opciones == 'fallecidos':

        return ['Atropello']

#----------

# Layout - Intersecciones
def hv_intersecciones():

    return html.Div([

        html.Br(),

        dbc.Row([

            # Controles
            dbc.Col([

                dbc.Card([
                    dbc.CardHeader([
                        dbc.Button([
                            "Fecha",
                            html.Img(src='data:image/png;base64,{}'.format(encoded_img1), 
                                        style={'width':'3%','float':'right'},
                                        className="pt-1")
                            ],
                            id="collapse_button_fecha",
                            className='btn btn-light btn-lg btn-block',
                            color="primary",
                            n_clicks=0,
                            style={'font-size':'16px'},
                        ),

                    ], style={'text-align':'center'}, className='p-0'),

                    dbc.Collapse([

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

                            

                            dbc.Checklist(
                                id = 'checklist_dias',
                                className = 'radio-group btn-group d-flex justify-content-center',
                                labelClassName = 'btn btn-secondary',
                                labelCheckedClassName = 'active',
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
                                updatemode='mouseup'
                            ),
                        ])

                    ], id="collapse_cal",
                        is_open=True,),

                ]),

            ],lg=4, md=4),

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
                            className='h-100'
                        ),
                    style={'padding':'0px'},
                    ),

                ], className="text-white bg-dark", style={'height':'70vh'}), 
                
                dbc.Card([

                    dbc.CardBody([
                        dcc.Store(id='datos_interseccion'),
                        html.Button([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                                    style={'width':'1.5%','float':'left'},
                                    className="pt-1"),
                            Download(id="download_data_int"),
                            html.B("Descargar datos en CSV"),
                            ], 
                            id="btn_perso_csv_inter",
                            className="btn btn-block",
                            n_clicks=None,
                            style={'float':'right','background-color':'#00b55b','color':'white'}
                        ),
                    ], className='p-0', style={'background-color':'transparent'}),
                ])

            ],lg=8, md=8)


        ], className="d-flex justify-content-between"),

        html.Br(),

        # Principales indicadores
        dbc.Row([

            dbc.Col([

                # Hechos viales por año
                dbc.Row([

                    dbc.Col([
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
                    ],lg=9, md=9),

                    dbc.Col([

                        # Tarjetas Indicadores
                        dbc.Card([

                            dbc.CardHeader('Hechos Viales Totales'),
                            dbc.CardBody(id = 'interseccion_hv'),

                        ]),

                        html.Br(),

                        dbc.Card([

                            dbc.CardHeader('Lesionados'),
                            dbc.CardBody(id = 'interseccion_les'),

                        ]),

                        html.Br(),

                        dbc.Card([

                            dbc.CardHeader('Fallecidos'),
                            dbc.CardBody(id = 'interseccion_fal'),

                        ])

                    ],lg=3, md=3, style={'text-align':'center'})

                ]),

            ]),

        ]),

        html.Br(),

        # Gráficas Tipos / Tipo y Causa
        dbc.Row([
            
            # Tipos de Hechos Viales
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Tipos de Hechos Viales'),
                    dbc.CardBody([
                        dcc.Store(id='tabla_data'),
                        dcc.Graph(
                            id = 'tabla',
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
                    ],
                    style={'padding':'0px'}),

                    dbc.CardHeader([

                        html.Button([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                                    style={'width':'1.5%','float':'left'},
                                    className="pt-1"),
                            Download(id="download-tipos-csv"),
                            html.B("Descargar datos en CSV"),
                            ], 
                            id="btn_tipos_csv",
                            className="btn btn-block",
                            n_clicks=None,
                            style={'float':'right','background-color':'#00b55b','color':'white'}
                        ),
                    ], className='p-0'),

                ], style={'height':'550px'})
            ]),
            
            # Hechos viales por Tipo y Causa
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([

                        html.Div([
                            'Tipos de Hechos Viales y sus Causas',
                            ],
                            className="mt-1", 
                            style={'width':'90%','display':'inline-block'}),

                       html.Div([

                            html.Span(
                                dbc.Button(
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img2), 
                                            style={'float':'right'},
                                            className="p-0 img-fluid"), 
                                    id="open1", 
                                    n_clicks=0, 
                                    style={'display':'inline-block',
                                            'float':'right','padding':'0', 
                                            'width':'5%','background-color':'transparent',
                                            'border-color':'transparent','padding-top':'2px'},
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
                                        html.Li([html.B('Atropello:'),' Ocurre cuando un vehículo en movimiento impacta con una persona. La persona puede estar estática o en movimiento ya sea caminando, corriendo o montando en patines, patinetas, o cualquier juguete similar, o trasladándose asistiéndose de aparatos o de vehículos no regulados por este reglamento, esto en el caso de las personas con discapacidad. Es imporante destacar que este tipo de hevho vial se asocia únicamente con peatones.']),
                                        html.Li([html.B('Caída de persona:'),' Ocurre cuando una persona cae hacia fuera o dentro de un vehículo en movimiento, comúnmente dentro de un autobús de transporte público. ']),
                                        html.Li([html.B('Choque de crucero:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación que convergen o se cruzan, invadiendo un vehículo parcial o totalmente el arroyo de circulación de otro. ']),
                                        html.Li([html.B('Choque de Reversa:'),' Ocurre cuando un vehículo choca con otro al ir de reversa.']),
                                        html.Li([html.B('Choque de Frente:'),' Ocurre entre dos o más vehículos provenientes de arroyos de circulación opuestos, los cuales chocan cuando uno de ellos invade parcial o totalmente el carril, arroyo de circulación o trayectoria contraria. ']),
                                        html.Li([html.B('Choque Diverso:'),' En esta clasificación queda cualquier hecho de tránsito no especificado en los puntos anteriores. ']),
                                        html.Li([html.B('Choque Lateral:'),' Ocurre entre dos o más vehículos cuyos conductores circulan en carriles o con trayectorias paralelas, en el mismo sentido chocando los vehículos entre sí, cuando uno de ellos invada parcial o totalmente el carril o trayectoria donde circula el otro.']),
                                        html.Li([html.B('Estrellamiento:'),' Ocurre cuando un vehículo en movimiento en cualquier sentido choca con algo que se encuentra provisional o permanentemente estático.']),
                                        html.Li([html.B('Incendio:'),' Ocurre cuando existe un incendio por un percance vial.']),
                                        html.Li([html.B('Volcadura:'),' Ocurre cuando un vehículo pierde completamente el contacto entre llantas y superficie de rodamiento originándose giros verticales o transversales']),

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
                        ])

                    ], className='d-flex align-items-center'),
                    
                    dbc.CardBody([
                        dcc.Store(id='treemap_data'),
                        dcc.Graph(
                            id = 'treemap',
                            figure = {},
                            style={'padding':'0px'},
                            config={
                                    'modeBarButtonsToRemove':
                                    ['lasso2d', 'pan2d',
                                    'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                    'resetScale2d', 'hoverClosestCartesian',
                                    'hoverCompareCartesian', 'toggleSpikelines',
                                    'select2d',],
                                    'displaylogo': False
                                },
                            )],
                    style={'padding':'0px'}),

                    dbc.CardHeader([

                        html.Button([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                                    style={'width':'1.5%','float':'left'},
                                    className="pt-1"),
                            Download(id="download-tiposyc-csv"),
                            html.B("Descargar datos en CSV"),
                            ], 
                            id="btn_tiposyc_csv",
                            className="btn btn-block",
                            n_clicks=None,
                            style={'float':'right','background-color':'#00b55b','color':'white'}
                        ),
                    ], className='p-0'),

                ], style={'height':'550px'}),
            ])
        ]),

    ])

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

# Cerrar la ventana de información de los tipos de hechos viales
def toggle_modal_afres(open1_afres, close1_afres, modal_afres):
    if open1_afres or close1_afres:
        return not modal_afres
    return modal_afres

# Filtro colapsable fechas 
def render_collapse_button_fecha(n, is_open):
    if n:
        return not is_open
    return collapse_button_fecha

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

# Datos de Intersecciones

# Nombre
def render_interseccion_nombre(clickData):
    if clickData is None:
        return 'Haz click en una intersección para conocer más'
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


# Hechos Viales por 
def render_interseccion_hv_tiempo(clickData, periodo_hv, start_date, end_date, slider_hora, checklist_dias):

    # Tab de Día
    if periodo_hv == 'dia' and clickData is None:

        # Mensaje fondo blanco
        fig = go.Figure()
        fig = px.scatter(
            x=[1, 2, 3],
            y=[1, 2, 3],
            template = 'plotly_white'
        )
        fig.add_annotation(x=2, y=2,
                    text="Haz click en una intersección para conocer más",
                    showarrow=False, 
                    font=dict(
                        family="Arial",
                        size=18,
                        )
                    )
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_yaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_traces(marker_color="white",
                    unselected_marker_opacity=1, hoverinfo='skip',hovertemplate=None)

        return fig

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
    elif periodo_hv == 'mes' and clickData is None:

        # Mensaje fondo blanco
        fig = go.Figure()
        fig = px.scatter(
            x=[1, 2, 3],
            y=[1, 2, 3],
            template = 'plotly_white'
        )
        fig.add_annotation(x=2, y=2,
                    text="Haz click en una intersección para conocer más",
                    showarrow=False, 
                    font=dict(
                        family="Arial",
                        size=18,
                        )
                    )
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_yaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_traces(marker_color="white",
                    unselected_marker_opacity=1, hoverinfo='skip',hovertemplate=None)

        return fig

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
    elif periodo_hv == 'año' and clickData is None:

        # Mensaje fondo blanco
        fig = go.Figure()
        fig = px.scatter(
            x=[1, 2, 3],
            y=[1, 2, 3],
            template = 'plotly_white'
        )
        fig.add_annotation(x=2, y=2,
                    text="Haz click en una intersección para conocer más",
                    showarrow=False, 
                    font=dict(
                        family="Arial",
                        size=18,
                        )
                    )
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_yaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_traces(marker_color="white",
                    unselected_marker_opacity=1, hoverinfo='skip',hovertemplate=None)

        return fig

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

# Hechos Viales por 
def render_interseccion_hv_tiempo_data(clickData, start_date, end_date, slider_hora, checklist_dias):

    # Tab de Día
    if clickData is None:

        datos_interseccion = {'x':[1, 2, 3],'y':[1, 2, 3],}

        return datos_interseccion

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
        hvi = hvi.set_index("fecha")
        hvi = hvi.sort_index()

        # Filtro por calendario
        hvi_cal = hvi.loc[start_date:end_date]

        # Filtro por día de la semana
        hvi_cal_dsm = hvi_cal[hvi_cal["dia_semana"].isin(checklist_dias)]

        # Filtro por hora
        hvi_cal_dsm_hora = hvi_cal_dsm[(hvi_cal_dsm['hora']>=slider_hora[0])&(hvi_cal_dsm['hora']<=slider_hora[1])]

        # Cambiar nombre
        datos_interseccion = hvi_cal_dsm_hora

        # Dejar fechas como texto
        datos_interseccion = datos_interseccion.reset_index()
        datos_interseccion['fecha'] = datos_interseccion['fecha'].astype(str)

        # DataFrame de Filtros
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '', ],'Filtros seleccionados': ['Fechas', 'Días de la semana', 'Horario', ], 'Valores': [hvi_cal_f,checklist_dias,slider_hora_f,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        datos_interseccion = pd.concat([datos_interseccion, filtros], axis=1, join="outer")

        datos_interseccion = pd.DataFrame(datos_interseccion)

        # Cambiar a JSON
        datos_interseccion = datos_interseccion.to_json(orient='columns')

        return datos_interseccion

 
# Descargar CSV
def render_down_data_inter(n_clicks, datos_interseccion):
    
    #data = json.dumps(datos_interseccion)
    a_json = json.loads(datos_interseccion)
    df = pd.DataFrame.from_dict(a_json, orient="columns")

    csv = send_data_frame(df.to_csv, "hechos_viales_interseccion_query.csv", index=False, encoding='ISO-8859-1')

    return csv

# Tabla de Tipos de hechos viales
def render_tabla(clickData, start_date, end_date, slider_hora, checklist_dias):
    
    # Si no se ha hecho click a una intersección en el mapa pon un cero
    if clickData is None:
        
        # Mensaje fondo blanco
        fig = go.Figure()
        fig = px.scatter(
            x=[1, 2, 3],
            y=[1, 2, 3],
            template = 'plotly_white'
        )
        fig.add_annotation(x=2, y=2,
                    text="Haz click en una intersección para conocer más",
                    showarrow=False, 
                    font=dict(
                        family="Arial",
                        size=18,
                        )
                    )
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_yaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_traces(marker_color="white",
                    unselected_marker_opacity=1, hoverinfo='skip',hovertemplate=None)

        tabla_data = {'x':[1, 2, 3],'y':[1, 2, 3],}

        return fig, tabla_data

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

        # DataFrame de Filtros
        interseccion_f = clickData['points'][0]['hovertext']
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '','',],'Filtros seleccionados': ['Intersección','Fechas', 'Días de la semana', 'Horario',], 'Valores': [interseccion_f,hvi_cal_f,checklist_dias,slider_hora_f,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        tabla_data = pd.concat([tipo_hv, filtros], axis=1, join="outer")

        # Pasar a JSON
        tabla_data = tabla_data.to_json(orient='columns')

        # Tabla
        tabla = go.Figure(
            [go.Table(
                    header=dict(values=['Tipo','Hechos viales','Lesionados','Fallecidos'],
                        fill_color='#343332',
                        font=dict(color='white'),
                        align='center'),
                    cells=dict(values=[tipo_hv.tipo_accidente, tipo_hv.hechos_viales, tipo_hv.lesionados, tipo_hv.fallecidos],
                       fill_color='#F7F7F7',
                       align='center',
                       height=35))
            ])
        tabla.update_layout(margin = dict(t=20, l=20, r=20, b=10))
    
    return tabla, tabla_data

# Descargar CSV
def render_down_data_tabla(n_clicks, tabla_data):
    
    a_json = json.loads(tabla_data)
    df = pd.DataFrame.from_dict(a_json, orient="columns")

    csv = send_data_frame(df.to_csv, "tipos_de_hechos_viales_query.csv", index=False, encoding='ISO-8859-1')

    return csv


# Treemap Hechos Viales por Tipo y Causa
def render_treemap(clickData, start_date, end_date, slider_hora, checklist_dias):

    # Si no se ha hecho click a una intersección en el mapa pon un cero
    if clickData is None:
        
        # Mensaje fondo blanco
        fig = go.Figure()
        fig = px.scatter(
            x=[1, 2, 3],
            y=[1, 2, 3],
            template = 'plotly_white'
        )
        fig.add_annotation(x=2, y=2,
                    text="Haz click en una intersección para conocer más",
                    showarrow=False, 
                    font=dict(
                        family="Arial",
                        size=18,
                        )
                    )
        fig.update_layout(showlegend=False)
        fig.update_xaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_yaxes(showgrid = False, 
                    showline = False, 
                    title_text='',color="white",)
        fig.update_traces(marker_color="white",
                    unselected_marker_opacity=1, hoverinfo='skip',hovertemplate=None)

        treemap_data = {'x':[1, 2, 3],'y':[1, 2, 3],}

        return fig, treemap_data

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
        df_causas['Total'] = df_causas['hechos_viales'].count()*['Total']

        # Quitar índice
        causa_hv = causa_hv.reset_index()

        # Cambiar nombre columnas
        causa_hv.columns = [" ".join(a) for a in causa_hv.columns.to_flat_index()]
        strings = causa_hv.columns.values
        new_strings = []

        for string in strings:
            new_string = string.replace("hechos_viales ", '')
            new_strings.append(new_string)

        treemap_data = causa_hv.set_axis(new_strings, axis=1)


        # DataFrame de Filtros
        interseccion_f = clickData['points'][0]['hovertext']
        hvi_cal_f = [start_date,' a ',end_date]
        slider_hora_f = [slider_hora[0],' a ', slider_hora[1]]
        filtros = {'': ['', '', '','',],'Filtros seleccionados': ['Intersección','Fechas', 'Días de la semana', 'Horario',], 'Valores': [interseccion_f,hvi_cal_f,checklist_dias,slider_hora_f,],}        
        filtros = pd.DataFrame(filtros)

        # Juntar Datos con filtros
        treemap_data = pd.concat([treemap_data, filtros], axis=1, join="outer")


        # Pasar a JSON
        treemap_data = treemap_data.to_json(orient='columns')

        # Treemap
        treemap = px.treemap(df_causas, 
                        path=['tipo_accidente', 'causa_accidente'], 
                        values='hechos_viales',
                        color='causa_accidente',
                        )
        treemap.update_layout(margin = dict(t=20, l=20, r=20, b=10))
        treemap.data[0].hovertemplate = '%{label}<br>%{value}'

        return treemap, treemap_data

# Descargar CSV
def render_down_data_treemap(n_clicks, treemap_data):
    
    a_json = json.loads(treemap_data)
    df = pd.DataFrame.from_dict(a_json, orient="columns")

    csv = send_data_frame(df.to_csv, "tipos_causas_de_hechos_viales_query.csv", index=False, encoding='ISO-8859-1')

    return csv

# Cerrar la ventana de información de los tipos de hechos viales
def toggle_modal(open1, close1, modal):
    if open1 or close1:
        return not modal
    return modal

# Layout - General
def hv_datos():

    return html.Div([

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Datos'),
                    dbc.CardBody(
                        dbc.Row([
                            dbc.Col(['Datos de hechos viales del 2015 en adelante proporcionados por la Secretaría de Seguridad Pública y procesados mensualmente por el IMPLANG.',
                                html.I(' Última actualización: Julio 2021')
                                ], style={'display':'inline-block'},lg=7, md=7),
                            dbc.Col([

                                dbc.Row([

                                    dbc.Col([
                                    
                                        html.Div([

                                            html.Span(
                                                
                                                html.Button([
                                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                                                            style={'width':'8%','float':'left'},
                                                            className="pt-1"),
                                                    html.B("Descargar Excel"),
                                                    ], 
                                                    id="btn_csv",
                                                    className="btn",
                                                    n_clicks=None,
                                                    style={'float':'right','background-color':'#016E38','color':'white'}
                                                ),

                                                id="tooltip-target-descbd",
                                            ),

                                            dbc.Tooltip(
                                                "Descarga toda la base de datos",
                                                target="tooltip-target-descbd",
                                            ),

                                            
                                            Download(id="download-dataframe-csv")
                                        ], className='d-flex justify-content-center'),

                                    ]),

                                    dbc.Col([

                                        html.Div([

                                            html.Span(

                                                html.Button([
                                                    html.Img(src='data:image/png;base64,{}'.format(encoded_img3), 
                                                            style={'width':'8%','float':'left'},
                                                            className="pt-1"),
                                                    html.B("Descargar SHP"),
                                                    ], 
                                                    id="btn_csv",
                                                    className="btn",
                                                    n_clicks=None,
                                                    style={'float':'right','background-color':'#636EFA','color':'white'}
                                                ),
                                                        

                                                id="tooltip-target-shp",
                                            ),

                                            dbc.Tooltip(
                                                "Descarga toda la base de datos en SHP",
                                                target="tooltip-target-shp",
                                            ),

                                            Download(id="download-dataframe-csv")
                                        ], className='d-flex justify-content-center')

                                    ])
                                ])

                            ], lg=5, md=5, style={'display':'inline-block'}, className='align-self-center',)
                        ])

                    )
                ])
            ])
        ], className="pt-4")

    ])

#----------