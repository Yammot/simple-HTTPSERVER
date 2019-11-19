from socket import *
import os
from threading import Thread

ADDR = ('127.0.0.1',10001)
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(10)

def deal_clinet_request(c):
    while True:
        try:
            data = c.recv(1024)
        except KeyboardInterrupt:
            os._exit(0)
        except Exception as e:
            print(e)
            continue
        if not data:
            break
        c.send(b'ok')
    c.close()

def main():
    while True:
        try:
            connfd, addr = s.accept()
            print('连接自:',addr)
        except KeyboardInterrupt:
            s.close()
            os._exit(0)
        except Exception as e:
            print(e)
            continue
        t = Thread(target=deal_clinet_request,args=(connfd,))
        t.setDaemon(True)
        t.start()








if __name__ == '__main__':
    main()
