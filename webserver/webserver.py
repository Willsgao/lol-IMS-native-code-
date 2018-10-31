#! /usr/bin/env python3
#! -*- coding=utf-8 -*-
'''
网络服务端，接收客户端访问请求的后端程序
'''
from socket import *
from threading import Thread
import re


#　处理http请求
class HttpServer(object):
    def __init__(self,app):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.app = app

    def bind(self, addr):
        self.sockfd.bind(addr)

    def start(self):
        self.sockfd.listen(5)
        while True:
            conn, cliaddr = self.sockfd.accept()
            print(cliaddr, '用户连接')
            handle_thread = Thread(target=self.handle_client, args=(conn,))
            handle_thread.start()

    def handle_client(self, conn):
        #　接受浏览器请求
        request_data = conn.recv(2048).decode('utf-8')
        request_lines = request_data.splitlines()
        print(request_lines)
        #　请求行
        request_line = request_lines[0]
        request_msges = request_lines[-1]
        print(request_line)
        #　GET or POST
        method = re.match(r'(\w+)\s+/\S*', request_line).group(1)
        filename = re.match(r'\w+\s+(/\S*)', request_line).group(1)
        # print('method=', method)
        # print('filename=', filename)
        # 将要传递的内容写入一个字典中，传递给应用程序
        env = {'METHOD':method, 'PATH_INFO':filename, 'MSG':request_msges}

        response_body = self.app(env, self.set_headers)
        response = self.response_headers + '\r\n' + response_body

        # 向客户端发送response
        conn.send(response.encode())
        conn.close()
        

    def set_headers(self, status, headers):
        '''
        在app调用该函数时，希望得到
        status = '200 OK'
        headers = [
            ('Content-Type','text/plain')
        ]
        '''
        response_headers = 'HTTP/1.1 {} \r\n'.format(status)
        for header in headers:
            response_headers += '%s:%s\r\n'%header
        self.response_headers = response_headers
