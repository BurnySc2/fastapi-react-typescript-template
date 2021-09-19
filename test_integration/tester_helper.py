import socket
from typing import Set

import psutil


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
