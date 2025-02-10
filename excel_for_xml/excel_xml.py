import os
import pandas as pd
import xml.etree.ElementTree as ET

def excel_to_xml(input_excel: str, output_xml: str):
    """
    Converte um arquivo Excel em um arquivo XML.

    Parâmetros:
        input_excel (str): Caminho para o arquivo Excel de entrada.
        output_xml (str): Caminho para o arquivo XML de saída.
    """
    if not os.path.exists(input_excel):
        raise FileNotFoundError(f"O arquivo {input_excel} não existe.")

    # Carrega o arquivo Excel
    try:
        df = pd.read_excel(input_excel)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo Excel: {e}")

    # Cria o elemento raiz do XML
    root = ET.Element("Root")

    # Itera pelas linhas do DataFrame e cria elementos XML
    for _, row in df.iterrows():
        row_element = ET.SubElement(root, "Row")
        for col_name, value in row.items():
            col_element = ET.SubElement(row_element, col_name)
            col_element.text = str(value) if pd.notna(value) else ""

    # Gera a árvore XML
    tree = ET.ElementTree(root)

    # Escreve o XML no arquivo
    try:
        with open(output_xml, "wb") as xml_file:
            tree.write(xml_file, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        raise IOError(f"Erro ao escrever o arquivo XML: {e}")

def main():
    # Diretório base do código
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    
    print("Bem-vindo ao Conversor de Excel para XML")
    print("Por favor, siga as instruções abaixo.\n")

    # Nome do arquivo Excel esperado
    nome_arquivo_excel = input("Digite o nome do arquivo Excel (com extensão) que está no mesmo diretório deste código: ").strip()
    caminho_excel = os.path.join(diretorio_base, nome_arquivo_excel)

    # Verifica se o arquivo Excel existe
    if not os.path.exists(caminho_excel):
        print(f"Arquivo Excel não encontrado no diretório: {diretorio_base}")
        print("Por favor, coloque o arquivo Excel no mesmo diretório que este código e tente novamente.")
        return
    else:
        print(f"Arquivo Excel encontrado: {caminho_excel}")

    # Caminho do arquivo XML de saída
    caminho_xml = os.path.splitext(caminho_excel)[0] + ".xml"

    # Confirmar os dados antes de prosseguir
    print("\nResumo das Informações:")
    print(f"Arquivo Excel: {nome_arquivo_excel}")
    print(f"Arquivo XML de saída: {os.path.basename(caminho_xml)}")
    confirmar = input("Deseja continuar com a conversão? (S/N): ").strip().lower()
    if confirmar != 's':
        print("Conversão cancelada pelo usuário.")
        return

    # Realiza a conversão
    try:
        excel_to_xml(caminho_excel, caminho_xml)
        print(f"\nConversão realizada com sucesso! O arquivo XML foi salvo como: {os.path.basename(caminho_xml)}")
    except Exception as e:
        print(f"Ocorreu um erro durante a conversão: {e}")

if __name__ == "__main__":
    main()
