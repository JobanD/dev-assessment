### PROJECT FOR CANADA CLEAN FUELS INC
### JOBAN DHINDSA
# Pdf file of assignment requirements available in directory

# IMPORTS
import pandas as pd
import os
import mysql.connector         # Python MySQL driver to access MySQL DB   
from dotenv import load_dotenv   
load_dotenv()

# Read CSV data into data var
data = pd.read_csv('fastfood.csv')

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
        # DELETE TABLE before creating new one to ensure it's made correctly from csv
        cursor.execute('DROP TABLE IF EXISTS mytable;')
        ### CREATE TABLE ###
        cursor.execute("""CREATE TABLE IF NOT EXISTS mytable(
            restaurant  VARCHAR(20) NOT NULL 
            ,item        VARCHAR(100) NOT NULL
            ,calories    INTEGER 
            ,cal_fat     INTEGER 
            ,total_fat   INTEGER 
            ,sat_fat     NUMERIC(5,1)
            ,trans_fat   NUMERIC(5,1)
            ,cholesterol INTEGER 
            ,sodium      INTEGER 
            ,total_carb  INTEGER 
            ,fiber       VARCHAR(5)
            ,sugar       INTEGER 
            ,protein     VARCHAR(5)
            ,vit_a       VARCHAR(5)
            ,vit_c       VARCHAR(5)
            ,calcium     VARCHAR(5)
            ,salad       VARCHAR(5)
        );""")
        print("Table created ... ")
        ### READ IN DATA ###
        # Loop through Dataframe
        for i, row in data.iterrows():
            sql = "INSERT INTO fastfood.mytable VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
        cursor.close()
        conn.close()
            
            
        
except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)
