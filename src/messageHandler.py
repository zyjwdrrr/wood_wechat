# -*- coding: utf-8 -*-
# filename: messageHandler.py

import csv

class User(object):
    def __init__(self,name,ulevel):
	self.name = name
	self.level = ulevel
    
    def toString(self):
    	return "your name is " + self.name + " level: " + self.level

class UserInfo(object):
    def __init__(self):
        self.userDict = {}

    def loadInfo(self):
        try:
            userFile = csv.reader(open('user.csv','r'))
            print userFile
            next(userFile)
            for line in userFile:
                self.userDict[line[1].decode('gb2312')] = User(line[0].decode('gb2312'),line[2].decode('gb2312'))
            return 1
        except Exception, Argument:
            return Argument

    def printInfo(self):
        print self.userDict['oiDAl1huE6NdA8JAi8ENTtTguHc4'].level

class MSG(object):
    def __init__(self,reply,price):
        self.reply = reply
        self.price = price

class MsgInfo(object):
    def __init__(self):
        self.msgDict = {}

    def loadMsg(self):
        try:
            msgFile = csv.reader(open('msg1.csv','r'))
            print msgFile
            next(msgFile)
            for line in msgFile:
                levelList = []
                for l in line[2:12]:
                    levelList.append(int(l))
                self.msgDict[line[0].decode('gb2312')] = MSG(line[1].decode('gb2312'),levelList)
            return 1    
        except Exception, Argument:
            return Argument


