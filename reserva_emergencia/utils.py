from datetime import datetime

def entrada_float(mensagem: str) -> float:
    """
    Solicita ao usuário uma entrada de número decimal (float).
    Exibe uma mensagem de erro em caso de entrada inválida.
    """
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("Valor inválido! Por favor, insira um número decimal.")

def entrada_data(mensagem: str) -> str:
    """
    Solicita ao usuário uma entrada de data no formato dd/mm/aaaa.
    Exibe uma mensagem de erro em caso de entrada inválida.
    """
    while True:
        data = input(mensagem).strip()
        try:
            dia, mes, ano = map(int, data.split("/"))
            datetime(ano, mes, dia)  # Valida a data
            return data
        except (ValueError, IndexError):
            print("Data inválida! Por favor, insira no formato dd/mm/aaaa.")

def exibir_menu() -> int:
    """
    Exibe o menu principal do sistema e solicita ao usuário que selecione uma opção.
    Retorna o número da opção escolhida.
    """
    print("\n========== MENU ==========")
    print("1. Cadastrar Ativos/FIIs")
    print("2. Calcular Quantidade por Investimento")
    print("3. Calcular Diversificação do Investimento")
    print("4. Gerar Relatórios e Salvar em Excel")
    print("5. Sair do Programa")
    print("==========================")
    
    while True:
        try:
            opcao = int(input("Escolha uma opção: "))
            if 1 <= opcao <= 5:
                return opcao
            else:
                print("Opção inválida! Escolha um número entre 1 e 5.")
        except ValueError:
            print("Entrada inválida! Por favor, insira um número inteiro.")

def registrar_log(mensagem: str):
    """
    Registra mensagens de log com timestamp.
    """
    with open("log.txt", "a") as arquivo_log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        arquivo_log.write(f"[{timestamp}] {mensagem}\n")
