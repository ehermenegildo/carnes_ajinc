import os
from datetime import date
from fpdf import FPDF
from num2words import num2words
from src.pix import PixProvider

# 1. Configuração de valores por categoria (Ajuste conforme necessário)
VALORES_CATEGORIA = {
    'Senior': 220.00,
    'Junior_2': 220.00,
    'Junior_1': 220.00,
    'Juvenil_2': 220.00,
    'Juvenil_1': 220.00,
    'Infantil_2': 220.00,
    'Infantil_1': 220.00,
    'Petiz_2': 175.00,
    'Petiz_1': 175.00,
    'Mirim_2': 130.00,
    'Mirim_1': 100.00,
}


class CarneAJINC(FPDF):
    """Classe para gerar carnês de pagamento da AJINC usando FPDF e integração com PixProvider."""
    def __init__(self):
        """Inicializa o PDF e o provedor de Pix com os dados da AJINC."""
        super().__init__()
        # Inicializa o provedor de Pix com os dados da AJINC
        self.pix_provider = PixProvider(
            nome_recebedor="AJINC",
            cidade="JARAGUA DO SUL",
            chave="7f33b1a2-039d-4f81-b001-29d22f83dd82"
        )

    def desenhar_carne(self, x, y, atleta, parcela, total_parc, data_venc, valor):
        """Desenha um carnê completo para um atleta, incluindo canhoto, corpo e QR code Pix.
            Args:
            x (float): Coordenada X inicial do carnê.
            y (float): Coordenada Y inicial do carnê.
            atleta (dict): Dicionário com informações do atleta (Nome, Categoria).
            parcela (int): Número da parcela atual.
            total_parc (int): Total de parcelas.
            data_venc (str): Data de vencimento no formato "DD/MM/AAAA".
            valor (float): Valor da parcela.
        """
        # --- Configurações de Estilo ---
        self.set_line_width(0.2)
        larg_canhoto = 55
        larg_corpo = 135
        alt = 65
        margem_logo = 2

        # --- 1. CANHOTO (Esquerda) ---
        self.rect(x, y, larg_canhoto, alt)

        # Logo no canhoto
        path_logo = "assets/logo.png"
        if os.path.exists(path_logo):
            self.image(path_logo, x + 2, y + 2, 10)

        self.set_font("helvetica", "B", 8)
        self.text(x + 14, y + 8, "AJINC - CANHOTO")

        self.set_font("helvetica", "", 7)
        self.text(x + 2, y + 18, f"ATLETA: {atleta['Nome'][:25]}")
        self.text(x + 2, y + 23, f"PARCELA: {parcela}/{total_parc}")
        self.text(x + 2, y + 28, f"VENCIMENTO: {data_venc}")
        self.text(x + 2, y + 33, f"CATEGORIA: {atleta['Categoria'].replace('_', ' ')}")       

        self.set_font("helvetica", "B", 9)
        self.text(x + 2, y + 40, f"VALOR: R$ {valor:,.2f}".replace(
            ',', 'X').replace('.', ',').replace('X', '.'))

        self.set_font("helvetica", "I", 6)
        self.text(x + 2, y + 58, "___________________________")
        self.text(x + 8, y + 61, "Assinatura Recebedor")

        # --- Opções de Pagamento no Canhoto ---
        self.set_font("helvetica", "", 7)
        box_size = 4
        bx = x + 2
        by = y + 46
        self.rect(bx, by, box_size, box_size)
        self.text(bx + box_size + 2, by + box_size - 1, "Dinheiro")
        self.rect(bx + 20, by, box_size, box_size)
        self.text(bx + 20 + box_size + 2, by + box_size - 1, "PIX")

        # --- 2. CORPO (Direita) ---
        xc = x + larg_canhoto + 2
        self.rect(xc, y, larg_corpo, alt)

        # Cabeçalho Corpo com Logo
        if os.path.exists(path_logo):
            self.image(path_logo, xc + 2, y + 2, 15)

        self.set_font("helvetica", "B", 9)
        self.text(xc + 20, y + 7,
                  "ASSOCIAÇÃO JARAGUAENSE DOS INCENT. DA NATAÇÃO COMPETITIVA")
        self.set_font("helvetica", "", 7)
        self.text(xc + 20, y + 12,
                  "R Gustavo Hagedorn, 636, Bairro Nova Brasília, Jaraguá do Sul - SC, CEP 89.265-252")
        self.text(xc + 20, y + 16,
                  "CNPJ: 03.191.568/0001-25 | Fone: (47) 0000-0000")

        # Dados do Atleta
        self.line(xc, y + 18, xc + larg_corpo, y + 18)
        self.set_font("helvetica", "", 8)
        self.text(xc + 2, y + 23, "NOME DO ATLETA")
        self.set_font("helvetica", "B", 10)
        self.text(xc + 2, y + 28, atleta['Nome'].upper())

        # Valor Nominal e Extenso
        valor_extenso = num2words(valor, lang='pt_BR', to='currency').upper()
        self.set_font("helvetica", "", 9)
        self.text(xc + 2, y + 36, f"VALOR NOMINAL: R$ {valor:,.2f}".replace(
            ',', 'X').replace('.', ',').replace('X', '.'))
        self.set_font("helvetica", "I", 8)
        self.set_text_color(50, 50, 50)  # Cinza escuro para o extenso
        self.text(xc + 2, y + 40, f"({valor_extenso})")
        self.set_text_color(0, 0, 0)  # Volta para preto

        # Vencimento e Parcela
        self.set_font("helvetica", "B", 9)
        self.text(xc + 2, y + 50, f"VENCIMENTO: {data_venc}")
        self.text(xc + 60, y + 50, f"PARCELA: {parcela}/{total_parc}")

        # --- Opções de Pagamento no Corpo ---
        self.set_font("helvetica", "", 7)
        box_size = 4
        bx2 = xc + 2
        by2 = y + 56
        self.rect(bx2, by2, box_size, box_size)
        self.text(bx2 + box_size + 2, by2 + box_size - 1, "Dinheiro")
        self.rect(bx2 + 20, by2, box_size, box_size)
        self.text(bx2 + 20 + box_size + 2, by2 + box_size - 1, "PIX")

        # --- 3. QR CODE PIX (Via Módulo pix.py) ---
        # Identificação amigável para o extrato do banco
        id_pix = f"MENS {atleta['Nome'].split()[0]} P{parcela}"
        img_buffer = self.pix_provider.gerar_qr_code(valor, id_pix)

        self.image(img_buffer, xc + 105, y + 33, 27, 27)
        self.set_font("helvetica", "B", 6)
        self.text(xc + 109, y + 62, "PAGUE COM PIX")


