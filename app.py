#Importações das bibliotecas necessárias
import streamlit as st	
import pandas as pd
import os
from datetime import date
import dotenv
import boto3
import pyodbc
#Importações das bibliotecas necessárias na construção e envio do email
import email.message
from pretty_html_table import build_table
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import emoji

#Conexão do BD
dotenv.load_dotenv(dotenv.find_dotenv())
server = os.getenv('SERVER_DB_KEY')
database = os.getenv('DATABASE_KEY')
username = os.getenv('USERNAME_DB_KEY')
password = os.getenv('PASSWORD_DB_KEY')
#Conexão email
ACCESS_ID = os.getenv('AWS_ACCESS_ID')
AWS_REGION_SERVE = os.getenv('AWS_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION_SERVE')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
