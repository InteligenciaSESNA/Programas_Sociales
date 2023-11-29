# coding=utf-8

# Este archivo contiene el código de la página principal de la app. Contiene todos los hipervínculos a 
# las demás páginas, así como la barra de navegación.

# Importar librerías
import dash
# Se utiliza la librería dash bootstrap
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from app import app
# se importan los archivos .py de la carpeta apps
from apps.segalmex import segalmex
from apps import home

# Se inicializa el componente dropdown que sirve para hacer el menu desplegable mostrado
# en la barra de navegación.
dropdown = dbc.DropdownMenu(
    children=[
        #dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("SEGALMEX", href="/segalmex"),
        # dbc.DropdownMenuItem("LICONSA", href="/page2"),
        # dbc.DropdownMenuItem("DICONSA", href="/page3"),
    ],
    nav = True,
    in_navbar = True,
    label = "Menú",
    style={'fontSize':'18px', 'padding':'0rem'}
)

# Se inicializa barra de navegación
navbar = dbc.Navbar(
    dbc.Container([
            # el logo y el nombre se ponen dentro de un hipervínculo que redirige a la página de inicio
            dbc.Row([
                dbc.Col(
                    html.Img(src="assets/Logotipo_blanco.png", height="40px"), 
                className='col-3', style={'paddingRight':'2rem', 'text-align':'right'}),
               
                dbc.Col([
                    html.A(
                        
                        dmc.Text("Secretaría Ejecutiva del Sistema Nacional Anticorrupción", size=20, color='white'),
                            
                        # en el href se marca a donde dirige cuando se da click en estas partes
                        # href="/home",
                        href="/segalmex",
                        style={"textDecoration": "none"},
                    ),  
                ], className='col-9', style={'paddingLeft':'1rem','paddingBottom':'1rem', 'text-align':'left'}),
                # dbc.Col([
                #     dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                #     # Aquí se incluhe el componente dropdown que ya se había hecho con anterioridad
                #     dbc.Collapse(
                #         dbc.Nav(
                #             [dropdown], navbar=True
                #         ),
                #         id="navbar-collapse",
                #         is_open=False,
                #         navbar=True,
                #     ),  
                # ], className='col-1', align="right", style={'paddingRight':'1rem'}),
            ], className='col-12'),
            
        ], style={'height':'5rem'}
    ),
    color="dark",
    dark=True,
    fixed='relative',
    className='col-lg-12 col-12',
)


# El siguiente callback sirve para cambiar entre la hamburguesa y la versión extendida
# del menú según el tamaño de la pantalla. 
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Se utiliza el componente navbar previamente construido en el layout de la app
app.layout = html.Div([
    # El siguient componente permite conocer el valor de la url en un momento dado.
    dcc.Location(id='url', refresh=False),
    navbar,
    # Se define un div con un id determinado que es el que contiene el contenido de la página y es
    # el que va cambiando conforme se va cambiando el valor de la url. 
    html.Div(id='page-content'),
    # footer 
    html.Footer([
        html.Br(),
        html.Br(),
        html.Center(
            dbc.Row([
                dbc.Col(
                    html.Img(src="assets/Logotipo_blanco.png", height="40px"), 
                className='col-4', style={'text-align':'right'}),
                
                dbc.Col([
                    html.A(
                        
                        dmc.Text("Secretaría Ejecutiva del Sistema Nacional Anticorrupción", size=20, color='white'),
                            
                        # en el href se marca a donde dirige cuando se da click en estas partes
                        #href="/home",
                        href="/segalmex",
                        style={"textDecoration": "none"},
                    ),  
                ], className='col-8', style={'paddingLeft':'0rem', 'text-align':'left'}),
                
                #     dbc.Col(html.Img(src="assets/Logotipo_blanco.png",height="40px"), style = {'textAlign':'right'} ),
                #     dbc.Col(dbc.NavbarBrand("Secretaría Ejecutiva del Sistema Nacional Anticorrupción", style={'color':'white', 'font-size': '24px', 'textAlign':'left'})),
            ], className='col-10', style={'paddingLeft':'0rem','paddingBottom':'6rem'}),
            ),
            # en el href se marca a donde dirige cuando se da click en estas partes
                #href="/home",
                #style={"textDecoration": "none"},
        #    ),

    ], className="col-12", style={'color':'white', 'backgroundColor':'#566573'}), #566573

])


# A continuación se define como cambia la página según las rutas, cada sección está escrita en su propio
# archivo
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):

    if pathname == '/segalmex':
        return segalmex.layout
    elif pathname == '/segalmex':
        return segalmex.layout
    elif pathname == '/segalmex':
        return segalmex.layout

    else:
        #return home.layout
        return segalmex.layout

#HOST = '10.14.10.145'
#PORT = 8000

if __name__ == '__main__':
    app.run_server(debug=False)
    #app.run_server(debug=False, host= HOST, port=PORT)
