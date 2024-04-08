from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# post schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# in-memory, not persistent
my_posts = [
    {'id': 1, 'title': 'python', 'content': 'AI/ML is future'},
    {'id': 2, 'title': 'javascript', 'content': 'Complex frontend development'},
    {'id': 3, 'title': 'flutter', 'content': 'Hybrid app development'},
]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post 

def find_post_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i
    return None

@app.get('/')
def home():
    return {'message': 'ok'}

# get all posts
@app.get('/posts')
def get_posts():
    return {'data': my_posts}

# create a new post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(data: Post):
    new_post = data.model_dump()
    new_post['id'] = randrange(0, 10000000)
    my_posts.append(new_post)
    return {'data': new_post}

# get a particular post
@app.get('/posts/{id}')
def get_post(id: int):
    my_post = find_post(id)
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such post exist with id : {id}')
    return {'message': f'post {id}', 'data': my_post}

# delete a post
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such post exist with id : {id}')
    
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a post
@app.put('/posts/{id}')
def update_post(id: int, data: Post):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No such post exist with id : {id}')
    
    post = data.model_dump()
    post['id'] = id
    my_posts[index] = post
    return {'message': f'post {id} updated', 'data': post}