from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# post schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='12433', cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print('Database connection established')
        break
    except Exception as error:
        print(error)
        print('Error connecting to database')
        time.sleep(3)


@app.get('/')
def home():
    return {'message': 'ok'}

# get all posts
@app.get('/posts', status_code=status.HTTP_200_OK)
def get_posts():
    curr.execute('''SELECT * FROM posts''')
    posts = curr.fetchall()
    print(posts)
    return {'data': posts}

# create a new post
@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    curr.execute(''' INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * ''', (post.title, post.content))
    new_post = curr.fetchone()
    conn.commit()
    return {'message': 'New post created successfully', 'data': new_post}

# get a particular post
@app.get('/posts/{id}')
def get_post(id: int):
    curr.execute(''' SELECT * FROM posts WHERE id = %s ''', (str(id),))
    post = curr.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No such post exist with id : {id}')
    return {'message': f'post {id}', 'data': post}

# delete a post
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    curr.execute(''' DELETE FROM posts WHERE id = %s RETURNING *''', (str(id),))
    deleted_post = curr.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No such post exist with id : {id}')

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# update a post
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    curr.execute(''' UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * ''', (post.title, post.content, str(id)))
    updated_post = curr.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No such post exist with id : {id}')

    return {'message': f'post {id} updated', 'data': updated_post}
