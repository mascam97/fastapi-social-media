from fastapi.testclient import TestClient
from main import app
from fastapi import status
from utils.jwt_manager import create_token
from services.publication import PublicationService
from schemas.publication import Publication
from config.database import Session
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b"<h1>Hello world</h1>"

def test_login():
    response = client.post("/login", json={"email": "admin@gmail.com", "password": "admin"})

    assert response.status_code == status.HTTP_200_OK
    assert (response.json()).get("token") is not None

def test_login_invalid():
    response = client.post("/login", json={"email": "admin@gmail.com", "password": "wrongPassword"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert (response.json()).get("detail") == "Invalid credentials"

def test_publications_endpoints_requires_authentication():
    index_response = client.get("/publications")
    assert index_response.status_code == status.HTTP_403_FORBIDDEN

    show_response = client.get("/publications/1")
    assert show_response.status_code == status.HTTP_403_FORBIDDEN

    create_response = client.post("/publications", json={"title": "Test", "body": "Test"})
    assert create_response.status_code == status.HTTP_403_FORBIDDEN

    update_response = client.put("/publications/1", json={"title": "Test", "body": "Test"})
    assert update_response.status_code == status.HTTP_403_FORBIDDEN

    delete_response = client.delete("/publications/1")
    assert delete_response.status_code == status.HTTP_403_FORBIDDEN

def test_publications_endpoints_requires_validations():
    create_response = client.post("/publications", headers= auth_token())
    assert create_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    update_response = client.put("/publications/1", headers=auth_token())
    assert update_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_publications_endpoints_response_not_found():
    show_response = client.get("/publications/1000", headers=auth_token())
    assert show_response.status_code == status.HTTP_404_NOT_FOUND
    assert (show_response.json()).get("message") == "Not Found"

    update_response = client.put(
        "/publications/1000",
        json={"title": "Publication", "content": "Publication content", "state": "active"},
        headers=auth_token())
    assert update_response.status_code == status.HTTP_404_NOT_FOUND
    assert (update_response.json()).get("message") == "Not Found"

def test_index_publications():
    response = client.get("/publications", headers=auth_token())
    assert response.status_code == status.HTTP_200_OK
    assert (response.json()).get("data") is not None

def test_index_publications_with_query_state():
    response = client.get("/publications?state=active", headers=auth_token())

    assert response.status_code == status.HTTP_200_OK

def test_show_publication():
    publication = new_publication(title="Publication", content="Publication content", state="active")

    response = client.get("/publications/"+ str(publication.id), headers=auth_token())

    assert response.status_code == status.HTTP_200_OK
    assert (response.json()).get("data").get("title") == "Publication"
    assert (response.json()).get("data").get("content") == "Publication content"
    assert (response.json()).get("data").get("state") == "active"

def test_create_publication():
    response = client.post(
        "/publications",
        json={"title": "Publication", "content": "Publication content", "state": "active"},
        headers=auth_token())

    assert response.status_code == status.HTTP_201_CREATED
    assert (response.json()).get("message") == "The publication was created"
    assert (response.json()).get("data").get("title") == "Publication"
    assert (response.json()).get("data").get("content") == "Publication content"
    assert (response.json()).get("data").get("state") == "active"

def test_update_publication():
    publication = new_publication(title="Publication", content="Publication content", state="active")

    response = client.put(
        "/publications/"+ str(publication.id),
        json={"title": "New Title publication", "content": "New publication content", "state": "new state"},
        headers=auth_token())

    assert response.status_code == status.HTTP_200_OK
    assert (response.json()).get("message") == "The publication was updated"
    assert (response.json()).get("data").get("title") == "New Title publication"
    assert (response.json()).get("data").get("content") == "New publication content"
    assert (response.json()).get("data").get("state") == "new state"

def test_delete_publication():
    publication = new_publication(title="Publication", content="Publication content", state="active")

    response = client.delete("/publications/"+ str(publication.id), headers=auth_token())

    assert response.status_code == status.HTTP_200_OK
    assert (response.json()).get("message") == "The publication was deleted"

    db = Session()
    publication = PublicationService(db).get_publication(publication.id)
    assert publication is None

def auth_token():
    return {"Authorization": "Bearer " + create_token({"email": "admin@gmail.com"})}
def new_publication(title = 'Publication title', content = 'Publication content', state = 'active'):
    db = Session()
    publication = PublicationService(db).create_publication(Publication(title=title, content=content, state=state))
    return publication

@pytest.fixture(autouse=True)
def run_around_tests():
    db = Session()
    yield db
    db.rollback()
    db.close()