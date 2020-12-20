from sanic import Sanic
from sanic.response import text, json, file, file_stream
from sanic.request import Request
from loguru import logger

import sqlite3
import os
from pathlib import Path

app = Sanic("App Name")
db = None


@app.get("/api/get")
async def show_all_todos(request: Request):
    todos = []
    for row in db.execute("SELECT id, task FROM todos"):
        todos.append(
            {"id": row[0], "content": row[1],}
        )
    return json(todos)


@app.post("/api/create")
async def create_new_todo(request: Request):
    new_todo = request.json.get("new_todo", None)
    if new_todo:
        logger.info(f"Attempting to insert: {new_todo}")
        db.execute("INSERT INTO todos (task) VALUES (?)", [new_todo])
        db.commit()
    return text("Success")


@app.delete("/api/delete")
async def remove_todo(request: Request):
    to_remove_todo = request.json.get("remove_todo_id", None)
    if to_remove_todo:
        logger.info(f"Attempting to remove todo id: {to_remove_todo}")
        db.execute("DELETE FROM todos WHERE id==(?)", [to_remove_todo])
        db.commit()
    return text(f"Successfully removed {to_remove_todo}")


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


if __name__ == "__main__":
    create_database_if_not_exist()
    app.run(host="0.0.0.0", port=8000, debug=True)
