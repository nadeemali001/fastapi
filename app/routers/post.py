from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schema
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql.expression import desc

router = APIRouter(
    prefix='/posts'
)


@router.get('/', response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    #cursor.execute(''' SELECT * from posts ''')
    #posts = cursor.fetchall()
    post = db.query(models.Post).all()
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute('''INSERT INTO POSTS (title,content,published) VALUES (%s,%s,%s) RETURNING *''',
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_posts = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/latest', response_model=schema.Post)
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute(''' SELECT * from posts order by id desc limit 1''')
    # latest_post = cursor.fetchone()
    latest_post = db.query(models.Post).order_by(desc(models.Post.id)).first()
    return latest_post


@router.get('/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * from posts where id = %s''', (str(id),))
    # posts = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details for id: {id} is not found in DB.")
    return posts


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * from posts where id = %s''', (str(id),))
    # posts = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id)
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't exits!!")
    else:
        # cursor.execute('''DELETE from posts where id = %s''', (str(id),))
        # conn.commit()
        posts.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schema.Post)
def update_post(id: int, post: schema.PostBase, db: Session = Depends(get_db)):
    # cursor.execute('''SELECT * from posts where id = %s''', (str(id),))
    # posts = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id)
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't exits!!")

    else:
        # cursor.execute('''UPDATE posts set title=%s,content=%s,published=%s where id = %s''',
        #                (post.title, post.content, post.published, str(id)))
        # # conn.commit()
        # cursor.execute('''SELECT * from posts where id = %s''', (str(id),))
        # posts = cursor.fetchone()
        posts.update(post.dict(), synchronize_session=False)
        db.commit()
    return posts.first()
