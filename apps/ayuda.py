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
                            dbc.Tab(label="Generales", tab_id="Generales"),
                            dbc.Tab(label="Monitoreo de Tráfico", tab_id="Monitoreo de Tráfico"),
                            dbc.Tab(label='Cerrar Vialidades', tab_id="Cerrar Vialidades")],
                            id='tabs',
                            active_tab="Generales",
                            card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="content"))
                ]), 
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
                html.H6('Ayudas generales'),
                html.Iframe(width='100%', height='590',
                           src='https://edgargtzgzz.carto.com/builder/47ec8c81-6afb-41bc-9946-5096f6223149/embed')
            ])
        )    


    ])


def render_ayuda(tab):
    if tab == 'Generales':
        return ayuda_generales()
    elif tab == 'Monitoreo de Tráfico':
        return html.Iframe(width='100%', height='390',
                           src='https://edgargtzgzz.carto.com/builder/47ec8c81-6afb-41bc-9946-5096f6223149/embed')
    elif tab == 'Cerrar Vialidades':
        return html.Iframe(width='100%', height='190',
                           src='https://edgargtzgzz.carto.com/builder/47ec8c81-6afb-41bc-9946-5096f6223149/embed')











