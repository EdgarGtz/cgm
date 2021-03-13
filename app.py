import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output
import dash_auth


app = dash.Dash(__name__, title='Centro de Gestión de Movilidad',
				external_stylesheets=[dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'}])



server = app.server

# Connect to app pages

from apps import home, datos, ayuda

# Connect to config

from config import user, password


# Login

auth = dash_auth.BasicAuth(
    app,
    {user: password}
    
)

# App Layout

app.layout = dbc.Container([

	dbc.NavbarSimple(
		[

        	dbc.DropdownMenu([
                	dbc.DropdownMenuItem('Monitoreo de Tráfico',
                		href='https://www.waze.com/en-GB/trafficview', target='blank'),
                	dbc.DropdownMenuItem('Comunicar Incidentes',
                		href='https://www.waze.com/reporting', target='blank'),
                	dbc.DropdownMenuItem('Cerrar Vialidades',
                		href='https://www.waze.com/editor', target='blank')
	            ],
	            label='Acciones',
	            group=True,
	            color='light'
        	),

        	dbc.Button('Datos', href='/apps/datos', color='light'),

        	dbc.Button('Ayuda', href='/apps/ayuda', color='light')

		],
		brand='Centro de Gestión de Movilidad',
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
		return datos.layout
	if pathname == '/apps/ayuda':
		return ayuda.layout
	else:
		return home.layout


if __name__ == '__main__':
	app.run_server(debug=True)

