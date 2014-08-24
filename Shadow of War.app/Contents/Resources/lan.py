import socket


def getsocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s # Use s as a argument for other functions

def getconn(s):
    s.listen(5)

    while 1:
        client = s.accept()

        return client[1]

