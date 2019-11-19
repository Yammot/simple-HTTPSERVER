from socket import *
from time import sleep

ADDR = ('127.0.0.1', 10001)
filename_list = '/home/tarena/ftp_备份'


class Ftpclinet:
    def __init__(self, s):
        self.__s = s

    def show_ftp(self):
        self.__s.send(b'ok')
        data = self.__s.recv(1024).decode()
        if data == 'ok':
            msg = self.__s.recv(1024).decode()
            print(msg)
        else:
            print(data)

    def download_ftp_file(self, filename):
        try:
            f = open(filename_list + '/' + filename[0], 'wb')
        except Exception:
            print('文件不存在')
            return
        while True:
            data = self.__s.recv(1024)
            if data == b'##':
                print('下载完成')
                break
            f.write(data)
        f.close()

    def upload_ftp_file(self, filename):
        for i in filename:
            self.__s.send(i.encode())
            sleep(0.1)
            f = open(i, 'rb')
            while True:
                data = f.read()
                if not data:
                    self.__s.send(b'##')
                    print('上传完毕')
                    break
                self.__s.send(data)
            f.close()

    def exit_ftp(self):
        data = self.__s.recv(1024).decode()
        if data == b'exit':
            self.__s.close()
            return


def main():
    s = socket()
    s.connect(ADDR)
    f = Ftpclinet(s)
    while True:
        print('L:list')
        print('D + filename:download')
        print('U + filepath:upload')
        print('E:exit')
        try:
            file = input('输入执行的操作:')
            s.send(file.encode())
            cmd = file.strip().split(' ')
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e)
            continue
        if cmd[0] == 'L':
            f.show_ftp()
        elif cmd[0] == 'D':
            filename = cmd[1:]
            f.download_ftp_file(filename)
        elif cmd[0] == 'U':
            filename = cmd[1:]
            f.upload_ftp_file(filename)
        elif cmd[0] == 'E':
            f.exit_ftp()
        else:
            print(cmd[0])


if __name__ == '__main__':
    main()
