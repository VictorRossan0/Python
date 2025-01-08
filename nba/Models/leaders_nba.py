from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import pandas as pd
import json

def extrair_info_lideres():
    print("Abrindo o navegador")
    firefox_options = Options()
    firefox_options.add_argument('--headless')

    driver = webdriver.Firefox(options=firefox_options)

    url = 'https://www.espn.com.br/nba/estatisticas'
    driver.get(url)
    print("Navegador aberto")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'espnfitt'))
        )
        print("Estrutura da página foi carregada com sucesso")
    except TimeoutException:
        print("Timeout: A estrutura da página não foi carregada dentro do tempo limite.")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//script[contains(text(), "__espnfitt__")]'))
        )

        # Use XPath para encontrar o script desejado
        script_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//script[contains(text(), "__espnfitt__")]'))
        )
        print("XPath encontrado")

        # Extraia o conteúdo do script
        script_content = script_element.get_attribute('innerHTML')
        espnfitt_match = re.search(r'window\[\'__espnfitt__\'\]=(\{.*?\});', script_content)

        print("Conteúdo extraído")

        if espnfitt_match:
            espnfitt_json = espnfitt_match.group(1)
            print("Json Carregado com sucesso")
            espnfitt_data = json.loads(espnfitt_json)
            print("Content do Json carregado")

            # Especificando o caminho do arquivo de texto
            caminho_arquivo = 'TXT/conteudo_espnfitt.txt'

            # Convertendo a estrutura combinada para uma string formatada

            json_formatado = json.dumps(espnfitt_data['page']['content']['statistics']['leaders'], indent=2, ensure_ascii=False)

            # Escrevendo o conteúdo no arquivo
            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(json_formatado)

                print(f"\nConteúdo do '__espnfitt__' também salvo em '{caminho_arquivo}'")

            try:

                leaders_ofensivos = espnfitt_data['page']['content']['statistics']['leaders']['0']['groups']
                leaders_defensivos = espnfitt_data['page']['content']['statistics']['leaders']['1']['groups']

                # Criar DataFrame do Pandas para todos os líderes
                df_geral = pd.DataFrame(
                    columns=['Tipo', 'Rank', 'Nome de Jogador', 'Time', 'Valor'])

                # Preencher DataFrame com informações
                for group in leaders_ofensivos:
                    header = group['header']
                    leaders = group['leaders']

                    for leader in leaders:
                        rank = leader['rank']
                        player_name = leader['name']
                        team = leader['team']
                        stat_value = leader['statValue']

                        df_geral = pd.concat([df_geral, pd.DataFrame(
                            {'Tipo': [header], 'Rank': [rank], 'Nome de Jogador': [player_name], 'Time': [team], 'Valor': [stat_value]})])

                for group in leaders_defensivos:
                    header = group['header']
                    leaders = group['leaders']

                    for leader in leaders:
                        rank = leader['rank']
                        player_name = leader['name']
                        team = leader['team']
                        stat_value = leader['statValue']

                        df_geral = pd.concat([df_geral, pd.DataFrame(
                            {'Tipo': [header], 'Rank': [rank], 'Nome de Jogador': [player_name], 'Time': [team], 'Valor': [stat_value]})])

                # Salvar DataFrame em arquivo Excel
                caminho_excel = 'Excel/leaders_nba.xlsx'

                # Remover a coluna 'Tipo' do DataFrame principal
                df_geral_sem_tipo = df_geral.drop(columns=['Tipo'])

                # Cria um escritor Excel
                writer = pd.ExcelWriter(caminho_excel, engine='xlsxwriter')

                # Filtra e salva cada tabela sem a coluna 'Tipo'
                for tipo, tabela in df_geral.groupby('Tipo'):
                    tabela_sem_tipo = tabela.drop(columns=['Tipo'])
                    tabela_sem_tipo.to_excel(writer, sheet_name=tipo, index=False)

                # Fecha o escritor Excel
                writer.close()

                print(f"\nLíderes salvos em '{caminho_excel}'")

            except KeyError as e:
                print(f"Erro: A chave {e} não foi encontrada na estrutura do JSON. Verifique se a estrutura mudou.")
        else:
            print("JSON de '__espnfitt__' não encontrado no script")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()