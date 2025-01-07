# Estrutura do Projeto

## Diretórios
- **data/**: Contém as imagens e os conjuntos de dados.
- **models/**: Modelos treinados e embeddings.
- **src/**: Código-fonte principal.
- **notebooks/**: Notebooks para prototipação.

## Arquivos
- **requirements.txt**: Lista de dependências.
- **README.md**: Documentação principal.
- **.gitignore**: Arquivos e diretórios ignorados pelo Git.

image-recommender/
├── .gitignore
├── .venv/
├── README.md
├── PROJECT_STRUCTURE.md
├── data/
│   ├── raw/                # Imagens originais
│   ├── processed/          # Imagens pré-processadas
│   ├── train/              # Conjunto de treino
│   ├── test/               # Conjunto de teste
├── notebooks/              # Jupyter Notebooks para prototipação
├── models/
│   ├── model.h5            # Modelo treinado
│   ├── embeddings.pkl      # Embeddings gerados
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # Código para carregar imagens
│   ├── train.py            # Treinamento da rede neural
│   ├── recommend.py        # Sistema de recomendação
│   ├── app.py              # Interface para o usuário (e.g., Flask/Streamlit)
├── requirements.txt        # Dependências do projeto
