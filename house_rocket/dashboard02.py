import geopandas
import folium

import streamlit      as st
import pandas         as pd
import numpy          as np
import plotly.express as px 

from datetime         import datetime, time
from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster

# ------------------------------------------
# settings
# ------------------------------------------
st.set_page_config( layout='wide' )
st.title('House Rocket Dashboard - Flipping Homes')
st.text('by Marx Cerqueira') 