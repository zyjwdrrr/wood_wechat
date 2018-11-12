# -*- coding: utf-8 -*-

import requests
import json
import threading

manager = ['oiDAl1j4jGulYpErdh0umCwOenek']

def usersto(users = None):
    if users == None:
        return manager[0]
    else:
        if isinstance(users,list):
            usersinfo = []
            for user in users:
                usersinfo.append(user)
            return ','.join(set(usersinfo))
        else:
            print "'users' must be a list!"
            return

def json_post_data_generator(content='我也不知道为啥我要发这个，可能是有弱智程序自动执行了',users = None):
    msg_content = {}
    msg_content['content'] = content
    post_data = {}
    post_data['text'] = msg_content
    post_data['touser'] = "%s" % usersto(users)
    post_data['toparty'] = ''
    post_data['msgtype'] = 'text'
    post_data['agentid'] = '9'
    post_data['safe'] = '0'
    return json.dumps(post_data,False,False)

def appInfos():
    APPID = "wxba82ef4565733356"
    APPSECRET = "83a7ad72ef125f72a8d0fb31183eca8d"
    return (APPID,APPSECRET)

def get_token_info():
    APPInfo = appInfos()
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % APPInfo)
    #print "Accessing %s" %r.url
    js =  r.json()
    if "errcode" not in js:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
    else:
        print "Can not get the access_token"
        print js
        quit()
    return access_token,expires_in

post_url_freshing = ['']

def post_url():
    access_token,expires_in = get_token_info()
    print "token expires_in:%s" % expires_in
    timer = threading.Timer((expires_in-200),post_url)
    timer.start()
    post_url_freshing[0] = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' %access_token

def sender(text_str,user_lis = None):
    posturl = post_url_freshing[0]
    post_data = json_post_data_generator(content=text_str,users = user_lis)
    r = requests.post(posturl,data=post_data)
    result = r.json()
    if result["errcode"] == 0:
        print "Sent successfully"
    else:
        print result["errmsg"]
