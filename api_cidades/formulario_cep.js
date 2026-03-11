async function main(){
  console.log('Inicializou...')

  carregar_cidade()

  botao = document.getElementById('btnConsultar')

  botao.onclick = async (event) => { await btnConsultarClick(event)}
}


async function carregar_cidade(){
  url = 'https://api-cidades-dapaz.onrender.com/cidades'

  const response = await fetch(url)

  if (response.ok){
    cidades = await response.json()

    for (cidade of cidades){
      console.log(cidade)
    }
  }
}

async function btnConsultarClick(event){
  // evita o reload
  event.preventDefault()

  // Pegando os Elemento HTML
  const cx_texto = document.getElementById('cep')
  const texto_cidade = document.getElementById('endereco')
  
  // Pegando atributos dos elementos htmo
  const cep = cx_texto.value

  
  // Chamada à API
  console.log('Início')
  const url = 'https://brasilapi.com.br/api/cep/v1/64027295'
  const response = await fetch(url)
  const dados = await response.json()

  if (response.ok){
    console.log('API OK')
    
    endereco = `Você mora na ${dados.street} da cidade ${dados.city}`
    
    texto_cidade.innerText = endereco
  }

  console.log('Fim')
}

main()