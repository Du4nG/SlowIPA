from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    
    print(res.json())
    
    assert posts_list[0].Post.id == test_posts[0].id
    assert res.status_code
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts')
    assert res.status_code == 401
    
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get('/posts/69')
    assert res.status_code == 404