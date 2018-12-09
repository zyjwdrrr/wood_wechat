# -*- coding: utf-8 -*-
# filename: messageHandler.py

import csv
import time
import threading
import token as tk
import image
import db
import re
import express as ep
from log import *


#==================================================
#============USER DEFINATIONS AREA=================
#==================================================

check_list = ['金星','1.8','镇','笔筒','1.5','2.0','把件','时来运转','1.2','1.0','0.8','瘤疤','水波','鱼鳞','龙鳞','火焰','泥料']   #关键词搜索
max_search_items = 1000     #最大搜索范围（从新到旧）
max_return_item = 8         #返回结果个数

#=========L1,L6,L7,L8 ==========<100,<200,<311,<401,<501
#============================L1  <100,<200,<300,<500,<800
stage = [[0,30,15,15],
         [-10,50,40,30],
         [-20,80,60,40],
         [-30,110,80,60],
         [-50,150,100,80]]
def calPriceIndex(price):
    if price < 100:
        return 0
    elif price < 200:
        return 1
    elif price < 300:
        return 2
    elif price < 500:
        return 3
    elif price < 800:
        return 4
    else:
        return 5
def calPrimeIndex(prime):
    if prime < 70:
        return 0
    elif prime < 200:
        return 1
    elif prime < 311:
        return 2
    elif prime < 401:
        return 3
    elif prime < 501:
        return 4
    elif prime < 1000:
        return 5
    else:
        return 6
def calcPrice(price,prime):
    rp = list()
    price_index = calPriceIndex(price)
    prime_index = calPrimeIndex(prime)
    if price == 0:
        for i in range(6):
            rp.append('询问客服')
    else:
        rp.append(str(price)) #L0
        if price_index == 5:
            price1 = int(price * 0.95)
            rp.append(str(price1))#1
        else:
            price1 = int(price + stage[price_index][0])
            rp.append(str(price)) #L1
        price2 = int(price1 * 0.99)
        price3 = int(price2 * 0.99)
        price4 = int(price3 * 0.98)
        price5 = int(price4 * 0.97)
        rp.append(str(price2))
        rp.append(str(price3))
        rp.append(str(price4))
        rp.append(str(price5))
    if prime_index < 5:
        prime6 = int(prime + stage[prime_index][1])
        prime7 = int(prime + stage[prime_index][2])
        prime8 = int(prime + stage[prime_index][3])
    elif prime_index ==5:
        prime6 = int(prime*1.15 + 80)
        prime7 = int(prime*1.15 + 50)
        prime8 = int(prime*1.15 + 30)
    else:
        prime6 = int(prime*1.1 + 150)
        prime7 = int(prime*1.1 + 120)
        prime8 = int(prime*1.08 + 100)
    rp.append(str(prime6))
    rp.append(str(prime7))
    rp.append(str(prime8))
    rp.append(str(prime)) #L9
    return rp
#==================================================
#============MANAGER COMMAND AREA==================
#==================================================
current_user = db.USER(9999,"None","None",0,0,0)
class CMD(object):
    def __init__(self,cmd,info,func,perm):
        self.cmd = cmd
        self.info = info
        self.func = func
        self.perm = perm

def cmd_update_msgInfo(content,user):
    mdb = db.DB()
    cont = re.split(r'[+|,|，|.|。| |*]+',content)
    errlist = ""
    success_cnt = 0
    not_in_list = ""
    not_in_list_cnt = 0
    for c in cont:
        ret = mdb.updateAnswer(c)
        if ret == 'success':
            success_cnt += 1
        elif ret == 'nomember':
            not_in_list += c
            not_in_list_cnt += 1
        else:
            errlist+= c + ": " + ret
    mdb.close()
    res = '成功更新'+str(success_cnt)+'个已出商品\n'
    tk.send_to_manager("%s %s\n%s"%(user.name,res,content))
    if not_in_list_cnt != 0:
        res += "数据库中未查询到的商品有"+str(not_in_list_cnt)+"个:\n" + not_in_list
    if errlist != '':
        res += "更新失败:\n" + errlist
    return res

def cmd_refresh(content,user):
    mDB = db.DB()
    try:
        mDB.refresh()
        mDB.close()
        append_str = ""
        if '图片' in content:
            append_str = "\n=====================\n"
            img_list = image.uploadAllImages(user.open_id)
            lens = len(img_list)
            if lens > 0:
                append_str = "刷新到%d个新的图片文件夹，稍后进行上传" % lens
            append_str += image.getNewsList(user.open_id)
        return "已刷新列表，建议获取用户列表来查看是否成功" + append_str
    except Exception as res:
        print res
        log_.warning("刷新错误消息：%s" % res)
        return res
    finally:
        mDB.close()

def cmd_getUser(content,user):
    cont = re.split(r'[+|,|，|.|。| |*]+',content)
    if len(cont) == 1:
        userInfo = "当前管理员用户总数" + str(len(db.user))
        for u in db.user.values():
            if u.level == 9:
                userInfo += "\n=====================\n" + u.open_id + "\n用户名:" + u.name
    else:
        open_id = cont[1]
        user = db.get_user(open_id)
        userInfo = open_id + "\n用户名:" + user.name + "\n等级" + str(user.level)
        print userInfo
    return userInfo

