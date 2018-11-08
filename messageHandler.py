# -*- coding: utf-8 -*-
# filename: messageHandler.py

class User(object):
    def __init__(self,name,userid,ulevel):
		self.name = name
		self.userid = userid
		self.ulevel = ulevel
    
    def toString(self):
    	return "your name is " + self.name + "  id: " + self.id + " level: " + self.level

    
userList = []
userList.append(User("杰","oiDAl1huE6NdA8JAi8ENTtTguHc4",1))
userList.append(User("VH小叶紫檀","oiDAl1j4jGulYpErdh0umCwOenek",2))
    