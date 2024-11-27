TransferLearningProject/
│
├── data/
│   ├── train/                # Imagens de treinamento (2 subpastas para cada classe)
│   ├── val/                  # Imagens de validação (2 subpastas para cada classe)
│   └── test/                 # Imagens de teste
│
├── models/
│   └── base_model.h5         # Modelo treinado salvo
│
├── notebooks/
│   └── transfer_learning.ipynb   # Notebook opcional (para experimentos interativos)
│
├── src/
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── utils.py
│
├── .gitignore
├── README.md
└── requirements.txt
