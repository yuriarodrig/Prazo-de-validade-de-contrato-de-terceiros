#Importações das bibliotecas necessárias
import streamlit as st	
import pandas as pd
import os
from datetime import date
import dotenv
import boto3

#Importações das bibliotecas necessárias na construção e envio do email
import email.message
from pretty_html_table import build_table
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import emoji