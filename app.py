import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output, State
import dash_auth


app = dash.Dash(__name__, title='Centro de Gestión de Movilidad',
				external_stylesheets = [dbc.themes.BOOTSTRAP],
				meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'},])

server = app.server

# Connect to app pages
from apps import home
from apps.alfonsoreyes import (alfonsoreyes, render_alfonsoreyes, render_conteo,
	render_opciones)
from apps.hechosviales import (hechosviales, render_hechosviales, render_interseccion_nombre,
	render_interseccion_hv, render_interseccion_les, render_interseccion_fal,
	render_interseccion_hv_tiempo, render_mapa
	)

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
			dbc.Button('Cámaras Viales', href = '/apps/alfonsoreyes', color = 'light'),

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

# Opciones
@app.callback(
	Output('my_dropdown', 'options'),
 	Input('my_dropdown_0', 'value'))

def get_opciones(tab):
    return render_opciones(tab)


# Conteo y Velocidades

@app.callback(
	Output('conteo2', 'figure'),
	[Input('periodo', 'active_tab'),
	Input('my_dropdown', 'value'),
	Input('my_dropdown_0', 'value'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date')])

def get_conteo1(tab, tab1, tab2, tab3, tab4):
    return render_conteo(tab, tab1, tab2, tab3, tab4)


# Alfonso Reyes - General

@app.callback(Output('alfonsoreyes_content', 'children'), 
	[Input('tabs', 'active_tab')])

def get_ayuda(tab):
    return render_alfonsoreyes(tab)


@app.callback(Output('output-container-range-slider', 'children'),
    [Input('slider_hora', 'value')])
def update_hora_selec(value):   
    return format(value)

# Hechos Viales

@app.callback(Output('hechosviales_content', 'children'), [Input('tabs', 'active_tab')])

def get_hechosviales(tab):
    return render_hechosviales(tab)

#-- Interseccion - Nombre

@app.callback(Output('interseccion_nombre', 'children'), [Input('mapa', 'clickData')])

def get_interseccion_nombre(clickData):
	return render_interseccion_nombre(clickData)

#-- Interseccion - Hechos Viales

@app.callback(Output('interseccion_hv', 'children'), 
	[Input('mapa', 'clickData'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date'),
	Input('slider_hora', 'value'),
	Input('checklist_dias', 'value')])

def get(clickData, start_date, end_date, hora, diasem):
 	return render_interseccion_hv(clickData, start_date, end_date, hora, diasem)

#-- Interseccion - Lesionados

@app.callback(Output('interseccion_les', 'children'), 
	[Input('mapa', 'clickData'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date'),
	Input('slider_hora', 'value'),
	Input('checklist_dias', 'value')])

def get(clickData, start_date, end_date, hora, diasem):
 	return render_interseccion_les(clickData, start_date, end_date, hora, diasem)

#-- Interseccion - Fallecidos

@app.callback(Output('interseccion_fal', 'children'), 
	[Input('mapa', 'clickData'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date'),
	Input('slider_hora', 'value'),
	Input('checklist_dias', 'value')])

def get(clickData, start_date, end_date, hora, diasem):
 	return render_interseccion_fal(clickData, start_date, end_date, hora, diasem)

#-- Mapa

@app.callback(Output('mapa', 'figure'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value')],
            prevent_initial_call=False)

def get(start_date, end_date, slider_hora, checklist_dias):
    return render_mapa(start_date, end_date, slider_hora, checklist_dias)

#-- Intersección - Hechos Viales por Año

@app.callback(Output('interseccion_hv_tiempo', 'figure'),
	[Input('mapa', 'clickData'),
	Input('periodo_hv', 'active_tab'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date'),
	Input('slider_hora', 'value'),
	Input('checklist_dias', 'value')])

def update_output(clickData, active_tab, start_date, end_date, hora, diasem):
 	return render_interseccion_hv_tiempo(clickData, active_tab, start_date, end_date, hora, diasem)


if __name__ == '__main__':
	app.run_server(debug=True)