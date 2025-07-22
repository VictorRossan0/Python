import pytest
from playwright.sync_api import Page


class TestEcommercePage:
    """
    Classe de teste que simula testes em um site de e-commerce.
    Demonstra testes mais complexos e realistas.
    """
    
    def test_pesquisa_produto(self, page: Page):
        """Testa a funcionalidade de pesquisa de produtos."""
        # Navegar para o site de exemplo
        page.goto("https://demoqa.com/")
        
        # Verificar se a página carregou
        assert "DEMOQA" in page.title()
        
        # Navegar para a seção Elements
        page.click("text=Elements")
        
        # Clicar em Text Box
        page.click("text=Text Box")
        
        # Verificar se chegou na página correta
        assert page.url.endswith("/text-box")
    
    def test_adicionar_ao_carrinho(self, page: Page):
        """Simula adicionar um produto ao carrinho."""
        page.goto("https://automationexercise.com/")
        
        # Aguardar página carregar
        page.wait_for_load_state("networkidle")
        
        # Verificar se a página principal carregou
        assert page.is_visible("text=Automation Exercise")
        
        # Navegar para produtos
        page.click("text=Products")
        
        # Aguardar lista de produtos
        page.wait_for_selector(".product-image-wrapper", timeout=10000)
        
        # Verificar se produtos foram carregados
        products = page.locator(".product-image-wrapper")
        assert products.count() > 0
    
    def test_processo_checkout(self, page: Page):
        """Simula um processo de checkout básico."""
        page.goto("https://demoqa.com/automation-practice-form")
        
        # Preencher formulário de prática
        page.fill("#firstName", "João")
        page.fill("#lastName", "Silva")
        page.fill("#userEmail", "joao.silva@email.com")
        
        # Selecionar gênero
        page.click("label[for='gender-radio-1']")
        
        # Preencher telefone
        page.fill("#userNumber", "1234567890")
        
        # Selecionar hobbies
        page.click("label[for='hobbies-checkbox-1']")
        
        # Preencher endereço
        page.fill("#currentAddress", "Rua das Flores, 123, São Paulo, SP")
        
        # Fazer scroll para o botão submit ficar visível
        page.locator("#submit").scroll_into_view_if_needed()
        
        # Clicar em submit
        page.click("#submit")
        
        # Verificar se o modal de confirmação apareceu
        modal = page.locator(".modal-content")
        modal.wait_for(state="visible", timeout=5000)
        
        # Verificar conteúdo do modal
        assert "Thanks for submitting the form" in modal.inner_text()


class TestFormularios:
    """Testes focados em diferentes tipos de formulários."""
    
    def test_formulario_upload(self, page: Page):
        """Testa upload de arquivos."""
        page.goto("https://demoqa.com/upload-download")
        
        # Preparar um arquivo de teste
        test_file_content = "Conteúdo do arquivo de teste"
        
        # Simular upload de arquivo
        file_input = page.locator("#uploadFile")
        
        # Criar arquivo temporário para upload
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_file_content)
            temp_file_path = f.name
        
        try:
            # Fazer upload do arquivo
            file_input.set_input_files(temp_file_path)
            
            # Verificar se o nome do arquivo apareceu
            uploaded_path = page.locator("#uploadedFilePath")
            assert uploaded_path.is_visible()
            
        finally:
            # Limpar arquivo temporário
            os.unlink(temp_file_path)
    
    def test_formulario_selects(self, page: Page):
        """Testa diferentes tipos de seleção."""
        page.goto("https://demoqa.com/select-menu")
        
        # Dropdown simples
        page.click("#oldSelectMenu")
        page.click("option[value='3']")
        
        # Multi-select
        page.click("#cars")
        page.select_option("#cars", ["volvo", "audi"])
        
        # Verificar seleções
        selected_old = page.locator("#oldSelectMenu").input_value()
        assert selected_old == "3"


class TestInteracoesAvancadas:
    """Testes que demonstram interações mais avançadas."""
    
    def test_drag_and_drop(self, page: Page):
        """Testa arrastar e soltar elementos."""
        page.goto("https://demoqa.com/droppable")
        
        # Localizar elementos
        draggable = page.locator("#draggable")
        droppable = page.locator("#droppable")
        
        # Verificar estado inicial
        assert "Drop here" in droppable.inner_text()
        
        # Fazer drag and drop
        draggable.drag_to(droppable)
        
        # Verificar se o drop foi bem sucedido
        assert "Dropped!" in droppable.inner_text()
    
    def test_hover_actions(self, page: Page):
        """Testa ações de hover (passar mouse sobre)."""
        page.goto("https://demoqa.com/menu")
        
        # Fazer hover no menu principal
        main_item = page.locator("text=Main Item 2")
        main_item.hover()
        
        # Verificar se submenu apareceu
        sub_menu = page.locator("text=Sub Item")
        sub_menu.wait_for(state="visible")
        
        # Fazer hover no submenu
        sub_menu.hover()
        
        # Verificar sub-submenu
        sub_sub_menu = page.locator("text=SUB SUB LIST »")
        if sub_sub_menu.is_visible():
            sub_sub_menu.hover()
    
    def test_keyboard_actions(self, page: Page):
        """Testa ações de teclado."""
        page.goto("https://demoqa.com/text-box")
        
        # Focar no campo de nome
        name_field = page.locator("#userName")
        name_field.click()
        
        # Digitar usando teclado
        page.keyboard.type("Teste com teclado")
        
        # Usar atalhos de teclado
        page.keyboard.press("Control+a")  # Selecionar tudo
        page.keyboard.type("Texto substituído")
        
        # Usar Tab para navegar
        page.keyboard.press("Tab")
        
        # Verificar se foi para o próximo campo
        email_field = page.locator("#userEmail")
        assert email_field.is_focused()
        
        # Digitar email
        page.keyboard.type("test@example.com")


@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_cross_browser(page: Page, browser_name):
    """
    Teste parametrizado para executar em diferentes navegadores.
    Demonstra como testar compatibilidade cross-browser.
    """
    page.goto("https://www.google.com")
    
    # Verificar se o Google carregou em todos os browsers
    assert "Google" in page.title()
    
    # Testar pesquisa básica
    search_box = page.locator('input[name="q"]')
    search_box.fill(f"Playwright {browser_name}")
    search_box.press("Enter")
    
    # Aguardar resultados
    page.wait_for_selector('div[data-async-context*="Playwright"]', timeout=10000)
    
    print(f"Teste executado com sucesso no {browser_name}")
