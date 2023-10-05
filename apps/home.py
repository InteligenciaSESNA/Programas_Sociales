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
    
    # Introduccion
    html.Center(
        html.Div(children=[
            dmc.Image(src="/assets/logo.svg",width='100%', withPlaceholder=True)
        ], style={"width": '15%',  "height":'15%', 'marginTop':'4rem', 'marginBottom':'2rem'},
        ),
    ),
    
    html.Div([
        dmc.Text("Programas sociales", color='black', weight=500, align='center', style={"fontSize": 50}),
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
                            className="col-8 col-md-8 col-12 mt-4", style={'paddingLeft':'3rem', 'paddingRight':'3rem'}
                            ),   
                            dbc.Col(
                                dmc.Text("Ramo", color='black', weight=500, align='left', style={"fontSize": 20}),
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
                            className="col-8 col-md-8 mt-1", style={'paddingLeft':'3rem', 'paddingRight':'3rem'}
                            ),   
                            dbc.Col(    
                                    dmc.Text("Organismo", color='black', weight=500, align='left', style={"fontSize": 20}),
                            className="col-4 col-md-4 mt-1"), 
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
                            className="col-8 col-md-8 mt-1", style={'paddingLeft':'3rem', 'paddingRight':'3rem'}
                            ),   
                            dbc.Col(
                                    dmc.Text("Programa social", color='black', weight=500, align='left', style={"fontSize": 20}),
                            className="col-4 col-md-4 mt-1"), 
                            
                    ], style={'marginBottom':'2rem'}),
                    
                    dbc.Row([
                            dbc.Col( 
                                dmc.Button(
                                    'Ir',
                                    id='submit-intro',
                                    n_clicks=0,
                                    #children='Actualizar',
                                    color = 'dark',
                                    fullWidth=True), 
                            
                            className="col-8 col-md-8 mt-1", style={'paddingLeft':'3rem', 'paddingRight':'3rem'}
                            ),  
                            dbc.Col(
                                    dmc.Text("", color='black', weight=500, style={"fontSize": 20}),
                            className="col-4 col-md-4 mt-1"), 
                            
                    ], justify="center", style={'marginBottom':'2rem'}),
                
                
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
        shadow="sm",
        radius="md",
        style={"width": '50%', 'background-color':'#F8F9F9'},
    ), style={ 'marginBottom':'4rem', 'padding':'2rem'} ),
    
], className="twelve columns", style={'backgroundColor': 'white', 'marginTop': '0rem'},
fluid=True
)


@app.callback(
    Output('home-link', 'href'),
    Input('submit-button','n_clicks')
)

def page_link(click):
    
    return dmc.NavLink(id='home-link', href="/segalmex"),