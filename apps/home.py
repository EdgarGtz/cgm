import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px


# App Layout

layout = html.Div([

    # Banner Principal

    dbc.Row(
        dbc.Col([
            html.Img(src='../assets/home2.jpeg', style={'width':'100%', 'height':'auto'}),
            html.H1('Centro de Gestión de Movilidad',
                style={'position': 'absolute', 'top': '50%', 'left': '50%',
                'transform': 'translate(-50%, -50%)','color': 'white','text-align':'center'})
        ])
    ),


    # Footer 

    dbc.Row([
        dbc.Col(
            html.H6('Instituto Municipal de Planeación y Gestión Urbana')),
        dbc.Col(
            html.H6('San Pedro Garza García, Nuevo León, México',
                style = {'textAlign': 'right'}))
    ], className='px-3 py-4', style={'background-color': 'black','color': 'white'})


])

