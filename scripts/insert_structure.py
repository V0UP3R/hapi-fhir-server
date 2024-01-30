import requests
import json

def insertStructure():
  with open('data/BrIndividuo.json', 'r', encoding='utf-8') as file:
      profile_data = json.load(file)

  server_url = 'http://localhost:8080/fhir'

  endpoint = '/StructureDefinition'

  url = f'{server_url}{endpoint}'

  headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
  }

  response = requests.post(url, headers=headers, json=profile_data)

  if response.status_code == 201:
      print(f"Perfil carregado com sucesso! (Status Code: {response.status_code})")
  else:
      print(f"Falha ao carregar o perfil. Status Code: {response.status_code}")
      print(f"Resposta do servidor: {response.text}")
