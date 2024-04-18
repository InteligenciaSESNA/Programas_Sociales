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
import mysql.connector
# import root
from path import root
# propiedades del mapa
from graficos.segalmex.mapa_settings import classes, colorscale, colorbar, style0, style, style2, ctg, style_handle
from graficos.segalmex.mapa_settings import get_info, get_info2
from graficos.segalmex.mapa_settings import info, info_escenarios_marginacion, info_num_benef, info_grado_marginacion, info_productores, info_vol_prod
# gráficos
from graficos.segalmex.chart1 import mapa1
from graficos.segalmex.chart2 import barplot1
# secciones del visualizador
from apps.segalmex3 import reglas_operacion
from apps.segalmex3.seccion1 import seccion1
from apps.segalmex3.seccion2 import seccion2
from apps.segalmex3.seccion3 import seccion3
from apps.segalmex3.seccion4 import seccion4
from apps.segalmex3.seccion5 import seccion5
from apps.segalmex3.seccion6 import seccion6
# importa modulos de seccion 7
from apps.segalmex3.seccion7 import get_card_centros_acopio
from apps.segalmex3.seccion7 import get_card_poblacion_beneficiaria_img
from apps.segalmex3.seccion7 import get_card_poblacion_beneficiaria_texto
from apps.segalmex3.seccion7 import get_card_poblacion_beneficiaria
from apps.segalmex3.seccion7 import get_card_volumen_incentivado
from apps.segalmex3.seccion7 import get_card_volumen_incentivado_promedio





#import plotly.io as pio
#pio.renderers.default = 'firefox'
# user='root'
# password='astro123'
# host='localhost'
# database='psociales'


# # coneccion con MySQL
# conn= mysql.connector.connect(user=user, 
#                             password=password,
#                             host=host,
#                             database=database)
# cursor = conn.cursor()
# # consulta
# query = 'select * from productores_mun;'

# # base
# cursor.execute(query)
# # nombre de campos
# column_names = [i[0] for i in cursor.description]
# # lectura de base
# base = cursor.fetchall() 
# # dataframe
# base_productores = pd.DataFrame(base, columns=column_names)
# # cierre de la conección
# cursor.close()
# conn.close()
# imprimimos primeras líneas


# --- Only run on the server
#engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
#base_productores = pd.read_sql(sql="select * from", con = engine)

# introducir directorio de la carpeta
#root = "C:/Users/jcmartinez/Desktop/Dashboard3"
#root = "/home/ubuntu/Desktop/Proyecto/ProgramasSociales"
# urls
#repo_est_url = ""
#estados_json = open(root + '/datasets/estadosMexico.json')
#mx_est_geo = json.load(estados_json)
#data2 = json.load(open(root +'/datasets/sample4.json'))
data2 = json.load(open(root +'/datasets/geoVolProd.json'))
#data3= json.load(open(root +'/datasets/sample5.json', "r", encoding="utf-8"))

# base lista de url's de todos los estados
estados_urls = pd.read_excel(root + '/datasets/estados.xlsx', converters={'cve_ent':str})
# base de beneficiarios por entidad
#base_beneficiarios_ent = pd.read_excel(root + '/datasets/base_entidad.xlsx', converters={'cve_ent':str})
cultivos_cambios = {'Trigo grano':'Trigo',
                    'Maíz grano blanco':'Maíz',
                    'Arroz':'Arroz',
                    'Leche':'Leche',
                    'Frijol':'Frijol'}

# base de beneficiarios por entidad
base_beneficiarios_ent_tprod = pd.read_excel(root + '/datasets/beneficiarios_ent.xlsx', converters={'cve_ent':str})
base_beneficiarios_ent_tprod['cultivo'] = base_beneficiarios_ent_tprod['cultivo'].map(cultivos_cambios)
base_beneficiarios_ent_tprod['tipo'] = [val.strip() for val in base_beneficiarios_ent_tprod['tipo']]

# base de beneficiarios por municipios
#base_beneficiarios_mun = pd.read_excel(root + '/datasets/base_municipio3.xlsx', converters={'cve_ent':str, 'cve_mun':str})
base_beneficiarios_mun_tprod = pd.read_excel(root + '/datasets/beneficiarios_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str, 'year':int})
base_beneficiarios_mun_tprod['tipo'] = [val.strip() for val in base_beneficiarios_mun_tprod['tipo']]

# base centros de acopio por entidad
base_centros_ent = pd.read_excel(root + '/datasets/centros_acopio_entidad.xlsx', converters={'cve_ent':str, 'cve_mun':str})

# base centros de acopio por municipio
base_centros = pd.read_excel(root + '/datasets/centros_acopio.xlsx', converters={'cve_ent':str, 'cve_mun':str, 'cve_loc':str, 'latitud':float, 'longitud':float})
base_centros = base_centros[~base_centros['cve_ent'].isna()]
base_centros = base_centros[~base_centros['cve_mun'].isna()]
base_centros = base_centros[~base_centros['cve_loc'].isna()]
base_centros = base_centros[~base_centros['latitud'].isna()]
base_centros = base_centros[~base_centros['longitud'].isna()]
# base de productores 

base_productores = pd.read_excel(root + '/datasets/productores_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str})
#base_productores2 = pd.read_excel(root + '/datasets/TotalProductores2.xlsx', converters={'cve_ent':str, 'cve_mun':str})
#base_productores = pd.read_excel(root + '/datasets/TotalProductores3.xlsx', converters={'cve_ent':str, 'cve_mun':str})

# base resumen de montos
base_resumen = pd.read_excel(root + '/datasets/resumen_montos.xlsx')


# Opciones
list_year = ['2019', '2020', '2021', '2022']
list_products = ['Arroz', 'Frijol', 'Leche', 'Maíz', 'Trigo']
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
        {"value": "Centros de Acopio", "label": "Centros de Acopio", "group": "Capa"},
        {"value": "Productores", "label": "Productores", "group": "Capa"},
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
        # Grado de marginación
        {"value": "Pequeño", "label": "Pequeño", "group": "Tamaño Productor"},
        {"value": "Mediano", "label": "Mediano", "group": "Tamaño Productor"},
        {"value": "Grande", "label": "Grande", "group": "Tamaño Productor"},
    ],
]

list_criterios = ['Marginación', 'Precio']



# Callback
# @app.callback(Output("section3-content", "children"), 
#               Input("tabs-example", "value"))
# def render_content(active):
    
#     base = base_resumen.copy()
#     # filtro de año
#     anio = int(active)
#     #
#     monto_active = barplot1(base, anio)
    
