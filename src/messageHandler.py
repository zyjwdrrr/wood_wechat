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
            userFile = csv.reader(open('data/user.csv','r'))
            next(userFile)
            for line in userFile:
                self.userDict[line[1]] = User(line[0],line[2])
            return 'success'
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
            msgFile = csv.reader(open('data/msg.csv','r'))
            next(msgFile)
            for line in msgFile:
                levelList = []
                for l in line[2:12]:
                    levelList.append(int(l))
                self.msgDict[line[0]] = MSG(line[1],levelList)
            return 'success'
        except Exception, Argument:
            return Argument


