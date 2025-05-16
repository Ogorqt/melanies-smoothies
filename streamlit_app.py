# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("Augustine's Smoothie")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

import streamlit as st

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on you Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
     my_dataframe,
     max_selections=5
)

# Slider for sugar level
sugar_level = st.slider(
    'Select your desired sugar level (percentage):',
    min_value=0,
    max_value=100,
    value=25,  # Default value
    step=5
)

if ingredients_list:

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order, sugar_level)
            values ('""" + ingredients_string + """','""" + name_on_order + """',""" + str(sugar_level) + """)"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
