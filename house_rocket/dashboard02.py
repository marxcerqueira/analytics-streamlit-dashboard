import geopandas
import folium
import time

import streamlit as st
import pandas               as pd
import numpy                as np
import plotly.express       as px 
import plotly.graph_objects as go
import streamlit.components.v1 as comp

from PIL              import Image
from datetime         import datetime
from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster
from numerize.numerize import numerize



# ------------------------------------------
# settings
# ------------------------------------------
# === page titles
st.set_page_config(page_title="HR Insights", page_icon="📊",
                   layout="wide")

#this is the header
t1, t2 = st.columns((0.07,1))

# image
with t1:
    photo = Image.open('house-rocket-logo.jpg')
    st.image(photo, width=200)

# headers
with t2:

    st.write('')
    HR_format = '<p style="font-family:sans-serif;' \
                   'color:#ed7f11;' \
                   'font-size: 50px;' \
                   'font-weight: bold;' \
                   '' \
                   'text-align: left;' \
                   '">House Rocket Company</p>'
    st.markdown(HR_format, unsafe_allow_html=True)

    welcome_format = '<p style="font-family:sans-serif;' \
                       'color:#ed7f11;' \
                       'font-size: 25px;' \
                       '' \
                       'text-align: left;' \
                       '">Real Estate Flipping Houses Company Report</p>'
    st.markdown(welcome_format, unsafe_allow_html=True)

t2.text("by: Marx Cerqueira") 
t2.markdown(" **Github:** https://github.com/marxcerqueira **| website:** https://marxcerqueira.github.io/portfolio_projetos/ **| email:** marxv49@gmail.com")

# =================================================
# =============== HELPER FUNCTIONS ================
# =================================================

@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    # data = data.head(1000) # filter data to edit faster

    data.style.format(formatter={('price', 'median_price_by_zipcode',
                                  'sale_price', 'profit'): '{:,.2f}'})

    return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)

    return geofile

@st.cache
def convert_csv(data):

    return data.to_csv().encode('utf-8')

def set_features(data):
    # create columns as needed

    return 

def overview_kpis(data):
    st.title('General Insights')
    exp_overall = st.expander("Click here to expand/close general insights section.", expanded=True)
    
    with exp_overall:
        invested = data[data['decision'] == 1]['price'].sum()
        returned = data[data['decision'] == 1]['sale_price'].sum()
        profit = data[data['decision'] == 1]['profit'].sum()
        gross_revenue = (profit / invested) * 100

        st.header('Profit Overview')
        c1, c2, c3 = st.columns((1,1,1))
        with c1:
            #st.subheader('Maximum Expected Profit')
            st.metric(label='Maximum Expected Profit', value=numerize(profit), delta=numerize(gross_revenue) + "%")
        with c2:
            #st.subheader('Maximum Value Invested')
            st.metric(label='Maximum Invested Amount', value=numerize(invested))
        with c3:
            #st.subheader('Maximum Revenue)
            st.metric(label='Maximum Revenue', value=numerize(returned))

        # mainly insights
        st.header('General Information:')
        st.write('**1. Houses prices with conditions 4 and 5 correspond to 48,45% of the total sum of the base prices.**')
        st.write('**2. 50% of the houses that should be bought are located within 15km radius from the lake, which correspond to 1888 houses.**')
        st.write('**3. Average house prices decrease as distance from lake increases.**')
        st.write('**4. Houses that were suggested to be bought within 15km radius from lake correspond to  63.23% of expected profit.**')  
        st.subheader('Number of houses on dataset: {:,}'.format(data.shape[0]))
        # st.subheader('Total of properties suggested to be purchased: {:,}'.format(data[data['decision'] == 1].shape[0]))
        st.subheader('Number of houses suggested to be purchased:')
        st.metric(label = '', value = data[data['decision'] == 1].shape[0], delta = numerize(data[data['decision'] == 1].shape[0]/data.shape[0]*100)+"%")

    return None

