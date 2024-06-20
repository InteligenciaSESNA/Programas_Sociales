
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
#                              Filtros principales
#########################################################################################

"""
                                Filtros

La sección contiene los dos filtros principales:
- Filtro de año
- Filtro de producto 
- Datos de descarga (desactivados)
- Reglas de operación

Los filtros principales van a fungir como filtros a partir de los cuales se actualizará
toda la información restante: el mapa, gráficos, reglas de operacipon, descargas, 
entre otras.

"""

list_year = ['2019','2020','2021','2022', '2023']
list_products = ['Ajonjoli grano', 'Amaranto', 'Arroz', 'Arvejon grano',
                'Avena grano', 'Cacahuate', 'Cacao', 'Cafe',
                'Calabaza chihua (pipian)', 'Caña de azucar', 'Cartamo grano',
                'Cebada grano', 'Chia', 'Colza o canola', 'Frijol',
                'Garbanzo grano', 'Girasol grano', 'Haba grano', 'Lenteja',
                'Linaza', 'Maiz grano', 'Nopal', 'Sorgo grano', 'Soya grano',
                'Trigo grano', 'Miel abeja', 'Milpa']
#################################################################
#          Filtros principales (año -producto) - Descargas
#################################################################
seccion4 = html.Div([
    dbc.Row([
        # Primera columna : Vacia
        dbc.Col([
            dmc.Button(
                    "Instrucciones: ",
                    id="fert_transition-instrucciones-btn",
                    variant="subtle",
                    leftIcon=DashIconify(icon="line-md:list"),
                    color="white",
                    n_clicks=0
                ),
            dbc.Fade(
                html.Div([
                    dmc.Text("El mapa se puede observar por año fiscal y producto. Para ello es necesario seleccionar un año y producto, y en seguida dar click en actualizar para observar los siguientes cambios: ", color='black', size=11),
                    dmc.Space(h=30),
                    dmc.List(
                        icon=dmc.ThemeIcon(
                            DashIconify(icon="ic:baseline-vignette", width=14),
                            radius="xl",
                            color="orange",
                            size=14,
                        ),
                        size="sm",
                        spacing="sm",
                        children=[
                            dmc.ListItem(dmc.Text("Mapa con la referencia geográfica de los beneficiarios.", color='black', size=12)),
                            dmc.ListItem(dmc.Text("Características del programa social (dar click en 'Carac. Prog. Sociales')", color='black', size=12)),
                            dmc.ListItem(dmc.Text("Bases de datos utilizada (dar click en 'Descargar xlsx')", color='black', size=12)), 
                        ],
                    ),    
                    
                ], style={'border-radius': '10px', 'backgroundColor':'#F2F3F4', 'padding':'1rem'}),
                id="fert_transition-instrucciones",
                is_in=False,
                appear=False,
                style={"transition": "opacity 2000ms ease"},
                timeout=2000,
            ),
       
        ], className='col-xl-4 col-0', style={'paddingRight':'4rem', 'paddingLeft':'4rem', 'paddingTop':'1rem'}),
        # Segunda columna : Selector AÑO
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dmc.Select(
                        icon=DashIconify(icon="material-symbols:filter-list-rounded"),
                        label=
                        dmc.Tooltip(
                            multiline=True,
                            width=200,
                            withArrow=True,
                            transition="fade",
                            position='right',
                            transitionDuration=300,
                            label="Seleccione un año fiscal",
                            children=["Seleccione el año"],
                            ),
                        id="fert_anio",
                        data=list_year,
                        value='2023',
                        searchable=True,
                        nothingFound="No options found",
                        style={"textAlign": "Left"}
                    ),
                ]),
                dbc.Col([
                    dmc.Select(
                        icon=DashIconify(icon="material-symbols:filter-list-rounded"),
                        label=
                        dmc.Tooltip(
                            multiline=True,
                            width=200,
                            withArrow=True,
                            transition="fade",
                            position='right',
                            transitionDuration=300,
                            label="Seleccione un producto",
                            children=["Seleccione el producto"],
                            ),
                        id="fert_producto",
                        data=list_products,
                        value='Arroz',
                        searchable=True,
                        nothingFound="No options found",
                        style={"textAlign": "left"},
                    ),
                ]),
            ], style={'marginBottom':'3rem','paddingBottom':'2rem', 'paddingRight':'1rem', 'paddingLeft':'1rem'}),
            
            dbc.Col([
                html.Center(
                    dbc.Row([
                        dbc.Col([
                            dmc.Button(
                                'Actualizar',
                                id='fert_submit-button',
                                n_clicks=0,
                                #children='Actualizar',
                                color = 'dark'
                            ),
                        ]),
                    ]),
                ),
            ]),
        ], className='col-xl-4 col-12',  style={'marginBottom':'4rem', 'paddingTop':'5rem'}),
        # Tercera columna : Selector Producto
        
        dbc.Col([
            dmc.Center(
                dbc.Row([
                    dcc.Download(id="fert_download"), 
                ], className='col-xl-6 col-8', style={'marginBottom':'0rem'}),
            ),
              
            
        ], className='col-xl-4 col-12', style={'marginBottom':'0rem'}),
        
        #  
        dmc.Center(
        dmc.Group([   
            html.Div([
                 #dmc.Anchor(
                    dmc.Button("Carac. Prog. Sociales",
                            id="fert_open",
                            variant="subtle",
                            leftIcon=DashIconify(icon="ant-design:read-outlined"),
                            color="white",
                            n_clicks=0), #, href='#'),
                    dbc.Modal([
                            dbc.ModalHeader(dbc.ModalTitle(
                                dmc.Grid(
                                    children=[
                                        dmc.Col(html.Div(dmc.Text("Características de los apoyos : ")), span=8),
                                        dmc.Col(html.Div(dmc.Text("2020", id="anio_filtro2")), span=2),
                                        dmc.Col(html.Div("-"), span=1),
                                        dmc.Col(html.Div(dmc.Text("Frijol", id="producto_filtro2")), span=1),
                                    ],
                                    justify="center",
                                    align="center",
                                    gutter="xl",
                                ),
                                style={'color':'#4e203a'}), style={'backgroundColor':'white'} ),
                            dbc.ModalBody(html.Div(children=[
                                ], id='fert_reglas-operacion', style={'paddingLeft':'2.5rem', 'paddingRight':'2.5rem'})
                            , style={'backgroundColor':'#2a3240'}),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Cerrar", id="fert_close", className="ms-auto", outline=False, color="dark", n_clicks=0
                                ), style={'backgroundColor':'white'}
                            ),
                        ],
                        id="modal",
                        size='xl',
                        centered=True,
                        zIndex=10000,
                        is_open=False
                    ),
            ]),
            dmc.Divider(orientation="vertical", style={"height": 30}),
            html.Div([
                #dmc.Anchor(
                    dmc.Button("Descarga xlsx",
                            id="fert_dowload_xlsx",
                            variant="subtle",
                            leftIcon=DashIconify(icon="eos-icons:database"),
                            color="white",
                            n_clicks=0) , #href='#'),
                    dcc.Download(id="fert_download-db-xlsx"),
            ], style={'display': 'inline-block'}),
            dmc.Divider(orientation="vertical", style={"height": 30}),
            html.Div([
                dmc.Button(
                    "...",
                    id="fert_fade-transition-button",
                    variant="subtle",
                    #leftIcon=DashIconify(icon="eos-icons:database"),
                    color="white",
                    n_clicks=0
                ),
            ]),
        ]), 
        ),
    ]),
], style={'marginBottom':'0rem', 'paddingTop':'1rem', 'paddingBottom':'1rem', 'backgroundColor':'#F4F6F6'})

# 'backgroundColor':'#F8F9F9' : gris original
