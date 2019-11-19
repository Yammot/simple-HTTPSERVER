from socket import *
import os
import signal

ADDR = ('127.0.0.1',10000)
s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(10)
# 处理僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

def deal_clinet_request(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data.decode())
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

        pid = os.fork()
        if pid == 0:
            s.close()
            deal_clinet_request(connfd)
            os._exit(0)
        else:
            connfd.close()


if __name__ == '__main__':
    main()
