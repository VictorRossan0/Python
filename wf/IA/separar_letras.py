import cv2
import os
import glob
import shutil

# Adicione essas linhas antes do restante do seu código
pasta_letras = 'IA/letras'
pasta_identificado = 'IA/identificado'

# Remover o conteúdo das pastas 'letras' e 'identificado' se já existirem
if os.path.exists(pasta_letras):
    shutil.rmtree(pasta_letras)
    print(f"Conteúdo da pasta '{pasta_letras}' removido com sucesso.")

if os.path.exists(pasta_identificado):
    shutil.rmtree(pasta_identificado)
    print(f"Conteúdo da pasta '{pasta_identificado}' removido com sucesso.")

# Criar novamente as pastas 'letras' e 'identificado'
os.makedirs(pasta_letras)
print(f"Pasta '{pasta_letras}' criada com sucesso.")

os.makedirs(pasta_identificado)
print(f"Pasta '{pasta_identificado}' criada com sucesso.")

arquivos = glob.glob('IA/Images_IA/*')  # Alteração do diretório de origem

for arquivo in arquivos:
    imagem = cv2.imread(arquivo)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    # EM PRETO E BRANCO
    _, imagem = cv2.threshold(imagem, 128, 255, cv2.THRESH_BINARY_INV)

    # # Visualizar a imagem após a binarização
    # cv2.imshow('Imagem binarizada', imagem)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # ENCONTRAR OS CONTORNOS DE CADA LETRA
    contornos, _ = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regiao_letras = []

    # Filtrar os contornos que são realmente de letras e números
    for i, contorno in enumerate(contornos, 1):
        (x, y, largura, altura) = cv2.boundingRect(contorno)
        area = cv2.contourArea(contorno)
        if area > 5.5:
            regiao_letras.append((x, y, largura, altura))
            print(f"Contornos{i}", (x, y, largura, altura))

    # Desenhar os contornos diretamente na imagem original
    imagem_final = imagem.copy()

    for i, retangulo in enumerate(regiao_letras, 1):
        x, y, largura, altura = retangulo
        imagem_letra = imagem[y:y+altura+5, x:x+largura+5]
        nome_arquivo = os.path.basename(arquivo).replace(".png", f"letra{i}numero{i}.png")
        cv2.imwrite(f'IA/letras/{nome_arquivo}', imagem_letra)  # Alteração do diretório de destino
        cv2.rectangle(imagem_final, (x, y), (x+largura+5, y+altura+5), (0, 255, 0), 1)
        print(f'IA/letras/{nome_arquivo}')

    nome_arquivo = os.path.basename(arquivo)
    cv2.imwrite(f"IA/identificado/{nome_arquivo}", imagem_final)
    print(f"IA/identificado/{nome_arquivo}")
