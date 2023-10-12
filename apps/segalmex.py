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
# import folium
# from folium.plugins import HeatMap
# from folium.plugins import MarkerCluster
from costumFunctions import make_dataframe_state_mun
import sys
import pymysql
import reglas_operacion



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

#import plotly.io as pio
#pio.renderers.default = 'firefox'


# CONFIG BASE DATOS (No activo)
#hostname="localhost"
#dbname=["nombre bases separadas por comas"]
#uname="root"
#pwd="myadmin"

# --- Only run on the server
#engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname[0], user=uname, pw=pwd))
#base = pd.read_sql(sql="select * from", con = engine, index_col="Date", parse_dates=True)

# introducir directorio de la carpeta
root = "C:/Users/jcmartinez/Desktop/Dashboard3"
#root = "/home/ubuntu/Desktop/Proyecto/ProgramasSociales"
# urls
#repo_est_url = ""
#estados_json = open(root + '/datasets/estadosMexico.json')
#mx_est_geo = json.load(estados_json)

json.load(open(root +'/datasets/sample.json'))
data2 = json.load(open(root +'/datasets/sample3.json'))

# base completa
# base_2019 = pd.read_excel(root + '/datasets/PBeneficiarios_data_2019.xlsx')
# base_2020 = pd.read_excel(root + '/datasets/PBeneficiarios_data_2020.xlsx')
# base_2021 = pd.read_excel(root + '/datasets/PBeneficiarios_data_2021.xlsx')


# bases Beneficiarios estado
base_entidad = pd.read_excel(root + '/datasets/base_entidad.xlsx')
base_entidad_tprod = pd.read_excel(root + '/datasets/base_entidad_tprod.xlsx')
# bases Beneficiarios Municipio
base_municipios = pd.read_excel(root + '/datasets/base_municipio3.xlsx')
base_municipios_tprod = pd.read_excel(root + '/datasets/base_municipio_tprod3.xlsx')
# base productores municipio
#base_productores_filter = pd.read_excel(root + '/datasets/baseTotalproductores.xlsx')
# bases de centros de acopio a nivel entidad y municipal
centros_entidad = pd.read_excel(root + '/datasets/centros_entidad.xlsx')
centros_municipio = pd.read_excel(root + '/datasets/centros_municipio2.xlsx')
# base productores
base_productores = pd.read_excel(root + '/datasets/TotalProductores2.xlsx')
# base resumen introduccion
base_resumen = pd.read_excel(root + '/datasets/resumen_montos.xlsx')

# sample maps P
# blue style
bstyle = "https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png"
# grey style
bstyle1 = 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png'
# black style
bstyle3 = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
# base centros de acopio
#df_centros = pd.read_excel(root + '/datasets/base_centros_inegi.xlsx')
#df_centros = df_centros

# base producción agrícola
#df_produccion = pd.read_excel(root + '/datasets/base_prodAgricola_con_claves_inegi.xlsx')
#df_produccion = df_produccion.dropna()
# georeferenciación de base producción - estados
#df_prod_est = pd.read_csv(root + '/datasets/produccion_estados.csv')

# opciones
list_year = ['2019', '2020', '2021']
list_products = ['Arroz', 'Frijol', 'Leche', 'Maíz', 'Trigo']
list_grado_marginacion = [['Muy bajo', 'blue'],
                          ['Bajo','indigo'],
                          ['Medio', 'green'],
                          ['Alto', 'red'],
                          ['Muy alto', 'orange',
                           'No disponible', 'yellow']]

list_tamano_productor = ['Pequeño', 'Mediano', 'Grande']
list_states = base_entidad['NOM_ENT'].unique()
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
    ],
]

list_criterios = ['Marginación', 'Precio']

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

# change color to click on state

# style_handle2 = assign("""function(feature, context){
#     const match = context.props.hideout &&  context.props.hideout.properties.name === feature.properties.name;
#     if(match) return {weight:1, fillColor:'#4e203a', color:'white', opacity:0.9 fillOpacity=0.9, dashArray:'1'};
# }""")

# app.clientside_callback("function(feature){return feature}", 
#                         Output("states", "hideout"), 
#                         [Input("states", "click_feature")])

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


# descripción de escenarios 
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

# información sobre los productores
info_productores = html.Div([
    dbc.Row(dmc.Text("(*) Productores se encuentran en escala logarítmica",weight=600, size=10, color='#4e203a', style={'marginTop':'3px'})),
], style={'opacity':'0.9', "position": "absolute", "bottom": "18px", "right": "50px", "z-index": "2000"})



######################################################################
####                 Header
######################################################################

# seccion 1 : header
seccion1 = html.Div([
    dbc.Row([
        dbc.Col([#dbc.NavbarBrand("Programa de Precios de Garantía",
                 #        style={'color':'white', 'font-size': '60px', 'textAlign':'center'}),
                dmc.Text("Programa de Precios de Garantía a", weight=500,size=30, color='white'),
                #html.Br(),
                dmc.Text("Productos Alimentarios Básicos",  weight=600, size=60, color='white')],
                style = {'textAlign':'center', 'color':'white', 'marginBottom':'5rem', 'marginTop':'6rem'} ),
    ], className='col-12'),
    # dbc.Row([
    #     dbc.Col([], className='col-5'),
    #     dbc.Col([], className='col-4'),
    #     dbc.Col([
    #         dmc.Button("Resumen Ejecutivo",
    #             id="open",
    #             leftIcon=DashIconify(icon="ant-design:read-outlined"),
    #             color="orange",
    #             n_clicks=0),
    #     ], className='col-3', style={'marginBottom':'2rem', 'paddingRight':'2rem'})
    # ], className='twelve columns'),
], className="twelve columns",  style={'opacity':'0.95','background-blend-mode':'overlay','background-image': 'url(/assets/maiz-mexico.jpg)','background-size': '100%','backgroundColor': '#2a3240', 'm':'0px', 'padding':'0px', 'height': '100%', 'padding':'2rem'})

##################################################################
#                          Introducción
##################################################################
seccion2 = html.Div([
    dbc.Row([
        dbc.Col([
            dmc.Paper(
                children=[
                    dmc.Text("¿Qué es el Programa Precios de Garantía a Productos Alimentarios Básicos?", size=24, color='white', align="justify"),
                    html.Br(),
                    dmc.Text("El Programa de Precios de Garantía a Productos Alimentarios Básicos forma parte de los Programas Prioritarios del Gobierno Federal que buscan brindar una atención integral a las problemáticas vinculadas con la autosuficiencia alimentaria, se encuentra a cargo de la Secretaría de Agricultura y Desarrollo Rural y es operado por uno de sus organismos descentralizados, Seguridad Alimentaria Mexicana (SEGALMEX).", color='white', align="justify"),
                    html.Br(),
                    dmc.Text("El objetivo general del Programa Precios de Garantía es complementar el ingreso de los pequeños y medianos productores agropecuarios de granos básicos y leche.", color='white', align="justify")],
                shadow="xs",
                style={'backgroundColor':'#2a3240'}
            ),
        ], className= 'col-xl-6 col-12',style={'backgroundColor':'#2a3240', 'padding':'2rem'}),
        #dmc.Divider(orientation="vertical", style={"height": 20}),
        dbc.Col([
            dmc.Text("Diagrama general de la dinámica del programa", size=24, color='white', align="center"),
            dmc.Image(src="/assets/logo10.svg",width='100%', withPlaceholder=True)
        ], className='col-xl-6 col-12',style={'padding':'2rem', 'margin':'0rem'}),
    ], className='col-12', style={'backgroundColor':'#2a3240'}),
], style={'marginTop':'5rem', 'backgroundColor':'#2a3240'})


