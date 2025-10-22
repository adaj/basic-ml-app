# basic-ml-app

Project structure

```
.
├── app/                        # Aplicação FastAPI
│   ├── app.Dockerfile          # Definição do ambiente em que o backend roda
│   └── app.py                  # Implementação do backend
├── db/                         # Lógica do banco de dados
├── intent-classifier/          # Scripts relacionados ao modelo de ML
│   ├── data/                   # Dados para os modelos de ML
│   ├── models/                 # Modelos treinados
│   └── intent-classifier.py    # Código principal do modelo de ML
├── tests/                      # Testes unitários e de integração
├── docker-compose.yml          # Arquivo de orquestração dos serviços envolvidos
├── requirements.txt            # Dependências do Python 
└── .gitignore                  
```