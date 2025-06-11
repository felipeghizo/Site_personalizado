import json  
import os  
from flask import Blueprint, render_template  

# Cria um "Blueprint" chamado 'home', que permite organizar o código em módulos reutilizáveis.
# Define onde estão os templates HTML e os arquivos estáticos relativos a este blueprint.
home_bp = Blueprint('home', __name__, template_folder='../templates', static_folder='../static')

# Define o caminho absoluto para o arquivo receitas.json, que está na pasta 'receitas'.
CAMINHO_JSON = os.path.join(os.path.dirname(__file__), '../receitas/receitas.json')

# Define a rota principal '/' da aplicação.
@home_bp.route('/')
def home():
    # Abre o arquivo JSON de receitas no modo leitura e com codificação UTF-8.
    with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
        receitas = json.load(f)  # Carrega os dados do JSON em um dicionário/lista Python.

    # Renderiza o template 'home.html', passando os dados das receitas para uso no HTML.
    return render_template("home.html", receitas=receitas)