#####  SECCIÓN : REGLAS DE OPERACIÓN
seccion3 = html.Div([
    dmc.Text("Recursos ejercidos en el Programa,", size=55, weight=600, color='#4e203a', align="center", style={'paddingBottom':'0rem'}),
    dmc.Text("por tipo de producto y año fiscal", size=45, weight=500, color='#4e203a', align="center", style={'marginBottom':'2rem'}),
    dmc.Tabs([  
        dmc.TabsList([
            dmc.Tab("2019", value="2019"),
            dmc.Tab("2020", value="2020"),
            dmc.Tab("2021", value="2021"),
        ], style={'padding':'0.5rem','Color':'white','backgroundColor':'white'}),
    ],
    id="tabs-example",
    orientation='horizontal',
    color="#4e203a",        
    value="2019"
    ),
    
    html.Div(id="section3-content", className='col-12', style={'marginTop':'2rem','marginBottom':'2rem', 'paddingLeft':'2rem', 'paddingRight':'2rem'}), 
], className='col-12', style={'paddingTop':'2rem','paddingBottom':'2rem','backgroundColor':'white'})


####   SECCIÓN : GRáfico resumen
# gráfico
def plot_section3(base, anio):
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # frontera eficiente
    df = base[base['Anio']==anio]
    montos = df['Monto_label'] #[millify(monto,) for monto in df['Monto']]

    fig.add_trace(go.Bar(
        x=df['Producto'].to_list(),
        y=df['Monto'].to_list(),
        text= montos,
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
        height=300,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=60,
            pad=0),
            plot_bgcolor='white',
            paper_bgcolor="white",
            )


    fig.update_layout(
        title="Monto de apoyos por producto",
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
    fig.update_yaxes(
        title_text="<b>Monto del Apoyo ($)</b>", 
        secondary_y=False)
    # fig.update_yaxes(
    #     title_text="<b>Porcentaje acumulado (%)</b>", 
    #     secondary_y=True)
    # drop grids
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    
    fig.update_layout(title_text='Monto de apoyos por producto', title_x=0.5)
    #fig.update_layout(hovermode="y")
    fig.update_xaxes(tickangle=0)
    
    return fig

# Callback
@app.callback(Output("section3-content", "children"), 
              Input("tabs-example", "value"))
def render_content(active):
    
    base = base_resumen.copy()
    # filtro de año
    anio = int(active)
    #
    monto_active = plot_section3(base, anio)
    
    if active == "2019":
        result = dbc.Row([
                    dbc.Col([
                        dmc.Text("En el año 2019, se destinó un aproximado de $ 8 billones al programa de Precios de Garantía a Productos Alimentarios Básicos, cuyos destinatarios serían los productores de cinco productos: maíz, trigo, frijol, leche y arroz. Para el caso de maíz se destinó un monto de $ 4 billones, lo que representó aproximadamente el 53.1% del total y, en segundo lugar, la cantidad de $2 billones (28.4% del total) fue designada a los productores de trigo.", size=18, color='#797D7F', align="justify"),
                        dmc.Space(h=20),
                        dmc.Text("Los productores de frijol y leche recibieron un monto de $ 695 millones (8.6%) y $ 534 millones (6.6%), respectivamente. Por último, a los productores de arroz se destinó $ 260 millones, equivalente a 3.2% del monto total.", size=18, color='#797D7F', align="justify"),
                    ], className='card col-lg-6 col-12', style={'padding':'2rem', 'backgroundColor':'#fdfefe', 'border-radius': '5px', 'border-right': '2px solid #f8f9f9', 'border-left': '1px solid #f8f9f9', 'border-top': '1px solid #f8f9f9', 'border-bottom': '2px solid #f8f9f9'}),
                    dbc.Col([
                        html.Div([
                            dcc.Graph(figure=monto_active)    
                        ])
                    ], className='col-lg-6 col-12', style={'padding':'1rem'})
                ], className='col-12', align="center", style={'padding':'1rem'})
    elif active == "2020":
        result = dbc.Row([
                    dbc.Col([
                        dmc.Text("En el año 2020, se destinó un aproximado de $ 9.5 billones al programa de Precios de Garantía a Productos Alimentarios Básicos, lo que representa un aumento del 18.2% en comparación con el monto destinado en 2019. Los productores de maíz recibieron $ 6.7 billones del total del monto de 2020 (70.9% del total).", size=18, color='grey', align="justify"),
                        dmc.Space(h=20),
                        dmc.Text("Por su parte, a los productores de trigo se destinó $1 billón (13.3% de total), para el caso de los productores de leche, se destinó un monto de $ 1 billón, correspondiente al 10.9% del total. En cuarto lugar, se encuentra el arroz, producto que recibió en 2020 $ 353 millones (3.7% del monto total del año respectivo). Finalmente, el frijol recibió un monto de apoyo de $ 117 millones, es decir, un 1.23% del monto total destinado al programa en 2020.", size=18, color='grey', align="justify"),
                    ], className='card col-lg-6 col-12', style={'padding':'2rem', 'backgroundColor':'#fdfefe', 'border-radius': '5px', 'border-right': '2px solid #f8f9f9', 'border-left': '1px solid #f8f9f9', 'border-top': '1px solid #f8f9f9', 'border-bottom': '2px solid #f8f9f9'}),
                   dbc.Col([
                        html.Div([
                            dcc.Graph(figure=monto_active)    
                        ])
                    ], className='col-lg-6 col-12', style={'padding':'1rem'})
                ], className='col-12', align="center", style={'padding':'1rem'})
    elif active == "2021":
        result = dbc.Row([
                    dbc.Col([
                        dmc.Text("En el año 2021, se destinó un aproximado de $ 6.8 billones al Programa Precios de Garantía a Productos Alimentarios Básicos lo que representa una disminución del 27.7% en comparación con el monto destinado en 2020. Para el caso de maíz se otorgaron $4 billones, lo que representó aproximadamente el 60.4% del total.", size=18, color='grey', align="justify"),
                        dmc.Space(h=20),
                        dmc.Text("Respecto al frijol, se destinó $1.6 billones, lo que representa el 22.9% del total del monto destinado en 2021 al programa. Los productores de leche recibieron $ 523 millones, correspondiente al 7.5% del total. En cuarto lugar, se encuentra el trigo, producto que recibió en 2021 $ 424 millones (6.1% del monto total del año respectivo). Finalmente, el arroz recibió un monto de apoyo de $ 202 millones, es decir, un 2.9% del monto total destinado al programa en 2020.", size=18, color='grey', align="justify"),
                    ], className='card col-lg-6 col-12', style={'padding':'2rem', 'backgroundColor':'#fdfefe', 'border-radius': '5px', 'border-right': '2px solid #f8f9f9', 'border-left': '1px solid #f8f9f9', 'border-top': '1px solid #f8f9f9', 'border-bottom': '2px solid #f8f9f9'}),
                    
                    dbc.Col([
                        html.Div([
                            dcc.Graph(figure=monto_active)    
                        ])
                    ], className='col-lg-6 col-12', style={'padding':'1rem'})
                ], className='col-12', align="center", style={'display':'flex','padding':'1rem'})

    else:
        result = dmc.Text('No action!')
        
    return result



#####
# seccion3_1 = html.Div([
#     ####### SECCION : PIE PLOT
#     dmc.Card([
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
#             html.Iframe(id='pie-plot1', srcDoc=open(root + "/graficos/piePlot_2020.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "1200px"}),
#         ),
#     ],
#     withBorder=True,
#     style={'backgroundColor':'white', 'marginTop':'4rem', 'marginBottom':'2rem'}
#     ),
# ], className="flip-card-front", style={'paddingLeft':'2rem', 'paddingRight':'2rem','backgroundColor':'white', 'm':'0px', 'padding':'0px'})
        
#################################################################
#          Filtros principales (año -producto) - Descargas
#################################################################
seccion4 = html.Div([
    dbc.Row([
        # Primera columna : Vacia
        dbc.Col([
            dmc.Button(
                    "Instrucciones: ",
                    id="transition-instrucciones-btn",
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
                        id="anio",
                        data=list_year,
                        value='2020',
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
                        id="producto",
                        data=list_products,
                        value='Frijol',
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
                                id='submit-button',
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
        
        #  
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

##############################################################
#########           Descripción del mapa
##############################################################

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
        # ], ),
        #dmc.Divider(orientation="vertical", style={"height": 20}),
        # html.Div([
        #     dmc.Text("Diagrama general de la dinámica del programa", size=24, color='#2a3240'),
        #     dmc.Image(src="/assets/logo10.svg",width='100%', withPlaceholder=True)
        # ]),
        ], style={'paddingBottom':'2rem', 'paddingTop':'2rem'}),
    id="fade-transition",
    is_in=True,
    style={"transition": "opacity 2000ms ease"},
    timeout=2000,
    ),
], style={'paddingBottom':'2rem', 'paddingTop':'2rem','opacity':'0.95','background-blend-mode':'overlay','background-image': 'url(/assets/#)','background-size': '100%','backgroundColor': '#2a3240', 'm':'0px', 'padding':'0px', 'height': '100%'} )




##############################################################
#########                MAPA                         ########
##############################################################

####################      sidebar left: Barra de control
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
            ], className="card col-12 col-md-8", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 0px 0px 0px', 'border-radius': '10px', 'backgroundColor': '#BFC9CA', }
            ),
            dbc.Col([
                sidebar_right

            ], className="card col-12 col-md-4", style={'padding':'.0rem', 'marginTop':'0rem', 'marginRight':'0rem', 'boxShadow': '#e3e3e3 0px 0px 0px', 'border-radius': '0px', 'backgroundColor': 'white', }
            )
        ]),
        # Barra de control
    ], className="twelve columns", style={'backgroundColor': '#F4F6F6', 'marginLeft': '2rem', 'marginRight': '2rem','marginBottom': '4rem'}
    )


