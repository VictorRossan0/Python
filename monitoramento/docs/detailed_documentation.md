# Documentação do Projeto

Este projeto tem como objetivo monitorar automações executadas por scripts Python em servidores distribuídos. Ele fornece um painel visual interativo para acompanhar o status, tempo de execução e outras métricas importantes.

---

## Estrutura do Projeto

```plaintext
monitoramento/
├── README.md            # Documentação principal do projeto
├── requirements.txt     # Dependências do projeto
├── .env                 # Configurações sensíveis (como credenciais)
├── data/                # Dados estáticos ou arquivos de entrada
├── docs/                # Documentação detalhada do projeto
├── src/                 # Código-fonte principal
│   ├── __init__.py      # Arquivo para tornar src um pacote Python
│   ├── database/        # Operações relacionadas ao banco de dados
│   │   ├── __init__.py
│   │   ├── connection.py  # Configurações de conexão
│   │   └── queries.py     # Consultas SQL e funções utilitárias
│   ├── processing/      # Processamento de dados e lógica
│   │   ├── __init__.py
│   │   └── processing.py  # Funções de processamento
│   ├── visualization/   # Código para painéis e gráficos
│   │   ├── __init__.py
│   │   └── dashboard.py  # Configuração do Streamlit
│   └── utils/           # Funções auxiliares
│       ├── __init__.py
│       └── helpers.py    # Funções gerais reutilizáveis
├── tests/               # Testes automatizados
│   ├── __init__.py
│   └── test_example.py
└── setup.py             # Configurações para pacotes Python
```

---

## Dependências

Liste todas as dependências do projeto no arquivo `requirements.txt`:

```plaintext
streamlit==1.15.2
mysql-connector-python==8.0.33
pandas==2.0.3
plotly==5.15.0
python-dotenv==1.0.0
```

Instale-as usando:

```bash
pip install -r requirements.txt
```

---

## Variáveis de Ambiente

Armazene as credenciais do banco de dados e outras configurações sensíveis no arquivo `.env`:

```plaintext
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco
```

---

## Fluxo Principal

### 1. Conexão com o Banco de Dados

O arquivo `src/database/connection.py` gerencia a conexão com o banco de dados usando as configurações do `.env`.

### 2. Consultas SQL

O arquivo `src/database/queries.py` contém funções para buscar dados necessários para o painel.

### 3. Processamento de Dados

O arquivo `src/processing/processing.py` realiza a manipulação e preparação dos dados para visualização.

### 4. Painel Visual

O arquivo `src/visualization/dashboard.py` implementa o painel interativo usando Streamlit e inclui filtros, gráficos e tabelas.

### 5. Funções Auxiliares

Funções utilitárias comuns estão no arquivo `src/utils/helpers.py`, como formatação de tempo e leitura de variáveis de ambiente.

---

## Testes Automatizados

Os testes estão localizados no diretório `tests/` e cobrem:

- Validação de funções auxiliares.
- Testes de consultas ao banco de dados.

Execute os testes com:

```bash
python -m unittest discover -s tests
```

---

## Como Executar o Projeto

1. Configure o ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate   # Windows
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente no arquivo `.env`.

4. Execute o painel Streamlit:

   ```bash
   streamlit run src/visualization/dashboard.py
   ```

---

## Contribuição

1. Crie um fork do repositório.

2. Crie uma branch para suas alterações:

   ```bash
   git checkout -b minha-feature
   ```

3. Faça commit das alterações:

   ```bash
   git commit -m "Descrição da feature"
   ```

4. Envie as alterações:

   ```bash
   git push origin minha-feature
   ```

5. Abra um Pull Request no repositório original.

---

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.

---

## Referências

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [MySQL Connector Python](https://dev.mysql.com/doc/connector-python/en/)
- [Plotly Python](https://plotly.com/python/)
