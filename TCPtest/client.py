import socket

hostname = '127.0.0.1'
port = 8443

while True:
    text = input('>>>:')
    if text == 'q':
        break

    with socket.create_connection((hostname, port)) as sock:
        sock.send(text.encode())
