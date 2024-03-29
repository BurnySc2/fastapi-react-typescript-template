import os
import signal
import socket
import subprocess
import time
from pathlib import Path
from typing import Set

import psutil
import psycopg2
import pymongo
from loguru import logger
from psycopg2 import OperationalError

# pylint: disable=E0611
from psycopg2._psycopg import connection, cursor
from pymongo import MongoClient

WEBSITE_IP = 'http://localhost'


class Timeout:
    """
    Run something for a maximum limited time
    try:
        with Timeout(seconds=2):
            ...
    except TimeoutError:
    """
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type_, value, traceback):
        signal.alarm(0)


def get_pid(name: str) -> Set[int]:
    """ Return a list of PIDs of all processes with the exact given name. """
    process_pids = set()
    for proc in psutil.process_iter():
        if name == proc.name():
            pid = proc.pid
            process_pids.add(pid)
    return process_pids


def remove_leftover_files(files: Set[Path]):
    for file in files:
        if file.is_file():
            os.remove(file)


def find_next_free_port(port: int = 10_000, max_port: int = 65_535, exclude_ports: Set[int] = None) -> int:
    if exclude_ports is None:
        exclude_ports = set()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        if port in exclude_ports:
            port += 1
            continue
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError('No free ports')


# pylint: disable=R1732
def check_if_docker_is_running() -> bool:
    p = subprocess.Popen(['docker', 'ps'], stdout=subprocess.PIPE)
    _return_code = p.wait()
    if not p.stdout:
        return False
    output = p.stdout.read().decode()
    docker_running = output.startswith('CONTAINER ID')
    if docker_running:
        logger.info('Docker running detected')
    return docker_running


def get_website_address(port: int) -> str:
    return f'{WEBSITE_IP}:{port}'


def generate_css_file():
    frontend_folder = Path(__file__).parent.parent / 'frontend'
    index_css_path = frontend_folder / 'src' / 'index.css'

    # If it already exists, skip generation of file
    # pylint: disable=R1732
    if index_css_path.is_file():
        return

    # Start compilation of index.css
    _tailwind_css_process = subprocess.Popen(['npm', 'run', 'tailwind:prod'], cwd=frontend_folder)

    # Wait for tailwindcss to compile index.css file
    wait_seconds = 0
    while not index_css_path.is_file() and wait_seconds < 30:
        wait_seconds += 1
        time.sleep(1)


def start_frontend_dev_server(
    port: int,
    NEWLY_CREATED_PROCESSES: Set[int],
    backend_proxy: str = 'localhost:8000',
):
    env = os.environ.copy()
    # Set port for dev server
    env['PORT'] = str(port)
    # Don't open frontend in browser
    env['BROWSER'] = 'none'
    # Which ip and port to use when sending fetch requests to api
    # Only REACT_APP_ prefixed env variables will be forwarded to the app: console.log(process.env)
    # https://create-react-app.dev/docs/adding-custom-environment-variables
    env['REACT_APP_PROXY'] = f'http://{backend_proxy}'
    env['REACT_APP_WEBSOCKET'] = f'ws://{backend_proxy}'

    currently_running_node_processes = get_pid('node')

    # pylint: disable=R1732
    generate_css_file()

    frontend_folder = Path(__file__).parent.parent / 'frontend'
    logger.info(
        f"Starting frontend on port {port}, using backend proxy {env['REACT_APP_PROXY']} and websocket address {env['REACT_APP_WEBSOCKET']}",
    )
    _ = subprocess.Popen(['npx', 'react-scripts', 'start'], cwd=frontend_folder, env=env)

    # Give it some time to create dev server and all (3?) node proccesses
    time.sleep(5)
    new_processes = get_pid('node') - currently_running_node_processes
    logger.info(f'New node processes: {new_processes}')
    NEWLY_CREATED_PROCESSES |= new_processes


