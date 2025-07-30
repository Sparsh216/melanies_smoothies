# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
# Write directly to the app
st.title(f"Customize Your Smoothies")
st.write(
  """Choose fruit you want in your custom smoothies
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ing_lis = st.multiselect(
    "Choose upto 5 ingredients",
    my_dataframe,
    max_selections=5
)
if ing_lis:
    st.write(ing_lis)
    st.text(ing_lis)
    ing_string = ''
    for fruit_chosen in ing_lis:
        ing_string += fruit_chosen+ ' '
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ing_string + """', '""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered: " + name_on_order, icon="✅")
