
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

from costumFunctions import make_dataframe_state_mun
import sys
import pymysql
from apps.segalmex import reglas_operacion



##################################################################
#                          Introducción
##################################################################

# Esta sección contien información introductoria sobre el programa de precios de garantía

seccion2 = html.Div([
    dbc.Row([
        dbc.Col([
            dmc.Paper(
                children=[
                    dmc.Text("¿Qué es el Programa Precios de Garantía a Productos Alimentarios Básicos?", size=24, color='white', align="justify"),
                    html.Br(),
                    dmc.Text("El Programa de Precios de Garantía a Productos Alimentarios Básicos forma parte de los Programas Prioritarios del Gobierno Federal que buscan brindar una atención integral a las problemáticas vinculadas con la autosuficiencia alimentaria, se encuentra a cargo de la Secretaría de Agricultura y Desarrollo Rural y es operado por uno de sus organismos descentralizados, Seguridad Alimentaria Mexicana (SEGALMEX).", color='white', align="justify"),
                    html.Br(),
                    dmc.Text("El objetivo general del Programa Precios de Garantía es complementar el ingreso de los pequeños y medianos productores agropecuarios de granos básicos y leche.", color='white', align="justify")],
                shadow="xs",
                style={'backgroundColor':'#2a3240'}
            ),
        ], className= 'col-xl-6 col-12',style={'backgroundColor':'#2a3240', 'padding':'2rem'}),
        #dmc.Divider(orientation="vertical", style={"height": 20}),
        dbc.Col([
            dmc.Text("Diagrama general de la dinámica del programa", size=24, color='white', align="center"),
            dmc.Image(src="./assets/logo10.svg",width='100%', withPlaceholder=True)
        ], className='col-xl-6 col-12',style={'padding':'2rem', 'margin':'0rem'}),
    ], className='col-12', style={'backgroundColor':'#2a3240'}),
], style={'marginTop':'5rem', 'backgroundColor':'#2a3240'})