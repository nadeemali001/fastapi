from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List

from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc
from . import models, schema, utils
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='fastapi', user='postgres', password='tiger', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('DB connected successfully!!')
        break
    except Exception as error:
        print('Connection failed to DB')
        print('Error: ', error)
        time.sleep(10)


@app.get('/')
def root():
    return {"message": "Hello Worlld!!!!!!!"}


# @app.get('/sqlalchemy')
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"status": posts}