def cmd_setAdmin(content,user):
    admin_id = content.split('客服')[1]
    admin_user = db.get_user(admin_id)
    if admin_user.level != 9:
        return "对方等级只有%d，请先将等级调整为9"%admin_user.level
    tk.manager.copy_from(admin_user)
    msg_send = "管理员：" + user.name + "已经将您设置为客服，所有未知信息都会通过公众号通知您"
    tk.sender(msg_send)
    return "已经成功设置客服为:" + admin_user.name

def cmd_setLevel(content,user):
    cont = re.split(r'[+|,|，|.|。| |*]+',content)
    if user.open_id != 'okPde1eyCobLENIrPIzXMvtA4yxM' :
        return "您不是数据库管理员，命令执行失败"
    mDB = db.DB()
    tUser = db.get_user(cont[1])
    tUser.level = int(cont[2])
    mDB.update_one_user(tUser)
    mDB.close()
    return "已成功设置"+tUser.open_id+"用户名："+tUser.name+"\n等级为" + str(tUser.level)

def cmd_add_new(content,user):
    key = content.split('【')[1].split('号')[0]
    author = user.name + "," + user.open_id
    answer = dict()
    group = 'V'
    title = ''
    info_r = ''
    if key.isdigit():
        key += '号'
    elif key[1:].isdigit():
        group = key[0]
        key = key[1:]
    else:
        return "你自己看我解析出了个啥。。" + key
    info = content.split('%')[0].split('#')[0]
    title = key + '待售'
    if '【0号' in content:
        info = info.strip('0号')
        title = '重磅大货！！'
        
    try:
        answer['详情'] = info
        answer['answer'] = title
        answer['syntax'] = group
        answer['author'] = author
        info_r = '找不到价钱分隔符符号#'
        #price_info = content.split('💰')[1]
        #cont = re.split(r'[#|￥|~]+',content)
        price_info = content.split('#')[1]
        print price_info
        info_r = '计算价格失败'
        price_all = calcPrice(int(price_info.split('%')[0]),int(price_info.split('%')[1]))
        info_r = '信息初始化失败'
        m_msg = db.MSG(key,answer,price_all)
        mDB = db.DB()
        info_r = '数据库更新失败'
        result = mDB.updateMsg(m_msg)
        mDB.close()
        if False == result:
            return result
        rmsg = "key:" + key + "\n价格:"
        rmsg += m_msg.price_str()
        rmsg += "详情:" + info
        return rmsg   
    except Exception as res:
        log_.warning("新增商品错误消息：%s ,错误状态 %s" % (res,info_r))
        return info_r

def cmd_edit_goods(content,user):
    info = re.split(r'[+|,|，|.|。| |*]+',content)
    key = info[0].split('修改')[1].split('号')[0] + '号'
    lens = (len(info) - 1)/2
    m_msg = db.MSG(key,dict(),[0]*10)
    if db.msg.has_key(key):
        m_msg.copyFrom(db.msg[key])
    else:
        return "找不到关键字:%s" % key
    for i in range(lens):
        index = i*2+1
        k = info[index]
        v = info[index+1]
        if 'l' in k:
            i = int(k.split('l')[1])
            m_msg.price[i] = v
        elif m_msg.answer.has_key(k):
            m_msg.answer[k] = v
            print k + ": " + v
        else:
            return "找不到元素:%s"%k
    mDB = db.DB()
    result = mDB.updateMsg(m_msg)
    mDB.close()
    return "已经修改:%s"%key
def cmd_edit_express(content,user):
    return ep.gen_random_access(user)
def get_perm(content):
    if 'level' in content:
        minLev = int(content.split('level')[1])
        return lambda user:user.level >= minLev
    if 'edit' in content:
        return lambda user:user.can_edit
    if 'address' in content:
        return lambda user:user.edit_address
    return lambda user:0

command = [CMD('用户','用户：查询所有管理员用户\n用户，VH小叶紫檀：查询该用户',cmd_getUser,get_perm('level9')),
           CMD('刷新','上传新文件以后，刷新数据使用',cmd_refresh,get_perm('level9')),
           CMD('修改','修改数据，格式为 修改XXX号,answer,还在,l1,100',cmd_edit_goods,get_perm('edit')),
           CMD('已出','可以将某个商品信息改为已出，注意：编号一定要放在前面！',cmd_update_msgInfo,get_perm('level7')),
           CMD('预留','可以将某个商品信息改为预留，注意：编号一定要放在前面！',cmd_update_msgInfo,get_perm('level7')),
           CMD('设置客服',"可以将未知信息转发给客服\n格式： 设置客服open_id\nopen_id通过<用户>命令获得",cmd_setAdmin,get_perm('level9')),
           CMD('更改等级','更改等级，VH小叶紫檀，9：\n设置该用户等级为9，仅数据库使用',cmd_setLevel,get_perm('level9')),
           CMD('【','新增数据，格式为【key】info...[金袋]售价%成本',cmd_add_new,get_perm('edit')),          
           CMD('快递','新增快递单',cmd_edit_express,get_perm('level7'))]
