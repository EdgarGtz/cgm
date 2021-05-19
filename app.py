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
from apps import home
from apps.hechosviales import (hechosviales, render_hechosviales, render_interseccion_nombre,
	render_interseccion_hv, render_interseccion_2015, render_interseccion_2016,
	render_interseccion_2017, render_interseccion_2018, render_interseccion_2019,
	render_interseccion_2020, render_vasconcelos_bar)
from apps.datos import datos, render_datos
from apps.ayuda import ayuda, render_ayuda

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

			dbc.Button('Hechos Viales', href='/apps/hechosviales', color='light'),
			
        	dbc.DropdownMenu([
                	dbc.DropdownMenuItem('Monitoreo de Tráfico',
                		href='https://www.waze.com/es/live-map', target='blank'),
                	dbc.DropdownMenuItem('Reporte de Eventos',
                		href='https://www.waze.com/reporting', target='blank', disabled=True),
                	dbc.DropdownMenuItem('Cierre de Vialidades',
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


# Display main pages

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])

def display_page(pathname):
	if pathname == '/apps/hechosviales':
		return hechosviales()
	elif pathname == '/apps/datos':
		return datos()
	elif pathname == '/apps/ayuda':
		return ayuda()
	else:
		return home.layout


# Hechos Viales

@app.callback(Output('hechosviales_content', 'children'), [Input('tabs', 'active_tab')])

def get_hechosviales(tab):
    return render_hechosviales(tab)

#-- Interseccion - Nombre

@app.callback(Output('interseccion_nombre', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_interseccion_nombre(clickData):
	return render_interseccion_nombre(clickData)

#-- Interseccion - Hechos Viales

@app.callback(Output('interseccion_hv', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_interseccion_hv(clickData)

#-- Interseccion - 2015

@app.callback(Output('interseccion_2015', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_interseccion_2015(clickData)

#-- Interseccion - 2016

@app.callback(Output('interseccion_2016', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_interseccion_2016(clickData)

#-- Interseccion - 2017

@app.callback(Output('interseccion_2017', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_interseccion_2017(clickData)

#-- Interseccion - 2018

@app.callback(Output('interseccion_2018', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_interseccion_2018(clickData)

#-- Interseccion - 2019

@app.callback(Output('interseccion_2019', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_interseccion_2019(clickData)

#-- Interseccion - 2020

@app.callback(Output('interseccion_2020', 'children'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_interseccion_2020(clickData)

#-- Vasconcelos (Bar)

@app.callback(Output('vasconcelos_bar', 'figure'), [Input('vasconcelos_map', 'clickData')])

def get_(clickData):
 	return render_vasconcelos_bar(clickData)



# Datos

@app.callback(Output('datos_content', 'children'), [Input('tabs', 'active_tab')])

def get_datos(tab):
    return render_datos(tab)

# Ayuda

@app.callback(Output('ayuda_content', 'children'), [Input('tabs', 'active_tab')])

def get_ayuda(tab):
    return render_ayuda(tab)


if __name__ == '__main__':
	app.run_server(debug=True)

