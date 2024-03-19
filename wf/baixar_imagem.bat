@echo off
for /l %%i in (1, 1, 50) do (
    echo Rodando iteracao %%i
    python IA/baixar_imagem.py >> log/log_baixar.txt
    if errorlevel 1 (
        echo Erro ao baixar imagem >> log/log_baixar.txt
    )
)
python IA/separar_letras.py >> log/log_separar.txt
if errorlevel 1 (
    echo Erro ao separar letras >> log/log_separar.txt
)
python IA/mover_letras.py >> log/log_mover.txt
if errorlevel 1 (
    echo Erro ao mover letras >> log/log_mover.txt
)
python IA/treinar_modelo.py >> log/log_treinar.txt
if errorlevel 1 (
    echo Erro ao treinar modelo >> log/log_treinar.txt
)
