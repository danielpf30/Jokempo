from flask import Flask, render_template, request, jsonify
from database import db
from models import Historico
from jogo import JokempoService                                    

# cria uma instancia o flask 
# pra usar o flask e pra q ele tenha acesso ao projeto por completo
app = Flask(__name__)

# Configuração do Banco (Onde ele fica)
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

@app.route('/game')
def game():
    return render_template('jogo.html') 


# ROTA DE JOGAR (Recebe o JSON do JS e salva no Banco)
@app.route('/jogar', methods=['POST'])
def jogar():
    # 1. Recebe o pacote JSON do JavaScript
    dados = request.get_json()
    
    nome_jogador = dados.get('nome')
    escolha_usuario = dados.get('escolha') # Ex: "PEDRA" (Maiúsculo)

    # 2. Prepara o Service
    service = JokempoService()
    
    # 3. Gera a jogada do PC (O service devolve um ENUM aqui, não string)
    pc_enum = service.jogadaPc()

    # 4. Verifica o Vencedor
    # chama o método do service pra validar o vencedor
    resultado = service.validarVencedor(escolha_usuario, pc_enum)

    # Se deu erro na validação (ex: jogada inválida), para aqui
    if resultado['resultado'] == 'ERRO':
        return jsonify(resultado), 400

    # 5. Salva no Banco de dados
    # tem que fazer isso pq acima foi chamado os metodos pra armazenar os dados em variaveis soltas, e isso serve pra unilas em formato da tabela historico pra o banco conseguir salvar, pq ele so salva objetos do formato historico  
    novo_jogo = Historico(
        nome=nome_jogador,
        escolha_usuario=escolha_usuario, 
        escolha_pc=resultado['jogada_pc'],
        resultado=resultado['resultado'] 
    )
    
    db.session.add(novo_jogo)
    db.session.commit()
    
    # 6. Devolve pro Front (Convertendo o objeto do banco para dicionário)
    return jsonify(novo_jogo.to_dict())

@app.route('/historico', methods=['GET'])
def historico():
    historicos = Historico.query.order_by(Historico.data_jogo.desc()).all() 

    return render_template('historico.html', dados_historico = historicos)

# O "if" é uma trava de segurança, garante que o servidor só rode se executar esse arquivo diretamente.
if __name__ == '__main__':
    app.run(debug=True) 