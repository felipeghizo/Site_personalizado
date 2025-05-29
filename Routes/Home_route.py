import json
import os
from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, template_folder='../templates', static_folder='../static')

CAMINHO_JSON = os.path.join(os.path.dirname(__file__), '../receitas/receitas.json')

@home_bp.route('/')
def home():
    with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
        receitas = json.load(f)
    return render_template("home.html", receitas=receitas)
