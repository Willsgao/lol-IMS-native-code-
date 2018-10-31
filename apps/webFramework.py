# -*- coding:utf-8 -*-
'''
功能:完成后端请求处理服务代码
说明：模拟web框架的基本原理
'''
import time,os
from .urls import urls
from urllib.parse import quote,unquote


# 设置静态文件的文件夹
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_ROOT_DIR = os.path.join(BASE_DIR, 'static')
#　存放python方法
PYTHON_DIR = './wsgipy'

class Application(object):
    def __init__(self,urls):
        self.urls = urls

    def __call__(self, env, set_headers):
        path = env.get('PATH_INFO','/')
        #/static/index.html
        #/time表示用python方法处理请求
        if path == '/':
            file_name = 'heroindex.html'
            filename = os.path.join(HTML_ROOT_DIR, file_name)
            print('路径',HTML_ROOT_DIR)
            print(filename)
            try:
               with open(filename, 'rb') as fd:
                print('进来了吧')
                file_data = fd.read()
                status = '200 OK'
                headers = [('Content-Type', 'text/html;charset=utf-8')]
                set_headers(status, headers)
                return unquote(file_data.decode('utf-8'))
            except IOError:
                status = '404 Not Found'
                headers = [('Content-Type', 'text/html;charset=utf-8')]
                set_headers(status, headers)
                return '<h1>+++++++So sorry!+++<h1>'

        elif path[-4:] == '.css':
            file_name = path.split('/')[-1]
            filename = os.path.join(HTML_ROOT_DIR, file_name)
            print('路径',HTML_ROOT_DIR)
            print(filename)
            try:
               with open(filename, 'rb') as fd:
                print('进来了吧')
                file_data = fd.read()
                status = '200 OK'
                headers = []
                set_headers(status, headers)
                return unquote(file_data.decode('utf-8'))
            except IOError:
                status = '404 Not Found'
                headers = []
                set_headers(status, headers)
                return '<h1>+++++++So sorry!+++<h1>'

        elif path.startswith('/static'):
            #获取静态网页
            file_name = path[8:]
            print('++++++++++++++++')
            print(file_name)
            print('++++++++++++++++')
            try:
                filename = os.path.join(HTML_ROOT_DIR, file_name)
                print(filename)
                fd =  open(filename, 'rb')
            except IOError as e:
                print(e)
                #　代表没有找到该静态网页
                status = '404 Not Found'
                headers = [('Content-Type', 'text/html;charset=utf-8')]
                set_headers(status, headers)
                return '<h1>+++++++So sorry!+++<h1>'
            else:
                file_data = fd.read()

                #　代表找到该静态网页
                status = '200 OK'
                headers = [('Content-Type', 'text/html;charset=utf-8')]
                set_headers(status, headers)
                return unquote(file_data.decode('utf-8'))
            finally:
                fd.close()
        else:
            for url,handler in self.urls:
                if path == url:

                    return handler(env,set_headers)
            #　请求的url未找到
            status = '404　Not Found'
            headers = [('Content-Type', 'text/html;charset=utf-8')]
            set_headers(status,headers)
            return 'Sorry url not found'



app = Application(urls)