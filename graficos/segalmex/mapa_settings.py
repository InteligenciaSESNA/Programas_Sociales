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



# background del mapa
bstyle = "https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png"
# grey style
bstyle1 = 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
# black style
bstyle3 = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'


# propiedades del mapa
####  Propiedades del MAPA
classes = [0, 1000,3000,5000,10000, 100000, 1000000, 3000000] #   #FF7F50
colorscale = ['#ffffe5','#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#005a32'] # '#0B5345'
# fillcolor : color de relleno de cada estado  
style2 = dict(weight=1, opacity=0.9, fillColor='#D4E6F1', color='white', dashArray='1', fillOpacity=0.9)
# fillOpacity : transparencia de color de relleno
style = dict(weight=1, opacity=0.9, fillColor='#f5cba7', color='white', dashArray='1', fillOpacity=0.9)
# estilo centros de acopio
#  color: color de fondo
style0 = dict(weight=1, opacity=0.9 ,color='#EBF5FB', dashArray='1', fillOpacity=0.9)
# Create colorbar.
ctg = ["{}+".format(millify(cls), classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(millify(classes[-1]))]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft", unit='/Ton')
# Geojson rendering logic, must be JavaScript as it is executed in clientside
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")


# cuadros de información con logo de cada estado
def get_info(feature=None):
    # Valores por defecto a nivel nacional
    #header = [html.H4("Beneficiarios")]
    #monto_apoyo_ent = base_entidad[base_entidad['NOM_ENT']==feature["properties"]["name"]]['MONTO_APOYO_TOTALsum'].sum()

    if not feature:
        return [
            html.H4("{}".format("Nacional")),
            dmc.Center(html.Img(id='image', src='../assets/entidades/Nacional.png', width="65", height="65"))]
        # valores a nivel estatal
    return [
            html.H4("{}".format(feature["properties"]["name"])),
            #html.Br(),
            #html.B("Estado"), ": ",
            #html.A("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/entidades/'+ str(feature["properties"]["name"]) +'.png', width="65", height="65")),
          ]

def get_info2(feature=None):
    # Valores por defecto a nivel nacional
    #header = [html.H4("Beneficiarios")]
    #monto_apoyo_ent = base_entidad[base_entidad['NOM_ENT']==feature["properties"]["name"]]['MONTO_APOYO_TOTALsum'].sum()

    if not feature:
        return html.Center([
            dbc.Col(html.Img(src='../assets/entidades/Nacional.png', height="90px")),
            dbc.Col(dmc.Text('Nacional', id='nacional', align="center", weight=700), style={'fontSize':40}),
        ])
    #[
    #        dmc.Center(html.H4("{}".format("Nacional"))),
    #        dmc.Center(html.Img(id='image', src='../assets/Nacional.png', width="65", height="65"))]
    # valores a nivel estatal
    return html.Center([
            dbc.Col(html.Img(id='image', src='../assets/entidades/'+ str(feature["properties"]["name"]) +'.png', width="65", height="90")),
            dbc.Col(html.H1("{}".format(feature["properties"]["name"]))),
        ])
    
    
# 
# Information
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

#info2 = html.Div(children=get_info2(), id="info2", className="info2",
#                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})

# muestra la simbología de grados de marginación 
info_grado_marginacion = html.Div([
    dbc.Row(dmc.Text("Grado de marginación:  ",weight=600, size=12, color='#4e203a', style={'marginBottom':'2px'})),
    dbc.Row([
        dbc.Col(dmc.Text([DashIconify(icon="bi:circle-fill", width=18, color='#084594', height=18), " Muy alto  ", " ",
                          DashIconify(icon="bi:circle-fill", width=18, color='#2171b5', height=18), " Alto  ", " ",
                          DashIconify(icon="bi:circle-fill", width=18, color='#4292c6', height=18), " Medio  ", " ",
                          DashIconify(icon="bi:circle-fill", width=18, color='#6baed6', height=18), " Bajo  ", " ",
                          DashIconify(icon="bi:circle-fill", width=18, color='#9ecae1', height=18), " Muy bajo  "], size=10, )),
       ], style={'marginBottom':'6px'}),
    #dbc.Row(dmc.Text("Volumen de producción (Ton/Lts): ",weight=600, size=14, color='#4e203a', style={'marginTop':'3px'})),
], style={'opacity':'0.9', "position": "absolute", "bottom": "88px", "left": "10px", "z-index": "2000"})

# muestra la simbología de beneficiarios número y monto
info_num_benef = html.Div([
    dbc.Row(dmc.Text("Núm. Beneficiarios/Monto del Apoyo:  ",weight=600, size=12, color='#4e203a', style={'marginBottom':'2px'})),
    dbc.Row([
        dbc.Col(dmc.Text(["Menor ", 
                          DashIconify(icon="mdi:code-less-than", width=14, color='black', height=14),  " ",
                          DashIconify(icon="bi:circle-fill", width=2, color='black', height=2),  " ",
                          DashIconify(icon="bi:circle-fill", width=4, color='black', height=4),  " ",
                          DashIconify(icon="bi:circle-fill", width=6, color='black', height=6),  " ",
                          DashIconify(icon="bi:circle-fill", width=8, color='black', height=8),  " ",
                          DashIconify(icon="bi:circle-fill", width=10, color='black', height=10),  " ",
                          DashIconify(icon="bi:circle-fill", width=14, color='black', height=14),  " ",
                          DashIconify(icon="mdi:code-greater-than", width=14, color='black', height=14), " Mayor  "], size=10, )),
       ], style={'marginBottom':'6px'}),
    #dbc.Row(dmc.Text("Volumen de producción (Ton/Lts): ",weight=600, size=14, color='#4e203a', style={'marginTop':'3px'})),
], style={'opacity':'0.9', "position": "absolute", "bottom": "140px", "left": "10px", "z-index": "2000"})


# título del volumen de producción
info_vol_prod = html.Div([
    dbc.Row(dmc.Text("Volumen de producción (Ton/Lts): ",weight=600, size=12, color='#4e203a', style={'marginTop':'3px'})),
], style={'opacity':'0.9', "position": "absolute", "bottom": "63px", "left": "10px", "z-index": "2000"})


# muestra la simbología de escenarios
info_escenarios_marginacion = html.Div([
    dbc.Row(dmc.Text("Beneficiarios:",weight=600, size=12, color='#4e203a', style={'marginBottom':'2px'})),
    dbc.Row([
        dbc.Col(dmc.Text([DashIconify(icon="akar-icons:circle", width=18, color='#1a5276', height=18), "Observados", " ",
                          DashIconify(icon="akar-icons:circle", width=18, color='#ee2a16', height=18), "Hipotéticos", " "], size=10)),
       ], style={'marginBottom':'6px', 'paddingBottom':'1rem'}),
    dbc.Row(dmc.Text("Monto del Apoyo:  ",weight=600, size=12, color='#4e203a', style={'marginBottom':'2px'})),
    dbc.Row([
        dbc.Col(dmc.Text(["Menor ", 
                          DashIconify(icon="mdi:code-less-than", width=14, color='black', height=14),  " ",
                          DashIconify(icon="bi:circle-fill", width=2, color='black', height=2),  " ",
                          DashIconify(icon="bi:circle-fill", width=4, color='black', height=4),  " ",
                          DashIconify(icon="bi:circle-fill", width=6, color='black', height=6),  " ",
                          DashIconify(icon="bi:circle-fill", width=8, color='black', height=8),  " ",
                          DashIconify(icon="bi:circle-fill", width=10, color='black', height=10),  " ",
                          DashIconify(icon="bi:circle-fill", width=14, color='black', height=14),  " ",
                          DashIconify(icon="mdi:code-greater-than", width=14, color='black', height=14), " Mayor  "], size=10, )),
       ], style={'marginBottom':'6px'}),
    #dbc.Row(dmc.Text("Volumen de producción (Ton/Lts): ",weight=600, size=14, color='#4e203a', style={'marginTop':'3px'})),
], style={'opacity':'0.9', "position": "absolute", "bottom": "20px", "left": "10px", "z-index": "2000"})

# muestra la simbología de productores
info_productores = html.Div([
    dbc.Row(dmc.Text("(*) Productores se encuentran en escala logarítmica",weight=600, size=10, color='#4e203a', style={'marginTop':'3px'})),
], style={'opacity':'0.9', "position": "absolute", "bottom": "18px", "right": "50px", "z-index": "2000"})

    