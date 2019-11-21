'''
    HTTPserver主体程序
    功能：
        获取http请求
        解析http请求
        将请求发送给WebFrame
        从WebFrame接收反馈数据
        将数据组织为Response格式发送给客户端
    for review
        该程序用io多路复用
'''
from socket import *
from select import *
from config import *
import json, re


# 用于和WebFrame交互
def interframe(request):
    '''
    :param request: 要发送的字典
    :return: WebFrame得到的数据
    '''
    s = socket()
    try:
        s.connect((FRAME_HOST, FRAME_PORT))
    except:
        print('连接不上WebFrame')
        return
    else:
        # 发送字典 {'method':xx,'info':xx}
        data = json.dumps(request)
        s.send(data.encode())
        # 接收返回的数据
        data = s.recv(1024 * 1024 * 10).decode()
        if data:
            return json.loads(data)  # 返回一个字典


# 封装http类
class HttpServer:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.address = (HOST, PORT)
        self.create_socket()
        self.fdmap = {}

    # 创建套接字
    def create_socket(self):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
        self.s.bind(self.address)

    # 启动函数
    def start(self):
        self.s.listen(3)
        print('你启动了http服务,监听%s' % self.port)
        self.e_poll()

    # 调用epoll函数
    def e_poll(self):
        self.ep = epoll()
        self.ep.register(self.s, EPOLLIN)  # 关注套接字
        self.fdmap[self.s.fileno()] = self.s
        while True:
            events = self.ep.poll()
            for fd, event in events:
                if fd == self.s.fileno():
                    c, addr = self.fdmap[fd].accept()
                    print('connect from:', addr)
                    self.ep.register(c, EPOLLIN | EPOLLET)  # 边缘触发,未处理不再一直提醒
                    self.fdmap[c.fileno()] = c
                else:
                    # 浏览器发送了请求
                    self.handle(self.fdmap[fd])  # 长期占用服务端
                    self.ep.unregister(fd)  # 取消关注
                    del self.fdmap[fd]

    def handle(self, c):
        request = c.recv(4096).decode()
        # 向WebFrame发送请求类型和请求内容
        pattern = r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)'
        try:
            env = re.match(pattern, request).groupdict()
        except:
            c.close()
            return
        else:
            data = interframe(env)
            print(data)
            if data:
                self.response(c, data)

    def response(self, c, data):
        # data = {'status': 200, 'data': xxxxx}
        if data['status'] == 200:
            res = 'HTTP/1.1 200 OK\r\n'
            res += 'Content-Type:text/html\r\n'
            res += '\r\n'
            res += data['data']
        elif data['status'] == 404:
            res = 'HTTP/1.1 404 not found\r\n'
            res += 'Content-Type:text/html\r\n'
            res += '\r\n'
            res += data['data']
        c.send(res.encode())


if __name__ == '__main__':
    http = HttpServer()
    http.start()  # 启动服务
