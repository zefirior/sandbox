import socket
import ssl


context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain('/home/liinda/setting/sslcert/MyCertificate.crt', '/home/liinda/setting/sslcert/MyKey.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 8443))
    sock.listen(5)
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            conn, addr = ssock.accept()
            print(conn.recv(1024))



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
