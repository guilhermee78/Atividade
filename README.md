📚 API de Reserva de Salas
Este repositório contém a API de gerenciamento de Atividades, desenvolvida com Flask e SQLAlchemy, projetada para ser executada em contêineres Docker como parte de uma arquitetura de microsserviços.

🧩 Arquitetura
A API de gerenciamento de Atividades é um microsserviço dedicado exclusivamente ao gerenciamento das atividades feitas pelos professores. Ela opera dentro de um sistema maior de Getão escolar o Gest-o-escolar-API.

⚠️ Importante: Esta API depende da API de Gerenciamento Escolar (responsável por turmas, alunos, professores). A API de Gerenciamento Escolar também deve estar em execução, atraves deste link https://gest-o-escolar-api-docker.onrender.com , para que a validação dos professores e alunos ocorra corretamente via requisições HTTP REST.

🚀 Tecnologias Utilizadas
Python 3.10+
Flask
SQLAlchemy
SQLite (utilizado como banco de dados local para desenvolvimento e persistência de reservas)
Requests (para comunicação com a API de Gerenciamento Escolar)
Docker (para containerização da aplicação)
▶️ Como Executar a API (com Docker)
A maneira mais recomendada de executar esta API é usando Docker. Certifique-se de ter o Docker Desktop (ou Docker Engine) instalado e rodando em sua máquina.

Clone o repositório:

Bash

git clone https://github.com/guilhermee78/Atividade
cd Atividade
obs* na branch Developing
Construa a imagem Docker da API de Atividade:

Bash

docker build -t minhas_atividades .
Este comando lê o Dockerfile no diretório atual e constrói uma imagem Docker chamada minhas_atividades.
Execute o contêiner da API de Reserva:

Bash

docker run -d -p 5003:5003 --name api-reservas minhas_atividades
-d: Executa o contêiner em modo detached (em segundo plano).
-p 5003:5003: Mapeia a porta 5003 do seu computador (host) para a porta 5003 dentro do contêiner. É através desta porta que você acessará a API.
--name api-atividades: Atribui um nome fácil de usar ao seu contêiner.
A aplicação estará disponível em: 📍 http://localhost:5003



📝 Observação: O banco de dados SQLite (instance/site.db) é criado automaticamente dentro do contêiner na primeira execução. Para persistência de dados entre reinícios do contêiner, você pode considerar usar um volume Docker (-v /caminho/do/seu/host/data:/app/instance).



📡 Endpoints Principais

A API de gerenciamento de Atividades expõe os seguintes endpoints, e alguns exemlos de entrada de dados:

POST atividade:   http://localhost:5003/atividades/

{
  "id_disciplina": 101,
  "professor_id": 50,
  "enunciado": "Desenvolver um ensaio sobre a Revolução Industrial no século XX."
}



POST resposta por id de atividade:   http://localhost:5003/atividades/{id atividade}/respostas

{
  "id_aluno": 10,
  "resposta": "Meu ensaio em anexo: ensaio_final_revolucao.pdf"
}



PUT nota(avaliação das respostas):  http://localhost:5003/atividades/{id atividade}/respostas/{id resposta}/nota

{
  "nota": 95
}


GET atividades por id : http://localhost:5003/atividades/{id atividade}

GET atividades : http://localhost:5003/atividades/

GET atividades, somente o professor associado pode acessar a atividade : http://localhost:5003/atividades/{id atividades}/professor/{id professor}

DELETE atividade por id : http://localhost:5003/atividades/{id atividade}




Para que a API de Gerenciamento de Atividades funcione corretamente, a API de Gerenciamento Escolar precisa estar acessível.

Certifique-se de que a API de Gerenciamento Escolar esteja rodando e acessível em:
https://gest-o-escolar-api-docker.onrender.com

Esta API de Atividade utiliza o endpoint https://gest-o-escolar-api-docker.onrender.com para validar a existência do professor e do aluno através de um cache interno.



📦 Estrutura do Projeto
RESERVA/
│
├── app.py                  # Ponto de entrada da aplicação Flask
├── config.py               # Configurações de porta e api   
├── Dockerfile              # Define a imagem Docker para a aplicação
├── atividade_model.py      # Modelo de dados da Atividade e Respostas (SQLAlchemy)
├── sql.py                  # Configuração do banco de dados (db Flask-SQLAlchemy)
├── atividade_controler.py  # Definição das rotas e lógica dos endpoints da API
├── clients.py              # liga a api principal e busca dados do professor e aluno
├── requirements.txt        # Dependências Python do projeto
└── README.md               # Este arquivo de documentação



🧑‍💻 Autor
Jonathan Nascimento 2401750 
Caio Matheus Caetano Silva  2401362
Juan Bernardini Grenzi Cavadinha  2401187
Guilherme Freire Azevedo  2401421

