import qrcode
from io import BytesIO
import unicodedata
import re

class PixProvider:
    def __init__(self, nome_recebedor, cidade, chave_cnpj):
        # Remove acentos e caracteres especiais do nome e cidade
        self.nome_recebedor = self._limpar_texto(nome_recebedor)[:25].upper()
        self.cidade = self._limpar_texto(cidade)[:15].upper()
        # Garante que a chave é apenas números (para CNPJ)
        self.chave_cnpj = "".join(filter(str.isdigit, chave_cnpj))

    def _limpar_texto(self, texto):
        """Remove acentos e mantém apenas letras e números básicos"""
        if not texto: return ""
        nfkd = unicodedata.normalize('NFKD', texto)
        texto_limpo = "".join([c for c in nfkd if not unicodedata.combining(c)])
        return re.sub(r'[^a-zA-Z0-9 ]', '', texto_limpo)

    def _formatar_campo(self, id_campo, valor):
        """Formata no padrão EMV: ID + TAMANHO + VALOR"""
        return f"{id_campo}{len(valor):02d}{valor}"

    def _calcular_crc16(self, payload):
        """Cálculo exato do CRC16-CCITT (XModem) para PIX"""
        payload += "6304" # Indica o início da tag do CRC
        crc = 0xFFFF
        for char in payload:
            crc ^= (ord(char) << 8)
            for _ in range(8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return f"{crc:04X}"

    def gerar_qr_code(self, valor, identificacao):
        # 00: Payload Format Indicator (Fixo '01')
        payload = self._formatar_campo("00", "01")
        
        # 01: Point of Initiation Method (12 para QR Estático Reutilizável)
        payload += self._formatar_campo("01", "12")
        
        # 26: Merchant Account Information
        gui = self._formatar_campo("00", "br.gov.bcb.pix")
        chave = self._formatar_campo("01", self.chave_cnpj)
        payload += self._formatar_campo("26", gui + chave)
        
        # 52: Merchant Category Code (0000)
        payload += self._formatar_campo("52", "0000")
        
        # 53: Transaction Currency (986 para Real Brasileiro)
        payload += self._formatar_campo("53", "986")
        
        # 54: Transaction Amount
        payload += self._formatar_campo("54", f"{valor:.2f}")
        
        # 58: Country Code (BR)
        payload += self._formatar_campo("58", "BR")
        
        # 59: Merchant Name
        payload += self._formatar_campo("59", self.nome_recebedor)
        
        # 60: Merchant City
        payload += self._formatar_campo("60", self.cidade)
        
        # 62: Additional Data Field Template (ID da Transação)
        # O ID não pode ter espaços ou acentos
        id_limpo = self._limpar_texto(identificacao).replace(" ", "")[:25]
        # Se o ID ficar vazio, usa-se '***' (padrão BCB para sem ID)
        if not id_limpo: id_limpo = "***"
        campo_id = self._formatar_campo("05", id_limpo)
        payload += self._formatar_campo("62", campo_id)
        
        # 63: CRC16
        payload_final = payload + "6304"
        payload_final += self._calcular_crc16(payload)
        
        # Criação da imagem do QR Code
        qr = qrcode.QRCode(box_size=10, border=0)
        qr.add_data(payload_final)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
    