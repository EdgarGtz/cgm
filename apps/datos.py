import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px


def datos():

    return html.Div([

        # Tabs

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs([
                            dbc.Tab(label="Monitoreo de Tráfico", tab_id="datos_monitoreo"),
                            dbc.Tab(label='Cerrar Vialidades', tab_id="datos_vialidades",
                                disabled=True)],
                            id='tabs',
                            active_tab="datos_monitoreo",
                            card=True
                        )
                    ),
                    dbc.CardBody(html.Div(id="datos_content"))
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


def datos_monitoreo():

    return html.Div([

        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Card header"),
                    dbc.CardBody([
                        html.H5("Card title", className="card-title"),
                        html.P("This is some card content that we'll reuse",
                            className="card-text")
                    ])  
                ], color='primary', outline='true')
            )
        ),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Card header"),
                    dbc.CardBody([
                        html.H5("Card title", className="card-title"),
                        html.P("This is some card content that we'll reuse",
                            className="card-text")
                    ])  
                ])
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Card header"),
                    dbc.CardBody([
                        html.H5("Card title", className="card-title"),
                        html.P("This is some card content that we'll reuse",
                            className="card-text")
                    ])  
                ])
            )
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Card header"),
                    dbc.CardBody([
                        html.H5("Card title", className="card-title"),
                        html.P("This is some card content that we'll reuse",
                            className="card-text")
                    ])  
                ])
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Card header"),
                    dbc.CardBody([
                        html.H5("Card title", className="card-title"),
                        html.P("This is some card content that we'll reuse",
                            className="card-text")
                    ])  
                ])
            ),

            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Card header"),
                    dbc.CardBody([
                        html.H5("Card title", className="card-title"),
                        html.P("This is some card content that we'll reuse",
                            className="card-text")
                    ])  
                ])
            )
        ])

    ])


def render_datos(tab):
    if tab == 'datos_monitoreo':
        return datos_monitoreo()





















