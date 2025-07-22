# Scripts úteis para executar testes Playwright

## 🚀 EXECUÇÃO DIRETA (NOVO!) - Mais Simples

### Comandos Básicos - Python Direto

```bash
# Executar testes básicos diretamente (HÍBRIDO)
python test_simples.py

# Executar exemplo standalone didático (NOVO)
python exemplo_direto.py
```

### Vantagens da Execução Direta

- ✅ **Simples**: Não precisa conhecer pytest
- ✅ **Visual**: Browser visível por padrão
- ✅ **Didático**: Código mais fácil de entender
- ✅ **Controle**: Fluxo personalizado
- ✅ **Iniciantes**: Ideal para aprender

## 🔧 EXECUÇÃO COM PYTEST - Modo Profissional

### Comandos básicos (Execute no terminal do VS Code)

### 1. Executar todos os testes simples

```bash
pytest test_simples.py -v
# OU usando caminho completo:
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py -v
```

### 2. Executar teste específico

```bash
pytest test_simples.py::test_navegacao_simples -v
# OU usando caminho completo:
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py::test_navegacao_simples -v
```

### 3. Executar com browser visível (modo debug)

```bash
pytest test_simples.py --headed
# OU usando caminho completo:
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --headed
```

### 4. Executar em modo lento (para visualizar melhor)

```bash
pytest test_simples.py --headed --slowmo=1000
# OU usando caminho completo:
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --headed --slowmo=1000
```

### 5. Executar com diferentes browsers

```bash
# Chrome/Chromium
pytest test_simples.py --browser chromium
# OU: C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --browser chromium

# Firefox
pytest test_simples.py --browser firefox
# OU: C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --browser firefox

# Safari (WebKit)
pytest test_simples.py --browser webkit
# OU: C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --browser webkit
```

## 📋 COMPARAÇÃO DE ABORDAGENS

### Quando usar EXECUÇÃO DIRETA (python arquivo.py)

- 🎯 **Aprendendo Playwright**: Código mais didático
- 🎯 **Prototipagem rápida**: Teste ideias rapidamente
- 🎯 **Debugging visual**: Ver browser executando
- 🎯 **Simplicidade**: Não quer complexidade pytest
- 🎯 **Demonstrações**: Mostrar Playwright funcionando

**Exemplos:**

```bash
python test_simples.py        # Híbrido: 5 testes básicos
python exemplo_direto.py      # Standalone: 3 exemplos didáticos
```

### Quando usar PYTEST

- 🎯 **Projeto profissional**: Recursos avançados
- 🎯 **Muitos testes**: Organização e relatórios
- 🎯 **CI/CD**: Integração com pipelines
- 🎯 **Paralelização**: Execução simultânea
- 🎯 **Relatórios HTML**: Documentação automática

**Exemplos:**

```bash
pytest test_simples.py -v                    # Testes básicos
pytest test_recursos_avancados.py -v         # Recursos avançados
pytest --html=reports/report.html           # Com relatório HTML
```

### 6. Executar testes mais complexos

```bash
# Testes avançados (alguns podem falhar por dependerem de sites externos)
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_advanced_examples.py -v

# Testes completos
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_comprehensive_examples.py -v
```

### 7. Gerar relatório HTML

```bash
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --html=reports/report.html --self-contained-html
```

### 8. Executar em paralelo (mais rápido)

```bash
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py -n 2
```

### 9. Capturar screenshots em falhas

```bash
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --screenshot=only-on-failure
```

### 10. Executar com vídeo

```bash
C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py --video=retain-on-failure
```

## Scripts para copiar e colar no terminal

### Script 1: Teste básico completo

```bash
cd "c:\Users\Hitss\Documents\Ferramentas\python\playwright" && C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py -v --html=reports/report.html --self-contained-html
```

### Script 2: Teste visual (browser visível)

```bash
cd "c:\Users\Hitss\Documents\Ferramentas\python\playwright" && C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py::test_navegacao_simples --headed --slowmo=1000
```

### Script 3: Teste cross-browser

```bash
cd "c:\Users\Hitss\Documents\Ferramentas\python\playwright" && C:/Users/Hitss/Documents/Ferramentas/python/playwright/.venv/Scripts/python.exe -m pytest test_simples.py::test_navegacao_simples --browser chromium --browser firefox
```

## Dicas importantes

1. **Sempre execute no diretório do projeto**
2. **Use --headed para ver o browser em ação**
3. **Use --slowmo para executar mais devagar**
4. **Screenshots são salvos automaticamente em falhas**
5. **Relatórios HTML são gerados em reports/**
6. **Videos são salvos em videos/** quando habilitados
