
from .apps import admin_reg,admin_log,register,login,do_dbswork


urls = [

    ('/register.html',admin_reg),
    ('/heroindex.html',admin_log),
    ('/register',register),    
    ('/login',login),
    ('/login/add',do_dbswork),
    ('/login/search',do_dbswork),
    ('/login/change',do_dbswork),
    ('/login/delete',do_dbswork),

]
