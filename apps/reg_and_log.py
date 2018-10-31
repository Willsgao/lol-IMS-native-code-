import re
from .mysqlpy import Mysqlhelp
from urllib.parse import unquote

do_mysql = Mysqlhelp('herodb2')

#静态文件存储路径
STATIC_DIR = './static'


def do_register(path):
    try:
        print('注册',path)
        pattern = r'username=(?P<NAME>\S*)&passwd=(?P<PWD>\S*)'
        env = re.match(pattern,path).groupdict()
        print('注册',env)
        sql_insert = "insert into user(username,passwd) values('%s','%s');"%(unquote(env['NAME']),unquote(env['PWD']))
        res = do_mysql.work(sql_insert)
        print(res)
    except Exception as e:
        print(e)
        res = '用户名已存在，请重新输入'
    return res


def do_login(mdt):
    try:
        sql_select = "select * from user where username='%s' and\
                        passwd='%s';"%(mdt['username'][0],mdt['passwd'][0])
        print(sql_select)
        res = do_mysql.getone(sql_select)
        print('######',res,'#######')
    except Exception as e:
        print('######','******')
        print(e)
        res = ''
    return res
