# -*- coding: utf-8 -*-
# filename: messageHandler.py

import csv
import time
import token as tk
import image
import db
import re

#==================================================
#============MANAGER COMMAND AREA==================
#==================================================
current_user = db.USER(9999,"None","None",0)
class CMD(object):
    def __init__(self,cmd,info,func):
        self.cmd = cmd
        self.info = info
        self.func = func

def cmd_update_msgInfo(content):
    mdb = db.DB()
    res = mdb.updateMsg(content)
    mdb.close()
    return res

def cmd_refresh(content):
    mDB = db.DB()
    mDB.refresh()
    img_list = image.uploadAllImages(current_user.open_id)
    mDB.close()
    lens = len(img_list)
    return "已刷新列表，建议获取用户列表来查看是否成功\n刷新到%d个新的图片文件夹，稍后进行上传" % lens

def cmd_getUser(content):
    cont = re.split(r'[+|,|，|.|。| |*]+',content)
    if len(cont) == 1:
        userInfo = "当前管理员用户总数" + str(len(db.user))
        for u in db.user.values():
            if u.level == 9:
                userInfo += "\n=====================\n" + u.open_id + "\n用户名:" + u.name
    else:
        open_id = cont[1]
        userInfo = open_id + "\n用户名:" + db.user[open_id].name + "\n等级" + str(db.user[open_id].level)
    return userInfo

def cmd_setAdmin(content):
    admin_id = content.split('客服')[1]
    admin_user = db.get_user(admin_id)
    if admin_user.level != 9:
        return "对方非管理员账户，请先将等级调整为9"
    tk.manager[0] = admin_id
    msg_send = "管理员：" + current_user.name + "已经将您设置为客服，所有未知信息都会通过公众号通知您"
    tk.sender(msg_send)
    return "已经成功设置客服为:" + admin_user.name

def cmd_setLevel(content):
    cont = re.split(r'[+|,|，|.|。| |*]+',content)
    if current_user.open_id != 'okPde1W62pEwb87C4yJU9RePe-cU':
        return "您不是数据库管理员，命令执行失败"
    mDB = db.DB()
    tUser = mDB.getTargetUser(cont[1])
    tUser.level = int(cont[2])
    mDB.update_one_user(tUser)
    mDB.close()
    return "已成功设置"+tUser.open_id+"用户名："+tUser.name+"\n等级为" + str(tUser.level)

command = [CMD('用户','用户：查询所有管理员用户\n用户，VH小叶紫檀，9：查询该用户',cmd_getUser),
           CMD('刷新','上传新文件以后，刷新数据使用',cmd_refresh),
           CMD('已出','可以将某个商品信息改为已出，注意：编号一定要放在前面！',cmd_update_msgInfo),
           CMD('设置客服',"可以将未知信息转发给客服\n格式： 设置客服open_id\nopen_id通过<用户>命令获得",cmd_setAdmin),
           CMD('修改等级','修改等级，VH小叶紫檀，9：\n设置该用户等级为9，仅数据库使用',cmd_setLevel)]
#==================================================
#============COMMON CALL FUNCTION==================
#==================================================

def loadMsg(open_id,content):
    if content == '自己id':
        return open_id
    user = db.get_user(open_id)
    if user.level == 9:
        try:
            target_user_name = user.name
            for cd in command:
                if cd.cmd in content:
                    print "管理员命令:" + content
                    current_user.name = user.name
                    current_user.open_id = user.open_id
                    cmdMsg = cd.func(content)
                    return cmdMsg
        except Exception as e:
            return e
    try :
        detail = re.split(r'[+|,|，|.|。| |*]+',content)#content.split('[+|,|，|.|。| |*]+')[1:]
        key_word = detail[0]
        detail = detail[1:]
        print detail
        msg = db.get_msg(key_word)       
        #detail = content.split('[\+|\,|\，|\.|\。| |\*]+')[1:]
        answer = msg.answer['answer'] + "\n价格是:" + msg.price[user.level]
        if len(detail) == 0:
            for t in db.title:
                answer += "\n=====================\n" + t + ":\n"
                answer += msg.answer[t]
        for d in detail:
            answer += "\n=====================\n" + d + "\n"
            if msg.answer.has_key(d):
                answer += msg.answer[d]
            else:
                answer += "关键词错误"  
    except Exception, Argument:
        try:
            if user.level == 9:
                answer = "未触发任何指令，您是管理员，是否想执行?"
                for c in command:
                    answer += "\n===================\n" + c.cmd + ":\n" + c.info
            else:
                print Argument
                print "未知问题"
                answer = content + "\n我没有理解你的问题，现在正将这条信息转发给客服"
                answer += "正确命令格式为：\n例：110号：查询所有信息 \n110号+图片：查询110号基本信息和图片，并确保您所查询的号数存在"
                msg_f = user.name + "问您:\n" + content
                if user.uid == 9999:
                    msg_f += "\n该用户未成功放入数据库，请注意"
                tk.sender(msg_f,None)
        except Exception as e:
            print e
            answer = e
    return answer
