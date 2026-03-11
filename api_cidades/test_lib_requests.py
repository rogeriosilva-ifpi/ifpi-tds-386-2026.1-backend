import requests

def main():
  cep = input('Digite seu CEP: ')
  url = f'https://brasilapi.com.br/api/cep/v1/{cep}'

  r = requests.get(url, )

  if r.status_code == 200:
    dados = r.json()
    print(f'Você mora na cidade {dados['city']}')
    print(f'Na rua {dados['street']} do bairro {dados['neighborhood']}')
  else:
    print('Erro ao buscar seu CEP.')


main()