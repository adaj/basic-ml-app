import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

# --- PREPARAÇÃO ---
# 1. Forçar o modo 'dev' para pular a autenticação (Depends(conditional_auth))
os.environ['ENV'] = 'dev'

# 2. Importar o app DEPOIS de definir a ENV
from app.app import app

# 3. Criar um "cliente" de teste para fazer requisições
client = TestClient(app)

# --- TESTES ---

def test_read_root():
    """Testa a rota raiz (GET /)"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Basic ML App is running in dev mode"}


def test_predict_unit_mocked(mocker):
    """
    Testa a rota POST /predict com MOCKS.
    Não fala com o banco e não usa o modelo de ML.
    """
    
    # 1. MOCK (Fingir) a coleção do MongoDB
    # Encontramos o alvo: 'app.app.collection' (o objeto global 'collection' no arquivo 'app.py')
    # Nós o substituímos por um "MagicMock"
    mock_collection = mocker.MagicMock()
    mocker.patch("app.app.collection", mock_collection)
    def mock_insert_one_behavior(results_dict):
    	results_dict['_id'] = "mocked_object_id_123"
    mock_collection.insert_one.side_effect = mock_insert_one_behavior
    # O insert_one real não retorna nada (None)

    # 2. MOCK (Fingir) o modelo de ML
    # Substituímos o dicionário global 'MODELS' por um falso
    mock_model = mocker.MagicMock()
    mock_model.predict.return_value = ("mocked_intent", {"mocked_intent": 1.0})
    mocker.patch("app.app.MODELS", {"mocked_model": mock_model})

    # 3. EXECUTAR A REQUISIÇÃO
    # Usamos 'params' porque a rota espera 'text: str' (não um JSON)
    test_text = "Isso é um teste unitário"
    response = client.post("/predict", params={"text": test_text})

    # 4. VERIFICAR (Asserts)
    assert response.status_code == 200
    
    # Verifique se o mock do banco foi chamado CORRETAMENTE
    # 'assert_called_once()' garante que o 'collection.insert_one' foi chamado
    mock_collection.insert_one.assert_called_once()
    
    # Verifique o conteúdo da resposta
    data = response.json()
    assert data["text"] == test_text
    assert data["owner"] == "dev_user" # Veio do ENV=dev
    assert data["predictions"]["mocked_model"]["top_intent"] == "mocked_intent"
    assert data["id"] == "mocked_object_id_123"
