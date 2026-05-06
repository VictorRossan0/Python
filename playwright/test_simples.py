import pytest
from playwright.sync_api import Page, sync_playwright


def test_navegacao_simples(page: Page):
    """
    Teste básico que demonstra navegação simples.
    Usando um site confiável para demonstração.
    """
    # Navegar para um site de exemplo
    page.goto("https://example.com")
    
    # Verificar se o título é correto
    assert "Example Domain" in page.title()
    
    # Verificar se o elemento h1 existe
    h1_element = page.locator("h1")
    assert h1_element.is_visible()
    
    # Verificar texto do h1
    assert "Example Domain" in h1_element.inner_text()
    
    print("✅ Teste de navegação simples passou!")


def test_playwright_site(page: Page):
    """
    Teste que acessa o site oficial do Playwright.
    """
    page.goto("https://playwright.dev/")
    
    # Aguardar a página carregar
    page.wait_for_load_state("networkidle")
    
    # Verificar se o título contém Playwright
    assert "Playwright" in page.title()
    
    print("✅ Site do Playwright carregou com sucesso!")


def test_captura_screenshot_simples(page: Page):
    """
    Teste que demonstra captura de screenshot.
    """
    page.goto("https://example.com")
    
    # Aguardar página carregar
    page.wait_for_load_state("networkidle")
    
    # Capturar screenshot
    page.screenshot(path="screenshots/example_site.png")
    
    print("✅ Screenshot capturado com sucesso!")


def test_interacao_basica(page: Page):
    """
    Teste usando um site de demonstração com formulários mais confiável.
    """
    page.goto("https://demoqa.com/text-box")
    
    # Aguardar página carregar com timeout maior
    page.wait_for_load_state("domcontentloaded")
    
    # Aguardar elementos estarem visíveis
    page.wait_for_selector("#userName", timeout=10000)
    
    # Preencher campos do formulário
    page.fill("#userName", "João Silva")
    page.fill("#userEmail", "joao@example.com")
    page.fill("#currentAddress", "Rua das Flores, 123")
    page.fill("#permanentAddress", "Avenida Principal, 456")
    
    # Verificar se os campos foram preenchidos
    assert page.input_value("#userName") == "João Silva"
    assert page.input_value("#userEmail") == "joao@example.com"
    assert "Rua das Flores" in page.input_value("#currentAddress")
    
    # Clicar no botão submit
    page.click("#submit")
    
    # Verificar se output apareceu
    output = page.locator("#output")
    output.wait_for(state="visible", timeout=10000)
    
    # Verificar conteúdo do output
    output_text = output.inner_text()
    assert "João Silva" in output_text
    assert "joao@example.com" in output_text
    
    print("✅ Interação com formulário funcionou!")


def test_elementos_dinamicos(page: Page):
    """
    Teste usando site de demonstração com elementos dinâmicos.
    """
    page.goto("https://the-internet.herokuapp.com/dynamic_loading/1")
    
    # Clicar no botão start
    page.click("button")
    
    # Aguardar texto aparecer (máximo 10 segundos)
    page.wait_for_selector("#finish", timeout=10000)
    
    # Verificar se o texto final apareceu
    finish_text = page.locator("#finish").inner_text()
    assert "Hello World!" in finish_text
    
    print("✅ Teste de elementos dinâmicos passou!")


def executar_testes_diretamente():
    """
    Executa os testes diretamente sem pytest.
    Permite executar com: python test_simples.py
    """
    print("🚀 Executando testes Playwright diretamente...")
    print("=" * 60)
    
    # Lista de testes para executar
    testes = [
        ("Navegação Simples", test_navegacao_simples),
        ("Site Playwright", test_playwright_site),
        ("Captura Screenshot", test_captura_screenshot_simples),
        ("Interação Básica", test_interacao_basica),
        ("Elementos Dinâmicos", test_elementos_dinamicos)
    ]
    
    sucessos = 0
    falhas = 0
    
    with sync_playwright() as p:
        # Iniciar browser (pode escolher: chromium, firefox, webkit)
        browser = p.chromium.launch(headless=False)  # headless=False para ver o browser
        context = browser.new_context()
        page = context.new_page()
        
        for nome_teste, funcao_teste in testes:
            try:
                print(f"\n🧪 Executando: {nome_teste}")
                print("-" * 40)
                
                funcao_teste(page)
                sucessos += 1
                print(f"✅ {nome_teste} - PASSOU")
                
            except Exception as e:
                falhas += 1
                print(f"❌ {nome_teste} - FALHOU")
                print(f"   Erro: {str(e)}")
            
            # Pequena pausa entre testes
            page.wait_for_timeout(1000)
        
        browser.close()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES:")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📈 Taxa de sucesso: {(sucessos/(sucessos+falhas)*100):.1f}%")
    
    if falhas == 0:
        print("🎉 TODOS OS TESTES PASSARAM!")
    else:
        print(f"⚠️  {falhas} teste(s) falharam")
    
    print("=" * 60)


if __name__ == "__main__":
    executar_testes_diretamente()
