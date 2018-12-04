# -*- coding: utf-8 -*-
# filename: db.py
import sqlite3
import chardet
import token as tk
#=========================================
#=============GLOBAL DEFINE===============
#=========================================
def toStr(content):
    if content == None:
        return ""
    return content.encode('utf-8')
def Xstr(content):
    res = []
    for v in content:
        res.append(toStr(v))
    return res
def toUni(content):
    return content.decode('utf-8')

user = dict()
msg = dict()
title = []
manager = dict()
default_list = ['key','answer','syntax','author','图片']

class USER:
    def __init__(self,uid,name,open_id,level,edit,address):
        self.uid = uid
        self.name = name
        self.open_id = open_id
        self.level = level
        self.can_edit = edit
        self.edit_address = address
    def copy_from(self,user):
        self.uid = user.uid
        self.name = user.name
        self.open_id = user.open_id
        self.level = user.level
        self.can_edit = user.can_edit
        self.edit_address = user.edit_address
    def toString(self):
        return self.name + "\n用户ID:" + self.uid + "\n等级:" + str(self.level) + "\n" + self.open_id

class MSG:
    def __init__(self,key,answer,price):
        self.key = key
        self.answer = answer
        self.price = price
        self.checkAnswer()
        
    def price_str(self):
        rmsg = ""
        for p in self.price:
            rmsg+= p + ","
        return rmsg
    def price_sql(self):
        rmsg = ""
        for p in self.price:
            rmsg+="\'"+p+"\',"
        return rmsg
        
    def checkAnswer(self):
        for t in title:
            if False == self.answer.has_key(t):
                self.answer[t] = ''
        for d in default_list:
            if False == self.answer.has_key(d):
                self.answer[d] = ''
    def copyFrom(self,omsg):
        self.key = omsg.key
        self.answer = omsg.answer
        self.price = omsg.price
#=========================================
#=============REFERENCE FUNC==============
#=========================================

def get_user(open_id):
    try:
        if user.has_key(open_id):
            return user.get(open_id)
        mDB = DB()
        new_user = mDB.getTargetUser(open_id)   
        if new_user.name != '未知用户':
            user.update({open_id:new_user})
            return user.get(open_id)
        nick_name = tk.get_userInfo(open_id)
        
        new_user = USER(9999,nick_name,open_id,0,0,0)
        if mDB.update_one_user(new_user):
            new_user = mDB.getTargetUser(open_id)
            user.update({open_id:new_user})
            mDB.close()
            return new_user
        else:
            mDB.close()
            return new_user
    except Exception as e:
        print e
        mDB.close()
        return USER(9999,"unknown user",open_id,0,0,0)

def get_msg(content):
    res = content.split('+')[0]
    return msg[res]
    
def login_verify(open_id):
    for v in manager.values():
        if v == open_id:
            return True
        else:
            return False

