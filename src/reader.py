import openpyxl

def ler_planilha(arquivo):
    # Carregar a planilha usando openpyxl
    workbook = openpyxl.load_workbook(arquivo)
    
    # Selecionar a primeira aba da planilha
    sheet = workbook.active
    
    # Ler os dados da planilha e armazenar em uma lista de dicionários
    dados = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Ignorar a primeira linha (cabeçalho)
        dados.append({
            'Nome': row[0],
            'Categoria': row[1],
        })
    
    return dados
