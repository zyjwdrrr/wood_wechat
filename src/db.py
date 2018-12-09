# -*- coding: utf-8 -*-
# filename: db.py
import sqlite3
import chardet
import token as tk
from log import log_
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
agents = dict()
default_list = ['key','answer','syntax','author','图片']

class AGENT:
    def __init__(self,sname,name,code):
        self.sname=sname
        self.name=name
        self.code=code

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
            rmsg+="'%s',"%str(p)
        return rmsg[:-1]
        
    def checkAnswer(self):
        for t in title:
            if False == self.answer.has_key(t):
                self.answer[t] = ''
        for d in default_list:
            if False == self.answer.has_key(d):
                self.answer[d] = ''
    def copyFrom(self,omsg):
        self.key = omsg.key
        for (k,a) in omsg.answer.items():
            self.answer[k] = a
        for i,p in enumerate(omsg.price):
            self.price[i] = str(p)
        #self.answer = omsg.answer
        #self.price = omsg.price
#=========================================
#=============REFERENCE FUNC==============
#=========================================

def get_user(open_id):
    if user.has_key(open_id):
        return user.get(open_id)
    try:   
        mDB = DB()
        new_user = mDB.getTargetUser(open_id)
        if new_user.name != '未知用户':
            user.update({open_id:new_user})
            mDB.refresh()
            return user.get(open_id)
        nick_name = tk.get_userInfo(open_id)
        new_user = USER(9999,nick_name,open_id,0,0,0)
        if mDB.update_one_user(new_user):
            new_user = mDB.getTargetUser(open_id)
            user.update({open_id:new_user})
            return new_user
        else:
            return new_user
    except Exception as e:
        print e
        log_.warning("获取用户信息失败:" + open_id)
        return USER(9999,"未知用户",open_id,0,0,0)
    finally:
        mDB.close()
        

def get_msg(content):
    res = content.split('+')[0]
    print res
    if msg.has_key(res):
        return msg[res]
    try:
        mDB = DB()
        mmsg = mDB.getAnswer(res)
        if mmsg != None:
            mDB.refresh()
            return msg[res]
    except Exception as err:
        print err
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
        log_.info("连接数据库")
        self.connect()
        
    def doNothing(self):
        return False

    def refresh(self):
        log_.info("刷新列表")
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
        ag = self.getAgent()
        for a in ag:
            agents[a.code] = a
        
    def getMsg(self):
        log_.info("获取消息列表")
        sql = "SELECT "
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
        log_.info("获取用户列表")
        self.cs.execute("SELECT id,name,open_id,level,edit,address from user")
        userlist = []
        for row in self.cs:
            userlist.append(USER(row[0],toStr(row[1]),toStr(row[2]),row[3],row[4],row[5]))
        return userlist

    def getAgent(self):
        log_.info("获取代理列表")
        self.cs.execute("SELECT sname,name,code from agent")
        agent_list = []
        for row in self.cs:
            agent_list.append(AGENT(toStr(row[0]),toStr(row[1]),row[2]))
        return agent_list
        
    def getTargetUser(self,open_id):
        try:
            log_.info("获取目标用户,open_id = " + open_id)
            sql = "SELECT id,name,level,edit,address from user WHERE open_id = \'" + open_id + '\''
            self.cs.execute(sql)
            res = self.cs.fetchone()
            user = USER(res[0],toStr(res[1]),toStr(open_id),res[2],res[3],res[4])
            return user
        except Exception as res:
            print res
            log_.warning("获取用户失败")
            return USER(9999,'未知用户',open_id,0,0,0)

    def update_one_user(self,user_info):
        try:
            log_.info("更新一个用户: name: %s open_id: %s level %d edit %d address %d"%(user_info.name,user_info.open_id,user_info.level,user_info.can_edit,user_info.edit_address))
            sql = "replace into user(name,open_id,level,edit,address) values(\'" + user_info.name +"\',\'" + user_info.open_id + "\'," + str(user_info.level) + "," + str(user_info.can_edit) + "," + str(user_info.edit_address) + ")"
            self.cs.execute(sql)
            self.conn.commit()
            return True
        except Exception as res:
            print res
            log_.warning("更新用户失败：" + res)
            return False
        
    def getTableName(self):
        try:
            log_.info("获取目录结构")
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
            log_.critical("目录获取失败：" + e)

    def getAnswer(self,content):
        try:
            log_.info("获取回答")
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
            log_.warning("回答获取失败：" + res)
            return res

    def updateAnswer(self,content):
        try :
            log_.info("更新回答")
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
            log_.warning("更新回答失败：" + res)
            return res
        
    def updateImageInMsg(self,key,news_id):
        try:
            sql = "update msg set \'图片\' = \'"+news_id+"\' where key = \'" + key + "\'"
            self.cs.execute(sql)    
        except Exception as res:
            print "updateImageInMsg ERR!!"
            log_.warning("升级图片信息失败：" + res)
            print res

    def updateFewImage(self,news):
        try:
            for (key,media_id) in news.items():
                self.updateImageInMsg(key,media_id)
            self.conn.commit()
            return True
        except Exception as res:
            print "updateFewImage ERR!!"
            print res
            log_.warning("升级多个图片失败：" + res)
            return False
    
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
            self.conn.commit()
        except Exception as res:
            print "updateImage ERR!!"
            log_.warning("更新图片失败：" + res)
            print res

    def updateMsg(self,m_msg):
        try:
            key = m_msg.key
            #sql = "replace into msg(key,answer,详情,l0,l1,l2,l3,l4,l5,l6,l7,l8,l9,syntax,author) values(\'"+key+"\',\'"+m_msg.answer['answer']+"\',\'"+m_msg.answer['详情']+"\',"+m_msg.price_sql()+"\'"+m_msg.answer['syntax']+"\',\'"+m_msg.answer['author']+"\')"
            #print sql
            d_l = ""
            d_v = ""
            l_l = ""
            l_v = ""
            for d in default_list[1:]:
                d_l += "%s,"%d
                d_v += "'%s',"%m_msg.answer[d]
            for l in title:
                l_l += "%s,"%l
                l_v += "'%s',"%m_msg.answer[l]   
            sql = "replace into msg(key,%s%sl0,l1,l2,l3,l4,l5,l6,l7,l8,l9) values('%s',%s%s%s)"%(d_l,l_l,m_msg.key,d_v,l_v,m_msg.price_sql())
            print sql
            self.cs.execute(sql)
            self.conn.commit()
            print 'success'
            msg.update({key:m_msg})
            return True
        except Exception as res:
            print "updateMsg Error!!"
            print res
            log_.warning("更新消息失败：" + res)
            return res
            
    def close(self):
        log_.info("数据库成功关闭")
        self.conn.close()
    
    def connect(self):
        try:
            self.conn = sqlite3.connect('/home/smbuser/data/wood.db')
            self.cs = self.conn.cursor()
        except Exception as res:
            print res
