import signal
import socket
import subprocess
from typing import Set

import psutil
import psycopg2
import pymongo
from loguru import logger
from psycopg2 import OperationalError

# pylint: disable=E0611
from psycopg2._psycopg import connection, cursor
from pymongo import MongoClient


class timeout:
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
    process_pids = set()
    for proc in psutil.process_iter():
        if name == proc.name():
            pid = proc.pid
            process_pids.add(pid)
    return process_pids


def find_next_free_port(port: int = 10_000, max_port: int = 65_535) -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError('no free ports')


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


def check_if_mongodb_is_running(port: int = 27017) -> bool:
    mongo_db_address = f'mongodb://localhost:{port}'
    try:
        with timeout(seconds=2):
            _my_client: MongoClient
            with pymongo.MongoClient(mongo_db_address) as _my_client:
                pass
    except TimeoutError:
        return False
    return True


# pylint: disable=R1732
def start_mongodb() -> int:
    # Start mongodb via docker
    port = 27017
    if check_if_mongodb_is_running(port):
        logger.info(f'MongoDB is already running on port {port}')
        return port
    command = [
        # TODO add volume to save db
        'docker',
        'run',
        '--rm',
        '-d',
        '-p',
        '27017-27019:27017-27019',
        '--name',
        'mongodb_test',
        'mongo:5.0.0',
    ]
    logger.info(f"Starting mongoDB with command: {' '.join(command)}")
    process = subprocess.Popen(command)
    process.wait()
    return port


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
def start_postgres() -> int:
    # Start postgres via docker
    postgres_port = 5432
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
            '-d',
            '--rm',
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


if __name__ == '__main__':
    logger.info(f'Docker running: {check_if_docker_is_running()}')
    logger.info(f'Postgres running: {check_if_postgres_is_running()}')
    logger.info(f'MongoDB running: {check_if_mongodb_is_running()}')
    start_postgres()
    start_mongodb()
