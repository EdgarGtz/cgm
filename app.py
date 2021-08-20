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
	render_interseccion_hv_tiempo, render_mapa_interac, render_down_data, toggle_modal, render_tabla,
	render_treemap, render_collapse_button_cal, render_collapse_button_dsem, render_collapse_button_hora,
	render_opciones_dos, render_opciones_dos_dos,
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
			dbc.Button('Hechos Viales', href='/apps/hechosviales', color='light'),

			dbc.Button('Alfonso Reyes', href = '/apps/alfonsoreyes', color = 'light',
				disabled = True)

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


@app.callback(
	Output('checklist_tipo_hv', 'options'),
 	Input('hv_usvuln_opciones', 'value'))

def get_opciones_dos(tab):
    return render_opciones_dos(tab)

@app.callback(
	Output('checklist_tipo_hv', 'value'),
 	Input('hv_usvuln_opciones', 'value'))

def get_opciones_dos_dos(tab):
    return render_opciones_dos_dos(tab)


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


# Hechos Viales

@app.callback(
	Output('hechosviales_content', 'children'), 
	[Input('tabs', 'active_tab')])

def get_hechosviales(tab):
    return render_hechosviales(tab)

# Filtro de hora

@app.callback(Output('output-container-range-slider', 'children'),
    [Input('slider_hora', 'value')])

def update_hora_selec(value):   
    return format(value)

#-- Interseccion - Nombre

@app.callback(
	Output('interseccion_nombre', 'children'), 
	[Input('mapa', 'clickData')])

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

#-- Mapa interactivo

@app.callback(Output('mapa_interac', 'figure'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usvuln_opciones', 'value'),
    Input('checklist_tipo_hv', 'value')],
            prevent_initial_call=False)

def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usvuln_opciones, checklist_tipo_hv):
    return render_mapa_interac(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usvuln_opciones, checklist_tipo_hv)

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

#-- Descargar Excel

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,)

def func(n_clicks):
    return render_down_data(n_clicks)

#-- Modal Tipos de Hechos Viales

@app.callback(
    Output("modal", "is_open"),
    [Input("open1", "n_clicks"), 
    Input("close1", "n_clicks")],
    [State("modal", "is_open")],)

def toggle_modal(open1, close1, modal):
    if open1 or close1:
        return not modal
    return modal

#-- Tabla Tipos de Hechos Viales

@app.callback(Output('tabla', 'figure'), 
    [Input('mapa', 'clickData'),
    Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value')])
    
def update_output(clickData, start_date, end_date, slider_hora, checklist_dias):
	return render_tabla(clickData, start_date, end_date, slider_hora, checklist_dias)

#-- Tabla Tipos y Causas de Hechos Viales

@app.callback(Output('treemap', 'figure'), 
    [Input('mapa', 'clickData'),
    Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value')])
    
def update_output(clickData, start_date, end_date, slider_hora, checklist_dias):
	return render_treemap(clickData, start_date, end_date, slider_hora, checklist_dias)

#-- Tarjeta colapsable calendario

@app.callback(
    Output("collapse_cal", "is_open"),
    [Input("collapse_button_cal", "n_clicks")],
    [State("collapse_cal", "is_open")],)

def render_collapse_button_cal(n, is_open):
    if n:
        return not is_open
    return is_open

#-- Tarjeta colapsable dias de la semana

@app.callback(
    Output("collapse_dsem", "is_open"),
    [Input("collapse_button_dsem", "n_clicks")],
    [State("collapse_dsem", "is_open")],)

def render_collapse_button_dsem(n, is_open):
    if n:
        return not is_open
    return is_open


#-- Tarjeta colapsable hora

@app.callback(
    Output("collapse_hora", "is_open"),
    [Input("collapse_button_hora", "n_clicks")],
    [State("collapse_hora", "is_open")],)

def render_collapse_button_hora(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
	app.run_server(debug=True)