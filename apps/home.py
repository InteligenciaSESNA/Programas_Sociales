import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from sqlalchemy import create_engine
import sys
import pymysql
from datetime import date, datetime, timedelta
from dash_iconify import DashIconify
from dash.dependencies import Input, Output, State
from app import app
from path import root
# se importan los archivos .py de la carpeta apps
from apps.precios_garantia import precios_garantia
from apps.produccion_bienestar import produccion_bienestar
from apps import home


list_ramos = ['precios_garantia', 'produccion_bienestar']
# change to app.layout if running as single page app instead
layout = dbc.Container([

    # word cloud
    dmc.Center(
        dbc.Row([
            html.Iframe(id='cloud', srcDoc=open(root + "/apps/cloud.html", 'r', encoding = 'utf-8').read(), style={"height": "480px", "width": "1400px", 'paddingTop':'2rem'}),
        ], style={"height": "480px", "width": "1400px", 'paddingTop':'3rem', 'marginBottom':'4rem'}),
    ),

    # Logotimo SESNA
    html.Center(
        html.Div(children=[
            dmc.Image(src="assets/Logotipo_blanco.png",width='100%', withPlaceholder=True)
        ], style={"width": '15%',  "height":'15%', 'marginTop':'0rem', 'paddingTop':'4rem'},
        ),
    ),
    # texto
    html.Div([
        dmc.Text("Programas sociales", color='white', weight=500, align='center', style={"fontSize": 50}),
    ], style={"text-aling":"center", "marginBottom":'2rem'}),


    ######    SECCIÓN : SELECTORES
    html.Center(
        dbc.Col([
            html.Div([
                dbc.Row(
                    dmc.Text("Ramo", color='black', weight=500, align='left', style={"fontSize": 20}),
                className="col-lg-10 col-md-10 col-12 mt-4", style={'paddingTop':'1rem',  'paddingLeft':'1rem', 'paddingRight':'1rem'}),
                dbc.Row(
                        dmc.Select(
                            id='ramos',
                            data=list_ramos,
                            value= "uno",
                            clearable=True,
                            #style={"width": 600}
                            ),
                className="col-lg-10 col-md-10 col-12", style={'paddingLeft':'1rem', 'paddingRight':'1rem'}
                ),
                dbc.Row(
                        dmc.Text("Organismo", color='black', weight=500, align='left', style={"fontSize": 20}),
                className="col-lg-10 col-md-10 col-12 mt-4", style={'paddingLeft':'1rem', 'paddingRight':'1rem'}),
                dbc.Row(
                        dmc.Select(
                            id='organismos',
                            data=list_ramos,
                            value= "uno",
                            clearable=True,
                            #style={"width": 600}
                            ),
                className="col-lg-10 col-md-10 col-12", style={'paddingLeft':'1rem', 'paddingRight':'1rem'}
                ),

                dbc.Row(
                        dmc.Text("Programa social", color='black', weight=500, align='left', style={"fontSize": 20, 'paddingLeft':'1rem', 'paddingRight':'1rem'}),
                className="col-lg-10 col-md-10 col-12 mt-4", style={'paddingLeft':'1rem', 'paddingRight':'1rem'}),
                dbc.Row(
                        dmc.Select(
                            id='selector_programa',
                            data=[
                                {'label': 'Programa de Precios de garantía', 'value': '/precios_garantia'},
                                {'label': 'Programa de Producción para el Bienestar', 'value': '/produccion_bienestar'},
                            ],
                            searchable=True,
                            clearable=True,
                            placeholder="Seleccione una opción",
                            #style={"width": 600}
                            ),
                className="col-lg-10 col-md-10 col-12", style={'paddingLeft':'1rem', 'paddingRight':'1rem'}
                ),
                #
                dbc.Row(
                    dmc.Button(
                        'Ir',
                        id = 'home_submit-button',
                        n_clicks=0,
                        color = 'dark',
                        fullWidth=True),
                className="col-lg-6 col-md-6 col-6", style={'marginTop':'4rem','paddingLeft':'1rem', 'paddingRight':'1rem'}
                ),
            ], style={'marginLeft':'1rem', 'marginTop':'1rem'}),
        ], className="card col-lg-5 col-md-6 col-10 justify-content-center", style={'backgroundColor':'#F4F6F6', 'paddingBottom':'2rem', 'boxShadow': '#e3e3e3 1px 1px 1px', 'border-radius': '5px'}),
    style={'paddingBottom':'6rem', 'paddingTop':'2rem'}),
], className="twelve columns", style={'backgroundColor': '#212F3C'},
fluid=True,
)


# Callbacks
@app.callback(
    Output('url', 'pathname'),
    Input('home_submit-button', 'n_clicks'),
    State('selector_programa', 'value'),
    prevent_initial_call=True,
)
def redirect_page(click, selected_page):
    if selected_page:
        # Concatenar las rutas seleccionadas
        return selected_page
    else:
        return '/'
    


@app.callback(Output('page-content2', 'children'),
              #Input('home_submit-button', 'n_clicks'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/precios_garantia':
        return precios_garantia.layout
    elif pathname == '/produccion_bienestar':
        return produccion_bienestar.layout
    else: 
        return home.layout
    # if programa == 'precios_garantia':
    #     return precios_garantia.layout
    # elif programa == 'produccion_bienestar':
    #     return produccion_bienestar.layout
    # else:
    #     return home.layout