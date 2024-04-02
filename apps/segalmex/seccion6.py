
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


##############################################################
#########                MAPA                         ########
##############################################################

####################  Barra de control derecha
sidebar_right = html.Div([
        # Filtros
        #dbc.Row([
            #html.Div([
                #dmc.Card([
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
                    # dmc.CardSection(
                    #     children=[
                    #         #dmc.Center(
                    #             dmc.SimpleGrid(cols=3, children=[
                    #                 dmc.Text('2020', id='anio_filtro1', size=12,weight=700, color="#4e203a", align="left"),
                    #                 dmc.Text(' - ', id='none', size=12, weight=700, color="#4e203a", align="center"),
                    #                 dmc.Text('ARROZ', id='producto_filtro1', weight=700, size="xl", color="#4e203a", align="left")
                    #             ], style={'margin':'0rem', 'padding':'0rem'}),
                    #         #),
                    #     ],
                    #     inheritPadding=False,
                    #     #pb="md",
                    #     style={'marginTop':'0rem', 'marginBottom':'0rem'}
                    # ),

                # ],
                # withBorder=True,
                # style={'backgroundColor':'#F4F6F6'}),

                
                #dmc.Text("Beneficiarios"),
                # dmc.Text("Seleccione la característica que desee visualizar", size="sm", color="gray"),
                #dmc.ChipGroup(
                #    [dmc.Chip(k, value=k) for k in list_bneficiarios_opciones],
                #    id='beneficiarios-opciones',
                #    multiple=False,
                #    value='Número de Beneficiarios'
                #),
                # dmc.RadioGroup(
                #         [dmc.Radio(k, value=k) for k in list_beneficiarios_opciones],
                #         id="beneficiarios-opciones",
                #         orientation="horizontal",
                #         #multiple=True,
                #         value="Número de Beneficiarios",
                #         #label="",
                #          mb=10,
                # ),

            #], className='mb-4 mt-2'),
            
            # capas y nivel de marginación
            # html.Div([
            #     dbc.Row([
            #         dbc.Col([
            #             dmc.Text("Seleccione la capa"),
            #             dmc.SegmentedControl(
            #             #dmc.ChipGroup(
            #             #    [dmc.Chip(k, value=k, variant='outline') for k in list_layers],
            #                 orientation="vertical",
            #                 fullWidth=True,
            #                 id='radio-centros',
            #                 data=list_layers,
            #                 color='#4E203A',
            #                 size='xs',
            #                 #multiple=False,
            #                 value='Centros de Acopio',
            #             ),
            #             #dmc.RadioGroup(
            #             #    [dmc.Radio(k, value=k) for k in list_layers],
            #             #    id="radio-centros",
            #             #    orientation="vertical",
            #             #    #multiple=True,
            #             #    value="Centros de acopio",
            #             #    #label="",
            #             #    size="sm",
            #             #    mt=5,
            #             #),
            #             #dmc.Text(id="radio-centros"),
            #         ], className='col-6 mb-2', style={'width': '50%'}),
            #         dbc.Col([
            #             #html.Div([
            #                 #dmc.Text("Nivel de Marginación"),
            #                 #dmc.MultiSelect(
            #                 #    id='grado_marginacion',
            #                 #    value= ['Muy bajo'],
            #                 #    data=list_grado_marginacion,
            #                     #color = '#4E203A',
            #                 #    clearable=True,
            #                 #    style={"width": 350}
            #                 #),
            #                 dmc.CheckboxGroup(
            #                     id="grado_marginacion",
            #                     label="Grado de marginación",
            #                     description="",
            #                     orientation="vertical",
            #                     #withAsterisk=True,
            #                     #offset="xs",
            #                     #gutter="xs",
            #                     #mb=0,
            #                     children=[
            #                         dmc.Checkbox(label="Muy bajo", value="Muy bajo", color="indigo"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Bajo", value="Bajo", color="blue"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Medio", value="Medio", color="green"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Alto", value="Alto", color="orange"),
            #                         #dmc.Space(h=0),
            #                         dmc.Checkbox(label="Muy alto", value="Muy alto", color="pink"),
            #                     ],
            #                     value=["Muy bajo", "Bajo","Medio","Alto","Muy alto"],
            #                 style={'height':'0rem', 'margin':'0rem', 'padding':'0rem'}),
            #                 #], className='mb-2'),
            #         ], className="col-6 mt-0", style={'marginBottom':'0rem', 'padding':'0rem'}),
            #     ]),

            # ], className='col-12'),
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
                    # dmc.Tooltip(
                    #     multiline=True,
                    #     width=150,
                    #     withArrow=True,
                    #     transition="fade",
                    #     position='left',
                    #     color='dark',
                    #     transitionDuration=300,
                    #     label="Muestra descripción general de la sección.",
                    #     children=[
                    #         dmc.Tab("Descripción",
                    #             icon=DashIconify(icon="carbon:license"),
                    #             value="descripcion",
                    #             style={'color':'#4e203a'}
                    #         )
                    # ], style={'fontSize':'12px'}),
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
            # card : criterios simulados
        #]),
        # tablero resumen
        # dmc.Card([
        #         #dmc.CardSection([
        #             dmc.SimpleGrid(cols=2,children=[
        #                 # card1 : centros de acopio
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'paddin':'0px','marginTop':'0em', 'marginBottom':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "1,332",
        #                             ], id='resumen-centros_acopio', style={'marginTop':'0em',"textAling":"center", "color":"red", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Centros Acopio", color='grey', weight=500, align='center', style={"fontSize": 10}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
        #                 # card2 : Beneficiarios
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image-poblacion_beneficiaria', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'margin':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "1,332",
        #                             ], id='resumen-poblacion_beneficiaria', style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Pob. Beneficiaria", id='resumen_texto_poblacion_beneficiaria', color='grey', weight=500, align='center', style={"fontSize": 11}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
        #                 # Card 3 : Monto de apoyos
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image', src='../assets/dollar.svg', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "1,332",
        #                             ], id='resumen-volumen_incentivado_total', style={'marginTop':'0em',"textAling":"center", "color":"green", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Vol. Incentivado (Total)", color='grey', weight=500, align='center', style={"fontSize": 11}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
        #                 # Card 4: Vol incentivado promedio
        #                 dmc.Card([
        #                     dbc.Row([
        #                         dbc.Col([
        #                             html.Img(id='image', src='../assets/porcentaje.png', width="65", height="65"),
        #                         ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
        #                         dbc.Col([
        #                             dbc.Row([html.Center(html.Div([
        #                             "51%",
        #                             ], id='resumen-volumen_incentivado_promedio', style={'marginTop':'0em',"textAling":"center", "color":"grey", 'font-size': '32px'}),
        #                             )]),
        #                             dbc.Row([html.Div([
        #                                 dmc.Text("Vol. Incentivado (Prom)", color='gray', weight=500, align='center', style={"fontSize": 11}),
        #                                 ]),
        #                             ]),
        #                         ], className="card col-9 border-0 bg-transparent"),
        #                     ], style={'border-radius': '5px', 'paddin':'0rem'}),
        #                 ],
        #                 withBorder=True,
        #                 shadow="sm",
        #                 radius="md",
        #                 style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},)
        #             ],
        #             style={"width": 360, "height": 160}
        #             ),
        #         # ],
        #         # inheritPadding=False,
        #         # mt="sm",
        #         # pb="md",),

        # ], style={'marginLeft':'0rem', 'paddingLeft':'0rem'}),

        # dbc.Row([
        #     #primero
        #     dbc.Col([
        #         #html.Div([
        #         dbc.Row([
        #             dbc.Col([
        #                 html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
        #             ],className="card col-3 border-0 bg-transparent", style={'paddin':'0px','marginTop':'0em', 'marginBottom':'0em', 'textAlign': 'left'}),
        #             dbc.Col([
        #                 dbc.Row([html.Center(html.Div([
        #                 "1,332",
        #                 ], id='resumen-centros_acopio', style={'marginTop':'0em',"textAling":"center", "color":"red", 'font-size': '32px'}),
        #                 )]),
        #                 dbc.Row([html.Div([
        #                     dmc.Text("Centros Acopio", color='grey', weight=500, align='center', style={"fontSize": 10}),
        #                     ]),
        #                 ]),
        #             ], className="card col-9 border-0 bg-transparent"),
        #         ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
        #     ],className=" card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),
        #     # segundo
        #     dbc.Col([
        #         dbc.Row([
        #             dbc.Col([
        #                 html.Img(id='image', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
        #             ],className="card col-3 border-0 bg-transparent", style={'margin':'0em', 'textAlign': 'left'}),
        #             dbc.Col([
        #                 dbc.Row([html.Center(html.Div([
        #                 "1,332",
        #                 ], id='resumen-poblacion_beneficiaria', style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
        #                 )]),
        #                 dbc.Row([html.Div([
        #                     dmc.Text("Pob. Beneficiaria", color='grey', weight=500, align='center', style={"fontSize": 11}),
        #                     ]),
        #                 ]),
        #             ], className="card col-9 border-0 bg-transparent"),
        #           ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
        #     ],className="card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),

        # ], style={'marginTop':'1rem'}),


        # Row three
    #     dbc.Row([
    #     #primero
    #         dbc.Col([
    #             dbc.Row([
    #                 dbc.Col([
    #                     html.Img(id='image', src='../assets/dollar.svg', width="65", height="65"),
    #                 ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
    #                 dbc.Col([
    #                     dbc.Row([html.Center(html.Div([
    #                     "1,332",
    #                     ], id='resumen-volumen_incentivado_total', style={'marginTop':'0em',"textAling":"center", "color":"green", 'font-size': '32px'}),
    #                     )]),
    #                     dbc.Row([html.Div([
    #                         dmc.Text("Vol. Incentivado (Total)", color='grey', weight=500, align='center', style={"fontSize": 11}),
    #                         ]),
    #                     ]),
    #                 ], className="card col-9 border-0 bg-transparent"),
    #             ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
    #         ],className="card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),
    #    # segundo
    #         dbc.Col([
    #             dbc.Row([
    #                 dbc.Col([
    #                     html.Img(id='image', src='../assets/porcentaje.png', width="65", height="65"),
    #                 ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
    #                 dbc.Col([
    #                     dbc.Row([html.Center(html.Div([
    #                     "51%",
    #                     ], id='resumen-volumen_incentivado_promedio', style={'marginTop':'0em',"textAling":"center", "color":"grey", 'font-size': '32px'}),
    #                     )]),
    #                     dbc.Row([html.Div([
    #                         dmc.Text("Vol. Incentivado (Prom)", color='gray', weight=500, align='center', style={"fontSize": 11}),
    #                         ]),
    #                     ]),
    #                 ], className="card col-9 border-0 bg-transparent"),
    #             ], style={'border-radius': '5px', 'backgroundColor': '#F4F6F6', 'paddin':'0rem'}),
    #         ],className="card col-12 col-md-6", style={'border-radius': '5px', 'backgroundColor': '#7c90ab', 'paddingLeft':'0.9rem', 'paddinRight':'1rem' }),

    #     ], style={'marginTop':'1rem', 'marginBottom':'1rem'}),

        ], style={'paddingLeft':'2rem', 'paddingRight':'2rem', 'marginTop':'0.5rem'}
    )


##################     Mapa interactivo ##############
seccion6 = html.Div([
        dbc.Row([
            dbc.Col([
                    html.Div([
                        #dbc.Tabs([
                        #        dbc.Tab(label="Mapa", tab_id="tab-1", label_style={"backgroundColor":"#2a3240","color": "white"}),
                        #
                        #        #dbc.Tab(label="Tabla", tab_id="tab-2",  label_style={"color": "#00AEF9"}),
                        #    ],
                        #    id="tabs-mapa",
                        #    active_tab="tab-1",
                        #    style={'backgroundColor':'#BFC9CA', 'padding':'.0rem'},
                        #),
                        #dl.Map(id="mapa1"),
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