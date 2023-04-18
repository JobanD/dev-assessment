### PROJECT FOR CANADA CLEAN FUELS INC
### JOBAN DHINDSA
# Pdf file of assignment requirements available in directory
### This file should only be run after creating database and table with create.py and insert.py ###
# 

# IMPORTS

import os
import tempfile
os.environ["MPLCONFIGDIR"]=tempfile.gettempdir()    # Improve speed of matplotlib import needed for seaborn
import mysql.connector         # Python MySQL driver to access MySQL DB   
from dotenv import load_dotenv   
load_dotenv()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
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
        cursor.execute("SELECT restaurant, item, calories, total_carb FROM fastfood.mytable")
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        # Create dataframe with pandas using results from SQL Query
        columns_names=["restaurant", "item", "calories", "total_carb"]    
        df = pd.DataFrame(result, columns=columns_names)
        
except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
    

# Below this will be where specific averages, mins/max will be calculated per restaurant
# Group data by restaurant names
# Find mean, min, max calories
# Find mean total carbs
calorieCalculations = df.groupby(['restaurant']).agg({'calories': ['mean', 'min', 'max'], 'total_carb': 'mean'}).reset_index()

# Drop column level to avoid multi-level indexing and make things simpler
calorieCalculations.columns = calorieCalculations.columns.droplevel(0)
# Rename Columns
calorieCalculations.columns = ['restaurant', 'calorie_mean', 'calorie_min', 'calorie_max', 'carb_mean']
# Round columns with mean values to 1 decimal
calorieCalculations['calorie_mean'] = calorieCalculations['calorie_mean'].round(decimals=1)
calorieCalculations['carb_mean'] = calorieCalculations['carb_mean'].round(decimals=1)

# Sort new data by lowest mean carbs
calorieCalculations = calorieCalculations.sort_values(by='carb_mean',ascending=True)

# Take top 5 restaurants based on lowest average carbs for data visualization
topFive = calorieCalculations.head(5)

print(topFive)

# np.arange used to create range of 5 values
N = 5
ind = np.arange(N)
width = 0.2

# Plot each bar with 0.2 units of space between and different colors
wvals = topFive['calorie_mean'].to_list()
bar1 = plt.bar(ind, wvals, width, color='r')

xvals = topFive['calorie_min'].to_list()
bar2 = plt.bar(ind+width, xvals, width, color='g')

yvals = topFive['calorie_max'].to_list()
bar3 = plt.bar(ind+width*2, yvals, width, color='b')

zvals = topFive['carb_mean'].to_list()
bar4 = plt.bar(ind+width*3, zvals, width, color='orange')

plt.xlabel('Restaurants')
plt.title('Top Five Restaurant Calorie and Carb Information')

plt.xticks(ind+width,topFive['restaurant'].to_list())
plt.legend( (bar1, bar2, bar3, bar4), ('Calorie Mean', 'Calorie Min', 'Calorie Max', 'Carb Mean'))
plt.show()