# backgroundColor': '#F4F6F6'
#############################################################
###            content2 - graficos barras
###    - Gráfico1 : Tamaño productor por estado
###    - Gráfico2 : Nivel de marginación por estado
#############################################################
#######################    content3 - gráficos por municipios

content2 = html.Div([
    dmc.Card(children=[
        dmc.CardSection(
            dmc.Group(
                children=[
                    dmc.Text("Review Pictures", weight=500),
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:overflow-menu-horizontal"),
                        color="gray",
                        variant="transparent",
                    ),
                ],
                position="apart",
            ),
            withBorder=True,
            inheritPadding=True,
            py="xs",
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
            html.Iframe(id="plot-r1", style={"height": "400px", "width": "1300px"}),
        ),
        # dmc.CardSection(children=[
        #         dmc.SimpleGrid(cols=2, children=[
        #             #dbc.Group([
        #                 # plot 1
        #                 dmc.Group([
        #                     dmc.CardSection(
        #                         dmc.Group(
        #                             children=[
        #                                 dmc.Text("Review Pictures", weight=500),
        #                                 dmc.ActionIcon(
        #                                     DashIconify(icon="carbon:overflow-menu-horizontal"),
        #                                     color="gray",
        #                                     variant="transparent",
        #                                 ),
        #                             ],
        #                             position="apart",
        #                         ),
        #                         withBorder=True,
        #                         inheritPadding=True,
        #                         py="xs",
        #                     ),
        #                     dmc.Text(
        #                         children=[
        #                             dmc.Text(
        #                                 "200+ images uploaded",
        #                                 color="blue",
        #                                 style={"display": "inline"},
        #                             ),
        #                             " since last visit, review them to select which one should be added to your gallery",
        #                         ],
        #                         mt="sm",
        #                         color="dimmed",
        #                         size="sm",
        #                     ),
        #                     dmc.CardSection(
        #                         html.Iframe(id="plot-r2", style={"height": "400px", "width": "800px"}),
        #                     ),
        #                 ]),
        #                 # plot 2
        #                 dmc.Group([
        #                     dmc.CardSection(
        #                         dmc.Group(
        #                             children=[
        #                                 dmc.Text("Review Pictures", weight=500),
        #                                 dmc.ActionIcon(
        #                                     DashIconify(icon="carbon:overflow-menu-horizontal"),
        #                                     color="gray",
        #                                     variant="transparent",
        #                                 ),
        #                             ],
        #                             position="apart",
        #                         ),
        #                         withBorder=True,
        #                         inheritPadding=True,
        #                         py="xs",
        #                     ),
        #                     dmc.Text(
        #                         children=[
        #                             dmc.Text(
        #                                 "200+ images uploaded",
        #                                 color="blue",
        #                                 style={"display": "inline"},
        #                             ),
        #                             " since last visit, review them to select which one should be added to your gallery",
        #                         ],
        #                         mt="sm",
        #                         color="dimmed",
        #                         size="sm",
        #                     ),
        #                     dmc.CardSection(
        #                         html.Iframe(id="plot-r3", style={"height": "400px", "width": "800px"}),
        #                     ),
        #                 ]),
        #                 #plot3
        #                 # dmc.Group([
        #                 #     dmc.CardSection(
        #                 #         dmc.Group(
        #                 #             children=[
        #                 #                 dmc.Text("Review Pictures", weight=500),
        #                 #                 dmc.ActionIcon(
        #                 #                     DashIconify(icon="carbon:overflow-menu-horizontal"),
        #                 #                     color="gray",
        #                 #                     variant="transparent",
        #                 #                 ),
        #                 #             ],
        #                 #             position="apart",
        #                 #         ),
        #                 #         withBorder=True,
        #                 #         inheritPadding=True,
        #                 #         py="xs",
        #                 #     ),
        #                 #     dmc.Text(
        #                 #         children=[
        #                 #             dmc.Text(
        #                 #                 "200+ images uploaded",
        #                 #                 color="blue",
        #                 #                 style={"display": "inline"},
        #                 #             ),
        #                 #             " since last visit, review them to select which one should be added to your gallery",
        #                 #         ],
        #                 #         mt="sm",
        #                 #         color="dimmed",
        #                 #         size="sm",
        #                 #     ),
        #                 #     dmc.CardSection(
        #                 #         html.Iframe(id="plot-r4", style={"height": "400px", "width": "400px"}),
        #                 #     ),
        #                 # ]),

        #             #], className='col-12'),
        #             # html.Iframe(id="plot-r2", style={"height": "300px", "width": "400px"}),
        #             # html.Iframe(id="plot-r3", style={"height": "300px", "width": "400px"}),
        #             #html.Iframe(id="plot-r4", style={"height": "300px", "width": "400px"}),
        #         ]),
        #     ],
        #     withBorder=True,
        #     inheritPadding=True,
        #     mt="sm",
        #     pb="md",
        # ),
        # dmc.CardSection(
        #     dmc.Group(
        #         children=[
        #             dmc.Text("Review Pictures", weight=500),
        #             dmc.ActionIcon(
        #                 DashIconify(icon="carbon:overflow-menu-horizontal"),
        #                 color="gray",
        #                 variant="transparent",
        #             ),
        #         ],
        #         position="apart",
        #     ),
        #     withBorder=True,
        #     inheritPadding=True,
        #     py="xs",
        # ),
        # dmc.Text(
        #     children=[
        #         dmc.Text(
        #             "200+ images uploaded",
        #             color="blue",
        #             style={"display": "inline"},
        #         ),
        #         " since last visit, review them to select which one should be added to your gallery",
        #     ],
        #     mt="sm",
        #     color="dimmed",
        #     size="sm",
        # ),
        # dmc.CardSection(
        #     html.Iframe(id="plot-r5", style={"height": "600px", "width": "1300px"}),
        # ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    className="col-12"),
    
    
],style={"paddin": '0rem', 'marginLeft':'2rem', 'marginRight':'2rem'})



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
        seccion2,
        # Resumen: Pie plot
        seccion3,
        # Filtros principales : Año - producto
        seccion5,
        # Introduccion
        seccion4,
        # Mapa
        seccion6,

        #####  SECCIÓN:  BARRA INDICADOR ESTADOS
        # dmc.Card([
        #     dbc.Row([
        #     #dbc.Col("", style={'marginLeft':'8px'}),
        #     dbc.Col(get_info2(), id="info2", md=4),
        #     dbc.Col([dbc.Row(dmc.Text('Año', id='anio_fijo', align="center")), dbc.Row(dmc.Text('2020', id='anio_filtro', align="center", weight=700))], style={'fontSize':40, 'marginTop':'1.2rem'}),
        #     dbc.Col([dbc.Row(dmc.Text('Producto', id='producto_fijo', align="center")), dbc.Row(dmc.Text('Arroz', id='producto_filtro', align="center", weight=700))], style={'fontSize':40, 'marginTop':'1.2rem'}),
        #     ]),
        # ],
        # withBorder=True,
        # shadow="sm",
        # radius="md",
        # style={'marginLeft':'1rem','marginRight':'1rem','backgroundColor': '#F4F6F6'}
        # ),

    
        
        #### SECCIÓN : GRAFICOS
        #content2,
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
        Output('anio_filtro2', 'children'),
        Output('anio_filtro1', 'children'),
        #Output('anio_filtro', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def anio(clicks, sel_producto, sel_anio):


    return sel_anio, sel_anio #, sel_anio

#########      CALL : Regresa producto  ################
@app.callback(# 'click_feature
        Output('producto_filtro2', 'children'),
        Output('producto_filtro1', 'children'),
        #Output('producto_filtro', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
    )
def producto(clicks, sel_producto, sel_anio):

    return sel_producto, sel_producto #, sel_producto

#########   CALL : Modal Reglas de operación  ################
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"),
     Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#########  CALL : Resumen Reglas de operación ################
@app.callback(
        Output('reglas-operacion', 'children'),
        Input('submit-button', 'n_clicks'),
        State('producto', 'value'),
        State('anio', 'value')
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
    Output("transition-instrucciones", "is_in"),
    [Input("transition-instrucciones-btn", "n_clicks")],
    [State("transition-instrucciones", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in

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
    
    
    # estado: feature["properties"]["name"]
    data = centros_municipio.copy()
    data = data[data['GM_2020'].isin(margin)]
    # condición
    if ('Centros de Acopio' not in capas_sel) or len(margin)==0:
        return '-'
    else:
        if not feature:
            result = np.sum(data['NUM_CENTROS'])  
        else:
            # filtro de estado
            data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
            # Sin dato nombre de dato faltante
            result = np.sum(data_filt['NUM_CENTROS'])
            
        res = "{:,}".format(result)

    return res
    
    
    
#########   CALL : Imagen Población beneficiaria / Monto Apoyo  ################
@app.callback(# 'click_feature
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

#########   CALL : Regresa texto Población Benef / Monto del apoyo  ################
@app.callback(# 'click_feature
        Output('resumen_texto_poblacion_beneficiaria', 'children'),
        Input('beneficiarios-opciones', 'value'),
    )
def resumen_benef_textImag2(beneficiarios):

    # condición
    if beneficiarios == 'Número de Beneficiarios':
        texto = "Pob. Beneficiaria"
    else:
        texto = "Monto del Apoyo"

    return texto

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

    data = base_municipios.copy()
    data['MONTO_APOYO_TOTALsum'] = data['MONTO_APOYO_TOTALsum'].astype('float')
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    data = data[data['GM_2020'].isin(margin)]
    # Condición
    if ('Beneficiarios' not in capas_sel) or len(margin)==0:
        return '-'
    else:
        if beneficiario == 'Número de Beneficiarios':
            if not feature:
                result = np.sum(data['NUM_BENEFsize'])
            else:
                # filtro de estado
                data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
                # Sin dato nombre de dato faltante
                result = np.sum(data_filt['NUM_BENEFsize'])

            return "{:,}".format(result)
        else:
            if not feature:
                result = np.sum(data['MONTO_APOYO_TOTALsum'])
            else:
                # filtro de estado
                data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
                # Sin dato nombre de dato faltante
                result = np.sum(data_filt['MONTO_APOYO_TOTALsum'].astype('float'))

            return millify(result, precision=1)




#                      CARD 3 : Monto apoyos total
# @app.callback(
#         Output('resumen-monto_apoyos_total', 'children'),
#         Input('submit-button', 'n_clicks'),
#         Input("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )
# def resumen_monto_apoyos_total(clicks, feature, sel_producto, sel_anio):

#     data = base_entidad.copy()
#     # filtros
#     data = data[data['Anio'] == int(sel_anio)]
#     data = data[data['Producto'] == sel_producto]

#     # Condición
#     if not feature:
#         result = np.sum(data['MONTO_APOYO_TOTALsum'])
#     else:
#         # filtro de estado
#         data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
#         # Sin dato nombre de dato faltante
#         result = np.sum(data_filt['MONTO_APOYO_TOTALsum'])
#     # millify(monto_apoyos, precision=2)
#     return millify(result, precision=1)

#                      CARD 4 : Monto apoyos promedio
# @app.callback(
#         Output('resumen_monto_apoyos_prom', 'children'),
#         Input('submit-button', 'n_clicks'),
#         Input("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )
# def resumen_monto_apoyos_promedio(clicks, feature, sel_producto, sel_anio):

#     data = base_entidad.copy()
#     # filtros
#     data = data[data['Anio'] == int(sel_anio)]
#     data = data[data['Producto'] == sel_producto]

#     # Condición
#     if not feature:
#         result = np.mean(data['MONTO_APOYO_TOTALsum'])
#     else:
#         # filtro de estado
#         data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
#         # Sin dato nombre de dato faltante
#         result = np.mean(data_filt['MONTO_APOYO_TOTALmean'])

#     # millify(monto_apoyos, precision=2)
#     return millify(result, precision=1)

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

    data = base_municipios.copy()
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    data = data[data['GM_2020'].isin(margin)]

    # condición
    if ('Beneficiarios' not in capas_sel) or len(margin)==0:
        return '-'
    else:
        if not feature:
            result = np.sum(data['VolumenIncentivadosum']) 
        else:
            # filtro de estado
            data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
            # Sin dato nombre de dato faltante
            result = np.sum(data_filt['VolumenIncentivadosum'])
            
        return millify(result, precision=1)
  


    # if not feature:
    #     result = np.sum(data['VolumenIncentivadosum'])
    # else:
    #     # filtro de estado
    #     data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
    #     # Sin dato nombre de dato faltante
    #     result = np.sum(data_filt['VolumenIncentivadosum'])
    # # millify(monto_apoyos, precision=2)
    # return millify(result, precision=1)

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

    data = base_municipios.copy()
    # filtros
    data = data[data['Anio'] == int(sel_anio)]
    data = data[data['Producto'] == sel_producto]
    data = data[data['GM_2020'].isin(margin)]
    
    # condición
    if ('Beneficiarios' not in capas_sel) or len(margin)==0:
        return '-'
    else:
        if not feature:
            result = np.sum(data['VolumenIncentivadosum'])/np.sum(data['NUM_BENEFsize'])  
        else:
            # filtro de estado
            data_filt = data[data['NOM_ENT'] == feature["properties"]["name"]]
            # Sin dato nombre de dato faltante
            if np.sum(data_filt['VolumenIncentivadosum']) == 0:
                result = 0
            else:
                result = np.sum(data_filt['VolumenIncentivadosum'])/np.sum(data_filt['NUM_BENEFsize']) 
            
        return millify(result, precision=1)
    # # condición para validar criterios de marginación: si la lista estpá vacia regresa '-'
    # if len(margin) == 0:
    #     return '-'
    # else:
    #     return '-'


# Descarga de resumen ejecutivo
# @app.callback(
#         Output("download", "data"),
#         Input("btn", "n_clicks"))
# def func(n_clicks):
#    return dcc.send_file("C:/Users/jcmartinez/Desktop/Dashboard3/salidas/RESUMEN EJECUTIVO PGPAB.pdf")

##########################################################################################
# SECCIÓN I :  mapa
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
        searchPlaceholder=['Agregar...', 'Remover...'],
        nothingFound=['Cannot find item to add', 'Cannot find item to remove'],
        placeholder=['No item left to add', 'No item left ro remove'],
        style={'fontSize':'10px','marginBottom':'0.5rem'}
    ),
    ############### Tablero resumen
    dmc.Card([
        #dmc.CardSection([
            dmc.SimpleGrid(cols=2,children=[
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
                                    dbc.Col([
                                        html.Img(id='image', src='../assets/centrosAcopio.png', width="65", height="65"),
                                    ],className="card col-3 border-0 bg-transparent", style={'paddin':'0px','marginTop':'0em', 'marginBottom':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='resumen-centros_acopio', style={'marginTop':'0em',"textAling":"center", "color":"red", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([html.Div([
                                            dmc.Text("Centros Acopio", color='grey', weight=500, align='center', style={"fontSize": 10}),
                                            ]),
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
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
                                        html.Img(id='image-poblacion_beneficiaria', src='../assets/poblacionBeneficiaria.png', width="65", height="65"),
                                    ],className="card col-3 border-0 bg-transparent", style={'margin':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='resumen-poblacion_beneficiaria', style={'marginTop':'0em',"textAling":"center", "color":"blue", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([html.Div([
                                            dmc.Text("Pob. Beneficiaria", id='resumen_texto_poblacion_beneficiaria', color='grey', weight=500, align='center', style={"fontSize": 11}),
                                            ]),
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                ], style={'fontSize':'12px'}),
                # Card 3 : Monto de apoyos
                dmc.Tooltip(
                        multiline=True,
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
                                        DashIconify(icon="emojione-monotone:balance-scale", width=60, height=60),
                                    ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "1,332",
                                        ], id='resumen-volumen_incentivado_total', style={'marginTop':'0em',"textAling":"center", "color":"green", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([html.Div([
                                            dmc.Text("Vol. Incentivado (Total)", color='grey', weight=500, align='center', style={"fontSize": 11}),
                                            ]),
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},),
                ], style={'fontSize':'11px'}),
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
                                        DashIconify(icon="emojione-monotone:balance-scale", width=60, height=60),
                                    ],className="card col-3 border-0 bg-transparent", style={'marginTop':'0em', 'textAlign': 'left'}),
                                    dbc.Col([
                                        dbc.Row([html.Center(html.Div([
                                        "51%",
                                        ], id='resumen-volumen_incentivado_promedio', style={'marginTop':'0em',"textAling":"center", "color":"grey", 'font-size': '32px'}),
                                        )]),
                                        dbc.Row([html.Div([
                                            dmc.Text("Vol. Incentivado (Prom)", color='gray', weight=500, align='center', style={"fontSize": 11}),
                                            ]),
                                        ]),
                                    ], className="card col-9 border-0 bg-transparent"),
                                ], style={'border-radius': '5px', 'paddin':'0rem'}),
                            ],
                            withBorder=True,
                            shadow="sm",
                            radius="md",
                            style={"width": 180, "padding":'0rem', 'backgroundColor': '#F4F6F6'},)
                ], style={'fontSize':'11px'}),
            ],style={"width": 360, "height": 160}
        ),
    ], style={'marginLeft':'0rem', 'paddingLeft':'0rem'}),

])

