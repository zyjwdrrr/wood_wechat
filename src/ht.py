# -*- coding: utf-8 -*-
# filename: ht.py

import reply
import receive
import messageHandler

class HT(object):
    def __init__(self):
        self.userInfo = messageHandler.UserInfo()
        self.msgInfo = messageHandler.MsgInfo()
        self.userInfo.loadInfo()
        self.msgInfo.loadMsg()

    def POST(self, toUser, fromUser, Content):
        try:
            toUser = toUser
            fromUser = fromUser
            content = Content
	    replyMsg = reply.TextMsg(toUser, fromUser, content, self.userInfo, self.msgInfo)
	    return replyMsg.send()
	except Exception, Argment:
	    return Argment
        

ht = HT()
print ht.POST("oiDAl1huE6NdA8JAi8ENTtTguHc4","asdasd","100号图片")
