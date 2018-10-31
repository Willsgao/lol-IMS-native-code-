#! /usr/bin/env python3
#! -*- coding=utf-8 -*-
'''
将数据库增删改查的功能封装成类供客户端调用
'''
from .mysqlpy import Mysqlhelp
from urllib.parse import quote,unquote
import re,os

FILE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static'

class Sqlfunction(object):
    def __init__(self,dbs,table):
        self.dbs = dbs
        self.tb = table
        self.mysql = Mysqlhelp(self.dbs)

    def dt_to_lt(self,dicts):
        lst = []
        for key in dicts:
            s = ''
            for skey in dicts[key]:
                s += skey
            lst.append((key,s))
        return lst

    # 将数据以字典方式存储，然后插入数据库
    def add_one(self, dicts):
        del (dicts['hinfo'])
        print('dicts=',dicts)
        lst = self.dt_to_lt(dicts)
        print('+++++++++++++++++++')
        print(lst)
        print('+++++++++++++++++++')

        sql = 'insert into %s (' % self.tb + ','.join([i[0] for i in lst]) + ')\
         values (' + ','.join([' %r ' % unquote(i[1]) for i in lst]) + ');'

        print('----------------------')
        print(sql)
        print('----------------------')
        res1 = self.mysql.work(sql)
        if res1 == 1:
            return '添加成功'
        else:
            return '添加失败'

    def add_all(self,filename):
        filename = os.path.join(FILE_DIR, filename)
        print(filename)
        with open(filename, 'r') as f:
            num = 0
            print('文件打开了，嘿嘿嘿嘿嘿')
            for line in f:
                print('-----------------------')
                data = line.split('\t')
                print('***********************')
                print(data)
                hid,hname,hattack,hposition,hbackground,hgender =\
                 int(data[0].strip()),data[1].strip(),data[2].strip(),data[3].strip(),data[4].strip(),data[5].strip()
                sql = "insert into %s (hid,hname,hattack,hposition,hbackground,hgender)\
                values(%d,%r,%r,%r,%r,%r)"\
                %(self.tb,hid,hname,hattack,hposition,hbackground,hgender)
                print(sql)

                res1 = self.mysql.work(sql)
                if res1 == 1:
                    num += 1
                else:
                    num += 0
        return '成功加入%s条数据'%num

    def change(self, dicts):
        lst = self.dt_to_lt(dicts)
        sql = 'UPDATE %s SET ' % self.tb+ ','.join(['%s=%r' % (k[0], unquote(k[1])) for k in lst])\
                   + ' WHERE hid="%s";'%dicts['hid'][0]
        print(sql)
        res1 = self.mysql.work(sql)
        if res1:
            return '修改成功'
        else:
            return '修改失败'

    def search(self,dicts):
        kwd = unquote(dicts['hinfo'][0]) # 获取前端的查询请求的关键词，并转化为中文
        self.keyword = kwd
        sql = 'select * from %s '%self.tb +'where hid like "{}" or hname like "{}" or hattack like "{}"\
        or hposition like "{}" or hbackground like "{}" or hgender like "{}";'.format(kwd,kwd,kwd,kwd,kwd,kwd)
        print('sql=',sql)
        try:
            res1 = self.mysql.getall(sql)
            if res1:
                data = self.search_info(res1)
                return data
            else:
                return '查询失败'
        except Exception as e:
            print(e)
            return e

    def search_hid(self,dicts):
        kwd = dicts['hid'][0] # 获取前端的查询请求的hid
        sql = 'select * from %s '%self.tb +'where hid = "%d"'%int(kwd)
        print('sql=',sql)
        try:
            res1 = self.mysql.getall(sql)
            print('res1 = ', res1)
            if res1:
                return 'Exist'
            else:
                return 'Nothing'
        except Exception as e:
            print(e)
            return 'Error'

    def search_info(self,res):
        info = ''
        for i in res:
            datas = '''<tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td class='c1'><a href='%s'>%s</a></td>
            <td>%s</td>
            </tr>'''%(i[1],i[2],i[3],i[4],i[5],i[5],i[6])
            info += datas

        web = '''<html lang='en'><head><meta charset='UTF-8'>
        <title>%s</title>
        <style type="text/css">
        　　　　body{
                height:1000px;
                background:red;
        }
            h1{
                text-align:center;
                font-family:'微软雅黑';
            }
            table{margin:0 auto;border:3px solid blue;opacity:0.5;
            text-align:center;font-family:'微软雅黑';background-color:FFE894;
            }
            td{
            width:150px;
            height:20px;
            border:2px solid green;
            }
            .c1{
            width:600px;
            }
            a{
            text-decoration:none;
            }
        </style>
        </head><body>
        <div>
            <h1>英雄联盟信息表——查询关键字：%s</h1>
            <table>
            <tr><td>序号</td><td>英雄</td><td>近远程</td><td>位置</td>
            <td>背景链接</td><td>性别</td>
            %s
            </table>
        </div>
        </body></html>

        '''%('英雄信息',self.keyword,info)

        return web


    def delete(self,dicts):
        mdt = {}
        print(dicts)
        for k in dicts:
            print(dicts[k][0])
            if dicts[k][0] != '':
                print(k,dicts[k][0])
                mdt.update({str(k):str(dicts[k][0])})
                print('_+_+_+_+_+_+_+_+')
                print(mdt)
        sql1 = 'select * from %s '%self.tb +'where '+' AND '.join(['%s=%r' % (k, mdt[k]) for k in mdt])+';'
        res1 = self.mysql.getone(sql1)
        if res1:
            sql2 = 'delete from %s '%self.tb +'where '+' AND '.join(['%s=%r' % (k, mdt[k]) for k in mdt])+';'
            print(sql2)
            res2 = self.mysql.work(sql2)
            return '删除成功'
        else:
            return '删除失败，请检查输入条件！'


workfunc1 = Sqlfunction('herodb2','user')
workfunc2 = Sqlfunction('herodb2','heros')
