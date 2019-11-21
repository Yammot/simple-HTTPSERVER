'''
    从httpserver接收具体请求
    根据请求进行逻辑处理和数据处理
    将需要的数据反馈给httpserver
'''

from socket import *
import json
from settings import *
from threading import Thread
from urls import *


class App:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.address = (HOST, PORT)
        self.create_socket()

    def create_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
        self.s.bind(self.address)

    def start(self):
        self.s.listen(3)
        print('监听来自:', self.port)
        while True:
            try:
                c, addr = self.s.accept()
                print('连接自:', addr)
            except Exception as e:
                print(e)
                continue
            t = Thread(target=self.main, args=(c,))
            t.daemon = True
            t.start()

    def main(self, c):
        # 接受请求
        request = c.recv(1024 * 1024 * 10).decode()
        data = json.loads(request)
        if not data:
            return
        if data['method'] == 'GET':
            if data['info'] == '/' or data['info'][-5:] == '.html':
                data = self.get_html(data['info'])
            else:
                data = self.get_data(data['info'])
        elif data['method'] == 'POST':
            pass
        c.send(data.encode())

    def get_html(self, request):
        if request == '/':
            filename = DIR + '/index.html'
        else:
            filename = DIR + request
        try:
            f = open(filename)
        except:
            return json.dumps({'status': 404, 'data': open(DIR + '/404.html').read()})
        else:
            return json.dumps({'status': 200, 'data': f.read()})

    def get_data(self, data):
        for url, func in urls:
            if data == url:
                return json.dumps({'status': 200, 'data': func()})
        return json.dumps({'status': 404, 'data': 'NOT FOUND'})


if __name__ == '__main__':
    p = App()
    p.start()
