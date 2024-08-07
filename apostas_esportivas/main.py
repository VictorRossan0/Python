def calcular_apostas(banca, valor_unidade):
    # Calcula o valor das apostas com base na banca e no valor da unidade
    aposta_1u = banca * 0.02  # 1 unidade representa 2% da banca
    aposta_05u = aposta_1u / 2
    aposta_025u = aposta_1u / 4
    return aposta_1u, aposta_05u, aposta_025u

def main():
    try:
        # Obtém o valor da banca e da unidade do usuário
        banca = float(input("Digite o valor da sua banca: ").replace(",", ""))
        if banca <= 0:
            raise ValueError("O valor da banca deve ser maior que zero.")
        valor_unidade = float(input("Digite o valor da sua unidade: ").replace(",", ""))
        if valor_unidade <= 0:
            raise ValueError("O valor da unidade deve ser maior que zero.")
        # Calcula as apostas
        aposta_1u, aposta_05u, aposta_025u = calcular_apostas(banca, valor_unidade)
        # Imprime os resultados formatados
        print(f"Para uma banca de ${banca:,.2f} e uma unidade de ${valor_unidade:,.2f}, as apostas seriam:\n"
              f"1u: ${aposta_1u:,.2f}\n"
              f"0.5u: ${aposta_05u:,.2f}\n"
              f"0.25u: ${aposta_025u:,.2f}")
    except ValueError as e:
        # Trata erros de valor inválido
        print(f"Erro: {e}. Por favor, digite um valor numérico válido.")

if __name__ == "__main__":
    main()
