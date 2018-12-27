import socket
import ssl

hostname = 'sandbox.cherrybase'
port = 8443
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
# context.load_cert_chain('/home/liinda/setting/sslcert/MyCertificate.crt')

while True:
    command = input('>>>:')
    if command == 'q':
        break

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssock.send(b'hello')
