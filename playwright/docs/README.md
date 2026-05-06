# Playwright - Guia de Estudos e Testes

Este projeto demonstra o uso do **Playwright** em Python como uma alternativa moderna ao Selenium para automação de testes web.

## O que é o Playwright?

O Playwright é uma biblioteca de automação de navegadores web desenvolvida pela Microsoft. Ele oferece:

- **Performance superior** ao Selenium
- **Auto-wait** inteligente para elementos
- **Suporte nativo** para Chrome, Firefox, Safari e Edge
- **Testes paralelos** por padrão
- **Interceptação de rede** para mocking
- **Screenshots e vídeos** automáticos
- **Emulação mobile** fácil
- **Testes de API** integrados

## Estrutura do Projeto

```bash
playwright/
├── .gitignore                          # Arquivos ignorados pelo Git
├── pytest.ini                         # Configurações do pytest
├── conftest.py                         # Configurações globais dos testes
├── test_simples.py                     # Testes básicos (híbrido: pytest + Python direto)
├── test_recursos_avancados.py          # Recursos avançados do Playwright
├── test_comprehensive_examples.py     # Exemplos completos com pytest
├── exemplo_direto.py                   # Exemplo standalone (só Python)
├── screenshots/                       # Screenshots dos testes
├── videos/                            # Vídeos dos testes
├── traces/                            # Traces para debugging
├── reports/                           # Relatórios HTML
├── README.md                          # Documentação principal
├── COMANDOS.md                        # Lista de comandos úteis
├── GUIA_EXECUCAO.md                   # Guia detalhado das formas de execução
└── STATUS.md                          # Status atual do projeto
```

## Instalação e Configuração

### 1. Instalar dependências

```bash
pip install playwright pytest pytest-playwright pytest-html pytest-xdist
```

### 2. Instalar browsers

```bash
playwright install
```

## Executando os Testes

### 🚀 NOVIDADE: Execução Direta com Python

Agora você pode executar os testes de **duas formas diferentes**:

#### 1. Execução Direta (Mais Simples)

```bash
# Executar testes básicos diretamente
python test_simples.py

# Executar exemplo standalone
python exemplo_direto.py
```

**Vantagens da execução direta:**

- ✅ Mais simples para iniciantes
- ✅ Não precisa conhecer pytest
- ✅ Controle total sobre o fluxo
- ✅ Relatórios personalizados
- ✅ Browser visível por padrão

#### 2. Execução com Pytest (Profissional)

```bash
# Executar todos os testes
pytest

# Executar testes específicos
pytest test_simples.py -v
pytest test_recursos_avancados.py -v
```

**Vantagens do pytest:**

- ✅ Recursos profissionais
- ✅ Relatórios HTML automáticos
- ✅ Paralelização de testes
- ✅ Integração com CI/CD

### Executar testes específicos com pytest

```bash
# Apenas testes básicos
pytest test_simples.py

# Apenas testes avançados
pytest test_recursos_avancados.py

# Apenas testes com marker específico
pytest -m "not slow"  # Exclui testes lentos
pytest -m "api"       # Apenas testes de API
```

### Executar em modo visual (com browser visível)

```bash
pytest --headed
```

### Executar em paralelo

```bash
pytest -n 4  # Usa 4 processos paralelos
```

### Executar com diferentes browsers

```bash
pytest --browser=chromium
pytest --browser=firefox
pytest --browser=webkit
```

### Gerar relatório HTML

```bash
pytest --html=reports/report.html --self-contained-html
```

## Exemplos de Testes Implementados

### 1. Testes Básicos (`test_simples.py`) - ⭐ HÍBRIDO

- ✅ **Execução dupla**: funciona com `python test_simples.py` OU `pytest test_simples.py`
- ✅ Navegação básica
- ✅ Interação com formulários
- ✅ Captura de screenshots
- ✅ Aguardar elementos dinamicamente
- ✅ Elementos dinâmicos

### 2. Exemplo Standalone (`exemplo_direto.py`) - ⭐ NOVO

- ✅ **Totalmente independente**: só precisa de `python exemplo_direto.py`
- ✅ Código didático e comentado
- ✅ Ideal para aprender Playwright
- ✅ Relatórios personalizados
- ✅ Browser visível por padrão

### 3. Testes Avançados (`test_recursos_avancados.py`)

- ✅ Múltiplos browsers (Chromium, Firefox, WebKit)
- ✅ Emulação mobile
- ✅ Interceptação de rede
- ✅ Métricas de performance
- ✅ Simulação de localização
- ✅ Testes parametrizados

### 4. Testes Completos (`test_comprehensive_examples.py`)

- ✅ Testes de performance
- ✅ Métricas Web Vitals
- ✅ Testes de API
- ✅ Testes de acessibilidade
- ✅ Tratamento de erros
- ✅ Testes orientados a dados
- ✅ Regressão visual

## Conceitos Importantes

### Auto-wait do Playwright

