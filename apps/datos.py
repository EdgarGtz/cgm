import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px


# App Layout

layout = html.Div([

    dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Tab 1", tab_id="tab-1"),
                    dbc.Tab(label="Tab 2", tab_id="tab-2"),
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-1",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
    ),  

    # Footer 

    dbc.Row(
        dbc.Col(
            html.H6('San Pedro Garza García, Nuevo León, México')
        ), className='px-3 py-4', style={'background-color': 'black','color': 'white'}
    )

])