#     if active == "2019":
#         result = dbc.Row([
#                     dbc.Col([
#                         dmc.Text("En el año 2019, se destinó un aproximado de $ 8 billones al programa de Precios de Garantía a Productos Alimentarios Básicos, cuyos destinatarios serían los productores de cinco productos: maíz, trigo, frijol, leche y arroz. Para el caso de maíz se destinó un monto de $ 4 billones, lo que representó aproximadamente el 53.1% del total y, en segundo lugar, la cantidad de $2 billones (28.4% del total) fue designada a los productores de trigo.", size=18, color='#797D7F', align="justify"),
#                         dmc.Space(h=20),
#                         dmc.Text("Los productores de frijol y leche recibieron un monto de $ 695 millones (8.6%) y $ 534 millones (6.6%), respectivamente. Por último, a los productores de arroz se destinó $ 260 millones, equivalente a 3.2% del monto total.", size=18, color='#797D7F', align="justify"),
#                     ], className='card col-lg-6 col-12', style={'padding':'2rem', 'backgroundColor':'#fdfefe', 'border-radius': '5px', 'border-right': '2px solid #f8f9f9', 'border-left': '1px solid #f8f9f9', 'border-top': '1px solid #f8f9f9', 'border-bottom': '2px solid #f8f9f9'}),
#                     dbc.Col([
#                         html.Div([
#                             dcc.Graph(figure=monto_active, animate=True)    
#                         ])
#                     ], className='col-lg-6 col-12', style={'padding':'1rem'})
#                 ], className='col-12', align="center", style={'padding':'1rem'})
#     elif active == "2020":
#         result = dbc.Row([
#                     dbc.Col([
#                         dmc.Text("En el año 2020, se destinó un aproximado de $ 9.5 billones al programa de Precios de Garantía a Productos Alimentarios Básicos, lo que representa un aumento del 18.2% en comparación con el monto destinado en 2019. Los productores de maíz recibieron $ 6.7 billones del total del monto de 2020 (70.9% del total).", size=18, color='grey', align="justify"),
#                         dmc.Space(h=20),
#                         dmc.Text("Por su parte, a los productores de trigo se destinó $1 billón (13.3% de total), para el caso de los productores de leche, se destinó un monto de $ 1 billón, correspondiente al 10.9% del total. En cuarto lugar, se encuentra el arroz, producto que recibió en 2020 $ 353 millones (3.7% del monto total del año respectivo). Finalmente, el frijol recibió un monto de apoyo de $ 117 millones, es decir, un 1.23% del monto total destinado al programa en 2020.", size=18, color='grey', align="justify"),
#                     ], className='card col-lg-6 col-12', style={'padding':'2rem', 'backgroundColor':'#fdfefe', 'border-radius': '5px', 'border-right': '2px solid #f8f9f9', 'border-left': '1px solid #f8f9f9', 'border-top': '1px solid #f8f9f9', 'border-bottom': '2px solid #f8f9f9'}),
#                    dbc.Col([
#                         html.Div([
#                             dcc.Graph(figure=monto_active)    
#                         ])
#                     ], className='col-lg-6 col-12', style={'padding':'1rem'})
#                 ], className='col-12', align="center", style={'padding':'1rem'})
#     elif active == "2021":
#         result = dbc.Row([
#                     dbc.Col([
#                         dmc.Text("En el año 2021, se destinó un aproximado de $ 6.8 billones al Programa Precios de Garantía a Productos Alimentarios Básicos lo que representa una disminución del 27.7% en comparación con el monto destinado en 2020. Para el caso de maíz se otorgaron $4 billones, lo que representó aproximadamente el 60.4% del total.", size=18, color='grey', align="justify"),
#                         dmc.Space(h=20),
#                         dmc.Text("Respecto al frijol, se destinó $1.6 billones, lo que representa el 22.9% del total del monto destinado en 2021 al programa. Los productores de leche recibieron $ 523 millones, correspondiente al 7.5% del total. En cuarto lugar, se encuentra el trigo, producto que recibió en 2021 $ 424 millones (6.1% del monto total del año respectivo). Finalmente, el arroz recibió un monto de apoyo de $ 202 millones, es decir, un 2.9% del monto total destinado al programa en 2020.", size=18, color='grey', align="justify"),
#                     ], className='card col-lg-6 col-12', style={'padding':'2rem', 'backgroundColor':'#fdfefe', 'border-radius': '5px', 'border-right': '2px solid #f8f9f9', 'border-left': '1px solid #f8f9f9', 'border-top': '1px solid #f8f9f9', 'border-bottom': '2px solid #f8f9f9'}),
                    
#                     dbc.Col([
#                         html.Div([
#                             dcc.Graph(figure=monto_active)    
#                         ])
#                     ], className='col-lg-6 col-12', style={'padding':'1rem'})
#                 ], className='col-12', align="center", style={'display':'flex','padding':'1rem'})

#     else:
#         result = dmc.Text('No action!')
        
#     return result




# backgroundColor': '#F4F6F6'
#############################################################
###            content2 - graficos barras
###    - Gráfico1 : Tamaño productor por estado
###    - Gráfico2 : Nivel de marginación por estado
#############################################################
#######################    content3 - gráficos por municipios
# content2 = html.Div([
#     dmc.Card(children=[
#         dmc.CardSection(
#             dmc.Group(
#                 children=[
#                     dmc.Text("Review Pictures", weight=500),
#                     dmc.ActionIcon(
#                         DashIconify(icon="carbon:overflow-menu-horizontal"),
#                         color="gray",
#                         variant="transparent",
#                     ),
#                 ],
#                 position="apart",
#             ),
#             withBorder=True,
#             inheritPadding=True,
#             py="xs",
#         ),
#         dmc.Text(
#             children=[
#                 dmc.Text(
#                     "200+ images uploaded",
#                     color="blue",
#                     style={"display": "inline"},
#                 ),
#                 " since last visit, review them to select which one should be added to your gallery",
#             ],
#             mt="sm",
#             color="dimmed",
#             size="sm",
#         ),
#         dmc.CardSection(
#             html.Iframe(id="plot-r1", style={"height": "400px", "width": "1300px"}),
#         ),
#         # dmc.CardSection(children=[
#         #         dmc.SimpleGrid(cols=2, children=[
#         #             #dbc.Group([
#         #                 # plot 1
#         #                 dmc.Group([
#         #                     dmc.CardSection(
#         #                         dmc.Group(
#         #                             children=[
#         #                                 dmc.Text("Review Pictures", weight=500),
#         #                                 dmc.ActionIcon(
#         #                                     DashIconify(icon="carbon:overflow-menu-horizontal"),
#         #                                     color="gray",
#         #                                     variant="transparent",
#         #                                 ),
#         #                             ],
#         #                             position="apart",
#         #                         ),
#         #                         withBorder=True,
#         #                         inheritPadding=True,
#         #                         py="xs",
#         #                     ),
#         #                     dmc.Text(
#         #                         children=[
#         #                             dmc.Text(
#         #                                 "200+ images uploaded",
#         #                                 color="blue",
#         #                                 style={"display": "inline"},
#         #                             ),
#         #                             " since last visit, review them to select which one should be added to your gallery",
#         #                         ],
#         #                         mt="sm",
#         #                         color="dimmed",
#         #                         size="sm",
#         #                     ),
#         #                     dmc.CardSection(
#         #                         html.Iframe(id="plot-r2", style={"height": "400px", "width": "800px"}),
#         #                     ),
#         #                 ]),
#         #                 # plot 2
#         #                 dmc.Group([
#         #                     dmc.CardSection(
#         #                         dmc.Group(
#         #                             children=[
#         #                                 dmc.Text("Review Pictures", weight=500),
#         #                                 dmc.ActionIcon(
#         #                                     DashIconify(icon="carbon:overflow-menu-horizontal"),
#         #                                     color="gray",
#         #                                     variant="transparent",
#         #                                 ),
#         #                             ],
#         #                             position="apart",
#         #                         ),
#         #                         withBorder=True,
#         #                         inheritPadding=True,
#         #                         py="xs",
#         #                     ),
#         #                     dmc.Text(
#         #                         children=[
#         #                             dmc.Text(
#         #                                 "200+ images uploaded",
#         #                                 color="blue",
#         #                                 style={"display": "inline"},
#         #                             ),
#         #                             " since last visit, review them to select which one should be added to your gallery",
#         #                         ],
#         #                         mt="sm",
#         #                         color="dimmed",
#         #                         size="sm",
#         #                     ),
#         #                     dmc.CardSection(
#         #                         html.Iframe(id="plot-r3", style={"height": "400px", "width": "800px"}),
#         #                     ),
#         #                 ]),
#         #                 #plot3
#         #                 # dmc.Group([
#         #                 #     dmc.CardSection(
#         #                 #         dmc.Group(
#         #                 #             children=[
#         #                 #                 dmc.Text("Review Pictures", weight=500),
#         #                 #                 dmc.ActionIcon(
#         #                 #                     DashIconify(icon="carbon:overflow-menu-horizontal"),
#         #                 #                     color="gray",
#         #                 #                     variant="transparent",
#         #                 #                 ),
#         #                 #             ],
#         #                 #             position="apart",
#         #                 #         ),
#         #                 #         withBorder=True,
#         #                 #         inheritPadding=True,
#         #                 #         py="xs",
#         #                 #     ),
#         #                 #     dmc.Text(
#         #                 #         children=[
#         #                 #             dmc.Text(
#         #                 #                 "200+ images uploaded",
#         #                 #                 color="blue",
#         #                 #                 style={"display": "inline"},
#         #                 #             ),
#         #                 #             " since last visit, review them to select which one should be added to your gallery",
#         #                 #         ],
#         #                 #         mt="sm",
#         #                 #         color="dimmed",
#         #                 #         size="sm",
#         #                 #     ),
#         #                 #     dmc.CardSection(
#         #                 #         html.Iframe(id="plot-r4", style={"height": "400px", "width": "400px"}),
#         #                 #     ),
#         #                 # ]),

