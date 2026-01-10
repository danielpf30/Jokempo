from flask import Flask, render_template, request, jsonify
from database import db
from jogo import JokempoService

# Configuração do Banco (Onde ele fica)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jokempo.db'

db.init_app(app)

# Garante q o app  vai acesar o models.py e criar as tabelas
with app.app_context():
    from models import Historico  # Import aqui dentro para ele registrar
    db.create_all()  # Cria o arquivo se não existir

# fica escutando a rota raiz
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jogar', methods=['POST'])
def jogar():
    dados = request.get_json()
    escolha_usuario = dados.get('escolha')

    service = JokempoService()
    resultado = service.validarVencedor(escolha_usuario)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True) 