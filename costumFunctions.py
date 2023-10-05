import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import requests


###
# En este espacio se anexara toda aquella función que sea utilizada en el dashboard
# se mandaran a llamar desde el encabezado principal de cada layout como
#   from costumFunctions import "nombre_de_la_función" 

# F1: Función para formar un dataframe 
# función 
def make_dataframe_state_mun(geo_data):
  '''
  Función para obtener un dataframe de estados y municipios 
  '''
  # get features
  features = geo_data['features']
  # get country, state and mun
  country = []
  state = []
  mun = []
  # loop for each feature
  for feature in features:
    country.append(feature['properties']['NAME_0'])
    state.append(feature['properties']['NAME_1'])
    mun.append(feature['properties']['NAME_2'])
  # dataframe
  df2 = pd.DataFrame([country, state, mun]).T
  df2.columns = ['country', 'state', 'mun']

  return df2


