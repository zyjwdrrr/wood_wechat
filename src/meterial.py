# -*- coding: utf-8 -*-
# filename: material.py
import urllib2
import json
import os
import poster.encode
from PIL import Image
from poster.streaminghttp import register_openers

import chardet

def getFileSize(file_path):
    fsize = os.path.getsize(file_path)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)
    
def resizeImage(file_path):
    img = Image.open(file_path)
    w,h = img.size
    img.resize((w/2,h/2)).save(file_path,"JPEG")

def rename(file_path,file_name):
    img = Image.open(file_path)
    img.save(file_name,"JPEG")

def toStr(content):
    return content.encode('utf-8') 

class Material(object):
    def __init__(self):
        register_openers()
        
    #upload image
    def uplaod(self, accessToken, filePath, mediaType,file_name):
        while getFileSize(filePath) > 2:
            resizeImage(filePath)
        rename(filePath,file_name)
        openFile = open(file_name, "rb")
        fileName = file_name
        print fileName
        param = {'media': openFile, 'filename': fileName}
        #param = {'media': openFile}
        postData, postHeaders = poster.encode.multipart_encode(param)
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        response = urlResp.read()
        res = json.loads(response)
        openFile.close()
        os.remove(file_name)
        if 'errcode' not in res:           
            return toStr(res["media_id"]),toStr(res["url"])
        else:
            print res
            return False,toStr(res['errmsg'])    

    def add_news(self, accessToken, title, detail, thumb, pic_list):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s" % accessToken
        news =(
        {
            "articles":
            [
                {
                "title":"test",
                "thumb_media_id":"",
                "author":"robot",
                "digest":"",
                "show_cover_pic":0,
                "content":"<p>",
                "content_source_url":"",
                }
            ]
        })
        news['articles'][0]['title'] = title
        news['articles'][0]['thumb_media_id'] = thumb
        content = "<p>%s<br  />"%detail
        for pic_url in pic_list:
            content += "<p><img src=\"%s\" alt=\"\" data-width=\"null\" data-ratio=\"NaN\"><br  />"%pic_url
        news['articles'][0]['content'] = content
        urlResp = urllib2.urlopen(postUrl, json.dumps(news,ensure_ascii=False))
        response = urlResp.read()
        res = json.loads(response)
        if 'errcode' not in res:
            return True,toStr(res["media_id"])
        else:
            print res
            return False,toStr(res['errmsg'])
        
    #download image
    def get(self, accessToken, mediaId,file_path):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print jsonDict
        else:
            buffer = urlResp.read()  # 素材的二进制
            mediaFile = file("test_media.jpg", "wb")
            mediaFile.write(buffer)
            print "get successful"
    #delete one meterial
    def delete(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        response = urlResp.read()
        res = json.loads(response)
        return toStr(res["errcode"])

    #get meterial list
    def batch_get(self, accessToken, mediaType, offset=0, count=20):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/material"
               "/batchget_material?access_token=%s" % accessToken)
        postData = ("{ \"type\": \"%s\", \"offset\": %d, \"count\": %d }"
                    % (mediaType, offset, count))
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()
