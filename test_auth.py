import pytest
from app import create_app
from models import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usando um banco de dados em memória para testes
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    # Testa o registro de um novo usuário
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User registered successfully!'

def test_login(client):
    # Primeiro registramos o usuário
    client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    # Depois testamos o login com as credenciais corretas
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'token' in response.get_json()  # O login deve retornar um token
