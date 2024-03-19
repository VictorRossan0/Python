from Execucao.limpeza import limpar_diretorio, limpar_pycache
from Execucao.login import preencher_captcha_e_enviar
from Execucao.consulta import fazer_consulta

if __name__ == "__main__":
    # Limpar o diretório __pycache__ antes de iniciar
    limpar_pycache()

    # Limpar o diretório Images antes de baixar novas imagens
    caminho_diretorio_images = 'Images'
    limpar_diretorio(caminho_diretorio_images)

    # Substitua 'seu_login' e 'sua_senha' pelos valores reais
    driver = preencher_captcha_e_enviar('t3wlvdt', 'SenhaWF2')

    # Fazer a consulta após preencher o captcha
    fazer_consulta(driver)
