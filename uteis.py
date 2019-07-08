from bs4 import BeautifulSoup
import requests

# Faz o request na url recebida e retorna o texto formatado
def retorna_html_parse(base_url):
    soup = ''
    try:
        resposta = requests.get(base_url)
        soup = BeautifulSoup(resposta.text, 'html.parser')
    except Exception as e:
        print('Error: ' + str(e))

    return soup

def formata_data(data):
    meses = ['jan', 'fev', 'mar', 'abr', 'maio', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data_split = data.split(' ')
    num_mes = meses.index(data_split[1].replace(',', '')) + 1
    mes_data = str(num_mes).zfill(2)

    formatacao = data_split[0] + '/' + mes_data + '/' + data_split[2]

    return formatacao