# 🎭 Playwright Python - Automação Web Moderna

Uma implementação completa do **Playwright** em Python como alternativa moderna ao Selenium.

## 🚀 Início Rápido

### Instalação

```bash
pip install playwright pytest pytest-playwright pytest-html pytest-xdist
playwright install
```

### Execução Simples (Recomendado para Iniciantes)

```bash
# Exemplo didático standalone
python exemplo_direto.py

# Testes básicos híbridos
python test_simples.py
```

### Execução Profissional (Pytest)

```bash
# Todos os testes
pytest -v

# Com relatório HTML
pytest --html=reports/report.html --self-contained-html
```

## 📁 Estrutura do Projeto

``` python
playwright/
├── 📄 exemplo_direto.py              # ⭐ Exemplo standalone (python direto)
├── 📄 test_simples.py                # ⭐ Testes híbridos (python + pytest)
├── 📄 test_recursos_avancados.py     # Recursos avançados do Playwright
├── 📄 test_comprehensive_examples.py # Exemplos completos
├── 📄 conftest.py                    # Configurações pytest
├── 📄 pytest.ini                     # Configurações do projeto
├── 📄 requirements.txt               # Dependências
├── 📄 .gitignore                     # Arquivos ignorados
├── 📂 docs/                          # 📚 Documentação completa
│   ├── README.md                     # Guia principal detalhado
│   ├── GUIA_EXECUCAO.md             # Guia de execução
│   ├── COMANDOS.md                  # Lista de comandos
│   ├── STATUS.md                    # Status do projeto
│   └── CORRECOES_FINAIS.md          # Histórico de correções
├── 📂 screenshots/                   # Screenshots capturados
├── 📂 videos/                       # Vídeos dos testes
├── 📂 traces/                       # Traces para debugging
└── 📂 reports/                      # Relatórios HTML
```

## 🎯 Escolha Sua Abordagem

### 🟢 Para Iniciantes - Execução Direta

- **Mais simples**: `python exemplo_direto.py`
- **Browser visível**: Veja a automação acontecendo
- **Sem complexidade**: Não precisa conhecer pytest

### 🔵 Para Desenvolvedores - Execução Híbrida

- **Flexível**: `python test_simples.py` OU `pytest test_simples.py`
- **Melhor dos dois mundos**: Simplicidade + recursos profissionais

### 🟡 Para Projetos - Execução Profissional

- **Recursos avançados**: `pytest -v --html=reports/report.html`
- **CI/CD**: Integração com pipelines
- **Paralelização**: Execução simultânea

## 📊 Status dos Testes

✅ **15/15 testes passando** (100% de sucesso)  
✅ **Cross-browser**: Chromium, Firefox, WebKit  
✅ **Documentação completa**: Guias detalhados  
✅ **Múltiplas formas de execução**: Máxima flexibilidade  

## 📚 Documentação

Para documentação completa, consulte:

- **[📖 Guia Principal](docs/README.md)** - Documentação detalhada
- **[🚀 Guia de Execução](docs/GUIA_EXECUCAO.md)** - Formas de executar
- **[💻 Lista de Comandos](docs/COMANDOS.md)** - Comandos úteis
- **[📊 Status do Projeto](docs/STATUS.md)** - Estado atual

## 🆚 Playwright vs Selenium

| Recurso | Playwright | Selenium |
|---------|------------|----------|
| **Performance** | ⚡ Muito rápido | 🐢 Mais lento |
| **Auto-wait** | ✅ Automático | ❌ Manual |
| **Setup** | ✅ Simples | ⚠️ Complexo |
| **Multi-browser** | ✅ Nativo | ⚠️ Drivers separados |

## 🎉 Começe Agora

1. **Clone o projeto**
2. **Execute**: `python exemplo_direto.py`
3. **Veja a mágica** acontecer! ✨

---

**Recursos:**
[Documentação Oficial](https://playwright.dev/python/)
[GitHub Playwright](https://github.com/microsoft/playwright)
[Documentação Completa](docs/README.md)
