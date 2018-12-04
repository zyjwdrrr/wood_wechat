# -*- coding: utf-8 -*-
# filename: express.py
import web
import random
import string
import threading

render=web.template.render('templates/')

Auth = dict()
class Express(object):
    def GET(self,auth_key):
        if Auth.has_key(auth_key):
            return render.express(True,Auth[auth_key].open_id,Auth[auth_key].name)
        else:
            return render.express(False,'1','1')
    def POST(self):
        return "71"
     
def gen_random_access(user):
    new_auth = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    Auth.update({new_auth:user})
    timer = threading.Timer(20,delete_auth,args=(new_auth,))
    #timer.start()
    return "wx.vhelpss.com/e"+new_auth

def delete_auth(auth):
    if Auth.has_key(auth):
        del Auth[auth]
        print auth + " has been deleted!!!"
