# basic-ml-app

Projeto em desenvolvimento... 

> Este código é de propósito educacional e pode conter alguns pequenos bugs que precisam ser consertados. 

Estrutura do projeto:
```
.                               # "Working directory"
├── app/                        # Lógica do serviço web 
│   ├── app.py                  # Implementação do backend com FastAPI
|   ├── app.Dockerfile          # Definição do container em que o backend roda
│   └── auth.py                 # Implementação do backend
├── db/                         # Lógica do banco de dados
│   └── engine.py               # Encapsulamento do pymongo
├── intent-classifier/          # Scripts relacionados ao modelo de ML
│   ├── data/                   # Dados para os modelos de ML
│   ├── models/                 # Modelos treinados
│   └── intent-classifier.py    # Código principal do modelo de ML
├── dags/                       # Workflows integrados no Airflow
│   └── ...                     # TODO
├── tests/                      # Testes unitários e de integração
│   └── ...                     # TODO
├── docker-compose.yml          # Arquivo de orquestração dos serviços envolvidos
├── requirements.txt            # Dependências do Python 
├── .env                        # Variáveis de ambiente
└── .gitignore                  
```

Como rodar localmente:
```
# Crie e ative um ambiente conda com as dependências do projeto
conda create -n intent-clf python=3.11
conda activate intent-clf 
pip install -r requirements.txt # instalar as dependências
# Ajuste seu .env (ex: dev ou prod?)
# ...
# Em .env, se ENV=prod, você precisará criar um token
python app/auth.py create --owner="alguem" --expires_in_days=365 
# Suba o serviço web e acesse-o em localhost:8000
uvicorn app.app:app --host 0.0.0.0 --port 8000 --log-level debug 
```

Como rodar utilizando o Docker:
```
docker build -t intent-clf:0.1 -f app/app.Dockerfile .
docker run -d -p 8080:8000 --name intent-clf-container intent-clf:0.1
# Checar os containers ativos
docker ps 
# Acompanhar os logs do container
docker logs -f intent-clf-container 
```

Como interromper a execução do container:
```
# Parar o container
docker stop intent-clf-container
# Deletar o container (com -f ou --force você deleta sem precisar parar)
docker rm -f intent-clf-container
```

Como rodar diretamente com o Docker Compose:
```
docker-compose up -d
# Checar os containers ativos
docker ps 
# Acompanhar os logs do container
docker logs -f intent-clf-container 
```

