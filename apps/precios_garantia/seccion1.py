
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
from apps.precios_garantia import reglas_operacion


#########################################################################################
#                                   Header
#########################################################################################


"""
                              Imagen de encabezado

    La sección contiene la imagen de fondo de bajo de la barra de control (navbar),
la cual puede modificarse o suprimirse.

"""

# seccion 1 : header
# Esta sección es exclusiva para el encabezado del programa de precios de garantía
seccion1 = html.Div([
    dbc.Row([
        dbc.Col([#dbc.NavbarBrand("Programa de Precios de Garantía",
                 #        style={'color':'white', 'font-size': '60px', 'textAlign':'center'}),
                dmc.Text("Programa de Precios de Garantía a", weight=500,size=30, color='white'),
                #html.Br(),
                dmc.Text("Productos Alimentarios Básicos",  weight=600, size=60, color='white')],
                style = {'textAlign':'center', 'color':'white', 'marginBottom':'5rem', 'marginTop':'6rem'} ),
    ], className='col-12'),
    # dbc.Row([
    #     dbc.Col([], className='col-5'),
    #     dbc.Col([], className='col-4'),
    #     dbc.Col([
    #         dmc.Button("Resumen Ejecutivo",
    #             id="open",
    #             leftIcon=DashIconify(icon="ant-design:read-outlined"),
    #             color="orange",
    #             n_clicks=0),
    #     ], className='col-3', style={'marginBottom':'2rem', 'paddingRight':'2rem'})
    # ], className='twelve columns'),
], className="twelve columns",  style={'opacity':'0.95','background-blend-mode':'overlay','background-image': 'url(/assets/maiz-mexico.jpg)','background-size': '100%','backgroundColor': '#2a3240', 'm':'0px', 'padding':'0px', 'height': '100%', 'padding':'2rem'})