#         #             #], className='col-12'),
#         #             # html.Iframe(id="plot-r2", style={"height": "300px", "width": "400px"}),
#         #             # html.Iframe(id="plot-r3", style={"height": "300px", "width": "400px"}),
#         #             #html.Iframe(id="plot-r4", style={"height": "300px", "width": "400px"}),
#         #         ]),
#         #     ],
#         #     withBorder=True,
#         #     inheritPadding=True,
#         #     mt="sm",
#         #     pb="md",
#         # ),
#         # dmc.CardSection(
#         #     dmc.Group(
#         #         children=[
#         #             dmc.Text("Review Pictures", weight=500),
#         #             dmc.ActionIcon(
#         #                 DashIconify(icon="carbon:overflow-menu-horizontal"),
#         #                 color="gray",
#         #                 variant="transparent",
#         #             ),
#         #         ],
#         #         position="apart",
#         #     ),
#         #     withBorder=True,
#         #     inheritPadding=True,
#         #     py="xs",
#         # ),
#         # dmc.Text(
#         #     children=[
#         #         dmc.Text(
#         #             "200+ images uploaded",
#         #             color="blue",
#         #             style={"display": "inline"},
#         #         ),
#         #         " since last visit, review them to select which one should be added to your gallery",
#         #     ],
#         #     mt="sm",
#         #     color="dimmed",
#         #     size="sm",
#         # ),
#         # dmc.CardSection(
#         #     html.Iframe(id="plot-r5", style={"height": "600px", "width": "1300px"}),
#         # ),
#     ],
#     withBorder=True,
#     shadow="sm",
#     radius="md",
#     className="col-12"),
    
    
# ],style={"paddin": '0rem', 'marginLeft':'2rem', 'marginRight':'2rem'})

################################################################
#                         Graficos
################################################################
def plot1():
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    #fig = go.Figure([])

    # frontera eficiente
    fig.add_trace(go.Bar(
        x=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u'], 
        y=[20, 14, 23, 20, 14, 23, 21, 15, 24, 14, 23, 21, 14, 23, 21,  21, 15, 24, 14, 23, 21],
        #name='Monto',
        width=0.85), secondary_y=False)

    # fig.add_trace(go.Scatter(
    #     x=df['Producto'].to_list(),
    #     y=df['Acumulado2'].to_list(),
    #     mode="lines+markers+text",
    #     textfont=dict(color='#cb4335'),
    #     line_color='#cb4335',
    #     marker=dict(color='#cb4335'),
    #     name='% acumulado',
    #     text= [str(np.round(val,0))+'%' for val in df['Acumulado2'].to_list()],
    #     textposition="bottom center"), secondary_y=True)

    fig.update_layout(
        showlegend=False,
        autosize=True,
        #width=650,
        height=200,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=20,
            pad=0),
            plot_bgcolor='white',
            paper_bgcolor="white",
            )


    fig.update_layout(
        title="",
        xaxis_title="Producto",
        yaxis_title="Monto del Apoyo ($)",
        legend_title="",
        font=dict(
            #family="Courier New, monospace",
            size=12,
            color="#2a3240"
            ))

    fig.update_traces(marker_color='#4e203a', marker_line_color='#4e203a',
                    marker_line_width=1, opacity=1)

    # Set y-axes titles
    # fig.update_yaxes(
    #     title_text="<b>Monto del Apoyo ($)</b>", 
    #     secondary_y=False)
    # fig.update_yaxes(
    #     title_text="<b>Porcentaje acumulado (%)</b>", 
    #     secondary_y=True)
    # drop grids
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    #fig.update_layout(title_text='Monto de apoyos por producto', title_x=0.5)
    #fig.update_layout(hovermode="y")
    fig.update_layout(showlegend=False)
    
    return fig

