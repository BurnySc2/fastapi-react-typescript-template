import uvicorn
from fastapi import FastAPI, Request
from loguru import logger

import sqlite3
import os
from pathlib import Path
from typing import List, Dict

app = FastAPI()
db: sqlite3.Connection = None


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/api")
async def show_all_todos() -> List[Dict[str, str]]:
    todos = []
    for row in db.execute("SELECT id, task FROM todos"):
        todos.append(
            {
                "id": row[0],
                "content": row[1],
            }
        )
    return todos


@app.post("/api/{todo_description}")
async def create_new_todo(todo_description: str):
    # https://fastapi.tiangolo.com/advanced/using-request-directly/
    if todo_description:
        logger.info(f"Attempting to insert new todo: {todo_description}")
        db.execute("INSERT INTO todos (task) VALUES (?)", [todo_description])
        db.commit()


# Alternative to above with request body:
# @app.post("/api")
# async def create_new_todo(request: Request) -> List[Dict[str, str]]:
#     """
#     Example with accessing request body.
#     Send a request with body {"new_todo": "<todo task description>"}
#     """
#     # https://fastapi.tiangolo.com/advanced/using-request-directly/
#     json_response = await request.json()
#     todo_item = json_response.get("new_todo", None)
#     if todo_item:
#         logger.info(f"Attempting to insert new todo: {todo_item}")
#         db.execute("INSERT INTO todos (task) VALUES (?)", [todo_item])
#         db.commit()


@app.delete("/api/{todo_id}")
async def remove_todo(todo_id: int):
    """ Example of using /api/itemid with DELETE request """
    logger.info(f"Attempting to remove todo id: {todo_id}")
    db.execute("DELETE FROM todos WHERE id==(?)", [todo_id])
    db.commit()


def create_database_if_not_exist():
    global db
    todos_db = Path(__file__).parent / "data" / "todos.db"
    if not todos_db.is_file():
        os.makedirs(todos_db.parent, exist_ok=True)
        db = sqlite3.connect(todos_db)
        db.execute("CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)")
        db.commit()
        logger.info(f"Created new database: {todos_db.name}")
    else:
        db = sqlite3.connect(todos_db)


create_database_if_not_exist()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
