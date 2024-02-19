from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.utils import get_column_letter
from Models.bundesliga import bundesliga
from Models.eredivisie import eredivisie
from Models.la_liga import la_liga
from Models.ligue1 import ligue1
from Models.premier_league import premier_league
from Models.premier_russia import premier_russia
from Models.primeira_liga import primeira_liga
from Models.serieA import serieA
from Models.super_lig import super_lig
from Models.tipico_bundesliga import tipico_bundesliga


def criar_novo_excel():
    wb_novo = Workbook()
    wb_novo.remove(wb_novo.active)  # Remove a folha em branco padrão

    # Chama as funções para extrair informações
    bundesliga()
    eredivisie()
    la_liga()
    ligue1()
    premier_league()
    premier_russia()
    primeira_liga()
    serieA()
    super_lig()
    tipico_bundesliga()
    
    # Abre os arquivos Excel existentes
    wb_bundesliga = load_workbook('Excel/dados_bundesliga.xlsx')
    wb_eredivisie = load_workbook('Excel/dados_eredivisie.xlsx')
    wb_laliga = load_workbook('Excel/dados_laliga.xlsx')
    wb_ligue1 = load_workbook('Excel/dados_ligue1.xlsx')
    wb_premier = load_workbook('Excel/dados_premier.xlsx')
    wb_russia = load_workbook('Excel/dados_premier_russia.xlsx')
    wb_primeira_liga = load_workbook('Excel/dados_primeira_liga.xlsx')
    wb_serieA = load_workbook('Excel/dados_serieA.xlsx')
    wb_super_lig = load_workbook('Excel/dados_super_lig.xlsx')
    wb_tipico = load_workbook('Excel/dados_tipico_bundesliga.xlsx')

    # Copia as abas para o novo arquivo Excel
    for sheet in wb_bundesliga.sheetnames:
        ws = wb_bundesliga[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_eredivisie.sheetnames:
        ws = wb_eredivisie[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_laliga.sheetnames:
        ws = wb_laliga[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)

    for sheet in wb_ligue1.sheetnames:
        ws = wb_ligue1[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_premier.sheetnames:
        ws = wb_premier[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_russia.sheetnames:
        ws = wb_russia[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_primeira_liga.sheetnames:
        ws = wb_primeira_liga[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_serieA.sheetnames:
        ws = wb_serieA[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_super_lig.sheetnames:
        ws = wb_super_lig[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)
    
    for sheet in wb_tipico.sheetnames:
        ws = wb_tipico[sheet]
        ws_novo = wb_novo.create_sheet(title=sheet)
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            values = [cell.value for cell in row]
            ws_novo.append(values)

    # Ajuste automático da largura da coluna
    for sheet in wb_novo.sheetnames:
        ws = wb_novo[sheet]
        for col in ws.columns:
            max_length = 0
            column = col[0].column  # Get the column name
            for cell in col:
                try:  # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            
            # Converta o número da coluna em uma string
            column_letter = get_column_letter(column)
            
            ws.column_dimensions[column_letter].width = adjusted_width

    # Salva o novo arquivo Excel
    wb_novo.save('Excel/planilha_TOP10_ligas.xlsx')

if __name__ == "__main__":
    criar_novo_excel()
    print(f"\nTodas as informações salvas em planilha_TOP10_ligas.xlsx")