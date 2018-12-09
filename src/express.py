# -*- coding: utf-8 -*-
# filename: express.py
import web
import random
import string
import threading
import db
import csv
import time
import os,stat

render=web.template.render('templates/')
file_name = "/home/smbuser/data/express.csv"
Auth = dict()

class Express(object):
    def GET(self,auth_key):
        if Auth.has_key(auth_key):
            return render.express(True,Auth[auth_key].open_id,Auth[auth_key].name,db.agents.keys())
        else:
            return render.express(False,'1','1','1')
    def POST(self,auth):    
        try:
            wi = web.input()
            user = wi.author_name.split(',')
            if db.user.has_key(user[1]):
                price = '12'
                if 'isShunfeng' in wi and wi.isShunfeng == 'on':
                    price = '23'
                with open(file_name,'a+') as f:
                    f.write("\r\n\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\""%(time.strftime('%Y%m%d-%H:%M',time.localtime(time.time())),wi.name,wi.context,wi.address,wi.remarks,wi.agent,price,user[0],user[1]))
                    f.close()
                    os.chmod(file_name,stat.S_IRWXO|stat.S_IRWXG|stat.S_IRWXU)
                return "1"
            else:
                return "0"
	except Exception as e:
            print e
        return "0"
     
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