#  Pestaña de opciones (Transfer list - Criterios simulados)
tab2_capas_criterios = html.Div([
    dmc.Card([
        
        dmc.SimpleGrid(cols=2, children=[
            # selector criterios simulados
            # chipgroup
            dmc.ChipGroup([
                    dmc.Chip(
                        x,
                        value=x,
                        variant="outline",
                    )
                    for x in ["Observado"]
                ],
                align='center',
                id="chip-observado",
                value=[],
                multiple=True,
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
        ], style={'marginBottom':'6rem'}),
        
        
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
        
    ], style={'padding':'0rem', 'marginBottom':'4rem'}),

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
@app.callback(Output("content-capas-criterios", "children"),
              Output("mapa", "children"),
             [Input("capas-criterios", "value")])
def switch_tab(active):
    if active == "capas":
        return tab1_capas_criterios, content_mapa1
    elif active == "criterios":
        return tab2_capas_criterios, content_mapa2

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


####   actualiza tabla-Mapa
#########    CALL : Indicador estado (MAPA)  ################
@app.callback(# 'click_feature
        Output('state_label', 'children'),
        Input("states", "click_feature")
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
        return [
            html.H4("{}".format(feature["properties"]["name"])),
            dmc.Center(html.Img(id='image', src='../assets/'+ str(feature["properties"]["name"]) +'.png', width="65", height="65")),
          ]

# actualiza infor en mapa
@app.callback(Output("info", "children"),
              Input("states", "click_feature"))
              #State('producto', 'value'),
              #State('anio', 'value'))
def info_hover(feature):
    return get_info(feature)


# base mapa 1   
# base_m1 = dl.GeoJSON(data=data2,  # url to geojson file  #283747
#                     options=dict(style=style_handle),  # how to style each polygon
#                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
#                     zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
#                     # color : color del perimetro del hover
#                     # dashArray : tipo de linea 
#                     # #154360
#                     hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
#                     hoverStyle=arrow_function(dict(weight=4, fillColor='#C51503', color='#C51503',opacity=0.1, fillOpacity=0.9, dashArray='2')), # color de fondo
#                     id='states')

# contenido mapas
# Base
base = dl.GeoJSON(data=data2,  # url to geojson file  #283747
                options=dict(style=style_handle),  # how to style each polygon
                zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
                # color : color del perimetro del hover
                # dashArray : tipo de linea 
                # #154360
                hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
                hoverStyle=arrow_function(dict(weight=4, fillColor='#C51503', color='#C51503',opacity=0.1, fillOpacity=0.9, dashArray='2')), # color de fondo
                id='states')

# volumen producción
def volumenProduccion_choice(producto, anio):
    anio_sel = anio
    producto_sel = producto
    # condition for year
    if int(anio_sel) == 2019 and producto_sel == 'Leche':
        colorprop = 1
        estilo = style2
    else:
        colorprop = f'{anio_sel}-{producto_sel}'
        estilo = style
    # layer
    volumen_produccion = dl.GeoJSON(data=data2,  # url to geojson file
                                options=dict(style=style_handle),  # how to style each polygon
                                zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                                zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
                                hideout=dict(colorscale=colorscale, classes=classes, style=estilo, colorProp=colorprop), #2e4053
                                hoverStyle=arrow_function(dict(weight=4, fillColor='#C51503', color='#C51503',opacity=0.1, fillOpacity=0.9, dashArray='1')),  # style applied on hover
                                id='states')

    return volumen_produccion

# Contenido por mapa
content_mapa1 = html.Div(id="mapa1")

# content_mapa1 = html.Div([
#         dl.Map(center=[22.76, -102.58], zoom=5, children=[base_mapa1, info]
#            , id="mapa1", style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}),
#         #html.Div(id="state"), html.Div(id="info2")
#     ])

content_mapa2 = html.Div(id="mapa2")


 
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
        Output('mapa1', 'children'),
        Input('submit-button', 'n_clicks'),
        #Input('grado_marginacion', 'value'),
        Input("beneficiarios-opciones", "value"),
        #Input("radio-centros", "value"),
        Input("transfer-list-simple", "value"),
        State('producto', 'value'),
        State('anio', 'value'),
        #prevent_initial_call=True,
    )

# def actualizar_mapa2(clicks, margin_sel, benef_sel,capas_sel, transfer_sel, producto_sel, anio_sel):
def actualizar_mapa1(clicks, benef_sel, transfer_sel, producto_sel, anio_sel):

    # capas
    capas_sel = [item['label']  for item in transfer_sel[1] if item['group']=='Capa']
    margin = [item['label'] for item in transfer_sel[1] if item['group']=='Grado Marginación']

    # if isinstance(capas_sel, str):
    #     capas = [capas_sel]
    # else:
    #     capas = capas_sel
    # nivel de marginación
    # if isinstance(margin_sel, str):
    #     margin = [margin_sel]
    # else:
    #     margin = margin_sel
    productores_filter = base_productores.copy()
    productores_filter = productores_filter[productores_filter['Producto']==producto_sel]
    productores_filter = productores_filter[productores_filter['Anio']==int(anio_sel)]
    productores_filter = productores_filter[productores_filter['GM'].isin(margin)]
    centros = centros_municipio.copy()
    centros = centros_municipio[centros_municipio['GM_2020'].isin(margin)]
    benef_filter = base_municipios[base_municipios['Producto'] == producto_sel]
    benef_filter = benef_filter[benef_filter['Anio'] == int(anio_sel)]
    benef_filter = benef_filter[benef_filter['GM_2020'].isin(margin)]
    benef_filter.dropna(subset = ['LAT_DECIMALmean'], inplace=True)

    # # opción de beneficiarios
    # if benef_sel=='Número de Beneficiarios':
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio,fillOpacity=1,fillColor=color, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'], benef_filter['GMMcolor'])])
    # else:
    #     benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio, color=color, children=[
    #         dl.Popup("Municipio: {}".format(mun))
    #         ]) for mun, lat, lon, radio, color in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['MONTO_APOYO_TOTALradio'], benef_filter['GMMcolor'])])


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
        
    # Centros de acopio 
    def centros_popup(ent, mun,gmargina,numcentros):
        
            result = html.Div([
                html.Div([
                    html.Img(id='image-centros-acopio2', src='../assets/centrosAcopio.png', width="65", height="65"),
                    dmc.Text('CENTRO(S) DE ACOPIO', weight=400, color='#4e203a'),
                ], style={'textAlign': 'center'}),
                
                
                dmc.Divider(size="xs"),
                dbc.Row([
                    dmc.Text(['Estado: ',ent]),
                    dmc.Text(['Municipio: ', mun]),
                    dmc.Space(h=4),
                    dmc.Text(['Grado de marginación: ', gmargina]),
                    dmc.Text(['No. Centros: ', numcentros]),

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
                    dmc.Text(['No. Productores (Estimado): ', prettify(numprod)]),

                ])
                
                ])
            return result
    
    # opción de beneficiarios
    def benef_choice(benef_sel):
        #benef_filter = base
        if benef_sel == 'Número de Beneficiarios':
            benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=(radio),fillOpacity=1,fillColor=color, color=color, children=[
                #dl.Popup("Municipio: {}".format(mun))
                dl.Tooltip(f"Beneficiario(s): {mun}-{ent}"),
                dl.Popup(beneficiarios_popup(ent, mun, gmargina, numbenef, monto))
                ]) for ent, mun, lat, lon, radio, color, gmargina, numbenef, monto in zip(benef_filter['NOM_ENT'], benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'], benef_filter['GMMcolor'], benef_filter['GM_2020'], benef_filter['NUM_BENEFsize'], benef_filter['MONTO_APOYO_TOTALsum'])])
        else:
            benef_option = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=(radio), color=color, children=[
                #dl.Popup("Municipio: {}".format(mun))
                dl.Tooltip(f"Beneficiario(s): {mun}-{ent}"),
                dl.Popup(beneficiarios_popup(ent, mun, gmargina, numbenef, monto))
                ]) for ent, mun, lat, lon, radio, color, gmargina, numbenef, monto in zip(benef_filter['NOM_ENT'], benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['MONTO_APOYO_TOTALradio'], benef_filter['GMMcolor'], benef_filter['GM_2020'], benef_filter['NUM_BENEFsize'], benef_filter['MONTO_APOYO_TOTALsum'])])
        return benef_option
    
    # capa de beneficiarios
    beneficiarios = benef_choice(benef_sel)

    # Centro de acopio
    centros = dl.Pane([dl.Marker(position=[lat, lon], icon=dict(iconUrl='../assets/centrosAcopio.png',iconSize=[12, 16]), children=[
                                    dl.Tooltip(f"Centro(s) de acopio: {mun}-{ent}"),
                                    dl.Popup(centros_popup(ent, mun,gmargina,numcentros))
                                    ]) for lat, lon,ent, mun, gmargina, numcentros in zip(centros['LAT_DECIMAL'],centros['LON_DECIMAL'], centros['NOM_ENT'], centros['NOM_MUN'], centros['GM_2020'], centros['NUM_CENTROS'])])

    # Productores
    productores = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=np.log(numprod), color='#E12726', children=[
        dl.Tooltip(f"Productores: {mun}-{ent}"),
        dl.Popup(productores_popup(ent, mun,gmargina,numprod))
        ]) for lat, lon, ent, mun, gmargina, numprod in zip(productores_filter['LAT_DECIMAL'],productores_filter['LON_DECIMAL'], productores_filter['NOM_ENT'], productores_filter['NOM_MUN'], productores_filter['GM'], productores_filter['TotalProductores'])])

    # # Base
    # base = dl.GeoJSON(data=data2,  # url to geojson file  #283747
    #                 options=dict(style=style_handle),  # how to style each polygon
    #                 zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
    #                 zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
    #                 # color : color del perimetro del hover
    #                 # dashArray : tipo de linea 
    #                 # #154360
    #                 hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2),
    #                 hoverStyle=arrow_function(dict(weight=4, fillColor='#C51503', color='#C51503',opacity=0.1, fillOpacity=0.9, dashArray='2')), # color de fondo
    #                 id='states')
    
    

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
    class Capas():
        # constructor
        def __init__(self, background_style=bstyle):
            self.base_layer = [#dl.TileLayer(url=background_style),
                                #dl.EasyButton(icon="fa fa-home fa-fw", id="btn_nacional"),
                                #html.Button("Zoom in", id="zoom_in"),
                                info,
                                base]
        # function
        def add(self, features):
            # add layers
            for feature in features:
                self.base_layer.append(layers[feature])
                
                if feature == 'Centros de acopio':
                    self.base_layer.append(info_grado_marginacion)
                if feature == 'Beneficiarios':
                    self.base_layer.append(info_num_benef)
                    self.base_layer.append(info_grado_marginacion)
                if (feature == 'Productores') and int(anio_sel) == 2021:
                    self.base_layer.append(info_productores)
                if feature == 'Volumen Producción':
                    self.base_layer.append(info_vol_prod)
                    self.base_layer.append(colorbar)
             
                # if (feature == 'Beneficiarios') or (feature == 'Productores') or (feature == 'Centros de Acopio'):
                #     self.base_layer.append(info_grado_marginacion)
            
            return self.base_layer
        
    # background style del mapa
    children_layer = Capas().add(capas_sel)
    # dl.LayersControl([dmc.Text('Muy Bajo')])
    tab2_mapa_content = html.Div([
        dl.Map(center=[22.76, -102.58], zoom=5, children=children_layer
           , style={'width': '100%', 'height': '100vh', 'backgroundColor':'white', 'margin': "auto", "display": "block"}),
        #html.Div(id="state"), html.Div(id="info2")
    ])
        
    return tab2_mapa_content


