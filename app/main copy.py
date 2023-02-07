from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='#Collins4u7', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connected")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(5)
    
    
my_posts = [{"title": "Hi there", "content": "This is my new ok", "rating": 2, "id":1}, {"title": "Hi there", "content": "This is my new ok", "rating": 2, "id":2}]

@app.get("/")
def root():
    return {"message": "Hello Collins"}


@app.get("/posts")
def get_posts():
    
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

# @app.post("/createposts")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']} content: {payload['content']}"}

# @app.post("/posts")
# def create_posts(new_post: Post):
#     print(new_post)
#     print(new_post.dict())
#     return {"data": new_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, (str(id),)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist")
    
    return {"data": updated_post}