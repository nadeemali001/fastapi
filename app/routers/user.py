from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users/{id}', response_model=schema.UserOut)
def find_user(id: int, db: Session = Depends(get_db)):
    user_detail = db.query(models.User).filter(models.User.id == id).first()
    if not user_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User is not found with id: {id}")
    return user_detail
