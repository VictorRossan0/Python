# Projeto de Transfer Learning em Python

Este projeto aplica **Transfer Learning** utilizando Python e TensorFlow para classificar imagens em duas classes personalizadas. 
O modelo pré-treinado VGG16 foi utilizado, e os dados foram processados e treinados em um ambiente local (VS Code).

## **Estrutura do Projeto:**

├── data/ # Dados organizados em pastas de treino, validação e teste 

├── models/ # Modelo treinado salvo em .h5 

├── src/ # Scripts Python para treinamento e avaliação 

├── notebooks/ # Jupyter Notebook opcional para testes 

├── project_structure.md # Estrutura do Projeto

├── README.md # Documentação do Projeto

└── requirements.txt # Lista de itens/pacotes para serem instalados

# Dependências necessárias

## **Dependências:**

Instale os pacotes necessários:

```bash
pip install -r requirements.txt
```

## **Como Executar:**

Organize suas imagens no diretório data/ em duas subpastas representando as classes.

Execute o treinamento:

```bash
python src/train_model.py
```

O modelo treinado estará disponível em models/base_model.h5.

# Resultados:

Acurácia alcançada: XX% (substituir após treinamento)

Gráficos de desempenho e exemplos de predição podem ser encontrados no notebook.

# Considerações Finais:

Este projeto demonstra como aproveitar o poder do Transfer Learning para treinar um modelo eficaz em um dataset personalizado. 
Adaptável para diferentes conjuntos de dados e aplicações reais.