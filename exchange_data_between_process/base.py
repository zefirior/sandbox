from enum import Enum
import socket
import time


BUFFSIZE = 1024
EOF = b'\b'


class COMMAND(Enum):
    READY_RECV = b'RR'
    EOF = b'EOF'

    def __init__(self, code):
        self.code = code


class Consumer:

    def __init__(self, sock: socket.SocketIO):
        self.sock = sock

    def recvmsg(self) -> bytes:
        chunks = []
        while True:
            chunk = self.sock.recv(BUFFSIZE)
            if chunk == COMMAND.EOF.code:
                return b''.join(chunks)

            chunks.append(chunk)
            self.sock.send(COMMAND.READY_RECV.code)


class Produser:

    def __init__(self, sock: socket.SocketIO):
        self.sock = sock

    def sendmsg(self, message: bytes):
        length = len(message)
        offset = 0
        while offset < length:
            chunk = message[offset:offset + BUFFSIZE]
            chunk_len = self.sock.send(message[offset:offset + BUFFSIZE])
            if chunk_len == 0:
                raise Exception
            offset += chunk_len

            command = self.sock.recv(BUFFSIZE)
            if command == COMMAND.READY_RECV.code:
                continue

        self.sock.send(COMMAND.EOF.code)