def data_size(data):

    with st.container():
        st.subheader('Choose database size')
        st.write('The complete database has', data.shape[0], 'registers. '
                 'If it is taking too long for the page to load, '
                        'please select a smaller database size below')
        # st.write('Note that the larger the size of the database selected '
        #          'the longer it may take to load the report. ')

        # selection of data sample
        data_25 = data[ (data.index > np.percentile(data.index, 00)) &
                        (data.index <= np.percentile(data.index, 25)) ]
        data_50 = data[ (data.index > np.percentile(data.index, 00)) &
                        (data.index <= np.percentile(data.index, 50)) ]
        data_75 = data[ (data.index > np.percentile(data.index, 00)) &
                        (data.index <= np.percentile(data.index, 75)) ]
        data_100 = data

        # list of database sizes

        option = st.selectbox('Select size', ('', '25% of data', '50% of data', '75% of data', '100% of data'), key='data_size')

        # filtering report data = data_r
        if option == '':
            data_r = []
            st.error('Choose database size on the list above to load the report')
        elif option == '25% of data':
            data_r = data_25
            st.write('You have chosen the first 25% registers of the database')
        elif option == '50% of data':
            data_r = data_50
            st.write('You have chosen the first 50% registers of the database')
        elif option == '75% of data':
            data_r = data_75
            st.write('You have chosen the first 75% registers of the database')
        elif option == '100% of data':
            data_r = data_100
            st.write('You have chosen the full database')
            st.warning('Please, note that choosing this option may slow down the report loading.')
        else:
            st.info('You must choose the database size')

        # st.write(data_r.index)

    return data_r, option


def data_information(data_r):
    st.title("Data Information")
    exp_data = st.expander("Click here to expand/close the dataset general information section.", expanded=False)
    with exp_data:
        c1, c2 = st.columns((1,3))
        with c1:
            st.subheader("Data Dimensions")
            st.write("Total Number of Registers:", data.shape[0])
            st.write("Number of Registers Selected:", data_r.shape[0])
            st.write("Number of Attributes:", data_r.shape[1])
            # st.write('index', data_r.index)
        with c2:
            st.subheader("Time Interval")
            st.write("First date:", data_r['date'].min())
            st.write("Last date from selection:", data_r['date'].max())
            st.write("Last date available on full database:", data['date'].max())


    exp_data.write("")
    exp_data.write("*End of data overview*")

    return None

def portfolio_density(data, geofile):
    st.title("Portfolio Distribution Map")
    exp_density = st.expander("Click here to expand/close this section with portfolio concentration map by location and expected profit.", expanded=False)
    with exp_density:

        note_format = '<p style="background-color:#FFF8D4; font-size: 16px; font-style: italic;"> ' \
                      'Remember that you have selected {} of the database. </p>'.format(data_size)
        st.write(note_format, unsafe_allow_html=True)

        st.write('')
        profit_format = '<p style= "font-size:18px; font-weight: bold"> The sum of expected profit is {}' \
                        ' for properties selected from the database according to previously agreed criteria.</p>'.format(numerize(data['profit'].sum()))
        st.write(profit_format, unsafe_allow_html=True)

        # checbox for map and table
        f_decision = st.checkbox('Check to see only properties suggested to be purchased.')
        if f_decision:
            data = data[data['decision'] == 1]
            st.write('There are', data.shape[0], 'properties from selected database fulfilling the requirements')
        else:
            data = data.copy()
            st.write('*All properties selected from the database are been shown.*')


        c1, c2 = st.columns((1, 1))

        c1.subheader('Properties Distribution') # map
        with c1:

            # defining map dataframe
            dfmap = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                               default_zoom_start=15)

            # grouping properties for dfmpap
            make_cluster = MarkerCluster().add_to(dfmap)

            # defining pin message
            for index, row in data.iterrows():
                folium.Marker([row['lat'], row['long']],
                              popup='Available since {0} for US$ {1}.'
                                    '\Sale price suggestion is US$ {2}, resulting on an expected profit of US$ {3}.'
                                    '\nZipcode: {4}'
                                    '\nProperty ID: {5}'
                                    .format(row['date'], row['price'], row['sale_price'],
                                            row['profit'], row['zipcode'], row['id']))\
                              .add_to(make_cluster)

            # coloring map area
            df_geofile = geofile[geofile['ZIP'].isin(data['zipcode'].tolist())]
            folium.features.Choropleth(data=data, geo_data=df_geofile, columns=['zipcode', 'profit'],
                                       key_on='feature.properties.ZIP',
                                       fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2,
                                       legend_name='Expected Profit').add_to(dfmap)

            folium_static(dfmap)

        c2.subheader('Properties Information') # table
        with c2:
    
            if f_decision:
                data = data[data['decision']==1]
            else:
                data = data.copy()

            table = data[['id', 'date', 'condition', 'zipcode', 'dist_fromlake',
                          'price', 'median_price_by_zipcode', 'sale_price', 'profit' ]].copy()
            
            st.dataframe(data = table)
            st.write('*Properties with selected attributes:', '{:,}*'.format(table['id'].count()))
            st.write('')

            # downloading table
            data_csv = convert_csv(data)
            st.write('**You can have a full copy of this table by clicking on the button below**')
            st.download_button(label="Download this table as CSV",
                               data=data_csv, file_name='selected_properties.csv',
                               mime='text/csv')

    exp_density.write("")
    exp_density.write("*End of distribution view*")

    return None

