from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of book",
                                       max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101)  # gt=greater than lt =less than

    class Config:
        schema_extra = {
            "example": {
                "id": "1d11046b-7277-41dc-8f4b-c3396c9fe30d",
                "title": "Computer Science Pro",
                "author": "Codingwithroby",
                "description": "A very nice descrioption of a book",
                "rating": 75
            }
        }


BOOKS = []


@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    return BOOKS


@app.get('/book/{book_id}')
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x


@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter-1] = book
            return BOOKS[counter-1]


@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"ID:{book_id} deleted!"


# adding elements to the book list for development purposes


def create_books_no_api():
    book_1 = Book(id="fd11046b-7277-41dc-8f4b-c3396c9fe30d",
                  title="title 1",
                  author="author 1",
                  description="descripiton 1",
                  rating=60)
    book_2 = Book(id="f211046b-7277-41dc-8f4b-c3396c9fe30d",
                  title="title 2",
                  author="author 2",
                  description="descripiton 2",
                  rating=70)
    book_3 = Book(id="fd11046b-7327-41dc-8f4b-c3396c9fe30d",
                  title="title 3",
                  author="author 3",
                  description="descripiton 3",
                  rating=45)
    book_4 = Book(id="fd12046b-7277-41dc-8f4b-c3396c9fe30d",
                  title="title 4",
                  author="author 4",
                  description="descripiton 4",
                  rating=55)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)
