import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from datetime import datetime

# --- PREPARAÇÃO ---
os.environ['ENV'] = 'dev' # Pular auth
from app.app import app

# Importar a engine do banco REAL para verificar os dados
from db.engine import get_mongo_collection

client = TestClient(app)

# Pegar a coleção REAL que o app vai usar
# (Isso só funciona se seu .env estiver correto)
try:
    collection_name = f"{os.getenv('ENV').upper()}_intent_logs"
    db_collection = get_mongo_collection(collection_name)
    print(f"\nConectado à coleção de teste: {collection_name}")
except Exception as e:
    print(f"ERRO: Não foi possível conectar ao Mongo para testes de integração. {e}")
    db_collection = None


def test_predict_integration_and_db_write():
    """
    Testa a rota POST /predict e verifica se o dado foi
    REALMENTE salvo no MongoDB.
    """
    if db_collection is None:
        print("Pulando teste de integração, sem conexão com DB.")
        return

    # 1. Preparar um texto único para podermos achar no banco
    test_text = f"teste_integracao_{datetime.now().isoformat()}"

    # 2. EXECUTAR A REQUISIÇÃO
    response = client.post("/predict", params={"text": test_text})

    # 3. VERIFICAR A RESPOSTA
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == test_text
    assert "id" in data # A resposta deve conter o ID do banco

    # 4. VERIFICAR O BANCO DE DADOS (A parte da "Integração")
    record = db_collection.find_one({"text": test_text})
    
    assert record is not None
    assert record["owner"] == "dev_user"
    assert str(record["_id"]) == data["id"] # Confirma que o ID bate

    # 5. LIMPEZA (MUITO IMPORTANTE!)
    # Apagar o registro de teste do banco de dados
    db_collection.delete_one({"_id": record["_id"]})
    print(f"Registro de teste {record['_id']} limpo do DB.")
