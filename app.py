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

def emissao_terceiro():
    cursor = conn.cursor()
    #Conexão com o banco de dados e buscando a minha query no banco procura a data de emissao, fornecedor, documento e a id do fornecedor
    query = pd.read_sql(
        "SELECT B6_EMISSAO AS DATA, B6_DOC AS DOCUMENTO, B6_CLIFOR AS C0D_FORNECEDOR, A2_NOME AS FORNECEDOR FROM SB6010 SB6 INNER JOIN SA2010 SA2 ON B6_CLIFOR = A2_COD WHERE B6_EMISSAO > '20220731'",
        conn)
    #data é a minha DATA DE EMISSAO DA NOTA, e vou transformar ela é datetime.    antes ela estava em object
    query['DATA'] = pd.to_datetime(query['DATA'])
    data = date.today()
    data = pd.to_datetime(data)  #transfomei a data atual em leitura datetime igual a minha query['DATA']
    query['Diferença de dias'] = data - query['DATA']  #Fiz a diferença de dias da data hoje(atual) com a data de emissão da nota 
    
    #Meu objetivo é avisar 1 semana antes data de vencimento, as notas tem um prazo de 180 dias
    #Então a diferença da data atual e a data emissão tem que ser 173 dias.   já está perto de 180 dias
    agrupar = (query.loc[(query['Diferença de dias'] == '173 days')])
    #Minha busca de notas está pronta