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
path_base = '/home/ftp/data/'

def getFolderList(root_path):
    for root,dirs,files in os.walk(root_path):
        return dirs

def getFileList(root_path):
    for root,dirs,files in os.walk(root_path):
        return files

def uploadAllImages(open_id):
    path = '/home/ftp/data/'
    folder_list =  getFolderList(path)
    thread = threading.Thread(target=uploadData,args=(folder_list,open_id))
    thread.start()
    return folder_list
     
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
                    print url
                    image_list.append(IMAGE(media_id,url))
                else:
                    print url
                    tk.sender(url,[open_id])
                    return False
            msg_info = db.msg[folder+'号']
            pic_list = []
            for image in image_list:
                pic_list.append(image.url)
            medai_id = mr.add_news(tk.get_url_token, msg_info, msg_info, image_list[0].media_id, pic_list)
            tk.send_media(medai_id,open_id)
    except Exception as e:
        print e
  
class IMAGE(object):
    def __init__(self,media_id,url):
        self.media_id = media_id
        self.url = url             
