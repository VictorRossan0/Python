import pytest
from playwright.sync_api import Page, expect, Browser, BrowserContext


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Configuração global para todos os contextos de browser.
    Define configurações padrão como viewport, user agent, etc.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }


@pytest.fixture
def authenticated_page(page: Page):
    """
    Fixture que retorna uma página já autenticada.
    Útil para testes que precisam de login.
    """
    # Simular login (adapte para seu sistema)
    page.goto("https://demoqa.com/login")
    
    # Se houvesse um sistema de login real:
    # page.fill("#username", "usuario_teste")
    # page.fill("#password", "senha_teste")
    # page.click("#login-button")
    # page.wait_for_url("**/dashboard")
    
    return page


class TestPerformance:
    """Testes focados em performance e métricas."""
    
    def test_tempo_carregamento(self, page: Page):
        """Testa o tempo de carregamento da página."""
        import time
        
        start_time = time.time()
        page.goto("https://playwright.dev/")
        page.wait_for_load_state("networkidle")
        end_time = time.time()
        
        load_time = end_time - start_time
        
        # Verificar se carregou em menos de 5 segundos
        assert load_time < 5.0, f"Página levou {load_time:.2f}s para carregar"
        
        print(f"Tempo de carregamento: {load_time:.2f}s")
    
    def test_metricas_web_vitals(self, page: Page):
        """Coleta métricas Web Vitals básicas."""
        page.goto("https://playwright.dev/")
        page.wait_for_load_state("networkidle")
        
        # Executar JavaScript para coletar métricas
        metrics = page.evaluate("""
            () => {
                return {
                    url: window.location.href,
                    title: document.title,
                    loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
                    domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
                    firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
                };
            }
        """)
        
        print(f"Métricas coletadas: {metrics}")
        
        # Verificar se as métricas estão dentro do esperado
        assert metrics['loadTime'] < 5000  # menos de 5 segundos
        assert len(metrics['title']) > 0


class TestAPI:
    """Testes de API usando o Playwright."""
    
    def test_api_request(self, page: Page):
        """Testa requisições diretas de API."""
        # Fazer requisição GET
        response = page.request.get("https://jsonplaceholder.typicode.com/users/1")
        
        assert response.status == 200
        
        data = response.json()
        assert data["id"] == 1
        assert "name" in data
        assert "email" in data
        
        print(f"Usuário obtido: {data['name']} - {data['email']}")
    
    def test_api_post(self, page: Page):
        """Testa requisição POST para API."""
        new_post = {
            "title": "Teste Playwright",
            "body": "Conteúdo do post de teste",
            "userId": 1
        }
        
        response = page.request.post(
            "https://jsonplaceholder.typicode.com/posts",
            data=new_post
        )
        
        assert response.status == 201
        
        created_post = response.json()
        assert created_post["title"] == new_post["title"]
        assert created_post["body"] == new_post["body"]
        
        print(f"Post criado com ID: {created_post['id']}")


class TestAccessibility:
    """Testes de acessibilidade."""
    
    def test_aria_labels(self, page: Page):
        """Verifica presença de labels de acessibilidade."""
        page.goto("https://demoqa.com/automation-practice-form")
        
        # Verificar se campos importantes têm labels
        first_name = page.locator("#firstName")
        assert first_name.get_attribute("placeholder") or page.locator("label[for='firstName']").count() > 0
        
        # Verificar botões com texto descritivo
        submit_button = page.locator("#submit")
        assert submit_button.inner_text().strip() != ""
    
    def test_keyboard_navigation(self, page: Page):
        """Testa navegação por teclado."""
        page.goto("https://demoqa.com/text-box")
        
        # Começar navegação por Tab
        page.keyboard.press("Tab")
        
        # Verificar se o primeiro campo está focado
        first_field = page.locator("#userName")
        assert first_field.is_focused()
        
        # Continuar navegação
        page.keyboard.press("Tab")
        email_field = page.locator("#userEmail")
        assert email_field.is_focused()


class TestErrorHandling:
    """Testes para tratamento de erros."""
    
    def test_pagina_404(self, page: Page):
        """Testa comportamento em página 404."""
        response = page.goto("https://httpstat.us/404")
        assert response.status == 404
    
    def test_timeout_handling(self, page: Page):
        """Testa tratamento de timeouts."""
        page.goto("https://demoqa.com/")
        
        # Tentar encontrar elemento que não existe com timeout curto
        with pytest.raises(Exception):
            page.wait_for_selector("#elemento-inexistente", timeout=1000)
    
    def test_network_failure(self, page: Page):
        """Simula falha de rede."""
        # Interceptar e falhar requisições
        page.route("**/*", lambda route: route.abort())
        
        # Tentar navegar (deve falhar)
        with pytest.raises(Exception):
            page.goto("https://www.google.com", timeout=5000)


@pytest.mark.slow
class TestDataDriven:
    """Testes orientados a dados (Data-Driven Tests)."""
    
    # Dados de teste
    test_users = [
        {"name": "João Silva", "email": "joao@test.com", "phone": "11999999999"},
        {"name": "Maria Santos", "email": "maria@test.com", "phone": "11888888888"},
        {"name": "Pedro Costa", "email": "pedro@test.com", "phone": "11777777777"}
    ]
    
    @pytest.mark.parametrize("user_data", test_users)
    def test_cadastro_usuarios(self, page: Page, user_data):
        """Testa cadastro com diferentes dados de usuário."""
        page.goto("https://demoqa.com/text-box")
        
        # Preencher formulário com dados do usuário
        page.fill("#userName", user_data["name"])
        page.fill("#userEmail", user_data["email"])
        page.fill("#currentAddress", f"Endereço de {user_data['name']}")
        
        # Submeter formulário
        page.click("#submit")
        
        # Verificar se dados foram exibidos
        output = page.locator("#output")
        assert output.is_visible()
        assert user_data["name"] in output.inner_text()
        assert user_data["email"] in output.inner_text()


class TestVisualRegression:
    """Testes de regressão visual (comparação de screenshots)."""
    
    def test_visual_homepage(self, page: Page):
        """Compara screenshot da homepage."""
        page.goto("https://playwright.dev/")
        page.wait_for_load_state("networkidle")
        
        # Capturar screenshot
        screenshot = page.screenshot()
        
        # Em um cenário real, você compararia com uma imagem baseline
        # assert compare_images(screenshot, "baseline/homepage.png")
        
        # Por enquanto, apenas verificamos se o screenshot foi capturado
        assert len(screenshot) > 0
    
    def test_visual_mobile(self, page: Page):
        """Teste visual em modo mobile."""
        # Configurar como dispositivo móvel
        page.set_viewport_size({"width": 375, "height": 667})
        
        page.goto("https://playwright.dev/")
        page.wait_for_load_state("networkidle")
        
        # Capturar screenshot mobile
        mobile_screenshot = page.screenshot()
        assert len(mobile_screenshot) > 0
        
        print("Screenshot mobile capturado com sucesso")
