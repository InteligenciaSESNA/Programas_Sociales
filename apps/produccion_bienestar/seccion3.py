
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
from apps.produccion_bienestar import reglas_operacion




#########################################################################################
#                     Información general del programa (se ha desactivado)
#########################################################################################


"""
                        Recursos ejercidos del programa

    La sección contiene informació sobre los recursos ejercidos del programa de 
Precios de garantía.

"""


seccion3 = html.Div([
    dmc.Text("Recursos ejercidos en el Programa,", size=55, weight=600, color='#4e203a', align="center", style={'paddingBottom':'0rem'}),
    dmc.Text("por tipo de producto y año fiscal", size=45, weight=500, color='#4e203a', align="center", style={'marginBottom':'2rem'}),
    dmc.Tabs([  
        dmc.TabsList([
            dmc.Tab("2019", value="2019"),
            dmc.Tab("2020", value="2020"),
            dmc.Tab("2021", value="2021"),
        ], style={'padding':'0.5rem','Color':'white','backgroundColor':'white'}),
    ],
    id="tabs-example",
    orientation='horizontal',
    color="#4e203a",        
    value="2019"
    ),
    
    html.Div(id="section3-content", className='col-12', style={'marginTop':'2rem','marginBottom':'2rem', 'paddingLeft':'2rem', 'paddingRight':'2rem'}), 
], className='col-12', style={'paddingTop':'2rem','paddingBottom':'2rem','backgroundColor':'white'})
