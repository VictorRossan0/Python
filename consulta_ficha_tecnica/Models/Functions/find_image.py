import cv2
import numpy as np

def find_image(template_path, screenshot_path, threshold=0.8):
    template = cv2.imread(template_path, 0)
    screenshot = cv2.imread(screenshot_path, 0)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # A imagem foi encontrada
        return max_loc
    else:
        # A imagem não foi encontrada
        return None

# Exemplo de uso
template_path = 'Images/header.png'
screenshot_path = 'Screenshots/aviso_multa.png'

# Localizar a imagem no screenshot
position = find_image(template_path, screenshot_path)

if position is not None:
    # A imagem foi encontrada
    x, y = position
    # Execute as ações necessárias com as coordenadas (x, y)
    print("Imagem encontrada nas coordenadas:", x, y)
else:
    # A imagem não foi encontrada
    print("Imagem não encontrada no screenshot.")