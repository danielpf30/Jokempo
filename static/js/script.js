// Variáveis de Estado (Memória do navegador)
let nomeJogador = "";
let pontosUser = 0;
let pontosPC = 0;

// Controla a entrada do nome 
function confirmarNome() {
    const input = document.getElementById('input-nome');
    const nomeDigitado = input.value.trim(); // .trim() remove espaços em branco

    if (nomeDigitado === "") {
        alert("Ei! Digite um nome para jogar.");
        return;
    }

    nomeJogador = nomeDigitado; 

    // Troca os elementos na tela
    document.getElementById('container-input').style.display = 'none'; // Some input
    document.getElementById('container-placar').style.display = 'block'; // Aparece placar
    
    // Atualiza o nome lá no canto esquerdo
    const displayNome = document.getElementById('nome-display');
    displayNome.innerText = nomeJogador;
    displayNome.style.display = 'inline-block';

    // Libera a mesa de jogo (Tira a transparência e permite clicar)
    const mesa = document.getElementById('mesa-jogo');
    mesa.style.opacity = '1';
    mesa.style.pointerEvents = 'auto'; // Reativa os cliques
}

//  Envia a jogada para o Python e recebe o resultado
async function jogar(escolha) {
    
    //  Prepara o pacote para enviar
    const dados = {
     // chave : valor/variavel
        escolha: escolha,
        nome: nomeJogador
    };

    try {
       // headers: tipo : categoria/tipo, q no caso é json
       // body: o conteudo real q vai ser enviado
        const response = await fetch('/jogar', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(dados)
        });
        
        // Recebe a resposta do Python
        if (!response.ok){
             throw new Error('Erro na conexão com o servidor');
        }
        // Abre a caixa e lê o conteudo que esta no body, transformando em json
        const resultado = await response.json();
        
        atualizarPlacar(resultado);

    } catch (erro) {
        console.error(erro);
        alert("Erro técnico! O servidor Python fora do ar!!");
    }
}

// Atualiza o placar e mensagens 
function atualizarPlacar(dados) {
    const txtResultado = document.getElementById('msg-resultado');
    
    // Define a mensagem e a cor
    if (dados.resultado === 'VITORIA') {
        txtResultado.innerText = `BOA, ${nomeJogador}! VOCÊ GANHOU!`;
        txtResultado.className = 'text-success fw-bold'; // Classe verde do Bootstrap
        pontosUser++;
    } else if (dados.resultado === 'DERROTA') {
        txtResultado.innerText = "IHH... O PYTHON GANHOU!";
        txtResultado.className = 'text-danger fw-bold'; // Classe vermelha do Bootstrap
        pontosPC++;
    } else {
        txtResultado.innerText = "EMPATE TÉCNICO!";
        txtResultado.className = 'text-warning fw-bold'; // Classe amarela do Bootstrap
    }

    // Atualiza os números
    document.getElementById('placar-user').innerText = pontosUser;
    document.getElementById('placar-pc').innerText = pontosPC;
}

// Permitir apertar ENTER no input de nome
/* usa o evento keypress como gatilho dizendo, avise toda vez que uma tecla for pressionada 
dentro do input de nome, o funcion(e), gera um relatorio automatico com informaçoes como,
qual tecla foi, o permite verificar se foi o Enter, pra chamar a função confirmarNome */
document.getElementById('input-nome').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        confirmarNome();
    }
});