#=========================================
#=============DATA === BASE===============
#=========================================
class DB(object):
    def __init__(self):
        self.connect()
        
    def doNothing(self):
        return False
    def refresh(self):
        ul = self.getUser()
        user.clear()
        manager.clear()
        for u in ul:
            user[u.open_id] = u
            if u.level == 9:
                manager[u.name] = u.open_id
        self.getTableName()
        msg.clear()
        ml = self.getMsg()
        for m in ml:
            msg[m.key] = m
        
    def getMsg(self):
        sql = "SELECT "#key,answer"
        for d in default_list:
            sql += d+","
        for t in title:
            sql += t+","
        sql +="l0,l1,l2,l3,l4,l5,l6,l7,l8,l9 from msg"
        self.cs.execute(sql)
        msglist = []
        for row in self.cs:
            key = toStr(row[0])
            answer_dict = dict()
            price = Xstr(row[-10:])
            for a in range(1,len(default_list)):
                answer_dict[default_list[a]] = toStr(row[a])
            for i in range(len(title)):
                answer_dict[title[i]] = toStr(row[i+len(default_list)])
            msglist.append(MSG(key,answer_dict,price))
        return msglist
        
    def getUser(self): 
        self.cs.execute("SELECT id,name,open_id,level,edit,address from user")
        userlist = []
        for row in self.cs:
            userlist.append(USER(row[0],toStr(row[1]),toStr(row[2]),row[3],row[4],row[5]))
        return userlist
        
    def getTargetUser(self,open_id):
        try:
            sql = "SELECT id,name,level,edit,address from user WHERE open_id = \'" + open_id + '\''
            self.cs.execute(sql)
            res = self.cs.fetchone()
            return USER(res[0],toStr(res[1]),toStr(open_id),res[2],res[3],res[4])
        except Exception as res:
            print res
            return USER(9999,'未知用户',open_id,0,0,0)

    def update_one_user(self,user_info):
        try:
            sql = "replace into user(name,open_id,level,edit,address) values(\'" + user_info.name +"\',\'" + user_info.open_id + "\'," + str(user_info.level) + "," + str(user_info.can_edit) + "," + str(user_info.edit_address) + ")"
            self.cs.execute(sql)
            self.conn.commit()
            return True
        except Exception as res:
            print res
            return False
        
    def getTableName(self):
        try:
            sql = "pragma table_info (\'msg\')"
            self.cs.execute(sql)
            res = self.cs.fetchall()
            for i in range(len(title)):
                del title[0]
            for rt in res:
                r = toStr(rt[1])
                if 'l' in r or r in default_list or '预留' in r:
                    continue
                else:
                    title.append(r)
        except Exception as e:
            print e

    def getAnswer(self,content):
        try:
            ask = content.split('+')
            sql = "SELECT answer"
            for t in title:
                sql += t
            sql +=",l0,l1,l2,l3,l4,l5,l6,l7,l8,l9 from msg WHERE key = \'" + ask[0] + '\''
            self.cs.execute(sql)
            res = self.cs.fetchone()
            answer_dict = {'answer':toStr(res[0])}
            price = Xstr(res[-9:])
            for i,t in title:
                answer_dict[t] = toStr(res[i+1])
            return MSG(ask[0],answer_dict,price)
        except Exception as res:
            print res
            return res

    def updateAnswer(self,content):
        try :
            key = content.split('号')[0] + '号'
            if not msg.has_key(key):
                return 'nomember'
            sql = "update msg set answer = \'" + content + "\' where key = \'" + key + "\'"    
            self.cs.execute(sql)
            self.conn.commit()
            msg[key].answer['answer'] = content
            return 'success'
        except Exception as res:
            print res
            return res
    def updateImageInMsg(self,key,news_id):
        try:
            sql = "update msg set \'图片\' = \'"+news_id+"\' where key = \'" + key + "\'"
            self.cs.execute(sql)
            self.conn.commit()
        except Exception as res:
            print "updateImageInMsg ERR!!"
            print res

    def updateImage(self,key,news,images):
        try:
            img_id = ""
            img_url = ""
            for img in images:
                img_id+= img.media_id + ","
                img_url+=img.url + ","
            sql = "replace into IMG(key,img_id,img_url) values(\'"+key+"\',\'"+img_id+"\',\'"+umg_url+"\')"
            self.cs.execute(sql)
            self.updateImageInMsg(new_key,news)
        except Exception as res:
            print "updateImage ERR!!"
            print res

    def updateMsg(self,m_msg):
        try:
            key = m_msg.key
            sql = "replace into msg(key,answer,详情,l0,l1,l2,l3,l4,l5,l6,l7,l8,l9,syntax,author) values(\'"+key+"\',\'"+m_msg.answer['answer']+"\',\'"+m_msg.answer['详情']+"\',"+m_msg.price_sql()+"\'"+m_msg.answer['syntax']+"\',\'"+m_msg.answer['author']+"\')"
            #print sql
            self.cs.execute(sql)
            self.conn.commit()
            print 'success'
            msg.update({key:m_msg})
            return True
        except Exception as res:
            print "updateMsg Error!!"
            return res
            
    def close(self):
        self.conn.close()
    
    def connect(self):
        try:
            self.conn = sqlite3.connect('/home/smbuser/data/wood.db')
            self.cs = self.conn.cursor()
        except Exception as res:
            print res
