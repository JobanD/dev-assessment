### PROJECT FOR CANADA CLEAN FUELS INC
### JOBAN DHINDSA
# Pdf file of assignment requirements available in directory
### This file should only be run after creating database and table with create.py and insert.py ###
# This file categorizes restaurant items into main, side, dessert (type)
# Mains are then sub categorized into chicken, beef, seafood, pork, other
# New data is exported into a csv file called food_cats.csv

# IMPORTS

import os
import mysql.connector         # Python MySQL driver to access MySQL DB   
from dotenv import load_dotenv   
load_dotenv()

import pandas as pd
import numpy as np
# Connect to and establish DB
try:
    conn = mysql.connector.connect(
        host=os.getenv('HOST'),
        database='fastfood',
        user=os.getenv('USERSQL'),
        password=os.getenv('PASSWORD'),
    )
    if conn.is_connected():
        cursor = conn.cursor()
        # SQL Query for the necessary column data from populated table
        # Sugar used to determine if dessert, calories used to determine type
        cursor.execute("SELECT restaurant, item, calories, sugar FROM fastfood.mytable")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        # Create dataframe with pandas using results from SQL Query
        columns_names=["restaurant", "item", "calories", "sugar"]    
        df = pd.DataFrame(result, columns=columns_names)
        
except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
    
# Determine type of food item based on calorie and sugar content
# RULES: If sugar >= 20g and calories < 500 then Dessert
#           Calories > =250 = Main, Else Side
typeDF = df
conditions  = [ (typeDF['sugar'] >= 20) & (typeDF['calories'] < 500 ), (typeDF['calories'] >= 250), typeDF['calories'] < 250 ]
choices     = [ 'Dessert', "Main", 'Side' ]
    
typeDF["type"] = np.select(conditions, choices, default=np.nan)

# Determine sub cat of Mains into Chicken, Beef, Seafood, Pork, Other
# Iterate through rows find items with type Main
# Add sub cats to list then append list to new sub cat column
beefSubStrings = ["beef", "burger", "steak", "dog", "mac", "whopper"]
seafoodSubStrings = ["fish", "lobster"]
porkSubStrings = ["pepperoni", "bacon", "rib"]
typeDF['contains'] = ''
for i, row in typeDF.iterrows():
    # Temp list to store value(s) of sub cats to later append to column
    temp = []
    # Check if type is main
    if row["type"] == "Main":
        
        if "chicken" in row["item"].lower():
            temp.append("Chicken")
        if any(str in row["item"].lower() for str in beefSubStrings):
            temp.append("Beef")
        if any(str in row["item"].lower() for str in seafoodSubStrings):
            temp.append("Seafood")
        if any(str in row["item"].lower() for str in porkSubStrings):
            temp.append("Pork")
        # IF list is empty then it is other
        if not temp:
            temp.append("Other")
        # Turn list to string
        tempString = ','.join(temp)
        typeDF.at[i, 'contains'] = tempString
    # If not main then N/A
    else:
        typeDF.at[i, 'contains'] = "N/A"
        

print(typeDF.head())

# EXPORT CSV
# Get current dir
cwd = os.getcwd()
df.to_csv(cwd+"/foodcats.csv", index=False, header=True)