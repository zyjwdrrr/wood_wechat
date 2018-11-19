# -*- coding: utf-8 -*-
# filename: image.py

import os
import threading
#import token as tk

def getFolderList(root_path):
    for root,dirs,files in os.walk(root_path):
        return dirs

def uploadAllImages(open_id):
    path = '/home/smbuser/data/'
    folder_list =  getFolderList(path)
    thread = threading.Thread(target=uploadData,args=(folder_list,open_id))
    thread.start()
    return folder_list
     
def uploadData(folder_list,open_id):
    print folder_list
    
    
class Media(object):
    def __init__(self,access_token):
        
        
    def up_image(file_path):
        
uploadAllImages()
