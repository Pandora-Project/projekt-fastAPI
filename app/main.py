from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Optional
from pydantic import BaseModel
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='password123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection successfull')
        break
    except Exception as error:
        print('Connecting to database failed', error)
        print('Error: ', error)
        time.sleep(5)

my_posts = [{
    'title': "title of post 1", "content": "content of post 1", "id": 1},
    {'title': "fun dog toys", "content": "a towel with snacks", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/')
async def root():
    return {'message': 'Hello World!'}


@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {'message': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {'data': post_dict}


@app.get('/posts/{id}')
async def get_post(id: int, Response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return {'post detail': f'Here is a post {id}, {post}'}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    print(post)
    return {'message': post_dict}
