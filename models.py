from database import db
from datetime import datetime

"""" O db.Model transforma o cod python em tabela no banco de dados """
class Historico(db.Model):
    # Nome da tabela no banco
    __tablename__ = 'historico_jogos'
    """" O create cria a tabela a partir dessa tabela """
    """" Definindo as colunas da tabela"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    escolha_usuario = db.Column(db.String(20), nullable=False)
    escolha_pc = db.Column(db.String(20), nullable=False)
    # Aqui guardamos o CÓDIGO (VITORIA, DERROTA, EMPATE)
    resultado = db.Column(db.String(20), nullable=False) 
    data_jogo = db.Column(db.DateTime, default=datetime.utcnow)
    

    def to_dict(self):
        """Converte o objeto em JSON para mandarmos pro Front"""
        return {
            "id": self.id,
            "nome": self.nome,
            "usuario": self.escolha_usuario,
            "pc": self.escolha_pc,
            "resultado": self.resultado,
            "data": self.data_jogo.strftime("%d/%m/%Y %H:%M")
        }