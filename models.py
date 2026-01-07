from database import db
from datetime import datetime

class Historico(db.Model):
    # Nome da tabela no banco
    __tablename__ = 'historico_jogos'

    id = db.Column(db.Integer, primary_key=True)
    escolha_usuario = db.Column(db.String(20), nullable=False)
    escolha_pc = db.Column(db.String(20), nullable=False)
    # Aqui guardamos o CÓDIGO (VITORIA, DERROTA, EMPATE)
    resultado = db.Column(db.String(20), nullable=False) 
    data_jogo = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Converte o objeto em JSON para mandarmos pro Front"""
        return {
            "id": self.id,
            "usuario": self.escolha_usuario,
            "pc": self.escolha_pc,
            "resultado": self.resultado,
            "data": self.data_jogo.strftime("%d/%m/%Y %H:%M")
        }