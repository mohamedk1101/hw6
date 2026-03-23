from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from supabase import create_client, Client
import os

app = FastAPI(title="My Personal Book API")

# Pulling the same credentials you used before
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
MY_SECRET = os.getenv("MY_API_KEY")

supabase: Client = create_client(URL, KEY)

class Book(BaseModel):
    title: str
    author: str
    rating: int

def verify_key(x_api_key: str = Header(...)):
    if x_api_key != MY_SECRET:
        raise HTTPException(status_code=401, detail="Invalid Key")
    return x_api_key

@app.get("/books")
def get_books():
    # Notice this now points to 'my_books' instead of 'president'
    response = supabase.table("my_books").select("*").execute()
    return response.data

@app.post("/books")
def add_book(book: Book, key: str = Depends(verify_key)):
    response = supabase.table("my_books").insert({
        "title": book.title, 
        "author": book.author, 
        "rating": book.rating
    }).execute()
    return response.data
