from cadastro import cadastrar_dados
from calculos import calcular_quantidade_por_investimento, calcular_diversificacao_por_investimento, calcular_rentabilidade
from relatorios import salvar_em_excel
from utils import exibir_menu, registrar_log

def main():
    """
    Função principal que controla o fluxo do programa de gestão de investimentos.
    """
    dados = []  # Lista para armazenar os dados cadastrados

    registrar_log("Programa iniciado.")  # Log de início do programa

    while True:
        try:
            # Exibir menu e capturar a opção do usuário
            opcao = exibir_menu()

            if opcao == 1:
                # Cadastrar novos ativos ou FIIs
                registrar_log("Usuário acessou a opção de cadastrar dados.")
                dados.extend(cadastrar_dados())
            
            elif opcao == 2:
                # Calcular quantidade necessária de cotas para atingir um valor investido
                if not dados:
                    print("Nenhum dado cadastrado. Por favor, cadastre ativos primeiro.")
                else:
                    registrar_log("Usuário acessou a opção de calcular quantidade por investimento.")
                    calcular_quantidade_por_investimento(dados)
            
            elif opcao == 3:
                # Calcular diversificação por investimento
                if not dados:
                    print("Nenhum dado cadastrado. Por favor, cadastre ativos primeiro.")
                else:
                    registrar_log("Usuário acessou a opção de calcular diversificação por investimento.")
                    calcular_diversificacao_por_investimento(dados)
            
            elif opcao == 4:
                # Gerar relatório e salvar no Excel
                if not dados:
                    print("Nenhum dado cadastrado. Por favor, cadastre ativos primeiro.")
                else:
                    registrar_log("Usuário acessou a opção de gerar relatório.")
                    relatorio_rentabilidade = calcular_rentabilidade(dados)
                    salvar_em_excel(dados, relatorio_rentabilidade)
            
            elif opcao == 5:
                # Encerrar o programa
                print("Saindo do programa. Até logo!")
                registrar_log("Programa encerrado pelo usuário.")
                break
            
            else:
                print("Opção inválida! Por favor, escolha uma opção válida.")
                registrar_log("Usuário tentou acessar uma opção inválida.")
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            registrar_log(f"Erro capturado: {e}")

if __name__ == "__main__":
    main()
