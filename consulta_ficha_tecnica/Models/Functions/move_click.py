from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def move_click(driver, xpath, string, max_wait=30):
    # Espera até que o elemento esteja clicável
    try:
        element = WebDriverWait(driver, max_wait).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        print(f"Tempo de espera esgotado para clicar em {string}")
        return False

    # Espera até que o spinner desapareça
    WebDriverWait(driver, max_wait).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'mdn-Spinner')))

    # Clica no elemento
    element.click()
    print(string)
    return True
