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





####################################################################################
#  Barplot
#   Gráfico de barras: muestra los montos ejercidos del programa social por año-producto
def barplot1(base, anio):
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