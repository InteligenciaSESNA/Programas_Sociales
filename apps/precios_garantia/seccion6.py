
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
#                                       Mapa
#########################################################################################

"""
                                        Mapa

    En esta sección se encuentra el mapa, los componentes que permiten manipular ciertas
características como:
    - Capas : beneficiarios, centros de acopio, volumen de producción, y productores.
    - Opción beneficarios : Monto y número de beneficiarios
    - Lista de tranbsferencia: Grado de marginación, y tamaño del productor, 
    - Estadísticos descriptivos
    
Se define en dos parte:
    - Izquierda : mapa
    - Derecha : sidebar 
"""

######                       Barra de control derecha
sidebar_right = html.Div([
        # Filtros
            dmc.Group([
                dmc.SimpleGrid(cols=2, children=[
                    html.Div([ 
                        dmc.Text('Año :', size=14,weight=350, color="black", align="left", style={'padding':'0rem', 'margin':'0rem'}),
                        dmc.Text('Producto :', size=14,weight=350, color="black", align="left", style={'padding':'0rem', 'margin':'0rem'}),
                    ]),
                    #dmc.Divider(orientation="vertical", style={"height": 30}),
                    html.Div([
                        dmc.Text('2020', id='anio_filtro1', size=14,weight=700, color="#4e203a", align="left", style={'padding':'0rem', 'margin':'0rem'}),    
                        dmc.Text('ARROZ', id='producto_filtro1', weight=700, size=14, color="#4e203a", align="left", style={'padding':'0rem', 'margin':'0rem'}),
                    ]),
                ], style={'padding':'0rem', 'margin':'0rem'}),
            ], style={'paddingTop':'1rem', 'paddingBottom':'1rem'}),
            
            dmc.Divider(orientation="horizontal", style={"weight":'100%', 'marginBottom':'1rem'}),
    
            # tabs para criterios y capas
            dmc.Tabs([
                dmc.TabsList([
                    dmc.Tooltip(
                        multiline=True,
                        width=150,
                        withArrow=True,
                        transition="fade",
                        position='right',
                        color='dark',
                        transitionDuration=300,
                        label="En esta sección se muestran características de beneficiarios, total de productores, centros de acopio, y volumen de producción. ",
                        children=[
                            dmc.Tab("Capas",
                                icon=DashIconify(icon="ic:baseline-edit-location-alt"),
                                value="capas",
                                style={'color':'#4e203a'}
                            )
                    ], style={'fontSize':'12px'}),
                    dmc.Tooltip(
                        multiline=True,
                        width=150,
                        withArrow=True,
                        transition="fade",
                        position='bottom',
                        color='dark',
                        transitionDuration=300,
                        label="En esta sección se muestran distintos escenarios sobre la redistribución de los apoyos otorgados considerando diversos criterios.",
                        children=[
                            dmc.Tab("Escenarios",
                                #id="tab-criterios",
                                icon=DashIconify(icon="ic:round-window"),
                                value="criterios",
                                style={'color':'#4e203a'}
                            )
                    ], style={'fontSize':'12px'}),
                    
                ]),
            ],
            id='capas-criterios',
            persistence= True,
            persistence_type = 'session',
            value="capas"),

            dmc.Card([
                    html.Div(
                        id="content-capas-criterios",
                        style={'marginTop':'1rem'}),
                ],
                withBorder=False,
                shadow=0,
                radius="md",
                style={"width": '100%',"padding":'0rem'},
                ),

        ], style={'paddingLeft':'2rem', 'paddingRight':'2rem', 'marginTop':'0.5rem'}
    )


##################                     Mapa interactivo                    ##############
seccion6 = html.Div([
        dbc.Row([
            dbc.Col([
                    html.Div([
                     ], id="mapa", style={"width": "100%", "height":'100%'}
                    ),   # style={'height':'100vh'}
            ], className="card col-12 col-md-12 col-lg-12 col-xl-8", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 0px 0px 0px', 'border-radius': '10px', 'backgroundColor': '#BFC9CA', }
            ),
            dbc.Col([
                sidebar_right

            ], className="card col-12 col-md-12 col-lg-12 col-xl-4", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 0px 0px 0px', 'border-radius': '0px', 'backgroundColor': 'white', }
            )
        ]),
        # Barra de control
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem', 'marginRight': '2rem','marginBottom': '4rem'}
    )