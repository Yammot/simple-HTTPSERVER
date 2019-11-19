from socket import *
import os
from multiprocessing import Process
import signal

ADDR = ('127.0.0.1',10001)
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(10)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

def deal_clinet_request(c):
    while True:
        s.close()
        data = c.recv(1024)
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

        p = Process(target=deal_clinet_request,args=(connfd,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()