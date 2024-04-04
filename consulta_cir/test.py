import cv2
import numpy as np
import pyautogui
import time

# Carregar o template
template = cv2.imread("Screenshot_1.png", cv2.IMREAD_GRAYSCALE)

pyautogui.hotkey('winleft','d')
time.sleep(3)

if template is None:
    print("Erro ao carregar o template.")
    exit()

# Capturar a tela
screenshot = pyautogui.screenshot()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Encontrar a correspondência do template na captura de tela
result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Se a correspondência for suficientemente boa
if max_val > 0.8:
    # Mover o mouse para a localização da correspondência
    template_w, template_h = template.shape[::-1]
    center_x = max_loc[0] + (template_w // 2)
    center_y = max_loc[1] + (template_h // 2)
    pyautogui.moveTo(center_x, center_y)
else:
    print("Template não encontrado na tela.")
    
pyautogui.doubleClick()