# coding=utf-8

# Importar librerías
import dash
import dash_auth
import dash_bootstrap_components as dbc
# Para poder hacer uso de la librería con componentes de bootstrap, es muy necesario
# utilizar una hoja de estilos que contenga las clases bootstrap. En este caso se utiliza el tema por default
external_css = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
external_stylesheets = dbc.themes.PULSE #JOURNAL

# Se inicializa la app. 
# Los  meta tags son necesarios para hacer que el layout sea responsivo, es decir, que se adapte a la vista en
app = dash.Dash(__name__, external_stylesheets=[external_css, external_stylesheets],
    meta_tags=[{'name':'viewport',
    'content':'width=device-width, initial-scale = 1.0, maximum-scale=1.5, minimum-scale=1.0'}])

# authenticación
VALID_USERNAME_PASSWORD_PAIRS = {
    'sesna': 'dgria'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


# la siguiente linea puede que se pueda quitar (se menciona en el archivo index.py que
server = app.server

# La siguiente configuración hace que el callback asociado a un output NO 
app.config.suppress_callback_exceptions = True