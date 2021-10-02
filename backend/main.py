import asyncio
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.routes.chat import chat_router
from backend.routes.hello_world import background_task_function, hello_world_router
from backend.routes.todolist import create_database_if_not_exist, get_db, todo_list_router

ENV = os.environ.copy()

app = FastAPI()
app.include_router(hello_world_router)
app.include_router(chat_router)
app.include_router(todo_list_router)

origins = [
    'https://burnysc2.github.io',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup_event():
    asyncio.create_task(background_task_function('hello', other_text=' world!'))
    create_database_if_not_exist()
    logger.info('Hello world!')


@app.on_event('shutdown')
def shutdown_event():
    db = get_db()
    if db():
        db.close()
    logger.info('Bye world!')


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
