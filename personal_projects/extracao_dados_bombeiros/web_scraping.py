import requests
from bs4 import BeautifulSoup
import csv

def extraction(url, table_name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

    page_request = requests.get(url, headers=headers)

    soup_bs4 = BeautifulSoup(page_request.text, 'html.parser')

    # Encontrar o texto 'CLCB Vigente' e limpar
    situacao_texto = soup_bs4.find('label', id='lblSituacao').text.strip()
    situacao_limpa = ' '.join(situacao_texto.split())  # Remove espaços extras

    if situacao_limpa.startswith("Situação:"):
        situacao_limpa = situacao_limpa[len("Situação:"):].strip()

    info_table = soup_bs4.find_all('script')[8].text

    # Removendo alguns dados que são lixos
    remove_trash = info_table.replace('//<![CDATA[', '').replace('//]]>', '').replace('inicializarMapa', '').replace('criarMarcador', '')

    # Limpar e dividir os dados em registros individuais
    records = remove_trash.strip().split(";")

    # Remover aspas desnecessárias de cada registro e converter cada registro em uma lista de campos
    records = [record.replace("'", "").replace('(', '').replace(')', '').strip().split(", ") for record in records if record]

    columns = [
        'Endereco', 'Numero', 'Bairro', 'Cidade', 'Registro',
        'Data', 'Categoria', 'Situacao'
    ]

    dict_records = []
    for record in records:
        dict_record = {
            'Endereco': record[0],
            'Numero': record[1],
            'Bairro': record[2],
            'Cidade': record[3],
            'Registro': record[4] if len(record) > 4 else '',
            'Data': record[5] if len(record) > 4 else '',
            'Categoria': record[9] if len(record) > 4 else '',
            'Situacao': situacao_limpa  # Adicionando o campo 'Situacao' limpo
        }
        dict_records.append(dict_record)

    # Salvando os dados em um arquivo CSV
    output_file = f'{table_name}.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=columns, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writeheader()
        csvwriter.writerows(dict_records)

    return output_file
