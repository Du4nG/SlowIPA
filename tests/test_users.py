from app import schemas
from .database import client, session

def test_root(client):
    res = client.get('/')
    print(res.json().get('message'))
    
def test_create_user(client):
    res = client.post('/users/', json={'email':'email@gmail.com',
                                      'password':'1'})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'email@gmail.com'
    assert res.status_code == 201
    
def test_login_user(client):
    res = client.post('/login', data = {'username':'email@gmail.com',
                                        'password':'1'})
    
    assert res.status_code == 200