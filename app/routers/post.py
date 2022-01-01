from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.openapi.models import MediaType
#from sqlalchemy.sql.functions import user
from app import oauth2
from .. import models, schema
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from sqlalchemy.sql.expression import desc

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schema.PostOut])
# @router.get('/')
def get_posts(db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user),
              limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    result = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # post = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=curr_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get('/latest', response_model=schema.Post)
# def get_latest_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
#     latest_post = db.query(models.Post).order_by(desc(models.Post.id)).first()
#     return latest_post


@router.get('/{id}', response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    #posts = db.query(models.Post).filter(models.Post.id == id).first()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details for id: {id} is not found in DB.")
    return posts


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    post_detail = posts.first()
    if post_detail == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't exits!!")

    if int(post_detail.owner_id) != int(curr_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this action!')

    posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schema.Post)
def update_post(id: int, post: schema.PostBase, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    post_detail = posts.first()
    if post_detail == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} doesn't exits!!")

    if int(post_detail.owner_id) != int(curr_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform this action!')
    posts.update(post.dict(), synchronize_session=False)
    db.commit()
    return posts.first()
