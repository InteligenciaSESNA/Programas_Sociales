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

from path import root

#########################################################################################
#                                       Cards
#########################################################################################

"""
                                        Cards

    En esta sección se definen las tarjetas del mapa. Las tarjetas del mapa son valores que
resumen información de selección (año, producto, estado, nivel de marginación, y
tamaño productor):

    - Centros de acopio: muestra el número de centros de acopio 
    - Población beneficiaria: muestra el número de beneficiarios del programa
    - Vol Incentivado Total : muestra el volumen incentivado total (en toneladas o litros)
    - Vol Incentivado Promedio : muestra el volumen incentivado promedio (en toneladas o litros)    
"""
cultivos_cambios = {'Trigo grano':'Trigo',
                    'Maíz grano blanco':'Maíz',
                    'Arroz':'Arroz',
                    'Leche':'Leche',
                    'Frijol':'Frijol'}
# base .json de estados
data2 = json.load(open(root +'/datasets/geoVolProd.json'))
# base lista de url's de todos los estados
estados_url = pd.read_excel(root + '/datasets/estados.xlsx', converters={'cve_ent':str})
# base de beneficiarios por entidad
base_beneficiarios_ent_tprod = pd.read_excel(root + '/datasets/beneficiarios_ent.xlsx', converters={'cve_ent':str})
# base de beneficiarios por municipios
base_beneficiarios_mun_tprod = pd.read_excel(root + '/datasets/beneficiarios_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str})
base_beneficiarios_mun_tprod['tipo'] = [val.strip() for val in base_beneficiarios_mun_tprod['tipo']]
# base centros de acopio por entidad
base_centros_ent = pd.read_excel(root + '/datasets/centros_acopio_entidad.xlsx', converters={'cve_ent':str, 'cve_mun':str})
# base centros de acopio por municipio
base_centros_mun = pd.read_excel(root + '/datasets/centros_acopio_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str})


def get_card_centros_acopio(app):
    #########      CALL : Cuenta centros de acopio  ################
    @app.callback(# 'click_feature
        Output('resumen-centros_acopio', 'children'),
        Input('submit-button', 'n_clicks'),
        Input("states", "click_feature"),
        Input("transfer-list-simple", "value"),
        State('producto', 'value'),
        State('anio', 'value')
    )

    def resumen_centros_acopio(clicks, feature, transfer_sel, sel_producto, sel_anio):

        # Nota:
        # existe un municipio sin grado de marginación 
        # únicamente se mostraran los 5 grados de marginación 
        # capas
        capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
        # grado de marginación
        margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
        # tamaño del productor
        data = base_centros_mun.copy()
        data = data[data['gm'].isin(margin)]
        data = data[data['year'] == int(sel_anio)]
        
        #data = data[data['TAMPROD'].isin(tproductor)]
        # condición
        if ('Centros de Acopio' not in capas_sel) or len(margin)==0:
            return '-'
        else:
            if not feature:
                result = np.sum(data['num_centros'])  
            else:
                # filtro de estado
                data_filt = data[data['cve_ent'] == feature["properties"]["id"]]
                # Sin dato nombre de dato faltante
                result = np.sum(data_filt['num_centros'])
                
            res = "{:,}".format(result)
            return res
        
   
def get_card_poblacion_beneficiaria_img(app): 
    #########   CALL : Imagen Población beneficiaria / Monto Apoyo  ################
    @app.callback(
            Output('image-poblacion_beneficiaria', 'src'),
            Input('beneficiarios-opciones', 'value'),
        )
    def resumen_benef_textImage(beneficiarios):

        # condición
        if beneficiarios == 'Número de Beneficiarios':
            #texto = "Pob. Beneficiaria"
            return '../assets/poblacionBeneficiaria.png'
        else:
            #texto = "Monto del Apoyo"
            return '../assets/dollar.svg'


def get_card_poblacion_beneficiaria_texto(app): 
    #########   CALL : Regresa texto Población Benef / Monto del apoyo  ################
    @app.callback(# 'click_feature
            Output('resumen_texto_poblacion_beneficiaria', 'children'),
            Input('beneficiarios-opciones', 'value'),
        )
    def resumen_benef_textImag2(beneficiarios):
        # condición
        if beneficiarios == 'Número de Beneficiarios':
            texto = "Población Beneficiaria"
        else:
            texto = "Monto Total del apoyo"

        return texto


def get_card_poblacion_beneficiaria(app): 
    #########  CALL : Regresa Cantidad Población Beneficiaria  ################
    @app.callback(
            Output('resumen-poblacion_beneficiaria', 'children'),
            Input('submit-button', 'n_clicks'),
            Input("states", "click_feature"),
            Input('beneficiarios-opciones', 'value'),
            Input("transfer-list-simple", "value"),
            State('producto', 'value'),
            State('anio', 'value')
        )

    def resumen_pablacion_beneficiaria(clicks, feature, beneficiario, transfer_sel, sel_producto, sel_anio):

        # capas
        capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
        # grado de marginación
        margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
        # tamaño del productor
        tproductor = [item['label'] for item in transfer_sel[1] if item['group']=='Tamaño Productor']
        
        # estado: feature["properties"]["name"]
        data = base_beneficiarios_ent_tprod.copy()
        data['monto_total'] = data['monto_total'].astype('float')
        # filtros
        data = data[data['year'] == int(sel_anio)]
        data = data[data['cultivo'] == sel_producto]
        data = data[data['gm'].isin(margin)]
        data = data[data['tipo'].isin(tproductor)]

        # Condición
        if ('Beneficiarios' not in capas_sel) or len(margin)==0:
            return '-'
        else:
            if beneficiario == 'Número de Beneficiarios':
                if not feature:
                    result = np.round(np.sum(data['benef_total']),0)
                else:
                    # filtro de estado
                    data_filt = data[data['cve_ent'] == feature["properties"]["id"]]
                    # Sin dato nombre de dato faltante
                    result = np.round(np.sum(data_filt['benef_total']))

                return "{:,}".format(result)
            else:
                if not feature:
                    result = np.sum(data['monto_total'])
                else:
                    # filtro de estado
                    data_filt = data[data['cve_ent'] == feature["properties"]["id"]]
                    # Sin dato nombre de dato faltante
                    result =  np.round(data_filt['monto_total'])

                return millify(result, precision=1)



def get_card_volumen_incentivado(app): 
    #########  CALL : Regresa Monto Volumne Incentivado  ################
    @app.callback(
            Output('resumen-volumen_incentivado_total', 'children'),
            Input('submit-button', 'n_clicks'),
            Input("states", "click_feature"),
            Input("transfer-list-simple", "value"),
            State('producto', 'value'),
            State('anio', 'value')
        )

    def resumen_volumen_incentivado_total(clicks, feature, transfer_sel, sel_producto, sel_anio):

        # capas
        capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
        # grado de marginación
        margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
        # tamaño del productor
        tproductor = [item['label'] for item in transfer_sel[1] if item['group']=='Tamaño Productor']
        
        # estado: feature["properties"]["name"]
        # filtros
        data = base_beneficiarios_mun_tprod.copy()
        data['monto_total'] = data['monto_total'].astype('float')
        # filtros
        data = data[data['year'] == int(sel_anio)]
        data = data[data['cultivo'] == sel_producto]
        data = data[data['gm'].isin(margin)]
        data = data[data['tipo'].isin(tproductor)]
        # condición
        if ('Beneficiarios' not in capas_sel) or len(margin)==0:
            return '-'
        else:
            if not feature:
                result = np.sum(data['volincentivado_total']) 
            else:
                # filtro de estado
                data_filt = data[data['cve_ent'] == feature["properties"]["id"]]
                # Sin dato nombre de dato faltante
                result = np.sum(data_filt['volincentivado_total'])
                
        return millify(result, precision=1)

# 
def get_card_volumen_incentivado_promedio(app): 
    #########  CALL : Regresa Monto Volumen Incentivado Promedio  ################
    @app.callback(
            Output('resumen-volumen_incentivado_promedio', 'children'),
            Input('submit-button', 'n_clicks'),
            Input("states", "click_feature"),
            Input("transfer-list-simple", "value"),
            State('producto', 'value'),
            State('anio', 'value')
        )
    def resumen_volumen_incentivado_promedio(clicks, feature, transfer_sel, sel_producto, sel_anio):

        # capas
        capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
        # grado de marginación
        margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
        # tamaño del productor
        tproductor = [item['label'] for item in transfer_sel[1] if item['group']=='Tamaño Productor']
        
        # estado: feature["properties"]["name"]
        # filtros
        data = base_beneficiarios_mun_tprod.copy()
        data['monto_total'] = data['monto_total'].astype('float')
        # filtros
        data = data[data['year'] == int(sel_anio)]
        data = data[data['cultivo'] == sel_producto]
        data = data[data['gm'].isin(margin)]
        data = data[data['tipo'].isin(tproductor)]
        # condición
        if ('Beneficiarios' not in capas_sel) or len(margin)==0:
            return '-'
        else:
            if not feature:
                result = np.sum(data['volincentivado_total'])/np.sum(data['benef_total'])
                return millify(result, precision=1)  
            else:
                # filtro de estado
                data_filt = data[data['entidad'] == feature["properties"]["name"]]
                # Sin dato nombre de dato faltante
                if np.sum(data_filt['volincentivado_total']) == 0:
                    return 0
                else:
                    result = np.sum(data_filt['volincentivado_total'])/np.sum(data_filt['benef_total']) 
                    return millify(result, precision=1)