def profit_business_attributes(data):
    st.title("Estimated Profit - Business Attributes")
    exp_att_bus = st.expander('Click here to expand/close this section with estimated profit table according to business attributes.', expanded=False)
    with exp_att_bus:
        note_format = '<p style="background-color:#FFF8D4; font-size: 16px; font-style: italic;"> ' \
                      'Remember that you have selected {} of the database. </p>'.format(data_size)
        st.write(note_format, unsafe_allow_html=True)

        # business data = b
        b = data[data['decision']==1][['id', 'date', 'condition', 'zipcode', 'dist_fromlake',
                                       'price', 'median_price_by_zipcode', 'sale_price', 'profit',
                                       'yr_built', 'yr_renovated', 'neighbourhood',
                                       'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'sqft_above', 'sqft_basement']].copy()

        # ===== creating filters
        c1, c2, c3 = st.columns((4, 1, 4))

        # filters: buying_price, expected_profit, dist_fromlake
        with c1:
            f_buying_price = st.slider('Select maximum price',
                                       int(b['price'].min()),
                                       int(b['price'].max()+1), key='price bus',
                                       value=int(b['price'].max()+1))
            f_expected_profit = st.slider('Select maximum expected profit',
                                          int(b['profit'].min()),
                                          int(b['profit'].max()+1),
                                          value=int(b['profit'].max()+1))
            f_dist_fromlake = st.slider('Select maximum distance from lake',
                                        int(b['dist_fromlake'].min()),
                                        int(b['dist_fromlake'].max()+1),
                                        value=int(b['dist_fromlake'].max()+1), step=2)

            # filtering business data = f_b
            f_b = b[(b['price'] <= f_buying_price) &
                    (b['profit'] <= f_expected_profit) &
                    (b['dist_fromlake'] <= f_dist_fromlake)]

        # filters: zipcode, id
        with c3:

            f_zipcode = st.multiselect('Type or select zipcodes',
                                       f_b['zipcode'].sort_values(ascending=True).unique())
            f_id = st.multiselect('Type or select properties ID',
                                  f_b['id'].sort_values(ascending=True).unique())

            # filtering business data = f_b2
            if (f_id != []) & (f_zipcode != []):
                f_b2 = f_b.loc[(f_b['id'].isin(f_id)) & (f_b['zipcode'].isin(f_zipcode)), :]
                # st.write('id and zipcode')
            elif (f_id != []) & (f_zipcode == []):
                f_b2 = f_b.loc[f_b['id'].isin(f_id), :]
                # st.write('id')
            elif (f_id == []) & (f_zipcode != []):
                f_b2 = f_b.loc[f_b['zipcode'].isin(f_zipcode), :]
                # st.write('zipcode')
            else:
                f_b2 = f_b.copy()
                # st.write('none')

        # ======= printing dataframe
        profit_format_2 = '<p style= "font-size:18px; font-weight: bold"> The sum of expected profit for the subset ' \
                          'below is {}'.format(numerize(f_b2['profit'].sum()))
        st.write(profit_format_2, unsafe_allow_html=True)
        st.dataframe(f_b2)
        st.write('*Properties with selected attributes:', '{:,}*'.format(f_b2['id'].count()))

        # downloading table
        data_csv = convert_csv(data)
        st.write('**You can have a full copy of this table by clicking on the button below**')
        st.download_button(label="Download this table as CSV",
                           data=data_csv, file_name='selected_business_attributes.csv',
                           mime='text/csv')

    exp_att_bus.write("")
    exp_att_bus.write("*End of business attributes view*")

    return None

def profit_properties_attributes(data):
    st.title("Estimated Profit - Properties Attributes")
    exp_att_prop = st.expander('Click here to expand/close this section with estimated profit table according to properties attributes.', expanded=False)
    with exp_att_prop:
        note_format = '<p style="background-color:#FFF8D4; font-size: 16px; font-style: italic;"> ' \
                      'Remember that you have selected {} of the database. </p>'.format(data_size)
        st.write(note_format, unsafe_allow_html=True)

        # properties data = p
        p = data[data['decision']==1][['id', 'date', 'condition', 'zipcode', 'dist_fromlake',
                                       'price', 'median_price_by_zipcode', 'sale_price', 'profit',
                                       'yr_built', 'yr_renovated', 'neighbourhood',
                                       'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'sqft_above', 'sqft_basement']].copy()

        # ======= creating filters
        c1, c2, c3 = st.columns((1,2,2))

        # filters: bedrooms, bathrooms
        with c1:

            f_bedrooms = st.selectbox('Select maximum number of bedrooms',
                                      p['bedrooms'].sort_values(ascending=True).unique().tolist(), key='bedrooms')

            f_bathrooms = st.selectbox('Select maximum number of bathrooms',
                                      p['bathrooms'].sort_values(ascending=True).unique().tolist(), key='bathrooms')

        # filters: sqft_living, sqft_basement
        with c2:
            f_sqft_living = st.slider('Select maximum interior living space size',
                                      int(p['sqft_living'].min()),
                                      int(p['sqft_living'].max()+1),
                                      value=int(p['sqft_living'].max()+1), key='living')

            f_sqft_basement = st.slider('Select maximum basement size',
                                      int(p['sqft_basement'].min()),
                                      int(p['sqft_basement'].max()+1),
                                      value=int(p['sqft_basement'].max()+1), key='basement')

        # filters: yrbuilt, yrrenovated
        with c3:
            f_yrbuilt = st.slider('Select minimum year property was built',
                                  int(p['yr_built'].min()),
                                  int(p['yr_built'].max()),
                                  value=int(p['yr_built'].min()), key='yrbuilt')

            f_yrrenovated = st.slider('Select minimum year property was renovated',
                                  int(p['yr_renovated'].min()),
                                  int(p['yr_renovated'].max()),
                                  value=int(p['yr_renovated'].min()), key='yrrenovated')

        # filters: buying_price
        f_buying_price = st.slider('Select maximum price',
                                   int(p['price'].min()),
                                   int(p['price'].max()+1),
                                   value=int(p['price'].max()+1), key='price prop')

        # ======= filtered properties data = f_p
        f_p = p[ (p['bedrooms']      <= f_bedrooms)  &
                 (p['bathrooms']     <= f_bathrooms) &
                 (p['sqft_living']   <= f_sqft_living ) &
                 (p['sqft_basement'] <= f_sqft_basement) &
                 (p['price']         <= f_buying_price) &
                 (p['yr_built']      >= f_yrbuilt) &
                 (p['yr_renovated']  >= f_yrrenovated)      ]


        # ======= printing dataframe
        profit_format_3 = '<p style= "font-size:18px; font-weight: bold"> The sum of expected profit for the subset ' \
                          'below is {}'.format(numerize(f_p['profit'].sum()))
        st.write(profit_format_3, unsafe_allow_html=True)
        st.dataframe(f_p)
        st.write('*Properties with selected attributes:', '{:,}*'.format(f_p['id'].count()))

        # downloading table
        data_csv = convert_csv(data)
        st.write('**You can have a full copy of this table by clicking on the button below**')
        st.download_button(label="Download this table as CSV",
                           data=data_csv, file_name='selected_properties_attributes.csv',
                           mime='text/csv')

    exp_att_prop.write("")
    exp_att_prop.write("*End of table view*")

    return None

# =================================================
# ================ MAIN FUNCTION ==================
# =================================================

if __name__ == '__main__':
    # ETL
    path = 'house_rocket.csv'
    url='https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    # load data
    data = get_data( path )
    geofile = get_geofile( url )

    #transform data
    set_features(data)

    overview_kpis(data)

    st.markdown('---')
    data_filtered, data_size = data_size(data)

    with st.spinner('Please wait...'):
        time.sleep(1)

    try:
        if data_filtered.shape[0]>=1:
            data_information(data_filtered)
            portfolio_density(data_filtered, geofile)  
            profit_properties_attributes(data_filtered)
    except:
        # st.error('Choose database size on the list above to load the report')        # st.write("An exception occurred")
        st.error('Error.')

   # === Personal Info Section
    st.markdown('---')
    st.title('Additional Information')
    st.subheader("Report Purpose:")
    st.markdown('This data visualization is part of **House Rocket Flipping Houses Company Report** made by **Marx Cerqueira**.')
    st.markdown('You can read the business context and check the code for this streamlit on [github](https://github.com/marxcerqueira/analytics-streamlit-dashboard).')
    st.write('')
    st.write('House Rocket is a Real Estate Flipping Houses business that goes on digital platform to buy and sell houses by using technology.')
    st.write("This report was created by a request from House Rocket's CEO to visualize "
             "all properties available to be bought at King County, Seatle.")
    st.write('')
    st.markdown('Other Projects: [Portfolio](https://marxcerqueira.github.io/portfolio_projetos/)')
    st.markdown('Contact me: [LinkedIn](https://www.linkedin.com/in/marxcerqueira/)')