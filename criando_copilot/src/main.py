def greet_user(user_name):
    """
    Função simples para o Copilot interagir com o usuário.
    """
    greeting = f"Olá, {user_name}! Sou seu Copiloto. Em que posso ajudar hoje?"
    print(greeting)
    return greeting

def respond_to_user(user_input):
    """
    Função simulada para fornecer respostas com base na entrada do usuário.
    """
    responses = {
        "ajuda": "Claro! Posso ajudá-lo a organizar tarefas ou responder dúvidas específicas.",
        "tarefa": "Ótimo! Qual tarefa você gostaria de criar ou gerenciar?",
        "sair": "Até logo! Estou aqui se precisar novamente."
    }

    response = responses.get(user_input.lower(), "Desculpe, não entendi. Pode reformular sua pergunta?")
    print(response)
    return response

# Simulação de uso
if __name__ == "__main__":
    user_name = "Victor"  # Exemplo de nome de usuário
    user_input = "ajuda"  # Exemplo de entrada do usuário

    greet_user(user_name)
    respond_to_user(user_input)
