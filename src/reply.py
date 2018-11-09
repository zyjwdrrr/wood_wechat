# -*- coding: utf-8 -*-
# filename: reply.py
import time
from messageHandler import UserInfo
from messageHandler import MSG
#import csv
class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class TextMsg(Msg):    
    def __init__(self, toUserName, fromUserName, content, userInfo, msgInfo):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content
        self.userInfo = userInfo
        self.msgInfo = msgInfo
    
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        myContent = self.__dict['Content']
        myMsgDict = self.msgInfo.msgDict
        myUserDict = self.userInfo.userDict
        if(myContent in myMsgDict):
            ll = 0
            toUser = self.__dict['ToUserName']
            if(toUser in myUserDict):
                ll = myUserDict[toUser].level
                print ll
            self.__dict['Content'] = myMsgDict[myContent].reply + myMsgDict[myContent].price[ll]
        return XmlForm.format(**self.__dict)

class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)
