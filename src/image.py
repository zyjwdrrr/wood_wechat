# -*- coding: utf-8 -*-
# filename: image.py

import os
import db
import threading
import urllib2
import token as tk
import poster.encode
import json
import config as cfg
from meterial import Material
from poster.streaminghttp import register_openers
from log import log_

#import token as tk
path_base = '/home/smbuser/data/Image/'

def toStr(content):
    return content.encode('utf-8') 

def getFolderList(root_path):
    for root,dirs,files in os.walk(root_path):
        return dirs

def getFileList(root_path):
    for root,dirs,files in os.walk(root_path):
        return files

def uploadAllImages(open_id):
    folder_list =  getFolderList(path_base)
    thread = threading.Thread(target=uploadData,args=(folder_list,open_id))
    thread.start()
    return folder_list

def getNewsList(open_id):
    getUrl = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s" % tk.get_url_token[0]
    print getUrl
    result = urllib2.urlopen(urllib2.Request(getUrl))
    res = json.loads(result.read())
    if 'errcode' not in res:
        total = int(res['news_count'])
        offset = int(cfg.wechat['last_news_id'])
        cnt = total - offset
        ret = "本地有素材%d个，服务器有素材%d个" % (offset,total)
        if cnt > 0:
            thread = threading.Thread(target=getAllNews,args=(open_id,cnt))
            thread.start()
            return ret + ",检测到%d个新素材" % cnt
        return ret + ",未检测到新素材"
    else:
        error = toStr(res['errmsg'])
        tk.sender(error,[open_id])
        log_.warning("服务器返回错误消息：" + error)
        return ""

def process_news(res):
    outStr = ""
    failed_str = ""
    image = dict()
    for r in res:
        media_id = toStr(r['media_id'])
        title = toStr(r['content']['news_item'][0]['title'])
        key = title.split('号')[0] + '号'
        key = key.strip().strip('【')
        if db.msg.has_key(key):
            outStr += "\n\"%s\",\"%s\""%(title,media_id)
            image[key] = media_id
        else:
            failed_str += "\n\"%s\",\"%s\""%(title,media_id)
    mDB = db.DB()
    ret = mDB.updateFewImage(image)
    mDB.close()
    with open(path_base+"success.csv",'a+') as f:
        f.write(outStr)
        f.close()
    if failed_str != "":
        with open(path_base+"failed.csv",'a+') as f:
            f.write(failed_str)
            f.close()
    return ret


def getAllNews(open_id,cnt):
    total_remained = cnt
    checked = 0
    while total_remained > 0:
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % tk.get_url_token[0]
        detail =(
        {
            "type":"news",
            "offset":"0",
            "count":"20"
        })
        offset = int(cfg.wechat['last_news_id'])
        detail['offset'] = offset
        check_cnt = 20
        if total_remained < 20:
            detail['count'] = total_remained
            check_cnt = total_remained
        print "start %d count %d"%(offset,total_remained)
        checked += int(detail['count'])
        urlResp = urllib2.urlopen(postUrl, json.dumps(detail,ensure_ascii=False))
        response = urlResp.read()
        res = json.loads(response)
        if 'errcode' not in res:
            if False == process_news(res['item']):
                return False
            cfg.updateValue('last_news_id',offset + check_cnt)
            total_remained -= 20
        else:
            tk.sender("已经成功更新了%d个素材,更新新素材时失败了\n"%(checked,toStr(res['errmsg'])),[open_id])
            return False
    tk.sender("成功更新了%d个素材"%checked,[open_id])
 

def removeDir(path):
    files = getFileList(path)
    files.sort()
    for mfile in files:
        file_path = path + "/" + mfile
        os.remove(file_path)
    os.rmdir(path)

def delAllImg(mr,image_list,open_id):
    for image in image_list:
        errcode = mr.delete(tk.get_url_token[0],image.media_id)
        if errcode != '0':
            tk.sender(image.url + "这张图片删除失败了，错误信息是："+errcode,[open_id])
            

def uploadData(folder_list,open_id):
    try:
        mr = Material()
        for folder in folder_list:
            path = path_base + folder
            files = getFileList(path)
            files.sort()
            image_list = []
            for i,mfile in enumerate(files):
                file_path = path + "/" + mfile
                file_name = folder + "_" + str(i) + ".jpg"
                media_id,url = mr.uplaod(tk.get_url_token[0],file_path,'image',file_name)
                if media_id != False:
                    image_list.append(IMAGE(media_id,url))
                else:
                    print url
                    delAllImg(mr,image_list,open_id)
                    tk.sender(url,[open_id])
                    return False
            msg_info = db.msg[folder+'号'].answer['详情']
            pic_list = []
            for image in image_list:
                pic_list.append(image.url)
            title = msg_info.split("规格")[0]
            success,media_id = mr.add_news(tk.get_url_token[0], title, msg_info, image_list[0].media_id, pic_list)
            if success:
                print media_id
                mDB = db.DB()
                mDB.updateImage(folder+'号',media_id,image_list)
                tk.send_media(media_id,open_id)
                removeDir(path)                
            else:
                delAllImg(mr,image_list,open_id)
                print media_id
                tk.sender(media_id,[open_id])
    except Exception as e:
        delAllImg(mr,image_list,open_id)
        tk.sender(e,[open_id])
        print e
  
class IMAGE(object):
    def __init__(self,media_id,url):
        self.media_id = media_id
        self.url = url             
