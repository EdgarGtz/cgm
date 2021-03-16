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
                ], style={'height':'800px'}), 
                xl=10
            ),
            justify = 'center'
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
                html.P('Utiliza el grupo de whatsapp oficial del Centro de Gestión de Movilidad para cualquier duda o aclaración.'),
                html.P('Envía un correo a edgar.gutierrez@sanpedro.gob.mx.')
            ])
        )    

    ])

def ayuda_monitoreo():

    return html.Div([

        dbc.Row(
            dbc.Col([
                html.H6('Ayudas monitoreo'),
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
   











