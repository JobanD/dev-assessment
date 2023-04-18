### PROJECT FOR CANADA CLEAN FUELS INC
### JOBAN DHINDSA
### This file establishes connection to mysql server and creates database
# Pdf file of assignment requirements available in directory


# IMPORTS
import os
import mysql.connector         # Python MySQL driver to access MySQL DB   
from dotenv import load_dotenv   
load_dotenv()

# Connect to and establish DB
try:
    conn = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USERSQL'),
        password=os.getenv('PASSWORD'),
    )
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS fastfood")
        print("DB Created")
        cursor.close()
        conn.close()
        
except mysql.connector.Error as e:
    print("Error while connecting to MySQL", e)