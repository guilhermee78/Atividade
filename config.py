# config.py
import os

# Configurações do SQLAlchemy
SQLALCHEMY_DATABASE_URI =  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///atividade.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configurações do servidor Flask (se você quiser centralizá-las aqui)
HOST = '0.0.0.0'
PORT = 5003
DEBUG = True