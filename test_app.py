import pytest
from app import app, Data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Configuration pour utiliser une base de données de test
TEST_DB_HOST = os.environ.get('TEST_DB_HOST', 'localhost')
TEST_DB_PORT = os.environ.get('TEST_DB_PORT', '3306')
TEST_DB_USER = os.environ.get('TEST_DB_USER', 'root')
TEST_DB_PASSWORD = os.environ.get('TEST_DB_PASSWORD', '')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME', 'test_mydatabase')

# Connexion à la base de données de test
test_engine = create_engine(
    f'mysql+pymysql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}')
TestSession = sessionmaker(bind=test_engine)
test_session = TestSession()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}'
    with app.test_client() as client:
        with app.app_context():
            # Créer les tables pour la base de données de test
            Data.metadata.create_all(test_engine)
            yield client
            # Nettoyer les tables après les tests
            Data.metadata.drop_all(test_engine)


def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"200 OK" in rv.data


def test_store_data(client):
    rv = client.post('/store_data', json={'name': 'test'})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'success'
    assert json_data['message'] == 'Data stored successfully'


def test_read_data(client):
    # First, store some data
    client.post('/store_data', json={'name': 'test'})

    # Then, read the data
    rv = client.get('/read_data')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) > 0
    assert json_data[0]['name'] == 'test'


def test_exit(client):
    rv = client.get('/exit')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'success'
    assert json_data['message'] == 'Server is shutting down...'


def test_cpu_load(client):
    rv = client.get('/cpu')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['status'] == 'success'
    assert json_data['message'] == 'CPU load started'
