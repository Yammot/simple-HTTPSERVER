from socket import *
import os
from threading import Thread
from time import sleep

ADDR = ('127.0.0.1', 10001)

class FTP(Thread):
    def __init__(self,c,file_shell):
        super().__init__()
        self.__c = c
        self.__file = file_shell

    def __download(self,filename):
        for file in self.__file:
            if file == filename[0]:
                try:
                    f = open(ftp_file_path + filename[0],'rb')
                except Exception:
                    self.__c.send('文件出错'.encode())
                    return
                while True:
                    data = f.read()
                    if not data:
                        sleep(0.1)
                        self.__c.send('##'.encode())
                        break
                    self.__c.send(data)
                f.close()
            else:
                sleep(0.1)
                self.__c.send('文件出错'.encode())


    def __show_ftp_file(self):
        if not self.__file:
            self.__c.send('文件库为空')
        else:
            s = '\n'.join(self.__file)
            self.__c.send(b'ok')
            sleep(0.01)
            self.__c.send(s.encode())


    def __upload(self,filename):
        f = open(ftp_file_path+filename,'wb')
        while True:
            data = self.__c.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    def __ftp_exit(self):
        self.__c.send(b'exit')
        os._exit(0)

    def run(self):
        while True:
            cmd= self.__c.recv(1024).decode().split(' ')
            print(cmd)
            if cmd[0] == 'L':
                self.__show_ftp_file()
            elif cmd[0] == 'D':
                self.__download(cmd[1:])
            elif cmd[0] == 'U':
                filename = cmd[1].split('/')[-1]
                self.__upload(filename)
            elif cmd[0] == 'E':
                self.__ftp_exit()


def main():
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)
    while True:
        try:
            connfd, addr = s.accept()
            print('连接自:', addr)
        except KeyboardInterrupt:
            s.close()
            os._exit(0)
        except Exception as e:
            print(e)
            continue
        f = FTP(connfd,ftp_shell)
        f.run()


if __name__ == '__main__':
    ftp_file_path = '/home/tarena/ftp/'
    ftp_shell = os.listdir(ftp_file_path)
    main()

