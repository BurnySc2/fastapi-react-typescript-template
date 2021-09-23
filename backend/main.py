import os
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# pylint: disable=E0611
from pydantic import BaseModel

ENV = os.environ.copy()
USE_MONGO_DB = ENV.get('USE_MONGO_DB', 'True') == 'True'
USE_POSTGRES_DB = ENV.get('USE_POSTGRES_DB', 'True') == 'True'
USE_LOCAL_SQLITE_DB = ENV.get('USE_LOCAL_SQLITE_DB', 'True') == 'True'
SQLITE_FILENAME = ENV.get('SQLITE_FILENAME', 'todos.db')
# TODO use different database tables when using stage = dev/staging/prod

app = FastAPI()
db: Optional[sqlite3.Connection] = None

origins = [
    'http://localhost',
    'http://localhost:8000',
    # The following 3 dont work, how to make it work so only this address can speak to api server?
    # 'https://burnysc2.github.io/fastapi-react-typescript-template',
    # 'https://burnysc2.github.io/fastapi-react-typescript-template/#/',
    # 'https://burnysc2.github.io/fastapi-react-typescript-template/#/todo',
    # TODO UNSAFE: Remove me
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def create_database_if_not_exist():
    # pylint: disable=W0603
    global db
    todos_db = Path(__file__).parent / 'data' / SQLITE_FILENAME
    if not todos_db.is_file():
        os.makedirs(todos_db.parent, exist_ok=True)
        db = sqlite3.connect(todos_db)
        db.execute('CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)')
        db.commit()
        logger.info(f'Created new database: {todos_db.name}')
    else:
        db = sqlite3.connect(todos_db)


@app.on_event('startup')
async def startup_event():
    create_database_if_not_exist()


@app.on_event('shutdown')
def shutdown_event():
    if db:
        db.close()


@app.get('/')
def hello_world():
    return {'Hello': 'World'}


@app.get('/api')
async def show_all_todos() -> List[Dict[str, str]]:
    todos = []
    if db:
        for row in db.execute('SELECT id, task FROM todos'):
            todos.append({
                'id': row[0],
                'content': row[1],
            })
    return todos


@app.post('/api/{todo_description}')
async def create_new_todo(todo_description: str):
    # https://fastapi.tiangolo.com/advanced/using-request-directly/
    if todo_description:
        logger.info(f'Attempting to insert new todo: {todo_description}')
        if db:
            db.execute('INSERT INTO todos (task) VALUES (?)', [todo_description])
            db.commit()


# Alternative to above with request body:
@app.post('/api_body')
async def create_new_todo2(request: Request):
    """
    Example with accessing request body.
    Send a request with body {"new_todo": "<todo task description>"}
    """
    # https://fastapi.tiangolo.com/advanced/using-request-directly/
    request_body = await request.json()
    todo_item = request_body.get('new_todo', None)
    if todo_item:
        logger.info(f'Attempting to insert new todo: {todo_item}')
        if db:
            db.execute('INSERT INTO todos (task) VALUES (?)', [todo_item])
            db.commit()


# pylint: disable=R0903
class Item(BaseModel):
    todo_description: str


# Alternative to above with model:
@app.post('/api_model')
async def create_new_todo3(item: Item):
    """
    Example with accessing request body.
    Send a request with body {"todo_description": "<todo task description>"}
    """
    # https://fastapi.tiangolo.com/tutorial/body/#import-pydantics-basemodel
    logger.info(f'Received item: {item}')
    if item and item.todo_description:
        logger.info(f'Attempting to insert new todo: {item.todo_description}')
        if db:
            db.execute('INSERT INTO todos (task) VALUES (?)', [item.todo_description])
            db.commit()


@app.delete('/api/{todo_id}')
async def remove_todo(todo_id: int):
    """ Example of using /api/itemid with DELETE request """
    logger.info(f'Attempting to remove todo id: {todo_id}')
    if db:
        db.execute('DELETE FROM todos WHERE id==(?)', [todo_id])
        db.commit()


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
