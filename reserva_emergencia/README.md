# Projeto: Gerenciador de Dividendos

## **Descrição**
Este projeto é um gerenciador de dividendos focado em investidores que desejam acompanhar seus rendimentos, calcular rentabilidades e diversificar investimentos. Ele permite cadastrar ativos, calcular diferentes métricas financeiras e gerar relatórios em Excel com gráficos interativos.

---

## **Funcionalidades**

1. **Cadastro de Ativos**:
   - Cadastro de ações e FIIs com valores de cotas, dividendos, datas de pagamento e valor total investido.
   
2. **Cálculos Financeiros**:
   - Quantidade necessária de cotas para atingir um valor investido.
   - Diversificação de investimentos entre vários ativos.
   - Rentabilidade de cada ativo com base nos dividendos recebidos.

3. **Relatórios e Gráficos**:
   - Geração de relatório consolidado em Excel.
   - Gráficos detalhados de dividendos recebidos por quantidade de cotas.

4. **Log de Operações**:
   - Registro automático de ações realizadas pelo usuário.

---

## **Como Executar o Projeto**

### **1. Pré-requisitos**

- Python 3.8 ou superior.
- Biblioteca `pandas`, `matplotlib`, e `openpyxl`.

Instale as dependências com o seguinte comando:
```bash
pip install -r requirements.txt
```

### **2. Estrutura do Projeto**

```plaintext
.
├── main.py                 # Arquivo principal que executa o programa.
├── cadastro.py             # Funções relacionadas ao cadastro de ativos.
├── calculos.py             # Funções para cálculos (quantidades, diversificação, rentabilidade).
├── visualizacao.py         # Funções para geração de gráficos.
├── relatorios.py           # Funções para salvar relatórios (Excel e logs).
├── utils.py                # Funções auxiliares (validação de entrada, logs, etc.).
├── README.md               # Documentação do projeto.
├── requirements.txt        # Dependências do projeto.
├── dividendos_atualizado.xlsx  # Arquivo Excel gerado pelo programa (após execução).
└── log_operacoes.txt       # Registro de operações realizadas pelo programa.
```

### **3. Executando o Programa**

Inicie o programa executando o arquivo `main.py`:
```bash
python main.py
```

---

## **Funcionalidades em Detalhes**

### **1. Cadastro de Ativos**
- Informe o código do ativo, valor da ação, dividendos por cota e a data de pagamento.
- Os dados cadastrados serão salvos para cálculos e relatórios futuros.

### **2. Cálculos Financeiros**
#### 2.1 Quantidade Necessária para Investimento
- Informe o valor que deseja investir e o programa calculará quantas cotas adicionais são necessárias.

#### 2.2 Diversificação de Investimentos
- Informe o valor total a ser investido e o número de ativos desejados. O programa sugere como distribuir o valor entre eles.

#### 2.3 Rentabilidade por Ativo
- Calcule a rentabilidade com base no total investido e os dividendos recebidos para cada ativo.

### **3. Relatórios e Gráficos**
- Gera um arquivo Excel consolidado com os dados cadastrados e gráficos para análise visual.

---

## **Exemplo de Uso**

### **Fluxo do Programa**
1. **Menu Inicial:**
   O usuário pode escolher entre as seguintes opções:
   - Cadastrar Ativos.
   - Calcular Quantidade por Investimento.
   - Calcular Diversificação.
   - Gerar Relatórios.
   - Sair.

2. **Cadastro de Dados:**
   O usuário insere informações como o valor da cota, dividendos e data do pagamento.

3. **Relatórios:**
   O programa gera um arquivo Excel e exibe gráficos para análise detalhada.

---

## **Requisitos Técnicos**

- **Linguagem:** Python 3.8+
- **Bibliotecas Utilizadas:**
  - `pandas`: Manipulação de dados.
  - `matplotlib`: Geração de gráficos.
  - `openpyxl`: Manipulação de arquivos Excel.

Instale as dependências com:
```bash
pip install -r requirements.txt
```

---

## **Licença**
Este projeto é de uso livre e pode ser modificado conforme a necessidade.