import asyncio
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.routes.chat import chat_router
from backend.routes.hello_world import hello_world_router
from backend.routes.todolist import create_database_if_not_exist, get_db, todo_list_router

ENV = os.environ.copy()

app = FastAPI()
app.include_router(hello_world_router)
app.include_router(chat_router)
app.include_router(todo_list_router)

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


async def background_task_function(my_text: str, other_text: str = ' something!'):
    """A background function that gets called once"""
    while 1:
        await asyncio.sleep(60 * 60)
        logger.info(f'Repeated {my_text}{other_text}')


if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
