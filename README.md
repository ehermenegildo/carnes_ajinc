Este projeto é uma ferramenta de automação desenvolvida em Python para a **AJINC (Associação Jaraguaense de Natação)**. O sistema processa uma lista de atletas em Excel e gera carnês de mensalidade em PDF, com QR Codes Pix dinâmicos e valores por categoria.

## 🚀 Funcionalidades

- **Leitura Inteligente:** Processa arquivos `.xlsx` capturando nome e categoria dos atletas.
- **Valores por Categoria:** Aplica automaticamente o valor da mensalidade baseado na categoria do atleta (Sênior, Júnior, Petiz, etc).
- **Pix Dinâmico (BR Code):** Gera um QR Code Pix para cada parcela, já com o valor correto, chave CNPJ da Instituição e identificação do atleta.
- **Cálculo de Datas:** Gera automaticamente 12 parcelas (de Março/2026 a Fevereiro/2027).
- **PDF Profissional:** Layout com canhoto e corpo do carnê, incluindo logo e valor por extenso.
- **Modularização:** Lógica de Pix separada para fácil manutenção.

## 📁 Estrutura do Projeto

```text
├── assets/             # Logo e recursos visuais
├── data/
│   ├── input/          # Local para colocar a planilha Excel
│   └── output/         # Local onde os PDFs serão gerados
├── src/
│   ├── reader.py       # Extrator de dados do Excel
│   ├── pix.py          # Gerador de QR Code Pix (Padrão BCB)
│   └── generator.py    # Motor de criação do PDF
├── main.py             # Arquivo principal de execução
├── requirements.txt    # Dependências do projeto
└── .gitignore          # Proteção para não subir dados sensíveis
