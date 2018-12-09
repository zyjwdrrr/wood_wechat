# -*- coding: utf-8 -*-
# filename: log.py

import logging
import os.path
import time
import os,stat
import threading

log_ = logging.getLogger()
log_.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d-%H%M',time.localtime(time.time()))

def init_log(): 
    logfile = 'Logs/' + rq + '.log'
    fh = logging.FileHandler(logfile,mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] : %(levelname)s /  %(message)s")
    fh.setFormatter(formatter)
    log_.addHandler(fh)
    #msg file
    
def logVip(nick,ask,answer):
    outStr = time.strftime('======================%Y/%m/%d-%H:%M======================',time.localtime(time.time()))
    outStr += "\r\n============================================================\r\n\t"
    outStr += nick + "问： " + ask
    outStr += "\r\n\t回答:\t" + answer.replace("\n","\r\n\t\t\t")
    thread = threading.Thread(target=print_to_file,args=(outStr,))
    thread.start()
    
def print_to_file(outStr):
    msg_ = open("/home/smbuser/data/Chat/"+rq+".log" ,'a+')
    try:
        msg_.write(outStr)
    except Exception as res:
        log_.critical("logVip can not write to "+ rq + " " + res)
    finally:
        msg_.close()
        os.chmod("/home/smbuser/data/Chat/"+rq+".log",stat.S_IRWXO|stat.S_IRWXG|stat.S_IRWXU)
