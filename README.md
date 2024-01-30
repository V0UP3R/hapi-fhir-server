# hapi-fhir-server
Documentação de Instalação e Configuração do 
Servidor FHIR com Docker e HAPI FHIR
Introdução
Este documento fornece um guia passo a passo para a instalação e configuração de um servidor FHIR 
(Fast Healthcare Interoperability Resources) utilizando uma imagem Docker pronta do HAPI FHIR. 
Certifique-se de ter o Docker instalado em seu sistema antes de prosseguir.
Pré-requisitos
Docker instalado: Instalação do Docker
Passo 1: Preparação do Ambiente
1.1 Crie um arquivo docker-compose.yml com o seguinte conteúdo:

1.2 Salve o arquivo e feche o editor.
Passo 2: Instalação e Inicialização do Servidor FHIR
2.1 No terminal, navegue até o diretório onde você salvou o arquivo docker-compose.yml.
2.2 Execute o seguinte comando para iniciar o servidor:
docker-compose up -d
Este comando baixará a imagem do HAPI FHIR, criará um contêiner e iniciará o servidor FHIR.
2.3 Aguarde até que o servidor esteja totalmente inicializado.
Passo 3: Verificação do Servidor FHIR
3.1 Abra um navegador da web e acesse http://localhost:8080/fhir/metadata.
Você deve ver a resposta XML ou JSON com as informações do servidor, indicando que o servidor FHIR 
está em execução corretamente
