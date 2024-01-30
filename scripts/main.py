from insert_patients import carregar_pacientes_csv
from insert_structure import insertStructure
import os

insertStructure()

nome_arquivo_csv = os.path.join(os.getcwd(), 'data', 'patients.csv')

url_servidor_fhir = 'http://localhost:8080/fhir'  
carregar_pacientes_csv(nome_arquivo_csv, url_servidor_fhir)


print('Rotina Rodada com sucesso')