# actualizar mapá a nacional
# @app.callback(
#         Output('submit-button', 'n_clicks'),
#         Input('btn_nacional', 'm_clicks'),
# )
# def regresa_nacional(n, m):
    
#     if(len(m)>0):
#         return n

 # capa base
capa_base = dl.GeoJSON(data=data2,  # url to geojson file
                        options=dict(style=style_handle),  # how to style each polygon
                        zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                        zoomToBoundsOnClick=False,  # when true, zooms to bounds of feature (e.g. polygon) on click
                        hideout=dict(colorscale=colorscale, classes=classes, style=style2, colorProp=2), #2e4053
                        hoverStyle=arrow_function(dict(weight=4, fillColor='#A91304', color='#A91304',opacity=0.1, fillOpacity=1, dashArray='1')),  # style applied on hover
                        id='states2')   
    
    
  


######### Mapa criterios simulados   ################
##   CALLBACK : MAPA
@app.callback(
        Output('mapa2', 'children'),
        Input('submit-button', 'n_clicks'),
        Input('criterios1', 'value'),
        Input('chip-observado', 'value'),
        #Input("beneficiarios-opciones", "value"),
        #Input("radio-centros", "value"),
        #Input("transfer-list-simple", "value"),
        State('producto', 'value'),
        State('anio', 'value'),
        #prevent_initial_call=True,
    )

