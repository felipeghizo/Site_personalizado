from flask import Flask, render_template
from Routes.Index_route import index_bp

app = Flask(__name__)

app.register_blueprint(index_bp, url_prefix='/dcre')

app.secret_key = 'Somos_uma_empresa_de_tecnologia_pensada_para_aprimorar_o_seu_negócio_e_a_sua_casa.'

@app.route("/")
def home():
    return render_template("portal/index.html")  

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")