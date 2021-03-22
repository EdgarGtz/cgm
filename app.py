import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output
import dash_auth
import os


app = dash.Dash(__name__, title='Centro de Gestión de Movilidad',
				external_stylesheets=[dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

# Connect to app pages

from apps import home, datos, ayuda
from apps.ayuda import ayuda, render_ayuda
from apps.datos import datos, render_datos

# Connect to config

from config import user, password

# Login

auth = dash_auth.BasicAuth(
    app,
    {user: password}
)


# App Layout

app.layout = html.Div([

	dbc.NavbarSimple(
		[

        	dbc.DropdownMenu([
                	dbc.DropdownMenuItem('Monitoreo de Tráfico',
                		href='https://www.waze.com/en-GB/trafficview', target='blank'),
                	dbc.DropdownMenuItem('Cerrar Vialidades',
                		href='https://www.waze.com/editor', target='blank', disabled=True)
	            ],
	            label='Acciones',
	            group=True,
	            color='light'
        	),

        	dbc.Button('Datos', href='/apps/datos', color='light'),

        	dbc.Button('Ayuda', href='/apps/ayuda', color='light')

		],
		brand='CGM',
		brand_href='/apps/home'
	),

	html.Div(id='page-content', children=[]),
	dcc.Location(id='url', refresh=False)

])


@app.callback(Output(component_id='page-content', component_property=
					'children'),
			[Input(component_id='url', component_property='pathname')])

def display_page(pathname):
	if pathname == '/apps/datos':
		return datos()
	if pathname == '/apps/ayuda':
		return ayuda()
	else:
		return home.layout


# Ayuda

@app.callback(Output('ayuda_content', 'children'), [Input('tabs', 'active_tab')])

def get_ayuda(tab):
    return render_ayuda(tab)

# Datos

@app.callback(Output('datos_content', 'children'), [Input('tabs', 'active_tab')])

def get_datos(tab):
    return render_datos(tab)



if __name__ == '__main__':
	app.run_server(debug=True)

