
from operator import index
from pickle import FALSE

#import dash
#from dash_extensions import Download
#from dash_extensions.enrich import DashProxy, html, Output, Input, dcc
#from dash_extensions.snippets import send_file
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from flask import Flask, render_template
import numpy as np
import pandas as pd
from millify import millify, prettify
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html, callback_context, no_update
import dash_lazy_load
import time
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
#from dash_extensions import Download
#from dash_extensions.snippets import send_file
from dash_iconify import DashIconify
#from dash_extensions.enrich import Dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function, assign
from sqlalchemy import create_engine
from app import app
import requests
import random
import json

import sys
import pymysql
#from apps.produccion_bienestar import reglas_operacion


#########################################################################################
#                                   Header
#########################################################################################


"""
                              Imagen de encabezado

    La sección contiene la imagen de fondo de bajo de la barra de control (navbar),
la cual puede modificarse o suprimirse.

"""

images = ["game-icons:corn", 
        "game-icons:jelly-beans", 
        "emojione-monotone:peanuts",
        "game-icons:wheat",
        "emojione-monotone:sheaf-of-rice",
        "game-icons:corn", 
        "game-icons:jelly-beans", 
        "emojione-monotone:peanuts",
        "game-icons:wheat",
        "emojione-monotone:sheaf-of-rice",
        "game-icons:corn", 
        "game-icons:jelly-beans", 
        "emojione-monotone:peanuts",
        "game-icons:wheat",
        "emojione-monotone:sheaf-of-rice"]

seccion1 = html.Div([
    # se agrega imagenes de cultivos 
    
    # Texto del programa social
    dbc.Row([
        dbc.Col([
                dmc.Text("Programa de ", weight=500,size=30, color='#F8F9F9'),
                dmc.Text("Producción para el Bienestar",  weight=600, size=60, color='#F8F9F9')],
                style = {'textAlign':'center', 'color':'white', 'marginBottom':'5rem', 'marginTop':'3rem'} ),
    ], className='col-12'),
    # imagenes
    dmc.SimpleGrid(
        cols=12,
        spacing="sm",
        verticalSpacing=0,
        children=[   
            html.Div(DashIconify(icon=images[i], width=45, height=40)) for i in range(12)]
    ),
    
], className="twelve columns",  style={'opacity':'0.95','background-blend-mode':'overlay', 'background-size': '100%','backgroundColor': '#212F3D', 'm':'0px', 'padding':'0px', 'height': '50%', 'padding':'2rem'})

# negro1 : #212F3D