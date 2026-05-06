#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de Playwright executado diretamente sem pytest.
Execute com: python exemplo_direto.py

Este arquivo demonstra como usar Playwright de forma standalone,
sem a necessidade do pytest.
"""

from playwright.sync_api import sync_playwright
import os


def criar_diretorio_screenshots():
    """Cria diretório para screenshots se não existir."""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")


def teste_navegacao_basica():
    """Teste básico de navegação."""
    print("🧪 Executando teste de navegação básica...")
    
    with sync_playwright() as p:
        # Iniciar browser
        browser = p.chromium.launch(headless=False)  # Mude para True se não quiser ver o browser
        page = browser.new_page()
        
        try:
            # Navegar para example.com
            page.goto("https://example.com")
            
            # Verificar título
            titulo = page.title()
            print(f"   📄 Título da página: {titulo}")
            
            if "Example Domain" in titulo:
                print("   ✅ Título correto encontrado!")
            else:
                print("   ❌ Título incorreto!")
                
            # Capturar screenshot
            criar_diretorio_screenshots()
            page.screenshot(path="screenshots/exemplo_direto.png")
            print("   📸 Screenshot capturado!")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False
        finally:
            browser.close()


def teste_formulario_demoqa():
    """Teste de preenchimento de formulário."""
    print("🧪 Executando teste de formulário...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navegar para formulário de teste
            page.goto("https://demoqa.com/text-box")
            print("   🌐 Página carregada")
            
            # Aguardar página carregar
            page.wait_for_selector("#userName", timeout=10000)
            
            # Preencher formulário
            page.fill("#userName", "Teste Playwright")
            page.fill("#userEmail", "teste@playwright.com")
            
            print("   ✏️  Formulário preenchido")
            
            # Verificar se foi preenchido
            nome = page.input_value("#userName")
            email = page.input_value("#userEmail")
            
            if nome == "Teste Playwright" and email == "teste@playwright.com":
                print("   ✅ Dados preenchidos corretamente!")
                return True
            else:
                print("   ❌ Erro no preenchimento!")
                return False
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False
        finally:
            browser.close()


def teste_site_playwright():
    """Teste acessando o site oficial do Playwright."""
    print("🧪 Executando teste do site Playwright...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navegar para site do Playwright
            page.goto("https://playwright.dev/")
            
            # Aguardar carregamento
            page.wait_for_load_state("networkidle")
            
            # Verificar título
            titulo = page.title()
            print(f"   📄 Título: {titulo}")
            
            if "Playwright" in titulo:
                print("   ✅ Site do Playwright carregado com sucesso!")
                return True
            else:
                print("   ❌ Erro ao carregar site!")
                return False
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return False
        finally:
            browser.close()


def main():
    """Função principal que executa todos os testes."""
    print("🚀 Iniciando testes Playwright standalone")
    print("=" * 60)
    
    # Lista de testes
    testes = [
        ("Navegação Básica", teste_navegacao_basica),
        ("Formulário DemoQA", teste_formulario_demoqa),
        ("Site Playwright", teste_site_playwright)
    ]
    
    sucessos = 0
    total = len(testes)
    
    # Executar cada teste
    for nome, funcao in testes:
        print(f"\n📋 {nome}")
        print("-" * 40)
        
        if funcao():
            sucessos += 1
        
        print()  # Linha em branco
    
    # Resumo final
    print("=" * 60)
    print("📊 RESUMO DOS TESTES:")
    print(f"✅ Sucessos: {sucessos}/{total}")
    print(f"❌ Falhas: {total - sucessos}/{total}")
    
    if sucessos == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
    else:
        print(f"⚠️  {total - sucessos} teste(s) falharam")
    
    print(f"📈 Taxa de sucesso: {(sucessos/total*100):.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    # Verificar se Playwright está instalado
    try:
        from playwright.sync_api import sync_playwright
        main()
    except ImportError:
        print("❌ Playwright não está instalado!")
        print("💡 Execute: pip install playwright")
        print("💡 E depois: playwright install")
