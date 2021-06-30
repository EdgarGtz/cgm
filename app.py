import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import dash_auth


app = dash.Dash(__name__, title='Centro de Gestión de Movilidad',
				external_stylesheets=[dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

# Connect to app pages
from apps import home
from apps.alfonsoreyes import alfonsoreyes, render_alfonsoreyes 
from apps.hechosviales import (hechosviales, render_hechosviales, render_interseccion_nombre,
	render_interseccion_hv, render_interseccion_les, render_interseccion_fal,
	render_interseccion_hv_ano, render_interseccion_hv_tipo, render_interseccion_hv_causa,
	render_interseccion_resp_edad, render_interseccion_afec_edad, 
	render_interseccion_resp_genero, render_interseccion_afec_genero,
	render_interseccion_resp_vehiculo, render_interseccion_afec_vehiculo)

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
			dbc.Button('Alfonso Reyes', href = '/apps/alfonsoreyes', color = 'light'),

			dbc.Button('Hechos Viales', href='/apps/hechosviales', color='light')
		],
		brand='CGM',
		brand_href='/apps/home'
	),

	html.Div(id='page-content', children=[]),
	dcc.Location(id='url', refresh=False)

])


# Display main pages

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])

def display_page(pathname):
	if pathname == '/apps/alfonsoreyes':
		return alfonsoreyes()
	elif pathname == '/apps/hechosviales':
		return hechosviales()
	else:
		return home.layout

#----------


# Alfonso Reyes

@app.callback(Output('alfonsoreyes_content', 'children'), [Input('tabs', 'active_tab')])

def get_ayuda(tab):
    return render_alfonsoreyes(tab)


# Hechos Viales

@app.callback(Output('hechosviales_content', 'children'), [Input('tabs', 'active_tab')])

def get_hechosviales(tab):
    return render_hechosviales(tab)

#-- Interseccion - Nombre

@app.callback(Output('interseccion_nombre', 'children'),
	[Input('vasconcelos_map', 'clickData')])

def get_interseccion_nombre(clickData):
	return render_interseccion_nombre(clickData)

#-- Interseccion - Hechos Viales

@app.callback(Output('interseccion_hv', 'children'), [Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_hv(clickData)

#-- Interseccion - Lesionados

@app.callback(Output('interseccion_les', 'children'), [Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_les(clickData)

#-- Interseccion - Fallecidos

@app.callback(Output('interseccion_fal', 'children'), [Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_fal(clickData)

#-- Intersección - Hechos Viales por Año

@app.callback(Output('interseccion_hv_ano', 'figure'), [Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_hv_ano(clickData)

#-- Intersección - Tipos de Hechos Viales

@app.callback(Output('interseccion_hv_tipo', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_hv_tipo(clickData)

#-- Intersección - Causas de Hechos Viales

@app.callback(Output('interseccion_hv_causa', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_hv_causa(clickData)

#-- Intersección - Edad de Responsables

@app.callback(Output('interseccion_resp_edad', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_resp_edad(clickData)

#-- Intersección - Edad de Afectados

@app.callback(Output('interseccion_afec_edad', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_afec_edad(clickData)

#-- Intersección - Género de Responsables

@app.callback(Output('interseccion_resp_genero', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_resp_genero(clickData)

#-- Intersección - Género de Afectados

@app.callback(Output('interseccion_afec_genero', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_afec_genero(clickData)

#-- Intersección - Vehículo del Responsable

@app.callback(Output('interseccion_resp_vehiculo', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_resp_vehiculo(clickData)

#-- Intersección - Vehículo del Afectado

@app.callback(Output('interseccion_afec_vehiculo', 'figure'),
	[Input('vasconcelos_map', 'clickData')])

def get(clickData):
 	return render_interseccion_afec_vehiculo(clickData)



if __name__ == '__main__':
	app.run_server(debug=True)

