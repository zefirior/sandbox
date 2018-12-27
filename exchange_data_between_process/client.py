import socket
import time

from base import Produser


SOCK_FILE = "/tmp/python_test_server.sock"


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(SOCK_FILE)
prod = Produser(sock)

# message = b'1234' * 1024  # Mb
message = b'1234' * int((1024 * 1024 / 4))  # Mb
# message = b'1234' * int((1024 * 1024 * 1024 / 4 / 8))  # Gb

start = time.time()
for _ in range(int(1024 / 8)):
    prod.sendmsg(message)
prod.sendmsg(b'stop')
print(time.time() - start)