def gerar_todos_carnes(lista_atletas):
    """Função principal para gerar o PDF com os carnês de pagamento para todos os atletas da lista.
        Args:
            lista_atletas (list): Lista de dicionários com informações dos atletas.
        Returns:
            None
        """
    pdf = CarneAJINC()

    # Gera 12 datas de 10/03/<ano> até 10/02/<ano+1> automaticamente
    start_month = 3  # março
    base_year = date.today().year
    datas = []
    for i in range(12):
        m = start_month + i
        year = base_year + (m - 1) // 12
        month = ((m - 1) % 12) + 1
        datas.append(f"10/{month:02d}/{year}")

    for atleta in lista_atletas:
        valor = VALORES_CATEGORIA.get(atleta['Categoria'], 100.00)
        pdf.add_page()
        y_pos = 15

        for i, dt in enumerate(datas):
            pdf.desenhar_carne(5, y_pos, atleta, i+1, len(datas), dt, valor)
            y_pos += 70

            # Se já desenhou 4 carnês e ainda faltam parcelas, cria nova página
            if (i + 1) % 4 == 0 and i < len(datas) - 1:
                pdf.add_page()
                y_pos = 15

    # Garante que a pasta de output existe
    if not os.path.exists("data/output"):
        os.makedirs("data/output")

    pdf.output(f"data/output/carnes_ajinc_{base_year}.pdf")
    print(f"Sucesso! O arquivo 'carnes_ajinc_{base_year}.pdf' foi gerado na pasta data/output.")

