# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write("Choose the fruits you want in your custome smoothie")

# option = st.selectbox(
#     "What is your favourite fruit",
#     ('Banana', 'Strawberries', 'Peaches'))

# Get the current credentials

name_on_smoothie=st.text_input("Name on Smoothies")

st.write("The name of your smoothie will be", name_on_smoothie)

df = session.table('smoothies.public.fruit_options').select(col('fruit_name'))

ingredient_list = st.multiselect(
    'Choose upto 5 ingredient', df, max_selections=5)
if ingredient_list:

    ingredient_string = ','.join(x for x in ingredient_list)

    insert_statement = f"""
        INSERT INTO smoothies.public.orders (name_on_order, ingredients)
        VALUES ('{name_on_smoothie}','{ingredient_string}')"""
    if ingredient_string and name_on_smoothie:
        if st.button('Submit Order'):
            session.sql(insert_statement).collect()
            st.success('Your smoothies is now ordered!')



