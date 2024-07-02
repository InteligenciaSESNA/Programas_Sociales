
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


# las siguiente listas son los años y productos que tenemos disponibles, en caso de que haya
# otro solo se agrega en las listas.

list_year = ['2019','2020','2021','2022']
list_products = ['Arroz', 'Frijol', 'Leche', 'Maíz', 'Trigo']



#########################################################################################
#                              Filtros principales                                      #
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
seccion4 = html.Div([
    dbc.Row([
        # Primera columna : Vacia
        dbc.Col([
            dmc.Button(   # Esta sección agrega un botón llamado "Instrucciones" el cual te da descripciones de algunas funcionalidades importantes del mapa
                    "Instrucciones: ",
                    id="transition-instrucciones-btn",  # id del boton
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
                id="transition-instrucciones",
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
                        dmc.Tooltip(   # Esta seccion de Tootlip es para los pequeños nombre que aparecen un poco arriba de los filtros
                            multiline=True,
                            width=200,
                            withArrow=True,
                            transition="fade",
                            position='right',
                            transitionDuration=300,
                            label="Seleccione un año fiscal",
                            children=["Seleccione el año"],
                            ),
                        id="anio",   # Aqui se coloca el id del filtro que en este caso es el año, que se va a seleccionar
                        data=list_year,
                        value='2020', # Este año lo va a mostrar por default
                        searchable=True,
                        nothingFound="No options found",
                        style={"textAlign": "Left"}
                    ),
                ]),
                # Esta columna es para el filtro de selccionar el producto, sigue la misma lógica con el botón de año
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
                        id="producto",
                        data=list_products,
                        value='Maíz',
                        searchable=True,
                        nothingFound="No options found",
                        style={"textAlign": "left"},
                    ),
                ]),
            ], style={'marginBottom':'3rem','paddingBottom':'2rem', 'paddingRight':'1rem', 'paddingLeft':'1rem'}),
            
            # Esta pequeña seccion es para poder definir el botón de "actualizar" esto para refrescar los datos por filtros seleccionados
            dbc.Col([
                html.Center(
                    dbc.Row([
                        dbc.Col([
                            dmc.Button(
                                'Actualizar',
                                id='submit-button',   # Id del bóton actualizar
                                n_clicks=0,
                                #children='Actualizar',
                                color = 'dark'
                            ),
                        ]),
                    ]),
                ),
            ]),
        ], className='col-xl-4 col-12',  style={'marginBottom':'4rem', 'paddingTop':'5rem'}),

        # Para la descarga de un resumen ejecutivo, ### pero no funciona, por ahora ###

        dbc.Col([
            dmc.Center(
                dbc.Row([
                # dmc.Button("Resumen Ejecutivo",
                #                 id="open",
                #                 leftIcon=DashIconify(icon="ant-design:read-outlined"),
                #                 color="blue",
                #                 n_clicks=0),
                # dbc.Button(
                #         "Resumen Ejecutivo",
                #         #href= "/Proyecto.pdf",
                #         download="Proyecto.pdf",
                #         external_link=False,
                #         color="red",
                #         id="btn",
                #     ),
                            
                    #     label="Click para descargar el resumen",
                    #     openDelay=500,
                    # ),
                    dcc.Download(id="download"), 
                ], className='col-xl-6 col-8', style={'marginBottom':'0rem'}),
            ),
              
            
        ], className='col-xl-4 col-12', style={'marginBottom':'0rem'}),
        
        ######### La siguiente parte es para agregar las reglas de operación para cada año y producto ###########
        dmc.Center(
        dmc.Group([   
            html.Div([
                 #dmc.Anchor(
                    dmc.Button("Carac. Prog. Sociales",
                            id="open",
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
                                ], id='reglas-operacion', style={'paddingLeft':'2.5rem', 'paddingRight':'2.5rem'})
                            , style={'backgroundColor':'#2a3240'}),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Cerrar", id="close", className="ms-auto", outline=False, color="dark", n_clicks=0
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

            # Esta sección es para agregar el botón de descarga de los datos, ##pero este no funciona por ahora##

            dmc.Divider(orientation="vertical", style={"height": 30}),
            html.Div([
                #dmc.Anchor(
                    dmc.Button("Descarga xlsx",
                            id="dowload_xlsx",
                            variant="subtle",
                            leftIcon=DashIconify(icon="eos-icons:database"),
                            color="white",
                            n_clicks=0) , #href='#'),
                    dcc.Download(id="download-db-xlsx"),
            ], style={'display': 'inline-block'}),
            dmc.Divider(orientation="vertical", style={"height": 30}),
            html.Div([
                dmc.Button(
                    "...",
                    id="fade-transition-button",
                    variant="subtle",
                    #leftIcon=DashIconify(icon="eos-icons:database"),
                    color="white",
                    n_clicks=0
                ),
            ]),
        ]), 
        ),
    ]),
], style={'marginBottom':'0rem', 'paddingTop':'1rem', 'paddingBottom':'1rem', 'backgroundColor':'#F8F9F9'})
