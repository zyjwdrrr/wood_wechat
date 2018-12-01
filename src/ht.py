# -*- coding: utf-8 -*-
# filename: ht.py

import reply
import receive
import db
import os
import signal
import threading
from image import IMAGE

class HT(object):
    def POST(self, toUser, fromUser, Content):
        try:
            toUser = toUser
            fromUser = fromUser
            content = Content
	    replyMsg = reply.TextMsg(toUser, fromUser, content)
	    return replyMsg.send()
	except Exception, Argment:
	    return Argment
	    
def post_url():
    timer = threading.Timer(5,post_url)
    timer.start() 

def setClose(a,b):
    print "test"
    os.kill(os.getpid(),signal.SIGKILL)
   
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
    
class A:
    def __init__(self,a,b,c):
        self.a = a
        self.b=b
        self.c=c
def getL(s):
    if s == 1:
        return lambda AX:AX.a
    else:
        return lambda AX:AX.b

t = getL(1)
a = A(1,2,3)
print t(a)
