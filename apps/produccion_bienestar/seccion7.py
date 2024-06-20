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
from graficos.produccion_bienestar.mapa_settings import get_info



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


data2 = json.load(open(root +'/datasets/geoVolProd.json'))
# base lista de url's de todos los estados
estados_url = pd.read_excel(root + '/datasets/estados.xlsx', converters={'cve_ent':str})
# base de beneficiarios por entidad
base_beneficiarios_ent = pd.read_excel(root + '/datasets/produccion_bienestar_ent.xlsx', converters={'cve_ent':str})
# base de beneficiarios por municipios
base_beneficiarios_mun = pd.read_excel(root + '/datasets/produccion_bienestar_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str})
# base centros de acopio por entidad
base_centros_ent = pd.read_excel(root + '/datasets/centros_acopio_entidad.xlsx', converters={'cve_ent':str, 'cve_mun':str})
# base centros de acopio por municipio
base_centros_mun = pd.read_excel(root + '/datasets/centros_acopio_mun.xlsx', converters={'cve_ent':str, 'cve_mun':str})
# base de productores
base_productores = pd.read_excel(root + '/datasets/TotalProductores.xlsx')
#
base_poblacion_indigena_ent = pd.read_excel(root + '/datasets/pueblos_indigenas_ent.xlsx')





#########      CALL : Cuenta centros de acopio  ################
def get_card_poblacion_indigena(app):
    
    @app.callback(# 'click_feature
        Output('prod_resumen-poblacion-indigena', 'children'),
        Input('prod_submit-button', 'n_clicks'),
        Input("prod_states", "click_feature"),
        Input("prod_transfer-list-simple", "value"),
        State('prod_producto', 'value'),
        State('prod_anio', 'value'),
    )

    def resumen_poblacion_indigena(clicks, feature, transfer_sel, producto_sel, anio_sel):

        # Nota:
        # existe un municipio sin grado de marginación
        # únicamente se mostraran los 5 grados de marginación
        # capas
        pob_indigena_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Población Indigena']

        # estado: feature["properties"]["name"]
        data = base_poblacion_indigena_ent.copy()
        #data = data[data['gm'].isin(margin)]
        #data = data[data['year'] == int(anio_sel)]
        #data = data[data['cultivo'] == producto_sel]
        #data = data[data['TAMPROD'].isin(tproductor)]
        # condición
        # if ('Centros de Acopio' not in capas_sel) or len(margin)==0:
        #     return '-'
        # else:
        if not feature:
            result = np.sum(data['num_tipo'])
        else:
            # filtro de estado
            data_filt = data[data['entidad'] == feature["properties"]["name"]]
            data_filt = data_filt[data_filt['tipo'].isin(pob_indigena_sel)]
            # Sin dato nombre de dato faltante
            result = np.sum(data_filt['num_tipo'])

        #res = result#"{:,}".format(result)
        return result

#########   CALL : Imagen Población beneficiaria / Monto Apoyo  ################
def get_card_poblacion_beneficiaria_img(app):
    
    @app.callback(# 'click_feature
            Output('prod_image-poblacion_beneficiaria', 'src'),
            Input('prod_beneficiarios-opciones', 'value'),
        )
    def resumen_benef_textImage(beneficiarios):

        # condición
        if beneficiarios == 'Número de Beneficiarios':
            #texto = "Pob. Beneficiaria"
            return '../assets/poblacionBeneficiaria.png'
        else:
            #texto = "Monto del Apoyo"
            return '../assets/dollar.svg'

#########   CALL : Regresa texto Población Benef / Monto del apoyo  ################
def get_card_poblacion_beneficiaria_texto(app):
    
    @app.callback(# 'click_feature
            Output('prod_resumen_texto_poblacion_beneficiaria', 'children'),
            Input('prod_beneficiarios-opciones', 'value'),
        )
    def resumen_benef_textImag2(beneficiarios):
        # condición
        if beneficiarios == 'Número de Beneficiarios':
            texto = "Población Beneficiaria"
        else:
            texto = "Monto Total del apoyo"

        return texto

#########  CALL : Regresa Cantidad Población Beneficiaria  ################
def get_card_poblacion_beneficiaria(app):
    
    @app.callback(
            Output('prod_resumen-poblacion_beneficiaria', 'children'),
            Input('prod_submit-button', 'n_clicks'),
            Input("prod_states", "click_feature"),
            Input('prod_beneficiarios-opciones', 'value'),
            Input("prod_transfer-list-simple", "value"),
            State('prod_producto', 'value'),
            State('prod_anio', 'value'),
        )

    # Resumen población beneficiaria 
    def resumen_pablacion_beneficiaria(clicks, feature, beneficiario, transfer_sel, sel_producto, sel_anio):

        # capas
        capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
        # grado de marginación
        margin_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
        # población indigena
        pob_indigena_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Población Indigena']
        # género
        sexo_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Sexo']
        # estado: feature["properties"]["name"]
        data = base_beneficiarios_ent.copy()
        #data = data.dropna(axis=0)
        data['monto_total'] = data['monto_total'].astype('float')
        # filtros
        data = data[data['year'] == int(sel_anio)]
        data = data[data['cultivo'] == sel_producto]
        data = data[data['gm'].isin(margin_sel)]
        data = data[data['sexo'].isin(sexo_sel)]
        data = data[data['tipo'].isin(pob_indigena_sel)]

        # Condición
        if ('Beneficiarios' not in capas_sel) or len(margin_sel)==0:
            return '-'
        else:
            if beneficiario == 'Número de Beneficiarios':
                if not feature:
                    result = np.round(np.sum(data['benef_total']),0)
                else:
                    # filtro de estado
                    data_filt = data[data['entidad'] == feature["properties"]["name"]]
                    # Sin dato nombre de dato faltante
                    result = np.round(np.sum(data_filt['benef_total']))

                return "{:,}".format(result)
            else:
                if not feature:
                    result = np.sum(data['monto_total'])
                else:
                    # filtro de estado
                    data_filt = data[data['entidad'] == feature["properties"]["name"]]
                    # Sin dato nombre de dato faltante
                    try:
                        result =  np.round(np.sum(data_filt['monto_total']))
                    except:
                        result = 0
                return millify(result, precision=1)


#########  CALL : Regresa Resumen Monto Promedio  ################
def get_card_monto_promedio(app):
    
    @app.callback(
            Output('prod_resumen-monto-promedio', 'children'),
            Input('prod_submit-button', 'n_clicks'),
            Input("prod_states", "click_feature"),
            Input("prod_transfer-list-simple", "value"),
            State('prod_producto', 'value'),
            State('prod_anio', 'value'),
        )

    def resumen_monto_promedio(clicks, feature, transfer_sel, sel_producto, sel_anio):

        # capas
        capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
        # grado de marginación
        margin_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
        # población indigena
        pob_indigena_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Población Indigena']
        # género
        sexo_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Sexo']
        # estado: feature["properties"]["name"]
        data = base_beneficiarios_ent.copy()
        #data = data.dropna(axis=0)
        data['monto_total'] = data['monto_total'].astype('float')
        # filtros
        data = data[data['year'] == int(sel_anio)]
        data = data[data['cultivo'] == sel_producto]
        data = data[data['gm'].isin(margin_sel)]
        data = data[data['sexo'].isin(sexo_sel)]
        data = data[data['tipo'].isin(pob_indigena_sel)]
        # condición
        if ('Beneficiarios' not in capas_sel) or len(margin_sel)==0:
            return '-'
        else:
            if not feature:
                result =  np.sum(data['monto_total']) / np.sum(data['benef_total']) #
                return millify(result, precision=1)
            else:
            # filtro de estado
                data_filt = data[data['entidad'] == feature["properties"]["name"]]
                # Sin dato nombre de dato faltante
                try:
                    if np.sum(data_filt['monto_total']) is None or np.sum(data_filt['benef_total']) is None:
                        return  0
                    result = np.sum(data_filt['monto_total']) / np.sum(data_filt['benef_total'])
                    return millify(result, precision=1)
                except:
                    return 0
                

#
def get_card_poblacion_mujeres(app):
    #########  CALL : Regresa Población de mujeres  ################
    @app.callback(
            Output('prod_resumen-poblacion-mujeres', 'children'),
            Input('prod_submit-button', 'n_clicks'),
            Input("prod_states", "click_feature"),
            Input("prod_transfer-list-simple", "value"),
            State('prod_producto', 'value'),
            State('prod_anio', 'value'),
        )
    def resumen_poblacion_mujeres(clicks, feature, transfer_sel, sel_producto, sel_anio):

        # capas
        capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
        # grado de marginación
        margin_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']
        # población indigena
        pob_indigena_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Población Indigena']
        # género
        #sexo_sel = [item['label'] for item in transfer_sel[1] if item['group']=='Sexo']
        # estado: feature["properties"]["name"]
        data = base_beneficiarios_ent.copy()
        #data = data.dropna(axis=0)
        data['monto_total'] = data['monto_total'].astype('float')
        # filtros
        data = data[data['year'] == int(sel_anio)]
        data = data[data['cultivo'] == sel_producto]
        data = data[data['gm'].isin(margin_sel)]
        data = data[data['tipo'].isin(pob_indigena_sel)]
        data_total = np.sum(data['benef_total'])
        data_muj = np.sum(data[data['sexo'] == 'M']['benef_total'])
        # condición
        if ('Beneficiarios' not in capas_sel) or len(margin_sel)==0:
            return '-'
        else:
            if not feature:
                result = data_muj
                return millify(result, precision=1)
            else:
                # filtro de estado
                data_filt = data[data['entidad'] == feature["properties"]["name"]]
                # Sin dato nombre de dato faltante
                data_total = np.sum(data_filt['benef_total'])
                data_muj = np.sum(data_filt[data_filt['sexo'] == 'M']['benef_total'])
                if data_muj == 0:
                    return 0
                else:
                    result =  data_muj 
                    return millify(result, precision=1)