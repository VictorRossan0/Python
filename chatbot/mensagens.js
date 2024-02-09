const opcoesFrequentes = [
    "1. Você sabe do que se trata a operação de Agendamento?",
    "2. Saberia me informar o que é um Roteador?",
    "3. Quais os serviços existentes para Configuração de Roteador?",
    // Adicione mais opções conforme necessário
];

const respostasOpcoesFrequentes = {
    "1": "Sim, o agendamento refere-se ao ato de programar e organizar eventos, tarefas ou atividades em um cronograma. No contexto de sistemas e software, o agendamento muitas vezes envolve a definição de horários para a execução automática de operações específicas.",
    "2": "Certamente! Um roteador é um dispositivo de rede que encaminha o tráfego de dados entre redes. Ele atua como um ponto de conexão entre diferentes redes, como a rede local em sua casa e a Internet. O roteador toma decisões com base nos endereços IP dos dados para encaminhá-los para o destino correto.",
    "3": "Existem vários serviços disponíveis para a configuração de roteadores, incluindo: ° Configuração Básica: Definir senha, nome da rede (SSID) e outros parâmetros, ° Encaminhamento de Porta: Direcionar o tráfego de entrada para serviços específicos,° Filtragem de Conteúdo: Controlar o acesso a determinados sites ou conteúdos,° VPN (Rede Privada Virtual): Configurar uma conexão segura entre redes remotas., ° Atualizações de Firmware: Manter o roteador atualizado para melhorar a segurança e desempenho.",
    // Adicione mais respostas conforme necessário
};

function exibirMensagem(chatMessages, mensagem) {
    chatMessages.innerHTML += `<div>${mensagem}</div>`;
}

function exibirOpcoesFrequentes() {
    const chatMessages = document.getElementById('chat-messages');

    opcoesFrequentes.forEach(opcao => {
        exibirMensagem(chatMessages, opcao);
    });

    exibirMensagem(chatMessages, 'Escolha uma opção digitando o número correspondente.');
}

function exibirResposta(chatMessages, usuario, resposta) {
    exibirMensagem(chatMessages, `Usuário: ${usuario}`);
    exibirMensagem(chatMessages, `Chatbot: ${resposta}`);
}

function exibirErro(chatMessages, mensagemErro) {
    exibirMensagem(chatMessages, mensagemErro);
}

function handleUserChoice(userChoice) {
    const chatMessages = document.getElementById('chat-messages');

    const choiceIndex = parseInt(userChoice) - 1;

    if (choiceIndex >= 0 && choiceIndex < opcoesFrequentes.length) {
        const selectedOption = opcoesFrequentes[choiceIndex];
        const resposta = respostasOpcoesFrequentes[userChoice];

        exibirResposta(chatMessages, selectedOption, resposta);
        salvarMensagemNoBancoDeDados(selectedOption);
    } else {
        exibirErro(chatMessages, 'Opção inválida. Por favor, escolha um número válido.');
    }
}

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const isUserChoice = /\b\d+\b/.test(userInput.trim());

    const chatMessages = document.getElementById('chat-messages');

    if (isUserChoice) {
        handleUserChoice(userInput.trim());
    } else {
        exibirMensagem(chatMessages, `Usuário: ${userInput}`);
        exibirMensagem(chatMessages, `Chatbot: Desculpe, ainda estou aprendendo. Não sei como responder a isso.`);
        salvarMensagemNoBancoDeDados(userInput);
    }

    // Limpar o conteúdo do campo de entrada do usuário
    document.getElementById('user-input').value = '';
}

function limparMensagens() {
    const chatMessages = document.getElementById('chat-messages');

    // Remover todas as mensagens (do Chatbot, Usuário ou mensagens de erro)
    const allMessages = Array.from(chatMessages.children);
    allMessages.forEach(message => {
        if (message.textContent.includes('Chatbot:') || message.textContent.includes('Usuário:') || message.textContent.includes('Opção inválida. Por favor, escolha um número válido.') || message.textContent.includes('Desculpe, ainda estou aprendendo. Não sei como responder a isso.')) {
            chatMessages.removeChild(message);
        }
    });
}

function salvarMensagemNoBancoDeDados(mensagem) {
    // Salvar a mensagem do usuário no banco de dados
    fetch('http://localhost:5000/salvar_mensagem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensagem }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Mensagem salva no banco de dados:', data);
        
        // Chamar a função para treinar o ChatBot com a nova mensagem
        treinarChatBotComNovaMensagem(mensagem);
    })
    .catch(error => console.error('Erro ao salvar mensagem no banco de dados:', error));
}

function treinarChatBotComNovaMensagem(mensagem) {
    // Chamar o backend para treinar o ChatBot com a nova mensagem
    fetch('http://localhost:5000/treinar_chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensagem }),  // Envie a mensagem como um objeto JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log('ChatBot treinado com sucesso:', data);
    })
    .catch(error => console.error('Erro ao treinar ChatBot:', error));
}

// Chamada inicial para exibir uma mensagem quando a página carregar
window.onload = function() {
    exibirOpcoesFrequentes();
};