```python
# ❌ Selenium - precisa de waits explícitos
from selenium.webdriver.support.ui import WebDriverWait
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "button"))
)

# ✅ Playwright - auto-wait automático
page.click("#button")  # Aguarda automaticamente o elemento ficar clicável
```

### Localizadores Modernos

```python
# Múltiplas formas de localizar elementos
page.locator("#id")                    # Por ID
page.locator(".class")                 # Por classe
page.locator("text=Texto")             # Por texto
page.locator("input[type='email']")    # Por seletor CSS
page.get_by_role("button")             # Por role de acessibilidade
page.get_by_text("Clique aqui")        # Por texto visível
```

### Interceptação de Rede

```python
# Interceptar e modificar requisições
def handle_route(route):
    if "/api/users" in route.request.url:
        route.fulfill(json={"users": ["mock_user"]})
    else:
        route.continue_()

page.route("**/*", handle_route)
```

### Contextos e Páginas

```python
# Um contexto pode ter múltiplas páginas
with browser.new_context() as context:
    page1 = context.new_page()
    page2 = context.new_page()
    # Cada página é independente mas compartilha cookies/storage
```

## Playwright vs Selenium

| Recurso | Playwright | Selenium |
|---------|------------|----------|
| **Performance** | ⚡ Muito rápido | 🐢 Mais lento |
| **Auto-wait** | ✅ Automático | ❌ Manual |
| **Setup** | ✅ Simples | ⚠️ Complexo |
| **Multi-browser** | ✅ Nativo | ⚠️ Drivers separados |
| **API Testing** | ✅ Integrado | ❌ Não nativo |
| **Screenshots** | ✅ Automático | ⚠️ Manual |
| **Paralelização** | ✅ Por padrão | ⚠️ Configuração extra |
| **Debugging** | ✅ Traces/Inspector | ⚠️ Limitado |

## Debugging e Troubleshooting

### 1. Executar com debug

```bash
pytest --headed --slowmo=1000  # Modo lento para visualizar
```

### 2. Usar Playwright Inspector

```python
page.pause()  # Para a execução e abre o inspector
```

### 3. Verificar traces

Os traces são salvos automaticamente quando testes falham em `traces/`

### 4. Screenshots e vídeos

Capturados automaticamente em falhas, salvos em `screenshots/` e `videos/`

## Comandos Úteis

### Execução Direta (Python)

```bash
# Executar testes básicos
python test_simples.py

# Executar exemplo standalone
python exemplo_direto.py

# Ver arquivos de exemplo
ls screenshots/  # Screenshots capturados
```

### Execução com Pytest

```bash
# Executar apenas testes que falharam
pytest --lf

# Executar com mais detalhes
pytest -v -s

# Executar com coverage
pytest --cov=.

# Parar no primeiro erro
pytest -x

# Executar testes específicos por palavra-chave
pytest -k "formulario"

# Executar com relatório HTML
pytest --html=reports/report.html --self-contained-html
```

## Boas Práticas

1. **Use Page Object Model** para testes complexos
2. **Aguarde elementos** ao invés de usar sleep()
3. **Capture evidências** (screenshots, vídeos) para debugging
4. **Use fixtures** para setup/teardown
5. **Organize testes** com markers e classes
6. **Execute em paralelo** para economizar tempo
7. **Use dados de teste** parametrizados
8. **Monitore performance** com métricas

## Próximos Passos

### Para Iniciantes 🚀

1. **Comece simples**: Execute `python exemplo_direto.py`
2. **Veja o browser**: Observe os testes executando
3. **Estude o código**: Analise `exemplo_direto.py` linha por linha
4. **Execute híbrido**: Teste `python test_simples.py`
5. **Modifique exemplos**: Adapte para seus casos de uso

### Para Usuários Avançados 🔧

1. **Use pytest**: Execute `pytest -v` para todos os testes
2. **Explore browsers**: Teste com `--browser=firefox`
3. **Configure CI/CD**: Implemente pipeline automatizado
4. **Page Object Model**: Organize testes complexos
5. **Testes de API**: Explore recursos avançados
6. **Performance**: Monitore métricas Web Vitals
7. **Acessibilidade**: Adicione testes inclusivos

### Escolhendo a Abordagem 🎯

**Use execução direta (`python arquivo.py`) quando:**

- 🎯 Está aprendendo Playwright
- 🎯 Quer algo simples e rápido
- 🎯 Precisa ver o browser executando
- 🎯 Não quer complexidade do pytest
- 🎯 Está prototipando testes

**Use pytest quando:**

- 🎯 Projeto profissional/produção
- 🎯 Precisa de relatórios avançados
- 🎯 Quer executar muitos testes
- 🎯 Integração com CI/CD
- 🎯 Testes paralelos e otimizados

---

**Recursos Adicionais:**

- [Documentação Oficial](https://playwright.dev/python/)
- [Playwright Inspector](https://playwright.dev/python/docs/debug)
- [Best Practices](https://playwright.dev/python/docs/best-practices)
