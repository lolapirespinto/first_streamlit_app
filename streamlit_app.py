import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My parents New Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado test')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Adice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?')
streamlit.write('The user entered ', fruit_choice)
# Vérifiez si l'utilisateur a saisi un fruit
if fruit_choice:
    try:
        # Effectuez la requête vers l'API Fruityvice
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

        # Vérifiez si la requête a réussi (statut 200)
        if fruityvice_response.status_code == 200:
            # Tentez de normaliser la réponse JSON
            try:
                fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
                streamlit.dataframe(fruityvice_normalized)
            except pandas.errors.JSONDecodeError as e:
                streamlit.error(f"Erreur lors de la normalisation JSON : {e}")
        else:
            streamlit.error(f"Erreur de requête vers Fruityvice API. Statut : {fruityvice_response.status_code}")
    except requests.exceptions.RequestException as e:
        streamlit.error(f"Erreur de connexion à l'API Fruityvice : {e}")


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit load list contains:")
streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into fruit_load_list values('from streamlit')"
