from flask import Flask, redirect, url_for
from Routes.Home_route import home_bp
from Routes.Adminuser_route import admin_bp 

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'

# Registrando os blueprints com prefixos
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(admin_bp, url_prefix='/adminuser')

# Rota raiz (/) direciona para tela de login admin
@app.route("/")
def home_redirect():
    return redirect(url_for('home.home'))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
