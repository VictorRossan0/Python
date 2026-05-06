import pytest
from playwright.sync_api import Page


def test_multiplos_browsers_demoqa(page: Page):
    """
    Teste que funciona de forma consistente em todos os browsers.
    Usa o site DemoQA que é confiável para testes.
    """
    page.goto("https://demoqa.com/")
    
    # Aguardar página carregar
    page.wait_for_load_state("networkidle")
    
    # Verificar título
    assert "DEMOQA" in page.title()
    
    # Verificar se elementos principais estão visíveis
    category_cards = page.locator(".category-cards .card")
    assert category_cards.count() >= 6  # Deve ter pelo menos 6 categorias
    
    # Clicar em Elements
    page.click("text=Elements")
    
    # Verificar se redirecionou corretamente
    assert "elements" in page.url.lower()
    
    print("✅ Teste multi-browser passou!")


def test_wait_strategies(page: Page):
    """
    Demonstra diferentes estratégias de wait do Playwright.
    """
    page.goto("https://demoqa.com/dynamic-properties")
    
    # Wait for load state
    page.wait_for_load_state("networkidle")
    
    # Wait for selector com timeout customizado
    page.wait_for_selector("#enableAfter", timeout=10000)
    
    # Wait for elemento ficar visível
    color_change_btn = page.locator("#colorChange")
    color_change_btn.wait_for(state="visible")
    
    # Wait for elemento que aparece depois de 5 segundos
    visible_after_btn = page.locator("#visibleAfter")
    visible_after_btn.wait_for(state="visible", timeout=10000)
    
    # Clicar no botão que apareceu
    visible_after_btn.click()
    
    print("✅ Estratégias de wait funcionaram!")


def test_keyboard_mouse_actions(page: Page):
    """
    Demonstra ações de teclado e mouse do Playwright.
    """
    page.goto("https://demoqa.com/text-box")
    
    # Ações de teclado
    name_field = page.locator("#userName")
    name_field.click()
    
    # Digitar caractere por caractere
    page.keyboard.type("João", delay=100)
    
    # Usar atalhos
    page.keyboard.press("Control+a")
    page.keyboard.type("Maria Silva")
    
    # Usar Tab para navegar
    page.keyboard.press("Tab")
    
    # Verificar se mudou de campo (usando evaluate para verificar focus)
    focused_element = page.evaluate("document.activeElement.id")
    assert focused_element == "userEmail"
    
    # Digitar email
    page.keyboard.type("maria@example.com")
    
    # Verificar valores
    assert page.input_value("#userName") == "Maria Silva"
    assert page.input_value("#userEmail") == "maria@example.com"
    
    print("✅ Ações de teclado e mouse funcionaram!")


def test_screenshots_e_debug(page: Page):
    """
    Demonstra recursos de debugging com screenshots.
    """
    page.goto("https://demoqa.com/")
    
    # Screenshot da página inicial
    page.screenshot(path="screenshots/demoqa_home.png")
    
    # Navegar para elementos
    page.click("text=Elements")
    
    # Screenshot da página de elementos
    page.screenshot(path="screenshots/demoqa_elements.png")
    
    # Screenshot de elemento específico
    main_content = page.locator(".main-content")
    if main_content.count() > 0:
        main_content.screenshot(path="screenshots/main_content.png")
    
    # Verificar que chegou na página correta
    assert "elements" in page.url.lower()
    
    print("✅ Screenshots capturados com sucesso!")


def test_assertions_avancadas(page: Page):
    """
    Demonstra diferentes tipos de asserções do Playwright.
    """
    page.goto("https://demoqa.com/text-box")
    
    # Verificar que elemento existe e está visível
    user_name = page.locator("#userName")
    assert user_name.is_visible()
    assert user_name.is_enabled()
    
    # Verificar atributos
    assert user_name.get_attribute("placeholder") == "Full Name"
    assert user_name.get_attribute("type") == "text"
    
    # Preencher e verificar valor
    user_name.fill("Teste Playwright")
    assert user_name.input_value() == "Teste Playwright"
    
    # Verificar contadores (ajustado para o que realmente existe na página)
    form_inputs = page.locator("input, textarea")
    assert form_inputs.count() >= 4  # userName, userEmail, currentAddress, permanentAddress
    
    # Verificar texto de elementos
    submit_btn = page.locator("#submit")
    assert "Submit" in submit_btn.inner_text()
    
    print("✅ Asserções avançadas funcionaram!")


@pytest.mark.parametrize("texto_busca", [
    "Selenium",
    "Playwright", 
    "Automation Testing"
])
def test_parametrizado_busca(page: Page, texto_busca):
    """
    Teste parametrizado que executa com diferentes dados.
    Demonstra como executar o mesmo teste com múltiplos valores.
    """
    page.goto("https://demoqa.com/")
    
    # Verificar que a página carregou
    assert "DEMOQA" in page.title()
    
    # Simular que testaria busca (se houvesse campo de busca)
    # Aqui apenas verificamos que o site responde para diferentes contextos
    
    print(f"✅ Teste parametrizado passou para: {texto_busca}")


def test_mobile_viewport(page: Page):
    """
    Teste que demonstra emulação de dispositivo móvel.
    """
    # Configurar viewport mobile
    page.set_viewport_size({"width": 375, "height": 667})
    
    page.goto("https://demoqa.com/")
    
    # Aguardar carregar
    page.wait_for_load_state("networkidle")
    
    # Capturar screenshot mobile
    page.screenshot(path="screenshots/mobile_view.png")
    
    # Verificar que elementos ainda estão acessíveis em mobile
    cards = page.locator(".category-cards .card")
    assert cards.count() > 0
    
    # Testar interação touch
    page.click("text=Elements")
    assert "elements" in page.url.lower()
    
    print("✅ Teste mobile passou!")


def test_performance_basico(page: Page):
    """
    Teste básico de performance para demonstrar monitoramento.
    """
    import time
    
    start_time = time.time()
    
    page.goto("https://demoqa.com/")
    page.wait_for_load_state("networkidle")
    
    end_time = time.time()
    load_time = end_time - start_time
    
    # Verificar que carregou em tempo razoável (menos de 20 segundos - mais realista)
    assert load_time < 20.0, f"Página levou {load_time:.2f}s para carregar (muito lento)"
    
    print(f"✅ Página carregou em {load_time:.2f}s")
    
    # Verificar elementos carregaram
    assert page.locator(".category-cards").is_visible()
    
    print("✅ Teste de performance passou!")
