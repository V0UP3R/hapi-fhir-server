import requests
import json
from datetime import datetime
import pandas as pd

def carregar_pacientes_csv(nome_arquivo_csv, url_servidor_fhir):
    df = pd.read_csv(nome_arquivo_csv, encoding='latin1')
    
    for _, linha in df.iterrows():
        paciente = criar_paciente_a_partir_da_linha(linha)
        
        url_paciente = f"{url_servidor_fhir}/Patient"
        
        response_paciente = requests.post(url_paciente, headers={"Content-Type": "application/fhir+json"}, json=paciente)
        
        if response_paciente.status_code == 201:
            print(f"Paciente {paciente['name'][0]['given'][0]} {paciente['name'][0]['family']} criado com sucesso!")
            
            observacao = str(linha['Observação']) if pd.notna(linha['Observação']) else ''

            paciente_id = json.loads(response_paciente.text).get('id')

            if pd.notna(observacao) and observacao != '':
                observation = criar_observacao_a_partir_da_linha(paciente_id, observacao)
                url_observacao = f"{url_servidor_fhir}/Observation"
                
                response_observacao = requests.post(url_observacao, headers={"Content-Type": "application/fhir+json"}, json=observation)
                
                if response_observacao.status_code == 201:
                    print(f"Observação para o paciente {paciente['name'][0]['given'][0]} {paciente['name'][0]['family']} criada com sucesso!")
                else:
                    print(f"Erro ao criar observação para o paciente {paciente['name'][0]['given'][0]} {paciente['name'][0]['family']}. Código de status: {response_observacao.status_code}")
                    print(response_observacao.text)
        else:
            print(f"Erro ao criar paciente. Código de status: {response_paciente.status_code}")
            print(response_paciente.text)

def criar_paciente_a_partir_da_linha(linha):
    nome = linha['Nome']
    nome = dividir_nome_sobrenome(nome)
    cpf = linha['CPF']
    genero = linha['Gênero']
    genero = "male" if genero.lower() == "masculino" else "female" if genero.lower() == "feminino" else "Gênero não reconhecido"
    data_nascimento_str = linha['Data de Nascimento']
    telefone = linha['Telefone']
    pais_nascimento = linha['País de Nascimento']
    data_nascimento = datetime.strptime(data_nascimento_str, '%d/%m/%Y').strftime('%Y-%m-%d')

    paciente = {
        "resourceType": "Patient",
        "active": True,
        "name": [
            {
                "use": "official",
                "family": nome[1],
                "given": [nome[0]]
            }
        ],
        "identifier": [{"system": "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRDocumentoIndividuo-1.0", "value": cpf}],
        "gender": genero.lower(),
        "birthDate": data_nascimento,
        "telecom": [{"system": "phone", "value": telefone}],
        "extension": [
            {
                "url": "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRRacaCorEtnia-1.0",
                "extension": [{"url": "race", "valueCodeableConcept": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v3-Race", "code": "2106-3", "display": "White"}]}}]
            },
            {
                "url": "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRMunicipio-1.0",
                "extension": [{"url": "city", "valueString": "Município de Nascimento"}]
            },
            {
                "url": "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRPais-1.0",
                "valueCodeableConcept": {"coding": [{"system": "http://www.saude.gov.br/fhir/r4/ValueSet/BRPais-1.0", "code": pais_nascimento, "display": pais_nascimento}]}
            },
            {
                "url": "http://www.saude.gov.br/fhir/r4/StructureDefinition/BRQualidadeCadastroIndividuo-1.0",
                "valueDecimal": 80
            }
        ],
        "deceasedBoolean": False,
        "maritalStatus": {
            "coding": [{"system": "http://www.saude.gov.br/fhir/r4/ValueSet/BREstadoCivil-1.0", "code": "S", "display": "Solteiro(a)"}]
        },
    }
    
    return paciente

def criar_observacao_a_partir_da_linha(paciente_id, observacao):
    observation = {
        "resourceType": "Observation",
        "status": "final",
        "code": {"coding": [{"system": "http://loinc.org", "code": "28127-9", "display": "Health status"}], "text": "Health status"},
        "subject": {"reference": f"Patient/{paciente_id}"},
        "valueString": observacao
    }

    return observation

def dividir_nome_sobrenome(nome_completo):
    palavras = nome_completo.split()

    palavras = [p for p in palavras if p.lower() not in ['de', 'do', 'da']]

    if len(palavras) == 1:
        return [palavras[0], '']
    elif len(palavras) == 2:
        return [palavras[0], palavras[1]]
    else:
        sobrenome = palavras[-1]
        nome = ' '.join(palavras[:-1])
        return [nome, sobrenome]