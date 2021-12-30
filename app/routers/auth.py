from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.encoders import generate_encoders_by_class_tuples
from sqlalchemy.orm import Session
from starlette.routing import Router
from .. import database, schema, models, utils

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: schema.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    return {"token": "Success token"}
