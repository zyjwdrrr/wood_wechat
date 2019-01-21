# -*- coding: utf-8 -*-
# filename: main.py
import web
import os
import sys
import src.messageHandler as mh
import src.token as tk
import src.db as dataBase
import src.config as cfg
from src.handle import Handle
from web import form
from src.express import Express
import src.log as log

urls = (
    '/wechat', 'Handle',
    '/e(.*)','Express'
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

class Watcher:
   def __init__(self):
       self.child = os.fork()
       if self.child == 0:
           return
       else:
           self.watch()
   
   def watch(self):
       try:
           os.wait()
       except KeyboardInterrupt:
           print 'KeyBoardInterrupt'
           self.kill()
       sys.exit()
   def kill(self):
       try:
           os.kill(self.child,signal.SIGKILL)
       except OSError:
           pass
           
def init_param():
    reload(sys)
    os.chdir("/var/project/wood_wechat")
    sys.setdefaultencoding('utf-8')
    log.init_log()
    log.log_.info("程序开始运行")
    Watcher()
    cfg.loadCfg()
    tk.post_url()
    #tk.post_menu()
    mDB = dataBase.DB()
    mDB.doNothing()
    mDB.refresh()
    mDB.close()
    
if __name__ == '__main__':
    init_param()
    app = web.application(urls, globals())
    app.run()
