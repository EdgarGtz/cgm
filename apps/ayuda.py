import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output




# App Layout

def ayuda():

    return html.Div([

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label="Generales", tab_id="tab-1"),
                            dbc.Tab(label="Monitoreo de Tráfico", tab_id="tab-2"),
                            dbc.Tab(label='Cerrar Vialidades', tab_id="tab-3")],
                            id='tabs',
                            active_tab="tab-1",
                            card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="content"))
                ]), 
                xl=11
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


def render_ayuda(tab):
    if tab == 'tab-1':
        return html.Iframe(width='100%', height='590',
                           src='https://edgargtzgzz.carto.com/builder/47ec8c81-6afb-41bc-9946-5096f6223149/embed')
    elif tab == 'tab-2':
        return html.Iframe(width='100%', height='390',
                           src='https://edgargtzgzz.carto.com/builder/47ec8c81-6afb-41bc-9946-5096f6223149/embed')
    elif tab == 'tab-3':
        return html.Iframe(width='100%', height='190',
                           src='https://edgargtzgzz.carto.com/builder/47ec8c81-6afb-41bc-9946-5096f6223149/embed')


