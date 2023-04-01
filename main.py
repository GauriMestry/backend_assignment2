from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional,Literal
from fastapi.encoders import jsonable_encoder
import random
import os
import json
from uuid import uuid4

app = FastAPI()

#Book Model
class Book(BaseModel):
    name: str
    price: float
    genre: Literal["Fiction" , "Novel" , "Love/Romantic" , "Play/Drama"]
    book_id: Optional[str] = uuid4().hex   


BOOK_FILE="books.json"
BOOK_DATABASE=[]

if os.path.exists(BOOK_FILE):
    with open(BOOK_FILE,"r") as f:
        BOOK_DATABASE= json.load(f)

#/
@app.get("/")
async def home():
    return {"Message":"Welcome to my bookstore"}

#/list-books
@app.get("/list-books")
async def list_books():
    return{"books" :BOOK_DATABASE}

#/book-by-index/{index}
@app.get("/book-by-index/{index}")
async def book_by_index(i:int):
    if i<0 or i>= len(BOOK_DATABASE):
       raise HTTPException(404,f"Index {i} is out of range {len(BOOK_DATABASE)}!")
    else:
        return{"book" :BOOK_DATABASE[i]}

#/get-random-book
@app.get("/get-random-book")
async def get_random_book():
    return {"book" :random.choice(BOOK_DATABASE)}

#/add-book
@app.post("/add-book")
async def add_book(book:Book):
    book.book_id= uuid4().hex
    json_book=jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(BOOK_FILE,"w") as f:
        json.dump(BOOK_DATABASE,f)
    return {"Message":f"Book {book} is added succssfully!", "book_id":book.book_id}

#/get-book?id=...
@app.get("/get-book")
async def get_book(book_id:str):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            return book
    raise HTTPException(404,f"Book notfound!: {book_id}")