# def actualizar_mapa2(clicks, margin_sel, benef_sel,capas_sel, transfer_sel, producto_sel, anio_sel):
def actualizar_mapa2(clicks, criterios_sel, benef_sel, producto_sel, anio_sel):

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

    #productores_filter = base_productores_filter.copy()
    #centros = centros_municipio.copy()
    #centros = centros_municipio[centros_municipio['GM_2020'].isin(margin)].dropna(axis=0)
    # base beneficiarios nivel municipio
    benef_filter = base_municipios[base_municipios['Anio'] == int(anio_sel)]
    benef_filter = benef_filter[benef_filter['Producto'] == producto_sel]
    # base productores
    # se seleccionan los registros por criterio seleccionado
    # if criterios == "Criterio de Marginación":
    #     productores_filter = base_productores.dropna(columns=['Escenario1'])
    # else:
    #     # criterio de precio
    #     productores_filter = base_productores.dropna(columns=['Escenario2'])
    productores_filter = base_productores.copy()   
    productores_filter = productores_filter[productores_filter['Producto'] == producto_sel]
    productores_filter = productores_filter[productores_filter['Anio'] == int(anio_sel)]
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
    
   
    # ópción para agregar beneficarios observados
    benef_filter = benef_filter[~benef_filter['LAT_DECIMALmean'].isna()]
    beneficiarios = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=radio,dashArray=1, fillOpacity=0, color='#1a5276', children=[
                dl.Popup("Municipio: {}".format(mun))
                ]) for mun, lat, lon, radio in zip(benef_filter['NOM_MUN'], benef_filter['LAT_DECIMALmean'], benef_filter['LON_DECIMALmean'], benef_filter['NUM_BENEFradio'])])
    
    # opción para agregar criterio del precio y marginación 
    if criterios_sel == 'Marginación':
        productores_filter = productores_filter[~productores_filter['Escenario1'].isna()]
        productores = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=np.log(radio), fillOpacity=0, color='#ee2a16', children=[
            dl.Popup("Municipio: {}".format(mun))
            ]) for lat, lon, mun, radio in zip(productores_filter['LAT_DECIMAL'],productores_filter['LON_DECIMAL'], productores_filter['NOM_MUN'], productores_filter['TotalProductores'])])
    else:
        productores_filter = productores_filter[~productores_filter['Escenario2'].isna()]
        productores = dl.Pane([dl.CircleMarker(center=[lat, lon], radius=np.log(radio), fillOpacity=0, color='#ee2a16', children=[
            dl.Popup("Municipio: {}".format(mun))
            ]) for lat, lon, mun, radio in zip(productores_filter['LAT_DECIMAL'],productores_filter['LON_DECIMAL'], productores_filter['NOM_MUN'], productores_filter['TotalProductores'])])

    if len(benef_sel) > 0:
        capas = [info_escenarios_marginacion,
                 info,
                 capa_base,
                 beneficiarios,
                 productores]   
    else:   
        capas = [info_escenarios_marginacion,
                 info,
                 capa_base,
                 productores] 
        
    # mapa
    tab2_mapa_content = html.Div([
        dl.Map(center=[22.76, -102.58], zoom=5,
               children=capas
               ,style={'width': '100%', 'backgroundColor':'white', 'height': '100vh', 'margin': "auto", "display": "block"}),
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

############################################################################################
# SECTION II :
############################################################################################

# Tabs actualization
# tab1_r2c1_content = html.Div([
#     html.Iframe(srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
# ])

# tab2_r2c1_content = html.Div([
#     dcc.Graph(id="plot2-r2c1")
#     #dcc.Graph(id="tabla-r2c1")
# ])
# @app.callback(Output("content-r2c1", "children"),
#               [Input("tabs-r2c1", "active_tab")])
# def switch_tab(at):
#     if at == "tab-r2c1-1":
#         return tab1_r2c1_content
#     elif at == "tab-r2c1-2":
#         return tab2_r2c1_content
#     return html.P("This shouldn't ever be displayed...")

# #----------------------------------------------------------------------------------
# #                     Actializa Gráfico 1:
# #----------------------------------------------------------------------------------
# @app.callback(
#         Output('plot1-r2c1', 'figure'),
#         Input('submit-button', 'n_clicks'),
#         #Input('estados', 'value'),
#         Input('anio', 'value')
#     )

# def actualizar_plot1_r2c1(clicks, anio_sel):


#     return

#----------------------------------------------------------------------------------
#                     Actializa Gráfico 2:
#----------------------------------------------------------------------------------

# tab1_r2c2_content = html.Div([
#         #dcc.Graph(id="mapa", mathjax=True)
#         html.Iframe(id='plot1-r2c2', srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
#     ]),

# tab2_r2c2_content = html.Div([
#     dt.DataTable(id="plot2-r2c2")
# ])

# #  Actualiza tabs - mapa
# @app.callback(Output("content-r2c2", "children"),
#               [Input("tabs-r2c2", "active_tab")])
# def switch_tab(at):
#     if at == "tab-r2c2-1":
#         return tab1_r2c2_content
#     elif at == "tab-r2c2-2":
#         return tab2_r2c2_content
#     return html.P("This shouldn't ever be displayed...")

#########  CALL : Actualiza gráfico cantidad/Monto productores  ################
# @app.callback(
#         Output('plot-r3c1', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )

# def actualizar_plot_r3c1(clicks, feature, producto_sel, anio_sel):
#     # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
#     # dist_plot = base[base['Anio'] == int(anio_sel)]
#     # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]

#     if feature == None:
#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
#     else:
#         entidad = feature["properties"]["name"]

#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()

#----------------------------------------------------------------------------------
#                     Actializa Gráfico 3:
#----------------------------------------------------------------------------------

# tab1_r2c2_content = html.Div([
#         #dcc.Graph(id="mapa", mathjax=True)
#         html.Iframe(id='plot1-r2c2', srcDoc=open(root + "/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "800px"})
#     ]),

# tab2_r2c2_content = html.Div([
#     dt.DataTable(id="plot2-r2c2")
# ])

# #  Actualiza tabs - mapa
# @app.callback(Output("content-r2c2", "children"),
#               [Input("tabs-r2c2", "active_tab")])
# def switch_tab(at):
#     if at == "tab-r2c2-1":
#         return tab1_r2c2_content
#     elif at == "tab-r2c2-2":
#         return tab2_r2c2_content
#     return html.P("This shouldn't ever be displayed...")

# # --------------------------------------------
# @app.callback(
#         Output('plot-r3c2', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )

# def actualizar_plot_r3c2(clicks, feature, producto_sel, anio_sel):
#     # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
#     # dist_plot = base[base['Anio'] == int(anio_sel)]
#     # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


#     if feature == None:
#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
#     else:
#         entidad = feature["properties"]["name"]

#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()



#########################################################################################
#  SECTION III - grafico Barras por municipio
##########################################################################################
# tab1_r3c1_content = html.Div([
#         #dcc.Graph(id="mapa", mathjax=True)
#         dcc.Graph(id="plot1-r3c1")
#     ]),

# tab2_r3c1_content = html.Div([
#      #dcc.Graph(id="plot2-r3c1")
#      html.Iframe(id='plot2-r3c1', srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read(), style={"height": "350px", "width": "1300px"})
# ], style={'height':'60vh'})



#--------------------------------------------------------------------------------------
#  Actualización Tab 1 : row3-col1 Grafico qqplot
#--------------------------------------------------------------------------------------
# @app.callback(
#         Output('plot-r1', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )

# def actualizar_plot_r1(clicks, feature, producto_sel, anio_sel):
#     # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
#     # dist_plot = base[base['Anio'] == int(anio_sel)]
#     # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


#     if feature == None:
#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
#     else:
#         entidad = feature["properties"]["name"]

#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})


# @app.callback(
#         Output('plot-r2', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )

# def actualizar_plot_r2(clicks, feature, producto_sel, anio_sel):
#     # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
#     # dist_plot = base[base['Anio'] == int(anio_sel)]
#     # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


#     if feature == None:
#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{'Nacional'}.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
#     else:
#         entidad = feature["properties"]["name"]

#         return open(root + f"/graficos/g1_barras/{str(anio_sel)}-{str(producto_sel)}-{entidad}.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})


# @app.callback(
#         Output('plot-r3', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )

# def actualizar_plot_r3(clicks, feature, producto_sel, anio_sel):
#     # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
#     # dist_plot = base[base['Anio'] == int(anio_sel)]
#     # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


#     if feature == None:
#         return open(root + f"/graficos/sunburstPlot2.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
#     else:
#         entidad = feature["properties"]["name"]

#         return open(root + f"/graficos/sunburstPlot2.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})


# @app.callback(
#         Output('plot-r4', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )

# def actualizar_plot_r4(clicks, feature, producto_sel, anio_sel):
#     # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
#     # dist_plot = base[base['Anio'] == int(anio_sel)]
#     # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]


#     if feature == None:
#         return open(root + f"/graficos/sunburstPlot3.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
#     else:
#         entidad = feature["properties"]["name"]

#         return open(root + f"/graficos/sunburstPlot3.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})

# @app.callback(
#         Output('plot-r5', 'srcDoc'),
#         Input('submit-button', 'n_clicks'),
#         State("states", "click_feature"),
#         State('producto', 'value'),
#         State('anio', 'value')
#     )

# def actualizar_plot_r5(clicks, feature, producto_sel, anio_sel):
#     # srcDoc=open("2019-Maíz-Durango.html", 'r', encoding = 'utf-8').read()
#     # dist_plot = base[base['Anio'] == int(anio_sel)]
#     # dist_plot = dist_plot[dist_plot['Producto']== producto_sel]

#     if feature == None:
#         return open(root + f"/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})
#     else:
#         entidad = feature["properties"]["name"]

#         return open(root + f"/graficos/sunburstPlot.html", 'r', encoding = 'utf-8').read()
#         #html.Iframe(id='plot2-r3c1',src=file, style={"height": "350px", "width": "1300px"})





