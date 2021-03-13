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
            html.Img(src='../assets/sanpedro.jpg', style={'max-width':'100%', 'height':'auto'}),
             html.H2('Construyendo una movilidad segura, eficiente y sustentable',
                style={'position': 'absolute', 'top': '50%', 'left': '50%',
                'transform': 'translate(-50%, -50%)','color': 'white','text-align':'center'})
        ])
    ),


    # Footer 

    dbc.Container(

    dbc.Row(
        dbc.Col(
            html.H6('San Pedro Garza García, Nuevo León, México')
        ), className='px-3 py-4', style={'background-color': 'black','color': 'white'}
    )

    )

])

