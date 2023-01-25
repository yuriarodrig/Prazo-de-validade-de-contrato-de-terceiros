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
EMAIL_ID = os.getenv('AWS_ACCESS_ID')
EMAIL_KEY = os.getenv('AWS_ACCESS_KEY')
EMAIL_REGIAO = os.getenv('AWS_REGION_SERVE')
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
    
    #Se o codigo do fornecedor estiver vazio, se for igual a false vai fazer o envio do email
    if agrupar['C0D_FORNECEDOR'].empty == False:
        html_tabela = build_table(agrupar, 'grey_light', font_family='sans-serif')
        corpo_email = html_tabela
        #grupo de emails que eu quero enviar essa notificação
        grupo_email = ['t.gmail.com', 't.gmail.com', 't.gmail.com']
        titulo = emoji.emojize(':warning: Notas a vencer prazo de 180 dias Poder 3º: ', variant="emoji_type")
        SENDER = 'WORKFLOW <ENVIAREMAIL@GMAIL.COM>'
        SUBJECT = titulo
        BODY_HTML = corpo_email
        CHARSET = 'UTF-8'
        
        #Conexão email 
        client = boto3.client('ses',region_name=EMAIL_REGIAO,
                    aws_access_key_id = EMAIL_ID,
                    aws_secret_access_key= EMAIL_KEY)

        msg = MIMEMultipart('mixed')
        msg['Subject'] = SUBJECT
        msg['From'] = SENDER
        msg['To'] = ', '.join(grupo_email)
        msg_body = MIMEMultipart('alternative')
        htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
        msg_body.attach(htmlpart)
        msg.attach(msg_body)
        
        response = client.send_raw_email(
            Source=SENDER,
            Destinations = grupo_email,
            RawMessage={
                'Data':msg.as_string(),
            },)
        print('''email enviado
        ---------------------''')
#CLIENTE ESTÁ VAZIO? TRUE(ESTÁ VAZIO)
    else:
        print('NÃO TEM NOTA')
emissao_terceiro()