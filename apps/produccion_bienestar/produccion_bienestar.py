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
import math
from dash import dash_table as dt
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_extensions as de
import dash_extensions
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
import mysql.connector
# import root
from path import root
# propiedades del mapa
from graficos.produccion_bienestar.mapa_settings import classes, colorscale, colorbar, style0, style, style2, ctg, style_handle
from graficos.produccion_bienestar.mapa_settings import get_info, get_info2
from graficos.produccion_bienestar.mapa_settings import info, info_escenarios_marginacion, info_num_benef, info_grado_marginacion, info_productores, info_vol_prod
# gráficos
from graficos.produccion_bienestar.chart1 import mapa1
#from graficos.produccion_bienestar.chart2 import barplot1
# secciones del visualizador
from apps.produccion_bienestar import reglas_operacion
from apps.produccion_bienestar.seccion1 import seccion1
from apps.produccion_bienestar.seccion2 import seccion2
from apps.produccion_bienestar.seccion3 import seccion3
from apps.produccion_bienestar.seccion4 import seccion4
from apps.produccion_bienestar.seccion5 import seccion5
from apps.produccion_bienestar.seccion6 import seccion6
# importa modulos de seccion 7
from apps.produccion_bienestar.seccion7 import get_card_poblacion_indigena
from apps.produccion_bienestar.seccion7 import get_card_poblacion_beneficiaria_img
from apps.produccion_bienestar.seccion7 import get_card_poblacion_beneficiaria_texto
from apps.produccion_bienestar.seccion7 import get_card_poblacion_beneficiaria
from apps.produccion_bienestar.seccion7 import get_card_poblacion_mujeres
from apps.produccion_bienestar.seccion7 import get_card_monto_promedio





data2 = json.load(open(root +'/datasets/geoVolProd.json'))

