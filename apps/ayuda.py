import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output




# App Layout

def ayuda():

    return html.Div([

        # Tabs

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label="Generales", tab_id="generales"),
                            dbc.Tab(label="Monitoreo de Tráfico", tab_id="monitoreo"),
                            dbc.Tab(label='Cerrar Vialidades', tab_id="cerrar_vialidades",
                                disabled=True)],
                            id='tabs',
                            active_tab="generales",
                            card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="content"))
                ], style={'min-height': '100vh'}), xl=10
            ), justify = 'center'
        ),

        #Footer 

        dbc.Row(
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México')
            ), className='px-3 py-4', style={'background-color': 'black','color': 'white'}
        )

    ])

def ayuda_generales():

    return html.Div([

        dbc.Row(
            dbc.Col([
                html.H5('Para cualquier duda o aclaración:'),
                html.Br(),
                html.P('1. Envía un mensaje al grupo de whatsapp oficial del Centro de Gestión de Movilidad.'),
                html.P('2. Envía un correo a edgar.gutierrez@sanpedro.gob.mx.')
            ])
        )    

    ])

def ayuda_monitoreo():

    return html.Div([

        dbc.Row(
            dbc.Col([
                html.H5('Objetivo'),
                html.Br(),
                html.P('Utiliza el mapa de Waze para identificar percances viales, semáforos descompuestos y otros eventos que tengan afectación en la vialidad del municipio.'),
                html.Br(),
                html.H5('Pasos'),
                html.Br(),
                html.P('1. Manten en todo momento el mapa de Waze abierto para visualizar los eventos en tiempo real.'),
                html.P('2. Observa y revisa la veracidad de eventos que aparezcan en el mapa, como percances viales, semáforos descompuestos o cualquier otro congestionamiento relevante.'),
                html.P('3. En caso de que uno de estos eventos no se haya reportado en el C4, levanta el reporte. Recuerda ingresar a Waze como fuente del reporte.'),
                html.Br(),
                html.H5('¿Cómo utilizar el mapa de Waze para monitorear tráfico?'),
                html.Br(),
                html.Iframe(width='100%', height='590',
                           src='https://edgargtzgzz.carto.com/builder/47ec8c81-6afb-41bc-9946-5096f6223149/embed')
            ])
        )    

    ])


def render_ayuda(tab):
    if tab == 'generales':
        return ayuda_generales()
    elif tab == 'monitoreo':
        return ayuda_monitoreo()
   











