from src.reader import ler_planilha
from src.generator import gerar_todos_carnes

xlsx = 'data/input/ATLETAS_AJINC_2026.xlsx'

dados = ler_planilha(xlsx)
gerar_todos_carnes(dados)
