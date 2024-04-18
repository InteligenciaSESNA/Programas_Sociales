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
from path import root
from graficos.segalmex.mapa_settings import classes, colorscale, colorbar, style0, style, style2, ctg, style_handle
from graficos.segalmex.mapa_settings import get_info, get_info2
from graficos.segalmex.mapa_settings import info, info_escenarios_marginacion, info_num_benef, info_grado_marginacion, info_productores, info_vol_prod

#json.load(open(root +'/datasets/sample3.json'))
#data2 = json.load(open(root +'/datasets/sample4.json'))
data2 = json.load(open(root +'/datasets/geoVolProd.json'))
estados_url = pd.read_excel(root + '/datasets/estados.xlsx')
# georeferencia municipal
#data3= json.load(open(root +'/datasets/sample5.json', "r", encoding="utf-8"))

##################################################################################
#                                    MAPA 1
#  Contiene información relativa a:
#   - Beneficiarios: Número y monto
#   - Centros de acopio
#   - Productores
#   - Volumen de Poroducción

# contenido mapas
# Base
base = dl.Pane(dl.LayerGroup(dl.GeoJSON(data=data2,  # url to geojson file  #283747
                options=dict(style=style_handle),  # how to style each polygon
                zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
                # color : color del perimetro del hover
                # dashArray : tipo de linea 
                # #154360
                hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
                hoverStyle=arrow_function(dict(weight=4, fillColor='#000066', color='#000066',opacity=0.1, fillOpacity=0.9, dashArray='2')), # color de fondo
                id='states')), name="base", style={'zIndex':1})

# volumen producción
def volumenProduccion_choice(producto, anio):
    anio_sel = anio
    producto_sel = producto
    # condition for year
    if int(anio_sel) == 2019 and producto_sel == 'Leche':
        colorprop = 1
        estilo = style2
    elif int(anio_sel) == 2022 and producto_sel == 'Leche':
        colorprop = 1
        estilo = style2
    else:
        colorprop = f'{anio_sel}-{producto_sel}'
        estilo = style
    # layer
    volumen_produccion = dl.Pane(dl.LayerGroup(dl.GeoJSON(data=data2,  # url to geojson file
                                options=dict(style=style_handle),  # how to style each polygon
                                zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                                zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
                                hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop), #2e4053
                                hoverStyle=arrow_function(dict(weight=4, fillColor='#000066', color='#000066',opacity=0.1, fillOpacity=0.9, dashArray='1')),  # style applied on hover
                                id='states')), name='Volumen Producción', style={'zIndex':2})

    return volumen_produccion


# # actualiza infor en mapa
# @app.callback(Output("state_choice", "children"),
#               Input("states", "click_feature"),
#               State('producto', 'value'),
#               State('anio', 'value'))
# def info_hover(feature):
#     return get_info(feature)
# ###  nivel municipio
# def state_choice(feature):
#     #anio_sel = anio
#     #producto_sel = producto
#     state = str(feature["properties"]["id"])
#     data = data3
#     data = data3['features'][:]['properties']['cve_ent'] == state
#     # condition for year
#     # if int(anio_sel) == 2019 and producto_sel == 'Leche':
#     #     colorprop = 1
#     #     estilo = style2
#     # else:
#     #     colorprop = f'{anio_sel}-{producto_sel}'
#     #     estilo = style
#     # layer
#     volumen_produccion = dl.Pane(dl.LayerGroup(dl.GeoJSON(data=data,  # url to geojson file
#                                 options=dict(style=style_handle),  # how to style each polygon
#                                 zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
#                                 zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
#                                 hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop), #2e4053
#                                 hoverStyle=arrow_function(dict(weight=4, fillColor='#000066', color='#000066',opacity=0.1, fillOpacity=0.9, dashArray='1')),  # style applied on hover
#                                 id='states')), name='Volumen Producción', style={'zIndex':2})

#     return volumen_produccion



