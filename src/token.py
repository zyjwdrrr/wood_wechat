# -*- coding: utf-8 -*-

import requests
import json
import threading
import config
from db import USER
from log import log_

manager = USER(9999,'None','okPde1eyCobLENIrPIzXMvtA4yxM',0,0,0)

def usersto(users = None):
    print users
    if users == None:
        return [manager.open_id]
    else:
        if isinstance(users,list):
            return users
        else:
            log_.warning("必须传入一个列表")
            print "'users' must be a list!"
            return

def json_post_data_generator(content='我也不知道为啥我要发这个，可能是有弱智程序自动执行了',users = None):
    msg_content = {}
    msg_content['content'] = content
    post_data = {}
    post_data['text'] = msg_content
    post_data['touser'] = "%s" % users
    post_data['toparty'] = ''
    post_data['msgtype'] = 'text'
    post_data['agentid'] = '9'
    post_data['safe'] = '0'
    return json.dumps(post_data,False,False)

def get_token_info():
    APPInfo = (config.wechat['appid'],config.wechat['appsecret'])
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % APPInfo)
    js =  r.json()
    if "errcode" not in js:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
    else:
        print "Can not get the access_token"
        print js
        log_.critical("获取access_token失败，%s"%js)
        quit()
    return access_token,expires_in

post_url_freshing = ['']
get_url_token = ['']

def post_url():
    access_token,expires_in = get_token_info()
    print "token expires_in:%s" % expires_in
    timer = threading.Timer((expires_in-200),post_url)
    timer.start()
    get_url_token[0] = "%s"%access_token.encode('utf-8')
    print access_token
    post_url_freshing[0] = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' %access_token
    log_.info("刷新token成功，%s"%post_url_freshing[0])
    log_.info("刷新token:%s"%get_url_token[0])

def get_userInfo(open_id):
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token="+get_url_token[0]+"&openid="+open_id+"&lang=zh_CN"
    log_.info("尝试获取用户信息：" + open_id)
    log_.info("url: " + url)
    res = requests.get(url)
    js =  res.json()
    if "errmsg" not in js:
        return js[u"nickname"].encode('utf-8')
    else:
        print "Can not get user information"
        print js
        log_.error("获取用户信息失败，%s"%js)
        print "use token: " + get_url_token[0]
        return "未知用户"
    
def sender(text_str,user_lis = None):
    posturl = post_url_freshing[0]
    users = usersto(user_lis)
    for u in users:
        post_data = json_post_data_generator(content=text_str,users = u)
        r = requests.post(posturl,data=post_data)
        result = r.json()
        if result["errcode"] == 0:
            print "Sent %s to %s successfully" % (text_str,u)
        else:
            print "send to user failed!!!"
            print posturl
            print result["errmsg"]
            log_.error("发送信息失败，%s, url: %s"%(result["errmsg"].encode('utf-8'),posturl))
        
def send_to_manager(text_str):
    user_list = [manager.open_id,'okPde1ZW2Pm2hXVITZkJoCyH-gEY']
    sender(text_str,user_list)
 
def send_media(media_id,toUser):
    posturl = post_url_freshing[0]
    m_id = {}
    m_id['media_id'] = media_id
    m_data = {}
    m_data['mpnews'] = m_id
    m_data['touser'] = "%s" % toUser
    m_data['msgtype'] = 'mpnews'
    post_data = json.dumps(m_data,False,False)
    r = requests.post(posturl,data=post_data)
    result = r.json()
    if result["errcode"] == 0:
        print "Sent successfully"
    else:
        print result["errmsg"]
        log_.error("发送图片失败，%s"%result["errmsg"].encode('utf-8'))
