import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import pandas as pd

def extrair_info_teams():
    print("Abrindo o navegador")
    firefox_options = Options()
    firefox_options.add_argument('--headless')

    driver = webdriver.Firefox(options=firefox_options)

    url = 'https://www.espn.com.br/nba/estatisticas/_/vista/time'
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
            caminho_arquivo = 'TXT/conteudo_teams.txt'

            # Convertendo a estrutura combinada para uma string formatada
            json_formatado = json.dumps(espnfitt_data, indent=2, ensure_ascii=False)

            # Escrevendo o conteúdo no arquivo
            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                arquivo.write(json_formatado)

            print(f"\nConteúdo do '__espnfitt__' também salvo em '{caminho_arquivo}'")

            try:
                # Criar listas para armazenar os dados temporariamente
                data = []

                # Preencher listas com informações de líderes ofensivos
                for group in espnfitt_data['page']['content']['statistics']['leaders']['0']['groups']:
                    header = group['header']
                    leaders = group['leaders']

                    for leader in leaders:
                        rank = leader['rank']
                        team = leader['name']
                        stat_value = leader['statValue']

                        data.append({'Tipo': header, 'Rank': rank, 'Nome do Time': team, 'Valor': stat_value})

                # Preencher listas com informações de líderes defensivos
                for group in espnfitt_data['page']['content']['statistics']['leaders']['1']['groups']:
                    header = group['header']
                    leaders = group['leaders']

                    for leader in leaders:
                        rank = leader['rank']
                        team = leader['name']
                        stat_value = leader['statValue']

                        data.append({'Tipo': header, 'Rank': rank, 'Nome do Time': team, 'Valor': stat_value})

                # Criar DataFrame do Pandas com os dados coletados
                df_geral = pd.DataFrame(data)

                # Salvar DataFrame em arquivo Excel
                caminho_excel = 'Excel/team_leaders_nba.xlsx'

                # Cria um escritor Excel
                with pd.ExcelWriter(caminho_excel, engine='xlsxwriter') as writer:
                    # Filtra e salva cada tabela sem a coluna 'Tipo'
                    for tipo, tabela in df_geral.groupby('Tipo'):
                        tabela_sem_tipo = tabela.drop(columns=['Tipo'])
                        tabela_sem_tipo.to_excel(writer, sheet_name=tipo, index=False)

                print(f"\nLíderes salvos em '{caminho_excel}'")

            except KeyError as e:
                print(f"Erro: A chave {e} não foi encontrada na estrutura do JSON. Verifique se a estrutura mudou.")
        else:
            print("JSON de '__espnfitt__' não encontrado no script")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()