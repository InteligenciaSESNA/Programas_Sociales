
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



#########################################################################################
#                                Descripción del mapa
#########################################################################################

"""
                            Descripción de mapa

    En esta sección se plasman las caracteristicas del mapa, su funcionamineto, así como
Componentes que lo integran de forma explícita. Así también el significado de la 
simbología utilizada: colores, tamaños, formas principalemente.

"""

seccion5 = html.Div([
    dbc.Fade(
        html.Div([  
            dmc.Paper(children=[
                    dmc.Text("Introducción al Mapa de características relacionadas con la implementación del Programa de Precios de Garantía a Productos Alimentarios Básicos", size=24, color='white'),
                    dbc.Row([
                        dbc.Col([
                            html.Br(),
                            dmc.Text("El mapa tiene la finalidad de comparar a los productores y población objetivo, respecto a las personas beneficiarias del Programa Precios de Garantía a Productos Alimentarios Básicos. Lo anterior a fin de contar con una herramienta de análisis para entender la manera en la que se distribuyeron territorialmente los beneficios del Programa que apoye a la identificación de posibles riesgos de corrupción, así como  los impactos en poblaciones vulnerables.", size=16, color='white', align="justify"),
                            html.Br(),
                            dmc.Text("¿Cómo usar el mapa?", size=24, color='white'),
                            html.Br(),
                            dmc.Text("El mapa tiene dos opciones para beneficiarios: Monto del apoyo y Número de beneficarios, y dos pestañas a) Capas, y b) Escenarios.", size=16, color='white', align="justify"),
                            html.Br(),
                            dmc.List(
                                icon=dmc.ThemeIcon(
                                    DashIconify(icon="radix-icons:check-circled", width=16),
                                    radius="xl",
                                    color="teal",
                                    size=24,
                                ),
                                size="sm",
                                spacing="sm",
                                children=[
                                    dmc.ListItem(dmc.Text("Capas", size=20, color='white')),
                                    dmc.Text("Muestra diversas variables relacionadas con la población objetivo del Programa que se superponen con el mapa para identificar relaciones geográficas. Tiene dos cuadros de filtros: 1) agregar, y 2) remover. Para agregar un filtro, en la caja de Agregar debe seleccionarse la casilla de la variable y, posteriormente, dar clic en la flecha que está en la esquina superior derecha. Para quitar variables del mapa, se selecciona la característica en el cuadro Remover, y se da clic en la flecha. Las capas que se pueden agregar o remover son:", size=16, color='white', align="justify"),
                                    dmc.List(
                                            icon=dmc.ThemeIcon(
                                            DashIconify(icon="pepicons-pencil:circle", width=8),
                                            radius="sm",
                                            color="blue",
                                            size=12,
                                        ),
                                        children=[
                                        dmc.ListItem(dmc.Text("Centros de acopio", size=16, color='white')),
                                        dmc.ListItem(dmc.Text("Beneficiarios", size=16, color='white')),
                                        dmc.ListItem(dmc.Text("Volumen de producción", size=16, color='white')),
                                        dmc.ListItem(dmc.Text("Productores", size=16, color='white')),]),
                            ]),
                        ], className='col-lg-6 col-sm-12 col-12'),
                        
                        dbc.Col([
                            html.Br(),
                            dmc.List(
                                icon=dmc.ThemeIcon(
                                    DashIconify(icon="radix-icons:check-circled", width=16),
                                    radius="xl",
                                    color="teal",
                                    size=24,
                                ),
                                size="sm",
                                spacing="sm",
                                children=[
                                    dmc.Text("Además, cada capa se encuentra desagregada, excepto Volumen de producción,  por grado de marginación: Muy bajo, bajo, Medio, Alto, y Muy alto", size=16, color='white', align="justify"),
                                    dmc.Text("Debajo de las cajas de filtros, se encuentran cuatro estadísticas descriptivas relacionadas con el Programa, que son:", size=16, color='white'),
                                    dmc.List(
                                            icon=dmc.ThemeIcon(
                                            DashIconify(icon="pepicons-pencil:circle", width=8),
                                            radius="sm",
                                            color="blue",
                                            size=12,
                                        ),
                                        children=[
                                        dmc.ListItem(dmc.Text("Centros de acopio : muestra el número de centros de acopio", size=16, color='white')),
                                        dmc.ListItem(dmc.Text("Pob. Beneficiaria : muestra el número/monto de población beneficiaria", size=16, color='white')),
                                        dmc.ListItem(dmc.Text("Vol. Incentivado (Total) : Muestra el monto total del volumen incentivado total", size=16, color='white')),
                                        dmc.ListItem(dmc.Text("Vol. Incentivado (Prom): Muestra el monto promedio del volumen incentivado total", size=16, color='white')),]),
                                    html.Br(),
                                    dmc.Text("Descripción de la simbología", size=16, color='white'),
                                    dmc.List(
                                            icon=dmc.ThemeIcon(
                                            DashIconify(icon="pepicons-pencil:circle", width=8),
                                            radius="sm",
                                            color="blue",
                                            size=12,
                                        ),
                                        children=[
                                        dmc.ListItem([
                                            dmc.Text("Al seleccionar Número de beneficiarios:", size=16, color='white'),
                                            dmc.List(
                                                icon=dmc.ThemeIcon(
                                                DashIconify(icon="codicon:circle-filled", width=8),
                                                radius="sm",
                                                color="yellow",
                                                size=8,
                                            ),
                                            children=[
                                            dmc.ListItem(dmc.Text("Ubicación del círculo: indica en dónde se encuentran ubicados los beneficiarios que recibieron el apoyo del programa.", size=16, color='white')),
                                            dmc.ListItem(dmc.Text("Color: el color hace referencia al grado de marginación al que pertenece el municipio en donde los beneficiarios entregaron sus productos.", size=16, color='white')),]),
                                            ]),
                                        dmc.ListItem([
                                            dmc.Text("Al seleccionar Montos de apoyo:", size=16, color='white'),
                                            dmc.List(
                                                icon=dmc.ThemeIcon(
                                                DashIconify(icon="codicon:circle-filled", width=8),
                                                radius="sm",
                                                color="yellow",
                                                size=8,
                                            ),
                                            children=[
                                            dmc.ListItem(dmc.Text("Ubicación del círculo: indica en dónde se encuentra ubicado el monto del apoyo del programa.", size=16, color='white')),
                                            dmc.ListItem(dmc.Text("Color: el color hace referencia al grado de marginación al que pertenece el monto total del lugar en donde los beneficiarios entregaron sus productos.", size=16, color='white')),
                                            dmc.ListItem(dmc.Text("Tamaño del círculo: indica el tamaño del monto que se recibió en ese municipio. A mayor tamaño del círculo, mayor tamaño del monto.", size=16, color='white')),]),        
                                            ]),
                                        ]),
                                    
                                    dmc.ListItem(dmc.Text("Escenarios", size=20, color='white')),
                                    dmc.Text("Muestra escenarios generados con respecto a la distribución del monto total otorgado, por año y producto, considerando los siguientes criterios:", size=16, color='white', align="justify"),
                                    dmc.List(
                                            icon=dmc.ThemeIcon(
                                            DashIconify(icon="pepicons-pencil:circle", width=8),
                                            radius="sm",
                                            color="yellow",
                                            size=12,
                                        ),
                                        children=[
                                        dmc.ListItem(dmc.Text("Marginación: ", size=16, color='white')),
                                        dmc.ListItem(dmc.Text("Precio: ", size=16, color='white')),]),
                            ]),
                        ], className='col-lg-6 col-sm-12 col-12')        
                    ]),
            ],
            shadow="xs",
            style={'opacity':'0.7', 'paddingRight':'2rem', 'paddingLeft':'2rem', 'backgroundColor':'#2a3240'}
            ),
        ], style={'paddingBottom':'2rem', 'paddingTop':'2rem'}),
    id="fade-transition",
    is_in=True,
    style={"transition": "opacity 2000ms ease"},
    timeout=2000,
    ),
], style={'paddingBottom':'2rem', 'paddingTop':'2rem','opacity':'0.95','background-blend-mode':'overlay','background-image': 'url(/assets/#)','background-size': '100%','backgroundColor': '#2a3240', 'm':'0px', 'padding':'0px', 'height': '100%'} )