# base lista de url's de todos los estados
estados_urls = pd.read_excel(root + '/datasets/estados.xlsx', converters={'cve_ent':str})
# base de beneficiarios por entidad
base_beneficiarios_ent_tprod = pd.read_excel(root + '/datasets/beneficiarios_ent.xlsx', converters={'cve_ent':str})
base_beneficiarios_ent_tprod['tipo'] = [val.strip() for val in base_beneficiarios_ent_tprod['tipo']]
# base de beneficiarios por municipios
base_beneficiarios_mun_tprod = pd.read_excel(root + '/datasets/produccion_bienestar_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str, 'year':int})
base_beneficiarios_mun_tprod['latitud'] = base_beneficiarios_mun_tprod['latitud'].astype('float')
base_beneficiarios_mun_tprod = base_beneficiarios_mun_tprod[base_beneficiarios_mun_tprod['latitud']>=0]
base_beneficiarios_mun_tprod = base_beneficiarios_mun_tprod[~base_beneficiarios_mun_tprod['latitud'].isna()]
# base centros de acopio por entidad
base_centros_ent = pd.read_excel(root + '/datasets/centros_acopio_entidad.xlsx', converters={'cve_ent':str, 'cve_mun':str})
base_centros = pd.read_excel(root + '/datasets/centros_acopio.xlsx', converters={'cve_ent':str, 'cve_mun':str, 'cve_loc':str, 'latitud':float, 'longitud':float})
base_centros = base_centros[~base_centros['cve_ent'].isna()]
base_centros = base_centros[~base_centros['cve_mun'].isna()]
base_centros = base_centros[~base_centros['cve_loc'].isna()]
base_centros = base_centros[~base_centros['latitud'].isna()]
base_centros = base_centros[~base_centros['longitud'].isna()]
# base de productores 
base_productores = pd.read_excel(root + '/datasets/productores_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str})
# base resumen de montos
base_resumen = pd.read_excel(root + '/datasets/resumen_montos.xlsx')




# Opciones
list_year = ['2019', '2020', '2021', '2022', '2023']
list_products = ['Ajonjoli grano', 'Amaranto', 'Arroz', 'Arvejon grano',
                'Avena grano', 'Cacahuate', 'Cacao', 'Cafe',
                'Calabaza chihua (pipian)', 'Caña de azucar', 'Cartamo grano',
                'Cebada grano', 'Chia', 'Colza o canola', 'Frijol',
                'Garbanzo grano', 'Girasol grano', 'Haba grano', 'Lenteja',
                'Linaza', 'Maiz grano', 'Nopal', 'Sorgo grano', 'Soya grano',
                'Trigo grano', 'Miel abeja', 'Milpa']
list_grado_marginacion = [['Muy bajo', 'blue'],
                          ['Bajo','indigo'],
                          ['Medio', 'green'],
                          ['Alto', 'red'],
                          ['Muy alto', 'orange',
                           'No disponible', 'yellow']]

list_tamano_productor = ['Pequeño', 'Mediano']
list_states = base_beneficiarios_ent_tprod['cve_ent'].unique()
list_layers = ['Centros de Acopio','Volumen Producción','Productores','All']
list_beneficiarios_opciones = ['Monto del Apoyo', 'Número de Beneficiarios']

list_capas_marginacion = initial_values = [
    [   # capas
        #{"value": "Beneficiarios", "label": "Beneficiarios", "group": "Capa"},
        #{"value": "Centros de Acopio", "label": "Centros de Acopio", "group": "Capa"},
        {"value": "Volumen Producción", "label": "Volumen Producción", "group": "Capa"},
        
    ],
    [
        {"value": "Beneficiarios", "label": "Beneficiarios", "group": "Capa"},
        # Grado de marginación
        {"value": "Muy bajo", "label": "Muy bajo", "group": "Grado Marginación"},
        {"value": "Bajo", "label": "Bajo", "group": "Grado Marginación"},
        {"value": "Medio", "label": "Medio", "group": "Grado Marginación"},
        {"value": "Alto", "label": "Alto", "group": "Grado Marginación"},
        {"value": "Muy alto", "label": "Muy alto", "group": "Grado Marginación"},
        {"value": "No disponible", "label": "No disponible", "group": "Grado Marginación"},
        # Población índigena
        {"value": "A", "label": "A", "group": "Población Indigena"},
        {"value": "B", "label": "B", "group": "Población Indigena"},
        {"value": "No aplica", "label": "No aplica", "group": "Población Indigena"},
        # sexo
        {"value": "H", "label": "H", "group": "Sexo"},
        {"value": "M", "label": "M", "group": "Sexo"},
    ],
]

list_criterios = ['Marginación', 'Precio']


# backgroundColor': '#F4F6F6'
# original 'backgroundColor': '#f2f2f2'
########################### layout  SEGALMEX
layout = dbc.Container([
        #  header
        seccion1,
        # Introduccion
        seccion4,
        # Mapa
        seccion6,
        #### SECCIÓN : GRAFICOS
        dbc.Row([
            dbc.Col([
                html.Br(),
                html.Br(),
            ]),
        ]),

    ], className="twelve columns", style={'backgroundColor': 'white', 'marginTop': '0rem', 'padding':'0rem'},
    fluid=True
    )
    # #EBF5FB
    # #F4F6F6
#########################################################################################
############################            Call backs         ##############################
#########################################################################################

#########      CARD 1 : Regresa estado  ################
@app.callback(# 'click_feature
        Output('state01', 'children'),
        Input("states", "click_feature")
    )
def get_state(clicks, feature):

    # condición
    if not feature:
        state = 'Nacional'
    else:
        # filtro de estado
        state = feature["properties"]["name"]

    return state
#########      CALL : Regresa año  ################
@app.callback(# 'click_feature
        Output('prod_anio_filtro1', 'children'),
        Output('prod_producto_filtro1', 'children'),
        Input('prod_submit-button', 'n_clicks'),
        State('prod_producto', 'value'),
        State('prod_anio', 'value'),
    )

def anio(clicks, sel_producto, sel_anio):


    return sel_anio, sel_producto

#########      CALL : Regresa producto  ################
@app.callback(# 'click_feat
        Output('prod_anio_filtro2', 'children'),
        Output('prod_producto_filtro2', 'children'),
        Input('prod_submit-button', 'n_clicks'),
        State('prod_producto', 'value'),
        State('prod_anio', 'value'),
    )
def producto(clicks, sel_producto, sel_anio):

    return sel_anio, sel_producto #, sel_producto

#########   CALL : Modal Reglas de operación  ################
@app.callback(
    Output("prod_modal", "is_open"),
    [Input("prod_open", "n_clicks"),
     Input("prod_close", "n_clicks")],
    [State("prod_modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#########  CALL : Resumen Reglas de operación ################
@app.callback(
        Output('prod_reglas-operacion', 'children'),
        Input('prod_submit-button', 'n_clicks'),
        State('prod_producto', 'value'),
        State('prod_anio', 'value'),
    )

def summary_reglas_operacion(clicks, producto_sel, anio_sel):

    result = reglas_operacion.resumen_reglas_operacion(anio_sel, producto_sel)
    
    return result



#########  Fade transsition : instrucciones
@app.callback(
    Output("prod_transition-instrucciones", "is_in"),
    [Input("prod_transition-instrucciones-btn", "n_clicks")],
    [State("prod_transition-instrucciones", "is_in")],
    #prevent_initial_call=True,
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in


################################################################
#  Cnetros de acopio
get_card_poblacion_indigena(app)
get_card_poblacion_beneficiaria_img(app)
get_card_poblacion_beneficiaria_texto(app)
get_card_poblacion_beneficiaria(app)
get_card_poblacion_mujeres(app)
get_card_monto_promedio(app)



##########################################################################################
#                           SECCIÓN I :  mapa
##########################################################################################
#########       CALL : Transfer list  ################

# opción Capas
tab1_capas_criterios = html.Div([
    dmc.Text("Seleccione la característica que desee visualizar", size=11, color="gray"),
    dmc.RadioGroup(
            [dmc.Radio(k, value=k) for k in list_beneficiarios_opciones],
            id="prod_beneficiarios-opciones",
            orientation="horizontal",
            #multiple=True,
            value="Número de Beneficiarios",
            #label="",
            style={'marginBottom':'1rem'}
    ),
    dmc.Text("Seleccione Capas y Grado de Marginación que desee visualizar", size=11, color="gray", style={'marginBottom':'1rem'}),
    dmc.TransferList(
        id="prod_transfer-list-simple",
        value=list_capas_marginacion,
        #sx={'height':'14rem'},
        searchPlaceholder=['Agregar...', 'Remover...'],
        nothingFound=['Cannot find item to add', 'Cannot find item to remove'],
        placeholder=['No item left to add', 'No item left ro remove'],
        style={'fontSize':'10px','marginBottom':'2rem'}
    ),
    ############### Tablero resumen
    dmc.Center([
        dmc.Card([
            dmc.SimpleGrid(cols=2,
                breakpoints=[
                    {"minWidth": 350, "maxWidth": 400, "cols": 1, "spacing": "md"},
                    {"minWidth": 350, "maxWidth": 400, "cols": 2, "spacing": "md"},
                ],children=[
                # card1 : centros de acopio
                dmc.Tooltip(
                        multiline=True,
                        width=200,
                        withArrow=True,
                        transition="fade",
                        position='bottom',
                        color='dark',
                        transitionDuration=300,
                        label="Centros de acopio: canales establecidos en el programa para la entrega de los productos a cambio del incentivo.",
                        children=[
                            dmc.Card([
                                dbc.Row([
                                    dbc.Col([ # col-sm-12 col-md-6
                                        html.Img(src='../assets/logos/pobIndigena.png',  width="63", height="65"),
                                    ],className="card col-lg-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem', 'marginTop':'0rem', 'marginBottom':'0rem', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='prod_resumen-poblacion-indigena', style={'marginTop':'0em','text-align': 'center', "color":"red", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Población Indigena", color='grey', weight=500, align='center', style={"fontSize": 10})
                                            ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'padding':'0rem', 'paddingLeft':'0.2rem'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": "100%", "margin":"0rem" ,"padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                ], style={'fontSize':'12px'}),
                # card2 : Beneficiarios
                dmc.Tooltip(
                        multiline=True,
                        width=200,
                        withArrow=True,
                        transition="fade",
                        color='dark',
                        position='bottom',
                        transitionDuration=300,
                        label="Población beneficiaria: personas que han recibido el incentivo del programa.",
                        children=[
                            dmc.Card([
                                dbc.Row([
                                    dbc.Col([ # col-sm-12 col-md-6
                                        html.Img(id='prod_image-poblacion_beneficiaria', src='../assets/poblacionBeneficiaria.png', width="63", height="65"),
                                    ],className="card col-lg-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem', 'marginTop':'0rem', 'marginBottom':'0rem', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='prod_resumen-poblacion_beneficiaria', style={'marginTop':'0em','text-align': 'center', "color":"blue", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Población Beneficiaria", id="prod_resumen_texto_poblacion_beneficiaria" , color='grey', weight=500, align='center', style={"fontSize": 10})
                                            ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'padding':'0rem', 'paddingLeft':'0.2rem'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": "100%", "margin":'0rem', "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                ], style={'fontSize':'12px'}),
                
                # Card 4: Vol incentivado promedio
                dmc.Tooltip(
                        multiline=True,
                        width=200,
                        withArrow=True,
                        transition="fade",
                        position='top',
                        color='dark',
                        transitionDuration=300,
                        label="Volumen incentivado promedio: Volumen de producción promedio (En toneladas, excepto leche en litros).",
                        children=[
                            dmc.Card([
                                dbc.Row([
                                    dbc.Col([
                                             DashIconify(icon="twemoji:women-holding-hands-light-skin-tone-dark-skin-tone", width=65, height=60),
                                    ],className="card col-lg-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem', 'marginTop':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "51%",
                                        ], id='prod_resumen-poblacion-mujeres', style={'padding':'0em',"textAling":"right", "color":"grey", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Población Benef. Mujeres", color='gray', weight=500, align='center', style={"fontSize": 10, 'text-align': 'center', 'paddingRight':'0rem'}),
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem', 'width':'100%'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": "100%", "padding":'0rem', 'backgroundColor': '#F4F6F6'},)
                ], style={'fontSize':'10px'}),
                # Card 3 : Monto de apoyos
                dmc.Tooltip(
                        multiline=False,
                        width=200,
                        withArrow=True,
                        transition="fade",
                        position='top',
                        color='dark',
                        transitionDuration=300,
                        label="Volumen incentivado total: Volumen de producción total incentivado (En toneladas, excepto leche en litros).",
                        children=[
                            dmc.Card([
                                dbc.Row([
                                    dbc.Col([
                                        DashIconify(icon="emojione:money-bag", width=65, height=60),
                                    ],className="card col-lg-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem','marginTop':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='prod_resumen-monto-promedio', style={'paddingRight':'0rem','text-align': 'center', "color":"green", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Monto total Promedio", color='grey', weight=500, align='center', style={"fontSize": 10, 'paddingRight':'0rem'}),
                                            
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem', 'width':'100%'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": "100%", "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                ], style={'fontSize':'10px'}),
            ]),
        ], style={'margin':'0rem', 'padding':'0rem'}),
    ]),
])

#  Pestaña de opciones (Transfer list - Criterios simulados)
tab2_capas_criterios = html.Div([
    dmc.Card([
        dmc.SimpleGrid(cols=2, children=[
            
            # selector criterios simulados
            dmc.Select(
                label='Escenarios',
                id='prod_criterios1',
                searchable=True,
                dropdownPosition='bottom',
                value= 'Marginación',
                data=list_criterios,
                nothingFound="No options found",
                style={"width": '100%'}
            ),
        ], style={'marginBottom':'8rem'}),
        
    ], style={'padding':'0rem', 'marginBottom':'2rem'}),
    
    
])

######### CALL : Download PDF  ################
# @app.callback(Output("download", "data"),
#               Input("btn_metodo_pdf", "n_clicks"),
#               prevent_initial_call=True)
# def func(n_clicks):
#     return dcc.send_file("C:/Users/jcmartinez/Desktop/Dashboard3/Proyecto.pdf")

########    Download xlsx
# @app.callback(
#     Output("download-db-xlsx", "data"),
#     Input("dowload_xlsx", "n_clicks"),
#     State('producto', 'value'),
#     State('anio', 'value'),
#     prevent_initial_call=True,
# )
# def download_xlsx(click_db, producto_sel, anio_sel):
#     base2019 = base_2019.copy()
#     base2020 = base_2020.copy()
#     base2021 = base_2021.copy()
#     if anio_sel == '2019':
#         base = base2019[base2019['Producto']==producto_sel]
#     elif anio_sel == '2020':
#         base = base2020[base2020['Producto']==producto_sel]
#     elif anio_sel == '2021':
#         base = base2021[base2021['Producto']==producto_sel]
    
#     return dcc.send_data_frame(base.to_excel, f"{anio_sel}-{producto_sel}.xlsx", sheet_name=f"{anio_sel}-{producto_sel}")

#########  CALL : Regresa opciones capas / criterios  ################
@app.callback(Output("prod_content-capas-criterios", "children"),
              Output("prod_mapa", "children"),
             [Input("prod_capas-criterios", "value")],
             #prevent_initial_call=True,
            )
            
def switch_tab(active):
    if active == "capas": # dmc.Loader(color="red", size="md", variant="oval")
        return tab1_capas_criterios,  dcc.Loading(id="prod_ls-loading-1",children=content_mapa1, type="default")
    elif active == "criterios":
        return tab2_capas_criterios, dcc.Loading(id="prod_ls-loading-2",children=content_mapa2, type="default") #content_mapa2
    return html.P("This shouldn't ever be displayed...")

#########  CALL : Regresa actualización del MAPA  ################
# declaración de parámetros para color y leyendas

@app.callback(Output("prod_ls-loading-output-1", "children"), 
              Input("prod_ls-input-1", "value"),
              #prevent_initial_call=True,
   )
def input_triggers_spinner(value):
    time.sleep(2)
    return value

@app.callback(Output("prod_ls-loading-output-2", "children"), 
              Input("prod_ls-input-2", "value"),
             # prevent_initial_call=True,
    )
def input_triggers_nested(value):
    time.sleep(1)
    return value

####   actualiza tabla-Mapa
#########    CALL : Indicador estado (MAPA)  ################
@app.callback(# 'click_feature
        Output('prod_state_label', 'children'),
        Input("prod_states", "click_feature"),
        #prevent_initial_call=True,
    )
def get_state(clicks, feature):

    # condición
    if not feature:
        return [
            html.H4("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='prod_image', src='../assets/'+ str("Nacional") +'.png', width="65", height="65")),
          ]
    else:
        # filtro de estado
        state = feature["properties"]["name"]
        urls_est = str(estados_urls[estados_urls['nom_ent']==state]['Liga'].to_list()[0])
    
        return [
            html.H4("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='prod_image', src='../assets/'+ str(feature["properties"]["name"]) +'.png', width="65", height="65")),
          ]

# actualiza infor en mapa
@app.callback(Output("prod_info", "children"),
              Input("prod_states", "click_feature"),
        )

def info_hover(feature):
    return get_info(feature)

###########################################################################
###                             Gráficos 
###########################################################################    


# Contenido por mapa
content_mapa1 = html.Div(dl.Map(center=[22.76, -102.58], zoom=5,
             id="prod_mapa1", attributionControl=False,  style={'width': '100%', 'height': '100vh', 'backgroundColor':'white', 'margin': "auto", "display": "block"}),
)


content_mapa2 = html.Div(dl.Map(center=[22.76, -102.58], zoom=5,
             id="prod_mapa2", attributionControl=False,  style={'width': '100%', 'height': '100vh', 'backgroundColor':'white', 'margin': "auto", "display": "block"}),
)


##   CALLBACK : MAPA
@app.callback(
        Output('prod_mapa1', 'children'),
        Input('prod_submit-button', 'n_clicks'),
        Input("prod_beneficiarios-opciones", "value"),
        Input("prod_transfer-list-simple", "value"),
        State('prod_producto', 'value'),
        State('prod_anio', 'value'),
    )

def actualizar_mapa1(clicks, benef_sel, transfer_sel, producto_sel, anio_sel):
    
    # capas
    capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
    margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
    # genero del beneficiario
    sexo_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Sexo']
    # tipo de pobalción
    tipo_poblacion = [item['label'] for item in transfer_sel[1] if item['group']=='Población Indigena']
    
    # Productores
    productores_filter = base_productores.copy()
    # filtro por productores > 0
    productores_filter = productores_filter[productores_filter['productores']>0]
    productores_filter = productores_filter[productores_filter['latitud']>0]
    productores_filter = productores_filter.dropna(subset='entidad', axis=0)
    # filtro por cultivo
    productores_filter = productores_filter[productores_filter['cultivo']==producto_sel]
    #productores_filter = productores_filter[productores_filter['year']==int(anio_sel)]
    productores_filter = productores_filter[productores_filter['gm'].isin(margin)]
    
    # Filtro centros de acopio
    centros = base_centros.copy()
    centros['year'] = centros['year'].astype('int')
    centros = centros[centros['gm'].isin(margin)]
    centros = centros[centros['year']==int(anio_sel)]
    
    # Beneficiarios
    benef_filter = base_beneficiarios_mun_tprod.copy()
    benef_filter = benef_filter[benef_filter['cultivo'] == producto_sel]
    benef_filter = benef_filter[benef_filter['year'] == int(anio_sel)]
    benef_filter = benef_filter[benef_filter['gm'].isin(margin)]
    benef_filter = benef_filter[benef_filter['sexo'].isin(sexo_sel)]
    benef_filter = benef_filter[benef_filter['tipo'].isin(tipo_poblacion)]
    
    return mapa1(clicks, benef_sel, transfer_sel, producto_sel, anio_sel, capas_sel, productores_filter, centros, benef_filter)


 # capa base
capa_base = dl.Pane(dl.GeoJSON(data=data2,  # url to geojson file
                        options=dict(style=style_handle),  # how to style each polygon
                        zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                        zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
                        hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2), #2e4053
                        hoverStyle=arrow_function(dict(weight=4, fillColor='#000066', color='#000066',opacity=0.1, fillOpacity=1, dashArray='1')),  # style applied on hover
                        id='prod_states'), name="base2", style={'zIndex':0}) 
    
######### Mapa criterios simulados   ################
##   CALLBACK : MAPA
@app.callback(  
        Output('prod_mapa2', 'children'),
        Input('prod_submit-button', 'n_clicks'),
        Input('prod_criterios1', 'value'),
        State('prod_producto', 'value'),
        State('prod_anio', 'value'),
    )

def actualizar_mapa2(clicks, criterios_sel, producto_sel, anio_sel):
    
    # capas
    productores_filter = base_productores.copy()
    # filtro por productores > 0
    productores_filter = productores_filter[productores_filter['productores']>0]
    #productores_filter = productores_filter[productores_filter['latitud']>0]
    productores_filter = productores_filter.dropna(subset='entidad', axis=0)
    # filtro por cultivo
    productores_filter = productores_filter[productores_filter['cultivo']==producto_sel]

    # base beneficiarios
    benef_filter = base_beneficiarios_mun_tprod.copy()
    benef_filter = benef_filter[benef_filter['cultivo'] == producto_sel]
    benef_filter = benef_filter[benef_filter['year'] == int(anio_sel)]
    benef_filter.dropna(subset = ['latitud', 'longitud'], inplace=True)

    # Beneficiarios 
    def beneficiarios_popup(ent, mun, gmargina, numbenef, monto):
        
            result = html.Div([
                html.Div([
                    html.Img(id='prod_image-poblacion_beneficiaria2', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
                    dmc.Text('BENEFICIARIO(S)', weight=400,color='#4e203a'),
                ], style={'textAlign': 'center'}),
                
                dmc.Divider(size="xs"),
                dbc.Row([
                    dmc.Text(['Estado: ',ent]),
                    dmc.Text(['Municipio: ', mun]),
                    dmc.Space(h=4),
                    dmc.Text(['Grado de marginación: ', gmargina]),
                    dmc.Text(['No. Beneficiarios: ', numbenef]),
                    dmc.Text(['Monto total del apoyo: ', f'$ {prettify(monto)}']),
                ])
                
                ])
            return result 
    
    # Total productores 
    def productores_popup(ent, mun,gmargina,numprod):
        
            result = html.Div([
                html.Div([
                    DashIconify(icon="noto-v1:man-farmer", width=65, height=65),
                    #html.Img(id='image-centros-acopio2', src='../assets/centrosAcopio.png', width="65", height="65"),
                    dmc.Text('PRODUCTORES', weight=400, color='#4e203a'),
                ], style={'textAlign': 'center'}),
                
                dmc.Divider(size="xs"),
                dbc.Row([
                    dmc.Text(['Estado: ',ent]),
                    dmc.Text(['Municipio: ', mun]),
                    dmc.Space(h=4),
                    dmc.Text(['Grado de marginación: ', gmargina]),
                    dmc.Text(['No. Productores: ', prettify(numprod)]),

                ])
                
                ])
            return result

    # ópción para agregar beneficarios observados
    beneficiarios = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=radio,fillOpacity=0, color="blue", children=[
                #dl.Popup("Municipio: {}".format(mun))
                dl.Tooltip(f"Beneficiario(s): {mun}-{ent}"),
                dl.Popup(beneficiarios_popup(ent, mun, gmargina, numbenef, monto))
                ]) for ent, mun, lat, lon, radio, color, gmargina, numbenef, monto in zip(benef_filter['entidad'], benef_filter['municipio'], benef_filter['latitud'], benef_filter['longitud'], benef_filter['benef_total_radio'], benef_filter['gm_color'], benef_filter['gm'], benef_filter['benef_total'], benef_filter['monto_total'])]), name='Beneficiarios', checked=True)

    # opción para agregar criterio del precio y marginación 
    if criterios_sel == 'Marginación':
        productores_filter = productores_filter[productores_filter['escenario_marginacion']>0]
    else:
        productores_filter = productores_filter[productores_filter['escenario_precio']>0]
    
    # Productores
    productores = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=np.log(numprod), color='#E12726', children=[
        dl.Tooltip(f"Productores: {mun}-{ent}"),
        dl.Popup(productores_popup(ent,mun,gmargina,numprod))
        ]) for lat, lon, ent, mun, gmargina, numprod in zip(productores_filter['latitud'],productores_filter['longitud'], productores_filter['cve_ent'], productores_filter['cve_mun'], productores_filter['gm'], productores_filter['productores'])]), name='Productores', checked=True)

    # capas por defecto
    capas = []
    # se agregan capas
    capas.extend([
                #dl.FullscreenControl(),
                info,
                capa_base,
                beneficiarios,
                productores
                ])   
    # mapa
    tab2_mapa_content = html.Div([
        dl.Map(center=[22.76, -102.58], zoom=5,
               children=dl.LayersControl(capas, position='bottomright')
               , attributionControl=False, style={'width': '100%', 'height': '100vh','backgroundColor':'white', 'margin': "auto", "display": "block"}),
        ])
    
    return tab2_mapa_content


