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



app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-2FB009N3XV"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-2FB009N3XV');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

server = app.server

# Connect to app pages
from apps import home
from apps.alfonsoreyes import (alfonsoreyes, render_alfonsoreyes, render_conteo,
	render_opciones)

from apps.hechosviales import (hechosviales, render_hechosviales, render_interseccion_nombre,
	render_interseccion_hv, render_interseccion_les, render_interseccion_fal,
	render_interseccion_hv_tiempo, render_mapa_interac, render_down_data, render_tabla,
	render_treemap, render_collapse_button_fecha, render_collapse_button_hv, render_collapse_button_bavan,
	toggle_modal, toggle_modal_sev, toggle_modal_usaf, toggle_modal_thv, toggle_modal_afres,
    render_hv_totales, render_hv_les_totales, render_hv_fall_totales,
    render_opciones_dos, render_opciones_dos_dos, render_mapa_data,  render_down_data_csv,
    render_down_data_tabla, render_down_data_treemap, render_interseccion_hv_tiempo_data, render_down_data_inter,
    render_pub_periodo,
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


#----------

# Hechos Viales

@app.callback(
	Output('hechosviales_content', 'children'), 
	[Input('tabs', 'active_tab')])

def get_hechosviales(tab):
    return render_hechosviales(tab)



#-- Intersecciones - Nombre

@app.callback(
	Output('interseccion_nombre', 'children'), 
	[Input('mapa', 'clickData')])

def get_interseccion_nombre(clickData):
	return render_interseccion_nombre(clickData)


#-- Intersecciones - Hechos Viales

@app.callback(Output('interseccion_hv', 'children'), 
	[Input('mapa', 'clickData'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date'),
	Input('slider_hora', 'value'),
	Input('checklist_dias', 'value')])

def get(clickData, start_date, end_date, hora, diasem):
 	return render_interseccion_hv(clickData, start_date, end_date, hora, diasem)


#-- Intersecciones - Lesionados

@app.callback(Output('interseccion_les', 'children'), 
	[Input('mapa', 'clickData'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date'),
	Input('slider_hora', 'value'),
	Input('checklist_dias', 'value')])

def get(clickData, start_date, end_date, hora, diasem):
 	return render_interseccion_les(clickData, start_date, end_date, hora, diasem)


#-- Intersecciones - Fallecidos

@app.callback(Output('interseccion_fal', 'children'), 
	[Input('mapa', 'clickData'),
	Input('calendario', 'start_date'),
	Input('calendario', 'end_date'),
	Input('slider_hora', 'value'),
	Input('checklist_dias', 'value')])

def get(clickData, start_date, end_date, hora, diasem):
 	return render_interseccion_fal(clickData, start_date, end_date, hora, diasem)


#-- Intersecciones - Hechos Viales por Año

@app.callback(Output('interseccion_hv_tiempo', 'figure'),
    [Input('mapa', 'clickData'),
    Input('periodo_hv', 'active_tab'),
    Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value')])

def update_output(clickData, active_tab, start_date, end_date, hora, diasem):
    return render_interseccion_hv_tiempo(clickData, active_tab, start_date, end_date, hora, diasem)

#-- Intersecciones - Hechos Viales por Año Data

@app.callback(Output('datos_interseccion', 'data'),
    [Input('mapa', 'clickData'),
    Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value')])

def update_output(clickData, start_date, end_date, slider_hora, checklist_dias):
    return render_interseccion_hv_tiempo_data(clickData, start_date, end_date, slider_hora, checklist_dias)

#-- Descargar CSV Datos Interseccion

@app.callback(
    Output("download_data_int", "data"),
    Input("btn_perso_csv_inter", "n_clicks"),
    State('datos_interseccion', 'data'),
    prevent_initial_call=True,)

def func(n_clicks, datos_interseccion):
    return render_down_data_inter(n_clicks, datos_interseccion)

#-- Intersecciones - Modal Tipos de Hechos Viales

@app.callback(
    Output("modal", "is_open"),
    [Input("open1", "n_clicks"), 
    Input("close1", "n_clicks")],
    [State("modal", "is_open")],)

def toggle_modal(open1, close1, modal):
    if open1 or close1:
        return not modal
    return modal


#-- Intersecciones - Tabla Tipos de Hechos Viales

@app.callback([Output('tabla', 'figure'),Output('tabla_data', 'data')], 
    [Input('mapa', 'clickData'),
    Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value')])
    
def update_output(clickData, start_date, end_date, slider_hora, checklist_dias):
    return render_tabla(clickData, start_date, end_date, slider_hora, checklist_dias)


#-- Descargar CSV Tipos de Hechos viales

@app.callback(
    Output("download-tipos-csv", "data"),
    Input("btn_tipos_csv", "n_clicks"),
    State('tabla_data', 'data'),
    prevent_initial_call=True,)


def func(n_clicks, data):
    return render_down_data_tabla(n_clicks, data)


#-- Intersecciones - Tabla Tipos y Causas de Hechos Viales

@app.callback([Output('treemap', 'figure'),Output('treemap_data', 'data')], 
    [Input('mapa', 'clickData'),
    Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value')])
    
def update_output(clickData, start_date, end_date, slider_hora, checklist_dias):
    return render_treemap(clickData, start_date, end_date, slider_hora, checklist_dias)

#-- Descargar CSV Tipos y Causas de Hechos viales

@app.callback(
    Output("download-tiposyc-csv", "data"),
    Input("btn_tiposyc_csv", "n_clicks"),
    State('treemap_data', 'data'),
    prevent_initial_call=True,)


def func(n_clicks, data):
    return render_down_data_treemap(n_clicks, data)


#-- Datos Generales - Tarjeta colapsable calendario

@app.callback(
    Output("collapse_cal", "is_open"),
    [Input("collapse_button_fecha", "n_clicks")],
    [State("collapse_cal", "is_open")],)

def render_collapse_button_fecha(n, is_open):
    if n:
        return not is_open
    return is_open


#-- Datos Generales - Tarjeta colapsable dias de la semana

@app.callback(
    Output("collapse_dsem", "is_open"),
    [Input("collapse_button_hv", "n_clicks")],
    [State("collapse_dsem", "is_open")],)

def render_collapse_button_hv(n, is_open):
    if n:
        return not is_open
    return is_open


#-- Datos Generales - Tarjeta colapsable hora

@app.callback(
    Output("collapse_hora", "is_open"),
    [Input("collapse_button_bavan", "n_clicks")],
    [State("collapse_hora", "is_open")],)

def render_collapse_button_bavan(n, is_open):
    if n:
        return not is_open
    return is_open


#-- Datos Generales - Mapa interactivo

@app.callback(Output('mapa_interac', 'figure'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')],
            prevent_initial_call=False)

def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_mapa_interac(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)

#-- Datos Generales - Mapa data

@app.callback(Output('mapa_data', 'data'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])

def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_mapa_data(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)



#-- Descargar CSV

@app.callback(
    Output("download-personal-csv", "data"),
    Input("btn_perso_csv", "n_clicks"),
    State('mapa_data', 'data'),
    prevent_initial_call=True,)


def func(n_clicks, data):
    return render_down_data_csv(n_clicks, data)





#-- Datos Generales Hechos viales totales

@app.callback(Output('hv_totales', 'children'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_hv_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)


#-- Datos Generales Lesionados totales

@app.callback(Output('hv_les_totales', 'children'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_hv_les_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)


#-- Datos Generales Fallecidos totales

@app.callback(Output('hv_fall_totales', 'children'), 
    [Input('calendario', 'start_date'),
    Input('calendario', 'end_date'),
    Input('slider_hora', 'value'),
    Input('checklist_dias', 'value'),
    Input('hv_graves_opciones', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('checklist_tipo_hv', 'value'),
    Input('hv_afres_opciones', 'value'),
    Input('hv_sexo_opciones', 'value'),
    Input('checklist_tipo_veh', 'value'),
    Input('slider_edad', 'value')])
def get(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones):
    return render_hv_fall_totales(start_date, end_date, slider_hora, checklist_dias, hv_graves_opciones, hv_usu_opciones, checklist_tipo_hv, hv_afres_opciones, checklist_tipo_veh, slider_edad, hv_sexo_opciones)


#-- Datos Generales - Modal Gravedad

@app.callback(
    Output("modal_sev", "is_open"),
    [Input("open1_sev", "n_clicks"), 
    Input("close1_sev", "n_clicks")],
    [State("modal_sev", "is_open")],)

def toggle_modal_sev(open1_sev, close1_sev, modal_sev):
    if open1_sev or open1_sev:
        return not modal_sev
    return modal_sev


#-- Datos Generales - Modal Usuario

@app.callback(
    Output("modal_usaf", "is_open"),
    [Input("open1_usaf", "n_clicks"), 
    Input("close1_usaf", "n_clicks")],
    [State("modal_usaf", "is_open")],)

def toggle_modal_usaf(open1_usaf, close1_usaf, modal_usaf):
    if open1_usaf or close1_usaf:
        return not modal_usaf
    return modal_usaf


#-- Datos Generales - Modal Tipo de hecho vial

@app.callback(
    Output("modal_thv", "is_open"),
    [Input("open1_thv", "n_clicks"), 
    Input("close1_thv", "n_clicks")],
    [State("modal_thv", "is_open")],)

def toggle_modal_thv(open1_thv, close1_thv, modal_thv):
    if open1_thv or close1_thv:
        return not modal_thv
    return modal_thv


#-- Datos Generales - Modal Afectado o responsable

@app.callback(
    Output("modal_afres", "is_open"),
    [Input("open1_afres", "n_clicks"), 
    Input("close1_afres", "n_clicks")],
    [State("modal_afres", "is_open")],)

def toggle_modal_afres(open1_afres, close1_afres, modal_afres):
    if open1_afres or close1_afres:
        return not modal_afres
    return modal_afres


#-- Datos Generales - Cargar opciones por usuario

@app.callback(
    Output('checklist_tipo_hv', 'options'),
    Input('hv_usu_opciones', 'value'),
    Input('hv_graves_opciones', 'value'),
    prevent_initial_call=False)

def get_opciones_dos(hv_usu_opciones, hv_graves_opciones):
    return render_opciones_dos(hv_usu_opciones, hv_graves_opciones)


#-- Datos Generales - Cargar valores por usuario

@app.callback(
    Output('checklist_tipo_hv', 'value'),
    Input('hv_usu_opciones', 'value'),
    Input('hv_graves_opciones', 'value'),
    prevent_initial_call=False)


def get_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones):
    return render_opciones_dos_dos(hv_usu_opciones, hv_graves_opciones)

#-- Descargar Excel

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,)


def func(n_clicks):
    return render_down_data(n_clicks)

#-- Público - Periodo

@app.callback(Output('pub_periodo', 'figure'),
    [Input('periodo_pub_tabs', 'active_tab')])

def update_output(periodo_pub_tabs):
    return render_pub_periodo(periodo_pub_tabs)

if __name__ == '__main__':
	app.run_server(debug=True)