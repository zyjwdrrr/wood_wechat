# -*- coding: utf-8 -*-
# filename: messageHandler.py

import csv
import time

user =dict()
msg = dict()

class USER(object):
    def __init__(self,name,level):
        self.name = name
        self.level = level

class MSG(object):
    def __init__(self,answer,price,cnt):
        self.answer = answer
        self.price = price
        self.cnt = cnt

def STR(str):
    return str.decode('gbk').encode('utf-8')

def getLevel(name):
    try:
        lv = user[name].level
        print "  User ID = " + name + "尝试咨询问题  等级: " + str(lv)
        return lv
    except Exception, Argument:
        print "  User ID = " + name + "尝试咨询问题  未查询到等级"
        return 0

def refreshUser():
    try:
        userFile = csv.reader(open('data/user.csv','r'))
        next(userFile)
        user.clear()
        for line in userFile:
            user[line[1]] = USER(STR(line[0]),int(line[2]))
        return "成功刷新用户列表"
    except Exception, Argument:
        return Argument

def getAllUser():
    print len(user)
    info = "当前总用户数: " + len(user)
    for key in user:
        info += "\n" + user[key].name + "," + key + "," + user[key].level
    return info

def getCommand(content):
    if '查询用户':
        return getAllUser()

def loadMsg(content,level):
    if 'cmd' in content and level == 9:
        cmdMsg = getCommand(content)
        print "管理员命令:" + content
        print cmdMsg
        return cmdMsg

    print 111
    try :
        if msg[content].cnt == '0':
            answer = content + " 已经被售出了"
        else:
            answer = "  A: " + msg[content].answer + " 价格是:" + msg[content].price[level]
    except Exception, Argument:
        print "未知问题"
        answer = "我没有理解你的问题，现在正将这条信息转发给客服"
    return answer


def refreshMsg():
    try:
        msgFile = csv.reader(open('data/msg.csv','r'))
        next(msgFile)
        msg.clear()
        for line in msgFile:
            if len(line) == 13:
                scnt = line[13]
            else:
                scnt = '1'
            msg[STR(line[0])] = MSG(STR(line[1]),line[2:12],scnt)
        return "成功刷新消息列表"
    except Exception, Argument:
        return Argument

def refresh():
    print refreshUser()
    print refreshMsg()

