import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 8443))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()

        message = []
        while True:
            block = conn.recv(1024)
            if not block:
                break
            message.append(block)

        print('massage:')
        print(b''.join(message).decode())



# import socket
# import ssl
#
# hostname = '127.0.0.1'
# port = 8443
# context = ssl.SSLContext(ssl.PROTOCOL_TLS)
#
# with socket.create_connection((hostname, port)) as sock:
#     with context.wrap_socket(sock, server_hostname=hostname) as ssock:
#         ssock.send(b'hello')
