from src.reader import ler_planilha
from src.generator import gerar_todos_carnes
from datetime import datetime

ano = datetime.now().year

xlsx = f'data/input/ATLETAS_AJINC_{ano}.xlsx'

dados = ler_planilha(xlsx)
gerar_todos_carnes(dados)
