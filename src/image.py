# -*- coding: utf-8 -*-
# filename: image.py

import os
import db
import threading
import urllib2
import token as tk
import poster.encode
from meterial import Material
from poster.streaminghttp import register_openers

#import token as tk
path_base = '/home/smbuser/data/'

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