seccion8 = html.Div([
    # first row
    dmc.Grid(children=[
       dmc.Col(
               html.Div(
                dmc.SimpleGrid(cols=1, spacing="lg", children=[
                    dmc.Card(
                        children=[
                            dmc.CardSection(
                                dmc.Group(
                                    children=[
                                        #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                                        # dmc.ActionIcon(
                                        #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                                        #     color="gray",
                                        #     variant="transparent",
                                        # ),
                                    ],
                                    position="apart",
                                ),
                                withBorder=True,
                                inheritPadding=False,
                                py="xs",
                                style={'padding':'0.2rem','backgroundColor':'#566573'}
                            ),
                            dmc.Text(
                                children=[
                                    dmc.Text(" Monto de apoyos por producto", weight=500, color='black', align='center', size=22),
                                    dmc.Text(
                                        "200+ images uploaded",
                                        color="blue",
                                        style={"display": "inline"},
                                    ),
                                    " since last visit, review them to select which one should be added to your gallery",
                                ],
                                mt="sm",
                                color="dimmed",
                                size="sm",
                            ),
                            dmc.CardSection(
                                dcc.Graph(id='boxplot_ent', config={'displayModeBar':False})
                                
                            ),
                            dmc.CardSection(
                                dmc.Group(
                                    children=[
                                        #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                                        # dmc.ActionIcon(
                                        #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                                        #     color="gray",
                                        #     variant="transparent",
                                        # ),
                                    ],
                                    position="apart",
                                ),
                                withBorder=True,
                                inheritPadding=False,
                                py="xs",
                                style={'padding':'0.2rem','backgroundColor':'#566573'}
                            ),
                            
                        ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        style={"width": '100%', 'height':'25rem'},
                    ),
                    dmc.Card(
                        children=[
                            dmc.CardSection(
                                dmc.Group(
                                    children=[
                                        #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                                        # dmc.ActionIcon(
                                        #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                                        #     color="gray",
                                        #     variant="transparent",
                                        # ),
                                    ],
                                    position="apart",
                                ),
                                withBorder=True,
                                inheritPadding=False,
                                py="xs",
                                style={'padding':'0.2rem','backgroundColor':'#566573'}
                            ),
                            dmc.Text(
                                children=[
                                    dmc.Text(" Monto de apoyos por producto", weight=500, color='black', align='center', size=22),
                                    dmc.Text(
                                        "200+ images uploaded",
                                        color="blue",
                                        style={"display": "inline"},
                                    ),
                                    " since last visit, review them to select which one should be added to your gallery",
                                ],
                                mt="sm",
                                color="dimmed",
                                size="sm",
                            ),
                            dmc.CardSection(
                                dcc.Graph(id='barplot_ent', config={'displayModeBar':False})
                                
                            ),
                            dmc.CardSection(
                                dmc.Group(
                                    children=[
                                        #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                                        # dmc.ActionIcon(
                                        #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                                        #     color="gray",
                                        #     variant="transparent",
                                        # ),
                                    ],
                                    position="apart",
                                ),
                                withBorder=True,
                                inheritPadding=False,
                                py="xs",
                                style={'padding':'0.2rem','backgroundColor':'#566573'}
                            ),
                            
                        ],
                        withBorder=True,
                        shadow="sm",
                        radius="md",
                        style={"width": '100%', 'height':'25rem'},
                    ),
                    #
                ], style={'marginBottom':'1.5rem'}),    
               ), span=8),
       dmc.Col(
           html.Div(
                dmc.Card(
                    children=[
                        dmc.CardSection(
                            dmc.Group(
                                children=[
                                    dmc.Text(" Monto de apoyos por producto", weight=500, color='white'),
                                    dmc.ActionIcon(
                                        DashIconify(icon="carbon:overflow-menu-horizontal"),
                                        color="gray",
                                        variant="transparent",
                                    ),
                                ],
                                position="apart",
                            ),
                            withBorder=True,
                            inheritPadding=False,
                            py="xs",
                            style={'padding':'0.3rem','backgroundColor':'#566573'}
                        ),
                        dmc.Text(
                            children=[
                                dmc.Text(
                                    "200+ images uploaded",
                                    color="blue",
                                    style={"display": "inline"},
                                ),
                                " since last visit, review them to select which one should be added to your gallery",
                            ],
                            mt="sm",
                            color="dimmed",
                            size="sm",
                        ),
                        dmc.CardSection(
                            dcc.Graph(id='table_ent', config={'displayModeBar':False}, style={"overflow": "scroll"})
                            
                        ),
                        dmc.CardSection(
                            dmc.Group(
                                children=[
                                    #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                                    # dmc.ActionIcon(
                                    #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                                    #     color="gray",
                                    #     variant="transparent",
                                    # ),
                                ],
                                position="apart",
                            ),
                            withBorder=True,
                            inheritPadding=False,
                            py="xs",
                            style={'padding':'0.2rem','backgroundColor':'#566573'}
                        ),
                        
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="md",
                    style={"width": '100%', 'height':'35rem'},
                ),
           ), style={'paddingRight':'0rem'}, span=4), 
    ]),
    
    # second row 
    dmc.SimpleGrid(cols=3, spacing="lg", children=[
        # card 1
        dmc.Card(
            children=[
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.Text(" Monto de apoyos por producto", weight=500, color='white'),
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.3rem','backgroundColor':'#566573'}
                ),
                dmc.Text(
                    children=[
                        dmc.Text(
                            "200+ images uploaded",
                            color="blue",
                            style={"display": "inline"},
                        ),
                        " since last visit, review them to select which one should be added to your gallery",
                    ],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
                dmc.CardSection(
                    dcc.Graph(id='plot1', config={'displayModeBar':False})
                    
                ),
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            # dmc.ActionIcon(
                            #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                            #     color="gray",
                            #     variant="transparent",
                            # ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.2rem','backgroundColor':'#566573'}
                ),
                
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": '100%'},
        ),
        # card 2 
        dmc.Card(
            children=[
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.3rem','backgroundColor':'#DC7633'}
                ),
                dmc.Text(
                    children=[
                        dmc.Text(
                            "200+ images uploaded",
                            color="blue",
                            style={"display": "inline"},
                        ),
                        " since last visit, review them to select which one should be added to your gallery",
                    ],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
                dmc.CardSection(
                    dcc.Graph(id='plot2', config={'displayModeBar':False})
                ),
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            # dmc.ActionIcon(
                            #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                            #     color="gray",
                            #     variant="transparent",
                            # ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.2rem','backgroundColor':'#DC7633'}
                ),
                
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": '100%'}
        ),
        # card 3 
        dmc.Card(
            children=[
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.3rem','backgroundColor':'#DC7633'}
                ),
                dmc.Text(
                    children=[
                        dmc.Text(
                            "200+ images uploaded",
                            color="blue",
                            style={"display": "inline"},
                        ),
                        " since last visit, review them to select which one should be added to your gallery",
                    ],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
                dmc.CardSection(
                    dcc.Graph(id='plot3', config={'displayModeBar':False})
                ),
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            # dmc.ActionIcon(
                            #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                            #     color="gray",
                            #     variant="transparent",
                            # ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.2rem','backgroundColor':'#DC7633'}
                ),
                
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": '100%'}
        ),
        
        
    ], style={'marginBottom':'1.5rem'}),
    
    dmc.SimpleGrid(cols=2, spacing="lg", children=[
        # card 1
        dmc.Card(
            children=[
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.3rem','backgroundColor':'#DC7633'}
                ),
                dmc.Text(
                    children=[
                        dmc.Text(" Monto de apoyos por producto", weight=500, color='white'),
                        dmc.Text(
                            "200+ images uploaded",
                            color="blue",
                            style={"display": "inline"},
                        ),
                        " since last visit, review them to select which one should be added to your gallery",
                    ],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
                dmc.CardSection(
                    dcc.Graph(id='plot1',figure=plot1(), config={'displayModeBar':False})
                    
                ),
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            # dmc.ActionIcon(
                            #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                            #     color="gray",
                            #     variant="transparent",
                            # ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.2rem','backgroundColor':'#DC7633'}
                ),
                
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": '100%'},
        ),
        # card 2 
        dmc.Card(
            children=[
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            dmc.ActionIcon(
                                DashIconify(icon="carbon:overflow-menu-horizontal"),
                                color="gray",
                                variant="transparent",
                            ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.3rem','backgroundColor':'#DC7633'}
                ),
                dmc.Text(
                    children=[
                        dmc.Text(
                            "200+ images uploaded",
                            color="blue",
                            style={"display": "inline"},
                        ),
                        " since last visit, review them to select which one should be added to your gallery",
                    ],
                    mt="sm",
                    color="dimmed",
                    size="sm",
                ),
                dmc.CardSection(
                    dcc.Graph(id='plot2', figure=plot1(), config={'displayModeBar':False})
                ),
                dmc.CardSection(
                    dmc.Group(
                        children=[
                            #dmc.Text("Monto de apoyos por producto", weight=500, color='white'),
                            # dmc.ActionIcon(
                            #     DashIconify(icon="carbon:overflow-menu-horizontal"),
                            #     color="gray",
                            #     variant="transparent",
                            # ),
                        ],
                        position="apart",
                    ),
                    withBorder=True,
                    inheritPadding=False,
                    py="xs",
                    style={'padding':'0.2rem','backgroundColor':'#DC7633'}
                ),
                
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": '100%'},
        ),
        
    ]),    
], style={'padding':'2rem'})



seccion1_1 = html.Div([
    dmc.Card(children=[
     dmc.Text(
            "¿Cómo se vería la recepción de beneficios del programa si la entrega se hubiera basado en los precios muy bajos de mercado del producto agrícola a los que se enfrenta el productor?",
            size="sm",
            color="white",
        ),   
    ], style={'backgroundColor':'#909497', 'marginBottom':'1rem'}),
    
    dmc.Grid(
        children=[
            dmc.Col(
                dmc.Card(children=[
                    dmc.Text(
                            "211",
                            size=30,
                            color="white",
                        ),   
                ], style={'backgroundColor':'#A2D9CE'}), span=3),
            dmc.Col(
                dmc.Card(children=[
                    dmc.Text(
                            "Personas beneficiadas realmente, que se tendría que enfrentar a la peor la situación en caso de no poder acceder al programa.",
                            size="xs",
                            color="black",
                        ),   
                ], style={'backgroundColor':'#A2D9CE'}), span=9),

    ]),
    dmc.Grid(
        children=[
            dmc.Col(
                dmc.Card(children=[
                    dmc.Text(
                            "824",
                            size=30,
                            color="white",
                        ),   
                ], style={'backgroundColor':'#F8C471 '}), span=3),
            dmc.Col(
                dmc.Card(children=[
                    dmc.Text(
                            "Población beneficiada hipotéticamente, que vive en lugares con alta y  muy alta marginación.",
                            size="xs",
                            color="black",
                        ),   
                ], style={'backgroundColor':'#F8C471 '}), span=9),

    ]),
])

# original 'backgroundColor': '#f2f2f2'
########################### layout  SEGALMEX
layout = dbc.Container([
      
        #
        #
        # dmc.Affix(
        #     dmc.Card([
        #         dmc.Text("Nacional - 2021 - Frijol", weight=600, color='white', size=18)
        #     ], className='col-12', style={'padding':'0.5rem 1rem 0.5rem 1rem', 'backgroundColor':'#2e4053'})    
        # ),
        #  header
        seccion1,
        # Introduccion
        #seccion2,
        # Resumen: Pie plot
        #seccion3,
        # Filtros principales : Año - producto
        #seccion5,
        # Introduccion
        seccion4,
        # Mapa
        seccion6,
        
        #### SECCIÓN : GRAFICOS
        # final break
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

#-------------------------------------------------------------------------------
#                              Resumen cards
#-------------------------------------------------------------------------------


#########      CARD 1 : Regresa estado  ################
# @app.callback(# 'click_feature
#         Output('state01', 'children'),
#         Input("states", "click_feature")
#     )
# def get_state(clicks, feature):

#     # condición
#     if not feature:
#         state = 'Nacional'
#     else:
#         # filtro de estado
#         state = feature["properties"]["name"]

#     return state
#########      CALL : Regresa año  ################
@app.callback(# 'click_feature
        Output('anio_filtro2', 'children', allow_duplicate=True),
        Output('anio_filtro1', 'children', allow_duplicate=True),
        #Output('anio_filtro', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value'),
        prevent_initial_call=True,
    )

def anio(clicks, sel_producto, sel_anio):


    return sel_anio, sel_anio #, sel_anio

#########      CALL : Regresa producto  ################
@app.callback(# 'click_feature
        Output('producto_filtro2', 'children', allow_duplicate=True),
        Output('producto_filtro1', 'children', allow_duplicate=True),
        #Output('producto_filtro', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value'),
        prevent_initial_call=True,
    )
def producto(clicks, sel_producto, sel_anio):

    return sel_producto, sel_producto #, sel_producto

#########   CALL : Modal Reglas de operación  ################
@app.callback(
    Output("modal", "is_open", allow_duplicate=True),
    [Input("open", "n_clicks"),
     Input("close", "n_clicks")],
    [State("modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#########  CALL : Resumen Reglas de operación ################
@app.callback(
        Output('reglas-operacion', 'children', allow_duplicate=True),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value'),
        prevent_initial_call=True,
    )

def summary_reglas_operacion(clicks, producto_sel, anio_sel):

    result = reglas_operacion.resumen_reglas_operacion(anio_sel, producto_sel)
    
    return result


#########      CALL : Pie Plot  ################
# @app.callback(# 'click_feature
#         Output('pie-plot1', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State('producto', 'value'),
#         State('anio', 'value'),
#         prevent_initial_call=True
#     )
# def pie_plo1(clicks, sel_producto, sel_anio):
#     #time.sleep(1)
#     return open(root + f"./graficos/piePlot_{str(2020)}.html", 'r', encoding = 'utf-8').read()

# @app.callback(Output("loading-output-1", "children"),
#           Input("loading-input-1", "value"))
# def input_triggers_spinner(value):
#     time.sleep(2)
#     return value


#########  Fade transsition : instrucciones
@app.callback(
    Output("transition-instrucciones", "is_in", allow_duplicate=True),
    [Input("transition-instrucciones-btn", "n_clicks")],
    [State("transition-instrucciones", "is_in")],
    prevent_initial_call=True,
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in


################################################################
#  Cnetros de acopio
get_card_centros_acopio(app)
get_card_poblacion_beneficiaria_img(app)
get_card_poblacion_beneficiaria_texto(app)
get_card_poblacion_beneficiaria(app)
get_card_volumen_incentivado(app)
get_card_volumen_incentivado_promedio(app)



##########################################################################################
#                           SECCIÓN I :  mapa
##########################################################################################
#########       CALL : Transfer list  ################

# opción Capas
tab1_capas_criterios = html.Div([
    dmc.Text("Seleccione la característica que desee visualizar", size=11, color="gray"),
    dmc.RadioGroup(
            [dmc.Radio(k, value=k) for k in list_beneficiarios_opciones],
            id="beneficiarios-opciones",
            orientation="horizontal",
            #multiple=True,
            value="Número de Beneficiarios",
            #label="",
            style={'marginBottom':'1rem'}
    ),
    dmc.Text("Seleccione Capas y Grado de Marginación que desee visualizar", size=11, color="gray", style={'marginBottom':'1rem'}),
    dmc.TransferList(
        id="transfer-list-simple",
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
                                        html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
                                    ],className="card col-lg-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem', 'marginTop':'0rem', 'marginBottom':'0rem', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='resumen-centros_acopio', style={'marginTop':'0em','text-align': 'center', "color":"red", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Centros  de  acopio", color='grey', weight=500, align='center', style={"fontSize": 10})
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
                                    dbc.Col([
                                        html.Img(id='image-poblacion_beneficiaria', src='../assets/poblacionBeneficiaria.png', width="63", height="65"),
                                    ],className="card col-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem', 'margin':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='resumen-poblacion_beneficiaria', style={'paddingRight':'0rem','text-align': 'center', "color":"blue", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Población Beneficiaria", id='resumen_texto_poblacion_beneficiaria', color='grey', weight=500, align='right', style={"fontSize": 10, 'paddingRight':'0rem'}),
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem', 'width':'100%'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": "100%", "margin":'0rem', "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                ], style={'fontSize':'12px'}),
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
                                        DashIconify(icon="emojione-monotone:balance-scale", width=65, height=60),
                                    ],className="card col-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem','marginTop':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='resumen-volumen_incentivado_total', style={'paddingRight':'0rem','text-align': 'center', "color":"green", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Vol Incentivado Total", color='grey', weight=500, align='right', style={"fontSize": 10, 'paddingRight':'0rem'}),
                                            
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem', 'width':'100%'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": "100%", "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                ], style={'fontSize':'10px'}),
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
                                             DashIconify(icon="emojione-monotone:balance-scale", width=65, height=60),
                                    ],className="card col-3 border-0 bg-transparent", style={'paddingTop':'0rem', 'paddingBottom':'0rem', 'marginTop':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "51%",
                                        ], id='resumen-volumen_incentivado_promedio', style={'padding':'0em',"textAling":"right", "color":"grey", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([
                                            dmc.Text("Vol Incentivado Prom.", color='gray', weight=500, align='right', style={"fontSize": 10, 'text-align': 'center', 'paddingRight':'0rem'}),
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem', 'width':'100%'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": "100%", "padding":'0rem', 'backgroundColor': '#F4F6F6'},)
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
            # chipgroup
            # dmc.ChipGroup([
            #         dmc.Chip(
            #             x,
            #             value=x,
            #             variant="outline",
            #         )
            #         for x in ["Beneficiarios"]
            #     ],
            #     align='center',
            #     id="chip-beneficiarios",
            #     value=[],
            #     multiple=True,
            # ),
            # selector adicional
            # dmc.Select(
            #     label='Otro selector',
            #     id='criterios2',
            #     value= ['Criterio de Marginación'],
            #     data=list_criterios,
            #     nothingFound="No options found",
            #     style={"width": '100%'}
            # ),
        ], style={'marginBottom':'1rem'}),
        
        dmc.SimpleGrid(cols=2, children=[
            
            # selector criterios simulados
            dmc.Select(
                label='Escenarios',
                id='criterios1',
                searchable=True,
                dropdownPosition='bottom',
                value= 'Marginación',
                data=list_criterios,
                nothingFound="No options found",
                style={"width": '100%'}
            ),
            # selector adicional
            # dmc.Select(
            #     label='Otro selector',
            #     id='criterios2',
            #     value= ['Criterio de Marginación'],
            #     data=list_criterios,
            #     nothingFound="No options found",
            #     style={"width": '100%'}
            # ),
        ], style={'marginBottom':'8rem'}),
        
        
        # dmc.Center([
        #     dmc.Button(
        #     "Ver Metodología",
        #     id='btn_metodo_pdf',
        #     variant="subtle",
        #     rightIcon=DashIconify(icon="ic:baseline-download"),
        #     color="blue",
        #     ),
        #     dcc.Download(id="download"),

        # ]),
        
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
@app.callback(Output("content-capas-criterios", "children", allow_duplicate=True),
              Output("mapa", "children", allow_duplicate=True),
             [Input("capas-criterios", "value")],
             prevent_initial_call=True,
            )
            
def switch_tab(active):
    if active == "capas": # dmc.Loader(color="red", size="md", variant="oval")
        return tab1_capas_criterios,  dcc.Loading(id="ls-loading-1",children=content_mapa1, type="default")
    elif active == "criterios":
        return tab2_capas_criterios, dcc.Loading(id="ls-loading-2",children=content_mapa2, type="default") #content_mapa2

    return html.P("This shouldn't ever be displayed...")
# #########  CALL : Regresa opciones criterios  ################
# @app.callback(Output("mapa", "children"),
#              [Input("capas-criterios", "value")],
#              PreventUpdate=False)
# def switch_tab2(active):
#     if active == "capas":
#         return content_mapa1
#     elif active == "criterios":
#         return content_mapa2

#     return html.P("This shouldn't ever be displayed...")


#########  CALL : Regresa actualización del MAPA  ################
# declaración de parámetros para color y leyendas

@app.callback(Output("ls-loading-output-1", "children", allow_duplicate=True), 
              Input("ls-input-1", "value"),
              prevent_initial_call=True,
   )
def input_triggers_spinner(value):
    time.sleep(2)
    return value

@app.callback(Output("ls-loading-output-2", "children", allow_duplicate=True), 
              Input("ls-input-2", "value"),
              prevent_initial_call=True,
    )
def input_triggers_nested(value):
    time.sleep(1)
    return value

####   actualiza tabla-Mapa
#########    CALL : Indicador estado (MAPA)  ################
@app.callback(# 'click_feature
        Output('state_label', 'children', allow_duplicate=True),
        Input("states", "click_feature"),
        prevent_initial_call=True,
    )
def get_state(clicks, feature):

    # condición
    if not feature:
        return [
            html.H4("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/'+ str("Nacional") +'.png', width="65", height="65")),
          ]
    else:
        # filtro de estado
        state = feature["properties"]["name"]
        urls_est = str(estados_urls[estados_urls['nom_ent']==state]['Liga'].to_list()[0])
    
        return [
            html.H4("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/'+ str(feature["properties"]["name"]) +'.png', width="65", height="65")),
          ]

# actualiza infor en mapa
@app.callback(Output("info", "children", allow_duplicate=True),
              Input("states", "click_feature"),
              prevent_initial_call=True,
        )
              #State('producto', 'value'),
              #State('anio', 'value'))
def info_hover(feature):
    return get_info(feature)

####################################################################
#    Gráficos
####################################################################
def boxplot(base, by, col, entidad):
    

  df_filter = base.copy()
  # define orden con base en la variable col
  df_mean = df_filter.groupby(by).agg({col:np.mean}).reset_index()
  df_mean = df_mean.sort_values(col, ascending=False)
  ent_order = df_mean.reset_index(drop=True).reset_index().drop(col, axis=1)
  # agrega variable orden a la base
  df_filter = df_filter.merge(ent_order, on=by, how='left')
  df = df_filter.sort_values('index', ascending=True)

  # entidad seleccionada
  entidad_color = entidad #'Sinaloa'
  idx = int(ent_order[ent_order[by]==entidad_color]['index'])
  #print(idx)
  # numero de estados 
  N = len(df[by].unique())
  # define colores para los estados
  markercolor = ['#EBEDEF',] * N
  linecolor = ['#EBEDEF',] * N
  # define color para la entidad seleccionada
  markercolor[idx] = '#3498DB'
  linecolor[idx] = '#3498DB'
  
  base_group_ent = df.groupby(by).agg({col:np.sum, 'index':np.mean}).sort_values('index', ascending=True)
  base_group_ent = base_group_ent.reset_index()
  # plot
  fig = make_subplots(rows=1, cols=1, shared_xaxes=False,horizontal_spacing=0.05)
  #fig = go.Figure()
  i = 0
  for ent in base_group_ent[by].to_list():
    # filtro de base por entidad
    base_monto_sum = base_group_ent[base_group_ent[by]==ent]
    # gráfico Box plot
    fig.add_traces(go.Box(
        y=base[base[by]==ent][col],
        name=i, #ent,
        marker_color=markercolor[i],
        marker_line_width=1,
        marker_size=1,
        line_color=linecolor[i],
        
      ))

    # gráfico de barras
    # fig.append_trace(go.Bar(
    #     x=[ent],
    #     y=base_monto_sum[col],
    #     text= [millify(val, precision=0) for val in base_monto_sum[col]], 
    #     name=ent,
    #     orientation='v',
    #     marker_color=markercolor[i],
    #     textfont=dict(
    #       color='white'
    #     )
    #     #line_color=linecolor[i]
    #   ), row=2, col=1)

    i += 1

    fig.update_layout(
            showlegend=False,
            autosize=True,
            #width=650,
            height=315,
            margin=dict(
                l=0,
                r=0,
                b=30,
                t=50,
                pad=0),
                plot_bgcolor='white',
                paper_bgcolor="white",
                )
    fig.update_traces(width=0.7)
  # yaxis
  fig.update_yaxes(title_text="Monto del apoyo ($)", row=1, col=1)
  fig.update_yaxes(title_text="Monto del apoyo ($)", row=2, col=1)
  fig.update_xaxes(title_text="Entidad", automargin = True, row=2, col=1)



  # format the layout
  fig.update_layout(showlegend=False, )
  
  return fig

# barplot
def barplot(base, by, col, entidad):

  df_filter = base.copy()
  # define orden con base en la variable col
  df_mean = df_filter.groupby(by).agg({col:np.sum}).reset_index()
  df_mean = df_mean.sort_values(col, ascending=False)
  ent_order = df_mean.reset_index(drop=True).reset_index().drop(col, axis=1)
  # agrega variable orden a la base
  df_filter = df_filter.merge(ent_order, on=by, how='left')
  df = df_filter.sort_values('index', ascending=True)

  # entidad seleccionada
  entidad_color = entidad #'Sinaloa'
  idx = int(ent_order[ent_order[by]==entidad_color]['index'])
  #print(idx)
  # numero de estados
  N = len(df[by].unique())
  # define colores para los estados
  markercolor = ['#EBEDEF',] * N
  linecolor = ['#EBEDEF',] * N
  # define color para la entidad seleccionada
  markercolor[idx] = '#3498DB'
  linecolor[idx] = '#3498DB'

  base_group_ent = df.groupby(by).agg({col:np.sum, 'index':np.mean}).sort_values(col, ascending=False)
  base_group_ent = base_group_ent.reset_index()
  # plot
  fig = make_subplots(rows=1, cols=1, shared_xaxes=True,horizontal_spacing=0.05)
  #fig = go.Figure()
  i = 0
  for ent in base_group_ent[by].to_list():
    # filtro de base por entidad
    base_monto_sum = base_group_ent[base_group_ent[by]==ent]
    # gráfico Box plot
    # fig.add_traces(go.Box(
    #     y=base[base[by]==ent][col],
    #     name=ent,
    #     marker_color=markercolor[i],
    #     line_color=linecolor[i]
    #   ))

    # gráfico de barras
    fig.append_trace(go.Bar(
        x=[i],
        y=base_monto_sum[col],
        text= [millify(val, precision=0) for val in base_monto_sum[col]],
        name= i, #ent,
        orientation='v',
        #line=dict(color=markercolor[i]),
        #fillcolor=markercolor[i],
        marker_color=markercolor[i],
        textfont=dict(
          color='white'
        )
        #line_color=linecolor[i]
      ), row=1, col=1)

    i += 1


  fig.update_layout(
          showlegend=False,
          autosize=True,
          #width=650,
          height=315,
          margin=dict(
              l=0,
              r=0,
              b=30,
              t=50,
              pad=0),
              plot_bgcolor='white',
              paper_bgcolor="white",
              )

  # yaxis
  fig.update_yaxes(title_text="Monto del apoyo ($)", row=1, col=1)
  fig.update_yaxes(title_text="Monto del apoyo ($)", row=2, col=1)
  fig.update_xaxes(title_text="Entidad", automargin = True, row=2, col=1)



  # format the layout
  fig.update_layout(showlegend=False, )

  return fig

# tabla 
def create_table_mun(base, entidad_sel):
  df_filter = base.copy()
  # filtro por año y por producto y entidad
  df_table1 = df_filter[df_filter['nom_ent']==entidad_sel]\
    .groupby(['nom_ent','Tamaño del productor','GMM'])\
    .agg({'cve_loc':np.size,
          #'Volumen incentivado (Litros / Toneladas)':np.mean,
          'Monto de apoyo total $':[np.mean, np.sum]})

  # round
  #df_table1['Volumen incentivado (Litros / Toneladas)'] = np.round(df_table1['Volumen incentivado (Litros / Toneladas)'],2)
  df_table1['Monto de apoyo total $'] = np.round(df_table1['Monto de apoyo total $'],2)
  # change column name
  df_table1.columns = [i[0] +'('+ i[1] + ')' for i in df_table1.columns]
  df_table1 = df_table1.reset_index()
  # gráfico
  fig = go.Figure()
  fig.add_traces(data=[
      go.Table(
          header=dict(values=['Ent','Tamaño Productor', 'Grado Marginación', 'No. Benef.', 'Monto Apoyo (prom.)', 'Monto Apoyo (total)'], font=dict(color='white', size=9)),
          cells=dict(values=[df_table1[col] for col in df_table1.columns.to_list()], align='left', font=dict(color='black', size=8)))
      ])
  fig.update_layout(
        showlegend=False,
        autosize=True,
        #width=420,
        height=810,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0),
            plot_bgcolor='white',
            paper_bgcolor="white",
            )

  return fig

 
#####################################################################
@app.callback(Output("boxplot_ent", "figure", allow_duplicate=True),
              Input("states", "click_feature"),
              State('producto', 'value'),
              State('anio', 'value'),
              prevent_initial_call=True,
        )

def create_boxplot(feature, producto_sel, anio_sel):
    # obtiene estado
    state = str(feature["properties"]["name"])
    df_filter = df.copy() 
    
    df_filter = df_filter[df_filter['cultivo']==producto_sel]
    df_filter = df_filter[df_filter['year']==int(anio_sel)]
    # define orden con base en la variable col
    fig = boxplot(base=df_filter, by='nom_ent', col='Monto de apoyo total $', entidad=state)
        
    return fig

# barplot entidad
@app.callback(Output("barplot_ent", "figure", allow_duplicate=True),
              Input("states", "click_feature"),
              State('producto', 'value'),
              State('anio', 'value'),
              prevent_initial_call=True,
    )

def create_boxplot(feature, producto_sel, anio_sel):
    # obtiene estado
    state = str(feature["properties"]["name"])
    df_filter = df.copy() 
    
    df_filter = df_filter[df_filter['Producto']==producto_sel]
    df_filter = df_filter[df_filter['Anio']==int(anio_sel)]
    # define orden con base en la variable col
    fig = barplot(base=df_filter, by='nom_ent', col='Monto de apoyo total $', entidad=state)
        
    return fig


# callback table
@app.callback(Output("table_ent", "figure", allow_duplicate=True),
              Input("states", "click_feature"),
              State('producto', 'value'),
              State('anio', 'value'),
              prevent_initial_call=True,
    )
def tabla(feature, producto_sel, anio_sel):
    
    state = str(feature["properties"]["name"])
    df_filter = df.copy() 
    
    df_filter = df_filter[df_filter['Producto']==producto_sel]
    df_filter = df_filter[df_filter['Anio']==int(anio_sel)]
    # define orden con base en la variable col
    fig = create_table_mun(df_filter,state)
        
    
    return fig
    




# Contenido por mapa
content_mapa1 = html.Div(dl.Map(center=[22.76, -102.58], zoom=5,
             id="mapa1", attributionControl=False,  style={'width': '100%', 'height': '100vh', 'backgroundColor':'white', 'margin': "auto", "display": "block"}),
)

# content_mapa1 = html.Div([
#         dl.Map(center=[22.76, -102.58], zoom=5, children=[base_mapa1, info]
#            , id="mapa1", style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
#         #html.Div(id="state"), html.Div(id="info2")
#     ])

#content_mapa2 = html.Div(id="mapa2")

content_mapa2 = html.Div(dl.Map(center=[22.76, -102.58], zoom=5,
             id="mapa2", attributionControl=False,  style={'width': '100%', 'height': '100vh', 'backgroundColor':'white', 'margin': "auto", "display": "block"}),
)

#  Btn regrasa a Nacional
# @app.callback(Output('submit-button', 'n_clicks'),
#               Input("btn_nacional", "n_click"))
#               #State('producto', 'value'),
#               #State('anio', 'value'))
# def regresa_nacional(click):
#     return click

# @app.callback(Output("info2", "children"),
#               Input("states", "click_feature"))
#               #State('producto', 'value'),
#               #State('anio', 'value'))
# def info_hover(feature):
#     return get_info2(feature)

##   CALLBACK : MAPA
@app.callback(
        Output('mapa1', 'children', allow_duplicate=True),
        Input('submit-button', 'n_clicks'),
        #Input('grado_marginacion', 'value'),
        Input("beneficiarios-opciones", "value"),
        #Input("radio-centros", "value"),
        Input("transfer-list-simple", "value"),
        State('producto', 'value'),
        State('anio', 'value'),
        prevent_initial_call=True,
    )

def actualizar_mapa1(clicks, benef_sel, transfer_sel, producto_sel, anio_sel):
    
    # capas
    capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
    margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
    tproductor = [item['label'] for item in transfer_sel[1] if item['group']=='Tamaño Productor']
    # bases
    productores_filter = base_productores.copy()
    # filtro por productores > 0
    productores_filter = productores_filter[productores_filter['productores']>0]
    productores_filter = productores_filter[productores_filter['latitud']>0]
    productores_filter = productores_filter.dropna(subset='entidad', axis=0)
    # filtro por cultivo
    productores_filter = productores_filter[productores_filter['cultivo']==producto_sel]
    #productores_filter = productores_filter[productores_filter['year']==int(anio_sel)]
    productores_filter = productores_filter[productores_filter['gm'].isin(margin)]
    #productores_filter = productores_filter[productores_filter['TAMPROD'].isin(tproductor)]
    centros = base_centros.copy()
    centros['year'] = centros['year'].astype('int')
    centros = centros[centros['gm'].isin(margin)]
    centros = centros[centros['year']==int(anio_sel)]
    
    # beneficiarios
    benef_filter = base_beneficiarios_mun_tprod.copy()
    benef_filter = benef_filter[benef_filter['cultivo'] == producto_sel]
    benef_filter = benef_filter[benef_filter['year'] == int(anio_sel)]
    benef_filter = benef_filter[benef_filter['gm'].isin(margin)]
    benef_filter = benef_filter[benef_filter['tipo'].isin(tproductor)]
     
    
    return mapa1(clicks, benef_sel, transfer_sel, producto_sel, anio_sel, capas_sel, productores_filter, centros, benef_filter)


 # capa base
capa_base = dl.Pane(dl.GeoJSON(data=data2,  # url to geojson file
                        options=dict(style=style_handle),  # how to style each polygon
                        zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                        zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
                        hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2), #2e4053
                        hoverStyle=arrow_function(dict(weight=4, fillColor='#000066', color='#000066',opacity=0.1, fillOpacity=1, dashArray='1')),  # style applied on hover
                        id='states'), style={'zIndex':0}) 
    
######### Mapa criterios simulados   ################
##   CALLBACK : MAPA
@app.callback(  
        Output('mapa2', 'children', allow_duplicate=True),
        Input('submit-button', 'n_clicks'),
        Input('criterios1', 'value'),
        #Input('chip-beneficiarios', 'value'),
        #Input("beneficiarios-opciones", "value"),
        #Input("radio-centros", "value"),
        #Input("transfer-list-simple", "value"),
        State('producto', 'value'),
        State('anio', 'value'),
        prevent_initial_call=True,
        #prevent_initial_call=True,
    )

# def actualizar_mapa2(clicks, margin_sel, benef_sel,capas_sel, transfer_sel, producto_sel, anio_sel):
def actualizar_mapa2(clicks, criterios_sel, producto_sel, anio_sel):
    
    # capas
    #capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
    #margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']

    # if isinstance(criterios_sel, str):
    #     criterios = [criterios_sel]
    # else:
    #     criterios = criterios_sel
    # nivel de marginación
    # if isinstance(margin_sel, str):
    #     margin = [margin_sel]
    # else:
    #     margin = margin_sel

    productores_filter = base_productores.copy()
    # filtro por productores > 0
    productores_filter = productores_filter[productores_filter['productores']>0]
    #productores_filter = productores_filter[productores_filter['latitud']>0]
    productores_filter = productores_filter.dropna(subset='entidad', axis=0)
    # filtro por cultivo
    productores_filter = productores_filter[productores_filter['cultivo']==producto_sel]
    #productores_filter = productores_filter[productores_filter['year']==int(anio_sel)]
    
    #productores_filter = productores_filter[productores_filter['year']==int(anio_sel)]
    #productores_filter = productores_filter[productores_filter['gm'].isin(margin)]
    
    #productores_filter = productores_filter[productores_filter['year']==int(anio_sel)]

    # base beneficiarios
    benef_filter = base_beneficiarios_mun_tprod.copy()
    benef_filter = benef_filter[benef_filter['cultivo'] == producto_sel]

    #benef_filter = benef_filter[benef_filter['cultivo'] == producto_sel]
    benef_filter = benef_filter[benef_filter['year'] == int(anio_sel)]
    benef_filter.dropna(subset = ['latitud', 'longitud'], inplace=True)
    
    # base productores
    # se seleccionan los registros por criterio seleccionado
    # if criterios == "Criterio de Marginación":
    #     productores_filter = base_productores.dropna(columns=['Escenario1'])
    # else:
    #  criterio de precio
    #  productores_filter = base_productores.dropna(columns=['Escenario2'])

    #productores_filter = productores_filter[productores_filter['GM_2020'].isin(margin)].dropna(axis=0)


    # # opción de beneficiarios
    # if benef_sel=='Número de Beneficiarios':
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio,fillOpacity=1,fillColor=color, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'], benef_filter['GMMcolor'])])
    # else:
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['MONTO_APOYO_TOTALradio'], benef_filter['GMMcolor'])])
    
    # Beneficiarios 
    def beneficiarios_popup(ent, mun, gmargina, numbenef, monto):
        
            result = html.Div([
                html.Div([
                    html.Img(id='image-poblacion_beneficiaria2', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
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
    # beneficiarios = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=radio,dashArray=1, fillOpacity=0, color='blue', children=[
    #             dl.Popup("Municipio: {}".format(mun))
    #             ]) for mun, lat, lon, radio in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'])]), name='panel20', checked=True)
    
    # opción para agregar criterio del precio y marginación 
    if criterios_sel == 'Marginación':
        productores_filter = productores_filter[productores_filter['escenario_marginacion']>0]
        # productores = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=np.log(radio), fillOpacity=0, color='#ee2a16', children=[
        #     dl.Popup("Municipio: {}".format(mun))
        #     ]) for lat, lon, mun, radio in zip(productores_filter['LAT_DECIMAL'],productores_filter['LON_DECIMAL'], productores_filter['NOM_MUN'], productores_filter['TotalProductores'])]), name='Marginación', checked=True)
    else:
        productores_filter = productores_filter[productores_filter['escenario_precio']>0]
    
    # productores = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=np.log(radio), fillOpacity=0, color='#ee2a16', children=[
    #     dl.Popup("Municipio: {}".format(mun))
    #     ]) for lat, lon, mun, radio in zip(productores_filter['LAT_DECIMAL'],productores_filter['LON_DECIMAL'], productores_filter['NOM_MUN'], productores_filter['TotalProductores'])]), name='Precio',  checked=True)
    # capas
    # Productores
    productores = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=np.log(numprod), color='#E12726', children=[
        dl.Tooltip(f"Productores: {mun}-{ent}"),
        dl.Popup(productores_popup(ent,mun,gmargina,numprod))
        ]) for lat, lon, ent, mun, gmargina, numprod in zip(productores_filter['latitud'],productores_filter['longitud'], productores_filter['cve_ent'], productores_filter['cve_mun'], productores_filter['gm'], productores_filter['productores'])]), name='Productores', checked=True)

    # capas por defecto
    capas = []
    # se agregan capas
    #if benef_sel == ["Beneficiarios"]:
    capas.extend([
                #info_escenarios_marginacion,
                info,
                capa_base,
                beneficiarios,
                productores
                ])   
    #else:   
        # capas.extend([
        #          info_escenarios_marginacion,
        #          info,
        #          capa_base,
        #          productores]) 
        
    # mapa
    tab2_mapa_content = html.Div([
        dl.Map(center=[22.76, -102.58], zoom=5,
               children=dl.LayersControl(capas, position='bottomright')
               , attributionControl=False, style={'width': '100%', 'height': '100vh','backgroundColor':'white', 'margin': "auto", "display": "block"}),
            #html.Div(id="state"), html.Div(id="info2")
        ])
    
    # elif capas_sel == ['Centros de Acopio']:
    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         # color : color del perimetro del hover
    #                         # dashArray : tipo de linea
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')), # color de fondo
    #                         id='states'),
    #             #benef_option,
    #             dl.Pane([dl.Circle(center=[lat, lon], radius=2, color='red', children=[
    #                             dl.Popup("Municipio: {}".format(mun))
    #                             ]) for lat, lon, mun in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_MUN'])]),
    #             #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])
    # elif capas_sel == ['Productores']:

    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         # color : color del perimetro del hover
    #                         # dashArray : tipo de linea
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')), # color de fondo
    #                         id='states'),
    #             #benef_option,
    #             dl.Pane([dl.CircleMarker(center=[lat, lon], radius=np.log(radio), color='black', children=[
    #                             dl.Popup("Municipio: {}".format(mun))
    #                             ]) for lat, lon, mun, radio in zip(productores_filter['LAT_DECIMAL'],productores_filter['LON_DECIMAL'], productores_filter['NOM_MUN'], productores_filter['TotalProductores'])]),
    #             #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])
    # elif capas_sel == ['Volumen Producción']:
    #     # Si el producto es del año 2019 y Leche, grafica fondo blanco
    #     #   en caso contrario fondo en verde degradado.
    #     #   Valor de cero para anio-producto dibuja fondo declarado en hoverStyle

    #     # opciones para anio:2019 y producto Leche, ya que no existen datos
    #     if int(anio_sel) == 2019 and producto_sel == 'Leche':
    #         colorprop = 1
    #         estilo = style2
    #     else:
    #         colorprop = f'{anio_sel}-{producto_sel}'
    #         estilo = style

    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop),
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')),  # style applied on hover
    #                         id='states'),
    #             #benef_option,           #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])
    # else:
    #     # opciones para anio:2019 y producto Leche, ya que no existen datos
    #     if int(anio_sel) == 2019 and producto_sel == 'Leche':
    #         colorprop = 1
    #         estilo = style2
    #     else:
    #         colorprop = f'{anio_sel}-{producto_sel}'
    #         estilo = style2

    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file
    #                         options=dict(style=style_handle),  # how to style each polygon
    #                         zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                         zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                         hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')),  # style applied on hover
    #                         hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop),
    #                         id='states'),
    #             # benef_option,
    #             # dl.Pane([dl.Circle(center=[lat, lon], radius=6, color='red', children=[
    #             #                 dl.Popup("Municipio: {}".format(mun))
    #             #                 ]) for lat, lon, mun in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_MUN'])]),
    #             # #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])

    # Base
    # base = dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                 options=dict(style=style_handle),  # how to style each polygon
    #                 zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                 zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                 # color : color del perimetro del hover
    #                 # dashArray : tipo de linea 
    #                 # #154360
    #                 hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                 hoverStyle=arrow_function(dict(weight=4, fillColor='#4e203a', color='#4e203a',opacity=0.1, fillOpacity=0.9, dashArray='2')), # color de fondo
    #                 id='states')

    # # opción de beneficiarios
    # def benef_choice(benef_sel):
    #     if benef_sel=='Número de Beneficiarios':
    #         benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=(radio),fillOpacity=1,fillColor=color, color=color, children=[
    #             dl.Popup("Municipio: {}".format(mun))
    #             ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'], benef_filter['GMMcolor'])])
    #     else:
    #         benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=(radio), color=color, children=[
    #             dl.Popup("Municipio: {}".format(mun))
    #             ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['MONTO_APOYO_TOTALradio'], benef_filter['GMMcolor'])])

    #     return benef_option

    # # capa de beneficiarios
    # beneficiarios = benef_choice(benef_sel)

    # # productores
    # # productores = dl.Pane([dl.Circle(center=[lat, lon], radius=2, color='black', children=[
    # #                                 dl.Popup("Municipio: {}".format(mun))
    # #                                 ]) for lat, lon, mun in zip(productores_filter['LAT_DECIMAL'], productores_filter['LON_DECIMAL'], productores_filter['NOM_MUN'])])

    # # Productores
    # productores = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=2, color='black', children=[
    #     dl.Popup("Municipio: {}".format(mun))
    #     ]) for lat, lon, mun in zip(productores_filter['LAT_DECIMAL'], productores_filter['LON_DECIMAL'], productores_filter['NOM_MUN'])])

    # volumen producción
    # def volumenProduccion_choice(producto, anio):
    #     anio_sel = anio
    #     producto_sel = producto
    #     # condition for year
    #     if int(anio_sel) == 2019 and producto_sel == 'Leche':
    #         colorprop = 1
    #         estilo = style2
    #     else:
    #         colorprop = f'{anio_sel}-{producto_sel}'
    #         estilo = style
    #     # layer
    #     volumen_produccion = dl.GeoJSON(data=data2,  # url to geojson file
    #                                 options=dict(style=style_handle),  # how to style each polygon
    #                                 zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                                 zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                                 hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop), #2e4053
    #                                 hoverStyle=arrow_function(dict(weight=4, fillColor='#4e203a', color='#4e203a',opacity=0.1, fillOpacity=0.9, dashArray='1')),  # style applied on hover
    #                                 id='states')

    #     return volumen_produccion

    #volumen_produccion = volumenProduccion_choice(producto_sel, anio_sel)

    # diccionarios de capas
    # layers = {
    #     #'Base': base,
    #     'Beneficiarios': beneficiarios,
    #     'Productores': productores,
    #     #'Centros de Acopio': centros,
    #     #'Volumen Producción': volumen_produccion
    # }

    # # class MAP
    # class Map():
    #     # constructor
    #     def __init__(self, background_style):
    #         self.base_layer = [dl.TileLayer(url=background_style),
    #                             colorbar,
    #                             info,
    #                             base]
    #     # function
    #     def add(self, features):
    #         # add layers
    #         for feature in features:
    #             self.base_layer.append(layers[feature])

    #         return self.base_layer
    # # background style del mapa
    # children_layer = Map(background_style=style1).add(criterios_sel)

    # tab2_mapa_content = html.Div([
    #     dl.Map(center=[22.76, -102.58], zoom=5, children=children_layer
    #        ,style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
    #     #html.Div(id="state"), html.Div(id="info2")
    # ])

    return tab2_mapa_content