#==================================================
#============COMMON CALL FUNCTION==================
#==================================================

def search_for_key(user,content):
    keys = sorted(db.msg.keys(),key = lambda k:int(k.strip('号')),reverse=True)[:max_search_items]    
    res_cnt = 0
    ret = ""
    for k in keys:
        info = db.msg[k].answer['详情']
        answer = db.msg[k].answer['answer']
        if content in info and '已出' not in answer:
            ret+=k
            res_cnt += 1
            if res_cnt >= max_return_item:
                return "找到了8个匹配项：\n"+ret
            else:
                ret+="\n"
    if res_cnt == 0:
        tk.send_to_manager("%s咨询您关键词（%s）未搜索到任何结果，请确认是否搜索范围过窄或是都已出售"%(user.name,content))
        return "没找到匹配项"
    else:
        return "找到了%d个匹配项：\n%s"%(res_cnt,ret)
    
def loadMsg(open_id,content):
    user = db.get_user(open_id)
    log_.info("处理消息：%s，用户：%s" % (content,user.name))
    if content == '查询自己':
        return open_id
    if user.level >= 1:
        try:
            if content == 'help':
                answer = "管理员命令:"
                for c in command:
                    answer += "\n===================\n" + c.cmd + ":\n" + c.info
                logVip(user.name,content,answer)
                return answer
            target_user_name = user.name
            for cd in command:
                if cd.cmd in content:
                    if cd.perm(user) == 0:
                        tk.send_to_manager("%s尝试使用管理员命令失败\n%s"%(user.name,content))
                        return "尝试使用管理员命令失败，请先联系客服获取权限"
                    print "管理员命令:" + content
                    current_user.name = user.name
                    current_user.open_id = user.open_id
                    cmdMsg = cd.func(content,user)
                    logVip(user.name,content,cmdMsg)
                    return cmdMsg
        except Exception as e:
            return e + "\nload msg error!"
    try :
        if content in check_list:
            return search_for_key(user,content)
        detail = re.split(r'[+|,|，|.|。| |*]+',content)#content.split('[+|,|，|.|。| |*]+')[1:]
        key_word = detail[0]
        if '号' not in key_word:
            key_word += '号'
        detail = detail[1:]
        msg = db.get_msg(key_word)       
        #detail = content.split('[\+|\,|\，|\.|\。| |\*]+')[1:]
        answer = msg.answer['answer'] + "\n"
        #if user.level > 0:
        #    answer += "您是尊贵的L" + str(user.level)+ "用户，"
        answer += "价格是:"
        if user.level == 9:
            for p in msg.price:
                answer += p + ","
        elif msg.price[user.level] == '0':
            answer += '未知，请询问客服'
        else:
            answer += msg.price[user.level]
        if len(detail) == 0:
            answer += "\n=====================\n图片:\n"
            if msg.answer['图片'] == '':
                print msg.answer['图片']
                answer += '管理员暂时未上传图片，请联系客服获取图片'
            else:
                answer += '图片将在1s后发送给您'
                timer = threading.Timer(1,tk.send_media,args=(msg.answer['图片'],open_id))
                timer.start()
            for t in db.title:
                answer += "\n=====================\n" + t + ":\n"
                answer += msg.answer[t]
        for d in detail:
            answer += "\n=====================\n" + d + "\n"
            if msg.answer.has_key(d):
                if t != '图片':
                    answer += msg.answer[t]
                elif msg.answer['图片'] == '':
                    answer += '管理员暂时未上传图片，请联系客服获取图片'
                else:
                    answer += '图片将在1s后发送给您'
                    timer = threading.Timer(1,tk.send_media)
                    timer.start()
            else:
                answer += "关键词错误"  
    except Exception as Argument:
        try:
            print Argument
            if user.level == 9:
                answer = "未触发任何指令，您是管理员，是否想执行管理员命令？获取指令信息回复help"
                answer += "正确命令格式为：\n例：110号：查询所有信息 \n110号+图片：查询110号基本信息和图片，并确保您所查询的号数存在"
            else:
                print Argument
                print "未知问题"
                answer = content + "\n我没有理解你的问题，现在正将这条信息转发给客服"
                answer += "正确命令格式为：\n例：110号：查询所有信息 \n110号+图片：查询110号基本信息和图片，并确保您所查询的号数存在"
                msg_f = user.name + "问您:\n" + content
                if user.uid == 9999:
                    msg_f += "\n该用户未成功放入数据库，请注意"
                tk.send_to_manager(msg_f)
            answer += "\n=======================\n"
            answer += "或是直接回复搜索指令关键词:"
            for l in check_list:
                answer += "[%s]"%l
        except Exception as e:
            print e
            log_.warning("消息处理错误：%s" % e)
            answer = e
    logVip(user.name,content,answer)
    return answer
