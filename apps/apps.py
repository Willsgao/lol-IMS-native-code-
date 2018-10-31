#! /usr/bin/env python3
#! -*- coding=utf-8 -*-
'''
将服务器端的登录注册及数据库操作等功能封装成类，供服务端主函数调用
'''
import os
from .db_work import workfunc1,workfunc2
from urllib.parse import quote,unquote
from collections import defaultdict
from .reg_and_log import do_register,do_login

BASE_DIR =  os.path.dirname(os.path.abspath(__file__))


def admin_reg(env,set_headers):
    status = '200　OK'
    headers = [('Content-Type', 'text/html;charset=utf-8')]
    set_headers(status, headers)
    filename = os.path.join(BASE_DIR, 'static/register.html')
    with open(filename,'r') as fd:
        data = fd.read()
    return data

def admin_log(env,set_headers):
    status = '200　OK'
    headers = [('Content-Type', 'text/html;charset=utf-8')]
    set_headers(status, headers)
    filename = os.path.join(BASE_DIR, 'static/heroindex.html')
    with open(filename,'rb') as fd:
        data = fd.read().decode('utf-8')
    return data

def msg_to_dict(msg):
    lst = msg.split('&')
    del lst[-1]
    print(lst)
    mdt = defaultdict(list)
    for i in lst:
        j = i.split('=')
        print(unquote(j[1]))
        mdt.setdefault('%s'%j[0], []).append(unquote(j[1]))
    return mdt

def register(env,set_headers):
    status = '200　OK'
    headers = [('Content-Type', 'text/html;charset=utf-8')]
    set_headers(status, headers)
    msg = env.get('MSG')
    print('**************')
    print(msg)
    res = do_register(msg)
    print('**************')
    print('res=',res)
    if res == 1:
        return '您已注册成功，请返回登录页面登录'
    else:
        return '用户名已存在，请返回注册页重新输入！'


def login(env,set_headers):
    status = '200　OK'
    headers = [('Content-Type', 'text/html;charset=utf-8')]
    set_headers(status, headers)
    msg = env.get('MSG')
    mdt = msg_to_dict(msg)
    print(mdt['username'][0])
    print(mdt['passwd'][0])
    if mdt['username'][0] == '' or mdt['passwd'][0] == '':
        return '用户名或密码有误，请重新输入！!'
    else:
        print('**************')
        print(mdt)
        res = do_login(mdt)
        print('**************')
        if res:
            filename = os.path.join(BASE_DIR, 'static/hero.html')
            print(filename)
            with open(filename,'r') as fd:
                data = fd.read()
            return data
        else:
            return 'Username or password is wrong!'


        # login_do = Dbs_Work(env,set_headers)
        # login_do.run()
def do_dbswork(env,set_headers):
    status = '200　OK'
    headers = [('Content-Type', 'text/html;charset=utf-8')]
    set_headers(status, headers)
    msg = env.get('MSG')
    if msg:
        login_do = Dbs_Work(env,set_headers)
        data = login_do.run()
        return data
    else:
        filename = os.path.join(BASE_DIR, 'static/hero.html')
        with open(filename,'r') as fd:
            data = fd.read()
        return data

class Dbs_Work(object):
    def __init__(self,env,set_headers):
        self.env = env
        self.set_headers = set_headers

    def run(self):
        self.msg = self.env.get('MSG')
        order_lines = self.env.get('PATH_INFO').split('/')
        self.mydict = msg_to_dict(self.msg)
        path = order_lines[-1]

        try:
            if path == 'add':
                data = self.add()
                # data = self.delete()
            elif path == 'delete':
                data = self.delete()
            elif path == 'change':
                data = self.change()
            elif path == 'search':
                print('开始查询了')
                print(self.mydict['hinfo'][0])
                data = self.search()
        except Exception as e:
            data = e
        return data

    def add(self):
        status = '200　OK'
        headers = [('Content-Type', 'text/html;charset=utf-8')]
        self.set_headers(status, headers)
        if self.msg == '':
            data = 'Request error'
        elif self.msg[-4:] == '.txt':
            filename = self.msg
            data = workfunc2.add_all(filename)
            print(data)
        else:
            # filename = 'ff.txt'
            # workfunc2.add_all(filename)
            if self.mydict['hinfo']:
                filename = self.mydict['hinfo'][0]
                data = workfunc2.add_all(filename)
            else:
                res = workfunc2.search_hid(self.mydict)
                if res == 'Nothing':
                    data = workfunc2.add_one(self.mydict)
                else:
                    data = '英雄ID已存在，请重新输入！'                    
        return data

    def delete(self):
        status = '200　OK'
        headers = [('Content-Type', 'text/html;charset=utf-8')]
        self.set_headers(status, headers)
        # res = workfunc2.search_hid(self.mydict)
        # print('res=res=res=res=res=res=res=res=',res)
        # if res == 'Nothing':
        #     return '不存在该英雄信息，请重新输入！'
        data = workfunc2.delete(self.mydict)
        return data

    def change(self):
        status = '200　OK'
        headers = [('Content-Type', 'text/html;charset=utf-8')]
        self.set_headers(status, headers)
        data = workfunc2.change(self.mydict)
        return data

    def search(self):
        status = '200　OK'
        headers = [('Content-Type', 'text/html;charset=utf-8')]
        self.set_headers(status, headers)
        data = workfunc2.search(self.mydict)
        return data


