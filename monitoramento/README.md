# Painel de Monitoramento de Automações

Este projeto é um sistema para monitorar automações executadas em servidores distribuídos. Ele utiliza um painel interativo desenvolvido com Streamlit para visualizar dados em tempo real.

---

## Funcionalidades

- **Painel Visual**: Monitora execuções de automações em tempo real.
- **Indicadores de Desempenho**: Exibe métricas como tempo médio de execução e total de execuções.
- **Filtros Dinâmicos**: Filtra dados por status ou ID específico.
- **Gráficos Interativos**: Analisa a distribuição do tempo de execução.

---

## Começando

### Pré-requisitos

1. Python 3.8+

2. Instale as dependências com:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` com as variáveis de ambiente necessárias:

   ```plaintext
   DB_HOST=localhost
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_NAME=seu_banco
   ```

### Executando o Projeto

1. Ative seu ambiente virtual:

   ```bash
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
   ```

2. Inicie o painel com o Streamlit:

   ```bash
   streamlit run src/visualization/dashboard.py
   ```

---

## Estrutura do Projeto

```plaintext
monitoramento/
├── README.md            # Introdução rápida ao projeto
├── requirements.txt     # Dependências
├── .env                 # Configurações sensíveis
├── data/                # Dados estáticos
├── docs/                # Documentação detalhada
├── src/                 # Código-fonte
│   ├── database/        # Conexão e consultas ao banco
│   ├── processing/      # Processamento de dados
│   ├── visualization/   # Painel e gráficos
│   └── utils/           # Funções auxiliares
├── tests/               # Testes automatizados
└── setup.py             # Configuração do pacote
```

---

## Contribuição

1. Faça um fork do repositório.

2. Crie uma branch para suas alterações:

   ```bash
   git checkout -b minha-feature
   ```

3. Envie um Pull Request quando estiver pronto.

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
