import requests
from PIL import Image
from io import BytesIO

# Baixar uma imagem aleatória da internet
url = "https://picsum.photos/id/237/200/300"  # URL para uma imagem aleatória do Lorem Picsum (400x300 pixels)
response = requests.get(url)

# Verificar se o download foi bem-sucedido
if response.status_code == 200:
    # Carregar a imagem diretamente da memória
    imagem = Image.open(BytesIO(response.content))
    
    # Converter a imagem para níveis de cinza
    imagem_cinza = imagem.convert("L")
    
    # Converter para imagem binarizada (preto e branco)
    limiar = 128
    imagem_binaria = imagem_cinza.point(lambda p: 255 if p > limiar else 0)
    
    # Combinar as três imagens lado a lado
    largura_total = imagem.width * 3
    altura = imagem.height
    
    # Criar uma nova imagem combinada
    imagem_comb = Image.new("RGB", (largura_total, altura))
    
    # Colocar as três imagens lado a lado
    imagem_comb.paste(imagem, (0, 0))
    imagem_comb.paste(imagem_cinza.convert("RGB"), (imagem.width, 0))
    imagem_comb.paste(imagem_binaria.convert("RGB"), (imagem.width * 2, 0))
    
    # Mostrar a imagem combinada
    imagem_comb.show()
    
    # Salvar a imagem combinada
    imagem_comb.save("imagem_comb.png")
    
    print("Imagem processada e salva como 'imagem_comb.png'")
else:
    print(f"Erro ao baixar a imagem. Código de status: {response.status_code}")