def start_backend_dev_server(
    port: int,
    NEWLY_CREATED_PROCESSES: Set[int],
    CREATED_FILES: Set[Path],
):
    root_folder = Path(__file__).parent.parent
    backend_folder = root_folder / 'backend'
    currently_running_uvicorn_processes = get_pid('uvicorn')
    env = os.environ.copy()
    env['USE_MONGO_DB'] = 'True'
    env['USE_POSTGRES_DB'] = 'True'
    env['USE_LOCAL_SQLITE_DB'] = 'True'

    sqlite_test_file_name = 'todos_TEST.db'
    sqlite_test_file_path = backend_folder / 'data' / sqlite_test_file_name
    CREATED_FILES.add(sqlite_test_file_path)
    remove_leftover_files({sqlite_test_file_path})
    env['SQLITE_FILENAME'] = sqlite_test_file_name

    logger.info(f'Starting backend on port {port}')
    _ = subprocess.Popen(
        ['poetry', 'run', 'uvicorn', 'backend.main:app', '--host', 'localhost', '--port', f'{port}'],
        cwd=root_folder,
        env=env,
    )
    # Give it some time to create dev server
    time.sleep(1)
    new_processes = get_pid('uvicorn') - currently_running_uvicorn_processes
    logger.info(f'New uvicorn processes: {new_processes}')
    NEWLY_CREATED_PROCESSES |= new_processes


def check_if_mongodb_is_running(mongo_db_port: int = 27017) -> bool:
    mongo_db_address = f'mongodb://localhost:{mongo_db_port}'
    try:
        with Timeout(seconds=2):
            _my_client: MongoClient
            with pymongo.MongoClient(mongo_db_address) as _my_client:
                pass
    except TimeoutError:
        return False
    return True


# pylint: disable=R1732
def start_mongodb(mongo_db_port: int = 27017) -> int:
    # Start mongodb via docker
    if check_if_mongodb_is_running(mongo_db_port):
        logger.info(f'MongoDB is already running on port {mongo_db_port}')
        return mongo_db_port
    command = [
        # TODO add volume to save db
        'docker',
        'run',
        '--rm',
        '-d',
        '--name',
        'mongodb_test',
        '-p',
        # TODO use mongo_db_port
        '27017-27019:27017-27019',
        'mongo:5.0.0',
    ]
    logger.info(f"Starting mongoDB with command: {' '.join(command)}")
    process = subprocess.Popen(command)
    process.wait()
    return mongo_db_port


def check_if_postgres_is_running(port: int = 5432) -> bool:
    # If we can connect to port 5432, postgres is already running
    try:
        conn: connection = psycopg2.connect(host='localhost', port=f'{port}', user='postgres', password='changeme')
        _cur: cursor = conn.cursor()
        conn.close()
        return True
    except OperationalError:
        return False


# pylint: disable=R1732
def start_postgres(postgres_port: int = 5432) -> int:
    # Start postgres via docker
    if check_if_postgres_is_running(postgres_port):
        logger.info(f'Postgres is already running on port {postgres_port}')
        return postgres_port
    postgres_container_name = 'postgres_test'
    postgres_volume_name = 'postgres_test'
    postgres_username = 'postgres'
    postgres_password = 'changeme'
    postgres_image = 'postgres:9.6.23-alpine3.14'
    # postgres_port = find_next_free_port()
    if check_if_docker_is_running():
        # docker run --rm --name postgres_test -p 5432:5432 --volume postgres_test:/data/postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=changeme postgres:9.6.23-alpine3.14
        command = [
            # TODO add volume to save db, or should that not be active while testing?
            'docker',
            'run',
            '--rm',
            '-d',
            '--name',
            postgres_container_name,
            '-p',
            f'{postgres_port}:{postgres_port}',
            '--volume',
            f'{postgres_volume_name}:/data/postgres',
            '-e',
            f'POSTGRES_USER={postgres_username}',
            '-e',
            f'POSTGRES_PASSWORD={postgres_password}',
            postgres_image,
        ]
        logger.info(f"Starting postgres with command: {' '.join(command)}")
        _process = subprocess.Popen(command)
    else:
        raise NotImplementedError()
    return postgres_port


def kill_processes(processes: Set[int]):
    # Soft kill
    for pid in processes:
        logger.info(f'Killing {pid}')
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    time.sleep(.1)

    # Force kill
    for pid in processes:
        logger.info(f'Force killing {pid}')
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


if __name__ == '__main__':
    logger.info(f'Docker running: {check_if_docker_is_running()}')
    logger.info(f'Postgres running: {check_if_postgres_is_running()}')
    logger.info(f'MongoDB running: {check_if_mongodb_is_running()}')
    start_postgres()
    start_mongodb()
    free_frontend_port = find_next_free_port()
    free_backend_port = find_next_free_port(exclude_ports={free_frontend_port})
    start_frontend_dev_server(free_frontend_port, set(), backend_proxy=f'http://localhost:{free_backend_port}')
    start_backend_dev_server(free_backend_port, set(), set())
    while 1:
        time.sleep(1)