def mapa1(clicks, benef_sel, transfer_sel, producto_sel, anio_sel, capas_sel, productores_filter, centros, benef_filter):

    
    # if isinstance(capas_sel, str):
    #     capas = [capas_sel]
    # else:
    #     capas = capas_sel
    # nivel de marginación
    # if isinstance(margin_sel, str):
    #     margin = [margin_sel]
    # else:
    #     margin = margin_sel


    # # opción de beneficiarios
    # if benef_sel=='Número de Beneficiarios':
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio,fillOpacity=1,fillColor=color, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['nom_mun'], benef_filter['latitud'], benef_filter['longitud'], benef_filter['NUM_BENEFradio'], benef_filter['gm_color'])])
    # else:
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['nom_mun'], benef_filter['latitud'], benef_filter['longitud'], benef_filter['monto_total_radio'], benef_filter['gm_color'])])


    # # opción centros de acopio y de producción
    # if capas_sel == ['Beneficiarios']:
    #     tab2_mapa_content = html.Div([
    #         dl.Map(center=[22.76, -102.58], zoom=5, children=[
    #             dl.TileLayer(url=style1),
    #             colorbar,
    #             info,
    #             dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                          options=dict(style=style_handle),  # how to style each polygon
    #                          zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                          zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                          # color : color del perimetro del hover
    #                          # dashArray : tipo de linea
    #                          hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                          hoverStyle=arrow_function(dict(weight=4, color='#154360', dashArray='2')), # color de fondo
    #                          id='states'),
    #             benef_option,
    #             #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])

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
    #                             ]) for lat, lon, mun in zip(centros['latitud'],centros['longitud'], centros['nom_mun'])]),
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
    #                             ]) for lat, lon, mun, radio in zip(productores_filter['latitud'],productores_filter['longitud'], productores_filter['nom_mun'], productores_filter['TotalProductores'])]),
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
    #             #                 ]) for lat, lon, mun in zip(centros['latitud'],centros['longitud'], centros['nom_mun'])]),
    #             # #dl.GeoJSON(url="https://gist.githubusercontent.com/mcwhittemore/1f81416ff74dd64decc6/raw/f34bddb3bf276a32b073ba79d0dd625a5735eedc/usa-state-capitals.geojson", id="capitals"),  # geojson resource (faster than in-memory)
    #             #dl.GeoJSON(url="https://raw.githubusercontent.com/SESNA-Inteligencia/Dashboard-1_1/master/datasets/estadosMexico.json", id="states",
    #             #           hoverStyle=arrow_function(dict(weight=5, color='#5D6D7E', dashArray=''))),  # geobuf resource (fastest option)
    #             ],style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, id="map"),
    #             #html.Div(id="state"), html.Div(id="info2")
    #         ])

    # Beneficiarios 
    def beneficiarios_popup(ent, mun, gmargina, numbenef, monto):
        
            result = html.Div([
                html.Div([
                    html.Img(id='image-poblacion_beneficiaria2', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
                    dmc.Text('BENEFICIARIO(S)', weight=400,color='#4e203a'),
                ], style={'textAlign': 'center'}),
                
                dmc.Divider(size="xs"),
                dbc.Row([
                    dmc.Text(['Estado: ',html.A(ent, href=str(estados_url[estados_url['nom_ent']==ent]['Liga'].to_list()[0]),  target="_blank")]),
                    dmc.Text(['Municipio: ', mun]),
                    dmc.Text(['Grado de marginación: ', gmargina]),
                    dmc.Space(h=4),
                    dmc.Text(['Núm. Beneficiarios: ', numbenef]),
                    dmc.Text(['Monto total del apoyo: ', f'$ {prettify(np.round(monto,2))}']),
                    dmc.Space(h=2),
                ])
                
                ])
            return result 
        
    # Centros de acopio 
    def centros_popup(ent, mun,loc, gmargina):
        
            result = html.Div([
                html.Div([
                    html.Img(id='image-centros-acopio2', src='../assets/centrosAcopio.png', width="65", height="65"),
                    dmc.Text('CENTRO(S) DE ACOPIO', weight=400, color='#4e203a'),
                ], style={'textAlign': 'center'}),
                 
                dmc.Divider(size="xs"),
                dbc.Row([
                    dmc.Text(['Estado: ',ent]), #html.A(ent, href=str(estados_url[estados_url['cve_ent']==ent]['Liga'].to_list()[0]), target="_blank")
                    dmc.Text(['Municipio: ', mun]),
                    dmc.Text(['Localidad: ', loc]),
                    dmc.Space(h=4),
                    dmc.Text(['Grado de marginación: ', gmargina]),
                    dmc.Text(['No. Centros: ', 1]),

                ])
                
                ])
            return result     
    
    # Total productores 
    def productores_popup(ent, mun,gmargina,numprod):
        
            result = html.Div([
                html.Div([
                    DashIconify(icon="noto-v1:man-farmer", width=65, height=65),
                    dmc.Text('PRODUCTORES', weight=400, color='#4e203a'),
                ], style={'textAlign': 'center'}),
                
                dmc.Divider(size="xs"),
                dbc.Row([
                    dmc.Text(['Estado: ',ent]),
                    dmc.Text(['Municipio: ', mun]),
                    dmc.Space(h=4),
                    dmc.Text(['Grado de marginación: ', gmargina]),
                    dmc.Text(['No. Productores : ', prettify(numprod)]),

                ])
                
                ])
            return result
    
    # opción de beneficiarios
    def benef_choice(benef_sel):
        #benef_filter = base
        if benef_sel == 'Número de Beneficiarios':
            benef_option = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=radio,fillOpacity=1,fillColor=color, color=color, children=[
                #dl.Popup("Municipio: {}".format(mun))
                dl.Tooltip(f"Beneficiario(s): {mun}-{ent}"),
                dl.Popup(beneficiarios_popup(ent, mun, gmargina, numbenef, monto))
                ]) for ent, mun, lat, lon, radio, color, gmargina, numbenef, monto in zip(benef_filter['entidad'], benef_filter['municipio'], benef_filter['latitud'], benef_filter['longitud'], benef_filter['benef_total_radio'], benef_filter['gm_color'], benef_filter['gm'], benef_filter['benef_total'], benef_filter['monto_total'])]), name='Beneficiarios', checked=True)
        else:
            benef_option = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=radio, fillOpacity=0, color=color, children=[
                #dl.Popup("Municipio: {}".format(mun))
                dl.Tooltip(f"Beneficiario(s): {mun}-{ent}"),
                dl.Popup(beneficiarios_popup(ent, mun, gmargina, numbenef, monto))
                ]) for ent, mun,  lat, lon, radio, color, gmargina, numbenef, monto in zip(benef_filter['entidad'], benef_filter['municipio'], benef_filter['latitud'], benef_filter['longitud'], benef_filter['monto_total_radio'], benef_filter['gm_color'], benef_filter['gm'], benef_filter['benef_total'], benef_filter['monto_total'])]), name='Beneficiarios', checked=True)
        return benef_option
    
    # capa de beneficiarios
    beneficiarios = benef_choice(benef_sel)
    # Centro de acopio
    centros = dl.Overlay(dl.LayerGroup([dl.Marker(position=[lat, lon], icon=dict(iconUrl='../assets/centrosAcopio.png',iconSize=[8, 12]), children=[
                                    dl.Tooltip(f"Centro(s) de acopio: {mun}-{ent}"),
                                    dl.Popup(centros_popup(ent, mun,loc, gmargina))
                                    ]) for lat, lon,ent, mun, loc, gmargina in zip(centros['latitud'],centros['longitud'], centros['entidad'], centros['municipio'], centros['localidad'], centros['gm'])]), name='Centros de Acopio', checked=True)

    # Productores
    productores = dl.Overlay(dl.LayerGroup([dl.CircleMarker(center=[lat, lon], radius=np.log(numprod), color='#E12726', children=[
        dl.Tooltip(f"Productores: {mun}-{ent}"),
        dl.Popup(productores_popup(ent, mun,gmargina,numprod))
        ]) for lat, lon, ent, mun, gmargina, numprod in zip(productores_filter['latitud'],productores_filter['longitud'], productores_filter['entidad'], productores_filter['municipio'], productores_filter['gm'], productores_filter['productores'])]), name='Productores', checked=True)

    # # Base
    # state_choice = dl.Pane(dl.LayerGroup(dl.GeoJSON(data=data2,  # url to geojson file
    #                             options=dict(style=style_handle),  # how to style each polygon
    #                             zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                             zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                             hideout=dict(colorscale=colorscale, classes=classes, colorProp='white'), #2e4053
    #                             hoverStyle=arrow_function(dict(weight=4, fillColor='#000066', color='#000066',opacity=0.1, fillOpacity=0.9, dashArray='1')),  # style applied on hover
    #                             id='states')), name='states', style={'zIndex':3})

    
    

    # volumen producción
    volumen_produccion = volumenProduccion_choice(producto_sel, anio_sel)

    # diccionarios de capas
    layers = {
        #'Base': base,
        'Beneficiarios': beneficiarios,
        'Productores': productores,
        'Centros de Acopio': centros,
        'Volumen Producción': volumen_produccion
    }
    
    # class MAP
    def Capas(features):
        # constructor
        # def __init__(self, background_style=bstyle):
        base_layer = [#dl.TileLayer(),
                      #dl.GestureHandling(),
                      #dl.EasyButton(icon="fa fa-home fa-fw", id="btn_nacional"),
                      # #html.Button("Zoom in", id="zoom_in"),
                      #dl.FullScreenControl(),
                      base,
                      info,
                      ]
        # function
        # def add(self, features):
            # add layers
        for feature in features:
            #self.
            base_layer.append(layers[feature])
            if feature == 'Centros de acopio':
                
                base_layer.append(info_grado_marginacion)
            if feature == 'Beneficiarios':
                
                base_layer.append(info_num_benef)
                base_layer.append(info_grado_marginacion)
            if (feature == 'Productores'):
                
                base_layer.append(info_productores)
            if feature == 'Volumen Producción':
                
                base_layer.append(info_vol_prod)
                base_layer.append(colorbar)
               
                # if (feature == 'Beneficiarios') or (feature == 'Productores') or (feature == 'Centros de Acopio'):
                #     self.base_layer.append(info_grado_marginacion)
            
        return base_layer
        
    # background style del mapa
    children_layer = Capas(capas_sel)
    # dl.LayersControl([dmc.Text('Muy Bajo')])
    tab2_mapa_content = html.Div([
        dl.Map(center=[22.76, -102.58], zoom=5, children=dl.LayersControl(children_layer, position='topleft')
           , attributionControl=False,  style={'width': '100%', 'height': '100vh', 'backgroundColor':'white', 'margin': "auto", "display": "block"}),
        #html.Div(id="state"), html.Div(id="info2")
    ])
        
    return tab2_mapa_content
