from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings as s
from app.database import Base, get_db
from app.oauth2 import create_access_token
from app import models
import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{s.database_username}:{s.database_password}@{s.database_hostname}/{s.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_user(client):
    user_data = {"email": "email@gmail.com",
                 "password": "1"}
    res = client.post('/users/', json=user_data)
    new_user = res.json()
    assert res.status_code == 201
    return new_user
    
@pytest.fixture
def token(test_user):
    create_access_token({"user_id": test_user['id']})
    
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
    
@pytest.fixture
def test_posts(test_user, session):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        }
    ]

    def create_post_model(post):
        models.Post(**post)
    
    post_list = list(map(create_post_model, posts_data))
    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts 