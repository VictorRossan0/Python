import pytest
from playwright.sync_api import Page


def test_exemplo_basico_navegacao(page: Page):
    """
    Teste básico que demonstra navegação e verificação de título.
    Este é um exemplo simples para começar a entender o Playwright.
    """
    # Navegar para o Google
    page.goto("https://www.google.com")
    
    # Verificar se o título contém "Google"
    assert "Google" in page.title()
    
    # Aguardar o campo de pesquisa estar visível
    search_box = page.locator('input[name="q"]')
    search_box.wait_for(state="visible")
    
    # Digitar uma pesquisa
    search_box.fill("Playwright Python")
    
    # Pressionar Enter
    search_box.press("Enter")
    
    # Aguardar os resultados carregarem
    page.wait_for_selector('div[data-async-context="query:Playwright Python"]', timeout=10000)
    
    # Verificar se encontrou resultados
    results = page.locator('div[data-async-context="query:Playwright Python"] h3')
    assert results.count() > 0


def test_interacao_com_formulario(page: Page):
    """
    Teste que demonstra como interagir com formulários.
    Mostra preenchimento de campos, seleção e submissão.
    """
    # Ir para uma página de exemplo com formulário
    page.goto("https://demoqa.com/text-box")
    
    # Preencher campos do formulário
    page.fill("#userName", "João Silva")
    page.fill("#userEmail", "joao@example.com")
    page.fill("#currentAddress", "Rua das Flores, 123")
    page.fill("#permanentAddress", "Avenida Principal, 456")
    
    # Clicar no botão de submit
    page.click("#submit")
    
    # Verificar se os dados foram exibidos corretamente
    output = page.locator("#output")
    assert output.is_visible()
    
    # Verificar conteúdo específico
    assert "João Silva" in output.inner_text()
    assert "joao@example.com" in output.inner_text()


def test_captura_screenshot(page: Page):
    """
    Teste que demonstra como capturar screenshots.
    Útil para debugging e documentação de testes.
    """
    # Navegar para uma página
    page.goto("https://playwright.dev/")
    
    # Aguardar a página carregar completamente
    page.wait_for_load_state("networkidle")
    
    # Capturar screenshot da página inteira
    page.screenshot(path="screenshots/playwright_homepage.png", full_page=True)
    
    # Capturar screenshot de um elemento específico
    hero_section = page.locator('.hero')
    if hero_section.count() > 0:
        hero_section.screenshot(path="screenshots/hero_section.png")
    
    # Verificar título da página
    assert "Playwright" in page.title()


def test_aguardar_elementos(page: Page):
    """
    Teste que demonstra diferentes formas de aguardar elementos.
    Uma das grandes vantagens do Playwright é o auto-wait.
    """
    page.goto("https://demoqa.com/dynamic-properties")
    
    # Aguardar elemento que aparece após 5 segundos
    color_change_button = page.locator("#colorChange")
    color_change_button.wait_for(state="visible")
    
    # Aguardar elemento ficar habilitado
    enable_after_button = page.locator("#enableAfter")
    enable_after_button.wait_for(state="visible")
    # Note: O Playwright aguarda automaticamente o elemento ficar clicável
    
    # Aguardar elemento que só aparece depois de um tempo
    visible_after_button = page.locator("#visibleAfter")
    visible_after_button.wait_for(state="visible", timeout=10000)
    
    # Clicar no botão que apareceu
    visible_after_button.click()


def test_mobile_emulation(page: Page):
    """
    Teste que demonstra emulação de dispositivos móveis.
    O Playwright facilita testes responsivos.
    """
    # Configurar viewport para simular um iPhone
    page.set_viewport_size({"width": 375, "height": 667})
    
    # Navegar para uma página responsiva
    page.goto("https://www.w3schools.com/css/css_rwd_intro.asp")
    
    # Verificar se a página carregou
    assert page.title()
    
    # Capturar screenshot em modo mobile
    page.screenshot(path="screenshots/mobile_view.png")
    
    # Testar interação touch (simular toque)
    if page.locator('button, a').first.is_visible():
        page.locator('button, a').first.tap()


def test_interceptar_network(page: Page):
    """
    Teste que demonstra interceptação de requisições de rede.
    Útil para mockar APIs e controlar respostas.
    """
    # Configurar interceptação
    def handle_route(route):
        # Verificar se é uma requisição para API
        if "/api/" in route.request.url:
            # Mockar resposta
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"message": "Resposta mockada", "success": true}'
            )
        else:
            # Continuar com requisição normal
            route.continue_()
    
    # Interceptar todas as requisições
    page.route("**/*", handle_route)
    
    page.goto("https://jsonplaceholder.typicode.com/")
    
    # Verificar se a página carregou
    assert page.title()


@pytest.mark.slow
def test_multiplas_abas(page: Page):
    """
    Teste que demonstra trabalho com múltiplas abas.
    Marcado como 'slow' para execução opcional.
    """
    page.goto("https://demoqa.com/browser-windows")
    
    # Aguardar o contexto de nova aba
    with page.expect_popup() as popup_info:
        page.click("#tabButton")
    
    new_page = popup_info.value
    
    # Aguardar a nova página carregar
    new_page.wait_for_load_state()
    
    # Verificar conteúdo da nova aba
    assert new_page.url != page.url
    
    # Fechar a nova aba
    new_page.close()
    
    # Voltar para a aba original
    assert "Browser Windows" in page.title()
