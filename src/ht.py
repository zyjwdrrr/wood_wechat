# -*- coding: utf-8 -*-
# filename: ht.py

import reply
import receive

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
        

ht = HT()
print ht.POST("oiDAl1huE6NdA8JAi8ENTtTguHc4","asdasd",'100号图片')
