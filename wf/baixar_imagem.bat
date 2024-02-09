@echo off
for /l %%i in (1, 1, 50) do (
    echo Rodando iteracao %%i
    python IA/baixar_imagem.py >> log/log_baixar.txt
)
python IA/separar_letras.py >> log/log_separar.txt
python IA/mover_letras.py >> log/log_mover.txt
python IA/treinar_modelo.py >> log/log_treinar.txt