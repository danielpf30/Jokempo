from enum import Enum
import random


class Jokempo(Enum):
    PEDRA = 'pedra'
    PAPEL = 'papel'
    TESOURA = 'tesoura'

    def vence(self, adversario):
        if self == adversario:

            return None  # Empate
        
        elif (self == Jokempo.PEDRA and adversario == Jokempo.TESOURA) or \
              self == Jokempo.PAPEL and adversario == Jokempo.PEDRA or \
              self == Jokempo.TESOURA and adversario == Jokempo.PAPEL:
            
             return True  # Venceu
        
        else:

             return False  # Perdeu

class JokempoService:
     
     def jogadaPc(self):
         try: 
             return random.choice(list(Jokempo))
         
         except Exception as e:
             print(f"Erro ao gerar jogada do PC: {e}")
             return None
         
     def validarVencedor(self, jogadaUsuarioStr, jogadaPc): 
         try:
           # Converter a jogada do usuário de string para o enum correspondente
            usuarioEnum = Jokempo(jogadaUsuarioStr)

           # Verificar o resultado da partida 
            resultado = usuarioEnum.vence(jogadaPc)

            # Pega o valor do pc como 'tesoura' pra mostrar na tela
            nome_pc = jogadaPc.value

            if resultado is None:
              return {
                  "mensagem": "Empate!",
                  "resultado": "EMPATE", # amarelo
                  "jogada_pc": nome_pc
              }
            
            elif resultado is True:
             return {
                 "mensagem": "Usuário venceu!",
                 "resultado": "VITORIA", # verde    
                 "jogada_pc": nome_pc
             }
            
            else:
             return {
                 "mensagem": "PC venceu!",
                 "resultado": "DERROTA", # vermelho
                 "jogada_pc": nome_pc
             }
            
         except ValueError:
             return {"mensagem": "Jogada Inválida!", "resultado": "ERRO", "escolha_pc": "?"}
         except Exception as e:
             return {"mensagem": "Erro interno", "resultado": "ERRO", "escolha_pc": "?"}