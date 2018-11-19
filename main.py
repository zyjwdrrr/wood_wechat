# -*- coding: utf-8 -*-
# filename: main.py
import web
#import model.py
import src.messageHandler as mh
import src.token as tk
import src.db as dataBase
from src.handle import Handle
from web import form
from src.index import Index

urls = (
    '/wechat', 'Handle',
    '/','Index',
)

class BASE_DEF(object):
    def POST(self):
        return 1
        
    def hGET(self):
        return 1
    
    def GET(self):
        if True:#dataBase.login_verify(self.get_cookie())
            return self.hGET()
        else:
            return 1
        
    def get_cookie(self):
        return web.cookies().get('open_id')
        
    def set_cookie(self):
        web.setcookie('open_id',str(user_id),settings.COOKIE_EXPIRES)

if __name__ == '__main__':
    #mh.refresh('')
    tk.post_url()
    mDB = dataBase.DB()
    mDB.refresh()
    mDB.close()
    app = web.application(urls, globals())
    app.run()
