#! /usr/bin/env python3
#! -*- coding = utf-8 -*-
'''
服务端运行的主程序．
'''
# 从方法类模块中导入sql执行方法
from webserver.webserver import HttpServer  # 导入网络服务端的主程序
from apps.webFramework import app   # 导入服务端启动所需的主要参数（addr,databases)
import sys,os

#　完成httpserver对象属性的添加和创建
def main():
    http_server = HttpServer(app)
    http_server.bind(('0.0.0.0', 8000))
    print('服务端监听8000端口')
    http_server.start()


if __name__ == '__main__':
    main()
