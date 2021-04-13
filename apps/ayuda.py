import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output


def ayuda():

    return html.Div([

        # Tabs

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label="Monitoreo de Tráfico", tab_id="ayuda_monitoreo"),
                            dbc.Tab(label='Reporte de Eventos', tab_id="ayuda_eventos"),
                            dbc.Tab(label='Cierre de Vialidades', tab_id="ayuda_vialidades",
                                disabled=True)],
                            id='tabs',
                            active_tab="ayuda_monitoreo",
                            card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="ayuda_content"))
                ], style={'min-height': '100vh'})
            ), justify = 'center'
        ),

        #Footer 

        dbc.Row(
            dbc.Col(
                html.H6('San Pedro Garza García, Nuevo León, México')
            ), className='px-3 py-4', style={'background-color': 'black','color': 'white'}
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
                html.H5('¿Cómo utilizar la herramienta de Monitoreo de Tráfico?'),
                html.Br(),
                html.Iframe(width='100%', height='560', 
                           src='https://www.youtube.com/embed/mJ00CJLHd8E'),
                html.Br(),
                html.Br(),
                html.H5('¿Te quedaron dudas?'),
                html.Br(),
                html.P('1. Envía un mensaje al grupo de whatsapp oficial del Centro de Gestión de Movilidad.'),
                html.P('2. Envía un correo a edgar.gutierrez@sanpedro.gob.mx.')
            ])
        )    

    ])


def ayuda_eventos():

    return html.Div([

        dbc.Row(
            dbc.Col([
                html.H5('Objetivo'),
                html.Br(),
                html.P('Utiliza el mapa de Waze para reportar percances viales, congestionamientos y otros eventos que tengan afectación en la vialidad del municipio. Al realizar el reporte, los ciudadanos que utilicen la aplicación de Waze recibirán la actualización del reporte en su celular.'),
                html.Br(),
                html.H5('Pasos'),
                html.Br(),
                html.P('1. Ingresa al mapa de Reporte de Eventos y da click en el punto en donde ocurrió el evento a reportar.'),
                html.P('2. Selecciona el tipo de reporte, subtipo, comentarios y fecha de inicio y fin del mismo.'),
                html.P('3. Da click en el botón de "Submit" para finalizar el reporte del evento.'),
                html.Br(),
                html.H5('¿Cómo utilizar la herramienta de Reporte de Eventos?'),
                html.Br(),
                html.Iframe(width='100%', height='560', 
                           src='https://embed.waze.com/iframe?zoom=14&lat=25.659477&lon=-100.384827&ct=livemap')
            ])
        )    

    ])




def render_ayuda(tab):
    if tab == 'ayuda_monitoreo':
        return ayuda_monitoreo()
    elif tab == 'ayuda_eventos':
        return ayuda_eventos()
   











