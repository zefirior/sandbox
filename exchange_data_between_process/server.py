import os
import socket

from base import Consumer


SOCK_FILE = "/tmp/python_test_server.sock"


if os.path.exists(SOCK_FILE):
  os.remove(SOCK_FILE)

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    sock.bind(SOCK_FILE)
    sock.listen(4)

    conn, _ = sock.accept()
    consumer = Consumer(conn)

    while True:

        message = consumer.recvmsg()
        if message == b'stop':
            break
        # print(len(message) / 1024 / 1024)
