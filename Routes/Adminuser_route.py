from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import json
import os

# Configurações do Blueprint
admin_bp = Blueprint('admin', __name__, template_folder='../templates', static_folder='../static')

# Caminho do arquivo JSON de receitas
CAMINHO_JSON = os.path.join(os.path.dirname(__file__), '../Receitas/receitas.json')

# Senha do admin
ADMIN_PASSWORD = 'admin123'


# 🔐 Rota de login do admin
@admin_bp.route('/adminuser', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['logado'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Senha incorreta.', 'error')
    return render_template('adminuser.html')


# 🏠 Dashboard principal do admin
@admin_bp.route('/admin-dashboard')
def dashboard():
    if not session.get('logado'):
        return redirect(url_for('admin.admin_login'))

    with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
        receitas = json.load(f)

    for i, receita in enumerate(receitas):
        receita['index'] = i  # ✅ Adiciona índice real

    return render_template('adminhome.html', receitas=receitas)


# ➕ Adicionar nova receita
@admin_bp.route('/admin-addreceita', methods=['GET', 'POST'])
def add_receita():
    if not session.get('logado'):
        return redirect(url_for('admin.admin_login'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        autor = request.form.get('autor')
        ingredientes = request.form.get('ingredientes')
        categoria = request.form.get('categoria')
        modo_preparo = request.form.get('modo_preparo')
        imagem_file = request.files.get('imagem')

        imagem_path = ''
        if imagem_file and imagem_file.filename != '':
            print("ok")
            # Gera nome de arquivo sem extensão
            nome_base = secure_filename(os.path.splitext(imagem_file.filename)[0])
            filename = f"{nome_base}.png"
            imagem_path = f'img/{filename}'

            # Caminho completo para salvar
            save_path = os.path.join('static', 'img', filename)

            # Abrir e converter imagem
            img = Image.open(imagem_file.stream).convert('RGB')  # ou 'RGBA' se quiser transparência
            img.save(save_path, 'PNG')

        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            receitas = json.load(f)

        nova_receita = {
            'nome': nome,
            'autor': autor,
            'ingredientes': ingredientes,
            'modo_preparo': modo_preparo,
            'imagem': imagem_path,
            'categoria': categoria,
            'descricao': '',
            'iniciais': ''.join([palavra[0].upper() for palavra in autor.split()])
        }

        receitas.append(nova_receita)

        with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
            json.dump(receitas, f, indent=4, ensure_ascii=False)
        return redirect(url_for('admin.dashboard'))

    return render_template('adminaddreceita.html')

# ✏️ Editar receita
@admin_bp.route('/admin-editreceita/<int:index>', methods=['GET', 'POST'])
def edit_receita(index):
    if not session.get('logado'):
        return redirect(url_for('admin.admin_login'))

    with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
        receitas = json.load(f)

    if index >= len(receitas):
        flash('Receita não encontrada.', 'error')
        return redirect(url_for('admin.dashboard'))

    receita = receitas[index]

    if request.method == 'POST':
        receita['nome'] = request.form.get('nome')
        receita['autor'] = request.form.get('autor')
        receita['descricao'] = request.form.get('descricao')
        receita['categoria'] = request.form.get('categoria')
        ingredientes = request.form.get('ingredientes')
        modo_preparo = request.form.get('modo_preparo')
        receita['ingredientes'] = ingredientes
        receita['modo_preparo'] = modo_preparo
        receita['imagem'] = request.form.get('imagem')
        receita['iniciais'] = ''.join([p[0].upper() for p in receita['autor'].split()])

        with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
            json.dump(receitas, f, indent=4, ensure_ascii=False)
        return redirect(url_for('admin.dashboard'))

    return render_template('admineditreceita.html', receita=receita, index=index)

# ❌ Excluir receita
@admin_bp.route('/admin-deletereceita/<int:index>')
def delete_receita(index):
    if not session.get('logado'):
        return redirect(url_for('admin.admin_login'))

    with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
        receitas = json.load(f)

    if index < len(receitas):
        del receitas[index]
        with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
            json.dump(receitas, f, indent=4, ensure_ascii=False)
    else:
        flash('Receita não encontrada.', 'error')

    return redirect(url_for('admin.dashboard'))

# 🔓 Logout
@admin_bp.route('/admin-logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('admin.admin_login'))
