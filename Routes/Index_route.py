from flask import Blueprint, render_template


index_bp = Blueprint('index', __name__,
                         template_folder='templates',
                         static_folder='static')

@index_bp.route('/')
def index_home():
    return render_template('datasheetos/datasheetos.html')
