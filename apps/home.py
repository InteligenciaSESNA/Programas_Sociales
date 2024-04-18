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

list_ramos = ['uno', 'dos', 'tres']
# change to app.layout if running as single page app instead
layout = dbc.Container([
    # html.Div([
    #     dbc.Carousel(
    #             items=[
    #                 {"key": "1", "src": "../assets/logo.svg", "header": "With header ","caption": "SESNA", "img_style":{"width":"100%","height":"550px" }},
    #                 {"key": "2", "src": "../assets/logo4.svg", "header": "With header ","caption": "SESNA", "img_style":{"width":"100%","height":"550px" }},
    #                 {"key": "3", "src": "../assets/logo9.svg", "header": "With header ","caption": "SESNA", "img_style":{"width":"100%","height":"550px" }},
    #             ],
    #             controls=True,
    #             indicators=False,
    #             interval=2000,
    #             ride="carousel",
    #             className="carousel", style={'backgroundColor':'white'},
    #     ),     
    # ], style={'marginBottom':'6rem'}),
    
    # word cloud
    #dmc.CardSection(
        html.Iframe(id='cloud', srcDoc=open(root + "/apps/cloud.html", 'r', encoding = 'utf-8').read(), style={"height": "450px", "width": "1300px", 'paddingTop':'2rem'}),
    #),
    # Introduccion
    html.Center(
        html.Div(children=[
            dmc.Image(src="assets/Logotipo_blanco.png",width='100%', withPlaceholder=True)
        ], style={"width": '15%',  "height":'15%', 'marginTop':'0rem', 'paddingTop':'3rem'},
        ),
    ),
    
    html.Div([
        dmc.Text("Programas sociales", color='white', weight=500, align='center', style={"fontSize": 50}),
    ], style={"text-aling":"center", "marginBottom":'2rem'}),
    

    ######    SECCIÓN : SELECTORES
    html.Center(
    dmc.Card([
        dbc.Row([
            # dbc.Col([
            #     html.Div([
            #         dmc.Image(src='/assets/logo7.svg'),
            #     ],style={'fluid':'top','padding':'0rem', 'width':'90%','marginTop':'2rem', 'marginBottom':'1rem'}
            #     ),
            # ], className="col-4"),
            dbc.Col([
                # first row 
                html.Div([
                    dbc.Row([
                            dbc.Col(
                                    dmc.Select(
                                        id='ramos', 
                                        data=list_ramos,
                                        value= "uno",
                                        clearable=True,
                                        #style={"width": 600}  
                                        ),       
                            className="col-8 col-md-8 col-12 mt-4", style={'paddingLeft':'2rem', 'paddingRight':'2rem'}
                            ),   
                            dbc.Col(
                                dmc.Text("Ramo", color='black', weight=500, align='left', style={"fontSize": 20, 'paddingLeft':'1rem', 'paddingRight':'2rem'}),
                            className="col-4 col-md-4 col-12 mt-4"), 
                            #dbc.Col(md=2),
                            #dbc.Col(html.Div([
                            #        dbc.Button("", color="dark",
                            #                   outline=True, href="#"),
                            #    ]),
                            #md=2),
                    ], style={'marginBottom':'2rem'}),
                    
                    # second row organismo
                    dbc.Row([
                            dbc.Col(
                                    dmc.Select(
                                        id='organismos', 
                                        data=list_ramos,
                                        value= "uno",
                                        clearable=True,
                                        #style={"width": 600}  
                                        ),       
                            className="col-8 col-md-8 col-12 mt-1", style={'paddingLeft':'2rem', 'paddingRight':'2rem'}
                            ),   
                            dbc.Col(    
                                    dmc.Text("Organismo", color='black', weight=500, align='left', style={"fontSize": 20, 'paddingLeft':'1rem', 'paddingRight':'2rem'}),
                            className="col-4 col-md-4 col-12 mt-1"), 
                            #dbc.Col(html.Div([
                            #        dbc.Button("", color="dark",
                            #                   outline=True, href="#"),
                            #    ]),
                            #md=2),
                    ], style={'marginBottom':'2rem'}),
                    
                    # third row : Programa social
                    dbc.Row([
                            dbc.Col(
                                    dmc.Select(
                                        id='progama_social', 
                                        data=list_ramos,
                                        value= "uno",
                                        clearable=True,
                                        #style={"width": 600}  
                                        ),       
                            className="col-8 col-md-8 col-12 mt-1", style={'paddingLeft':'2rem', 'paddingRight':'2rem'}
                            ),   
                            dbc.Col(
                                    dmc.Text("Programa social", color='black', weight=500, align='left', style={"fontSize": 20, 'paddingLeft':'1rem', 'paddingRight':'2rem'}),
                            className="col-4 col-md-4 col-12 mt-1"), 
                            
                    ], style={'marginBottom':'3rem'}),
                    
                    dbc.Row([
                            dbc.Col( 
                                dmc.Button(
                                    'Ir',
                                    #id='submit-intro',
                                    id = 'submit-button',
                                    n_clicks=0,
                                    #children='Actualizar',
                                    color = 'dark',
                                    fullWidth=True), 
                            className="col-8 col-md-8 col-8  mt-1", style={'paddingLeft':'1rem', 'paddingRight':'1rem'}
                            ),  
                            dbc.Col(
                                    dmc.Text("", color='black', weight=500, style={"fontSize": 20, 'paddingLeft':'0rem', 'paddingRight':'2rem'}),
                            className="col-4 col-md-4 col-12  mt-1"), 
                            
                    ], justify="center", style={'marginBottom':'0rem'}),
                
                            # dbc.Button("Ir", 
                            #         id ="submit-home",
                            #         color="dark", 
                            #         #size="xl",
                            #         className="me-1",
                            #         #outline=True, 
                            #         href="/segalmex"),
                ], ),  
            ], className="col-12"),
        ]),
        
        ],
        withBorder=True,
        shadow="md",
        radius="md",
        className="col-6 col-md-6 col-12",
        style={"width": '50%', 'background-color':'#F8F9F9', 'paddingTop':'3rem', 'paddingBottom':'3rem'},
    ), style={ 'marginBottom':'0rem', 'paddingBottom':'6rem'} ),
    
#], className="twelve columns", style={'backgroundColor': '#2E4053', 'marginTop': '0rem'},
], className="twelve columns", style={'backgroundColor': '#212F3C', 'marginTop': '0rem'},


fluid=True, 
)


# @app.callback(
#     Output('home-link', 'href'),
#     Input('submit-button','n_clicks')
# )

# def page_link(click):
    
#     return dmc.NavLink(id='home-link', href="/home"),