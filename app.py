# app.py
from flask import Flask
from sql import db # Assumindo que 'sql.py' contém a instância 'db = SQLAlchemy()'
from atividade_controler import atividade_bp # Importa o Blueprint

app = Flask(__name__)

# --- CARREGA AS CONFIGURAÇÕES DO SEU ARQUIVO config.py ---
# O nome 'config' refere-se ao nome do arquivo config.py
app.config.from_object('config')

db.init_app(app) # Inicializa o SQLAlchemy com a aplicação Flask

# Registra o Blueprint da atividade
app.register_blueprint(atividade_bp, url_prefix='/atividades')

# Cria as tabelas do banco de dados se elas não existirem
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Use as configurações de HOST, PORT, DEBUG do config.py
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )