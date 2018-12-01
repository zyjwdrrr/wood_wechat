# -*- coding: utf-8 -*-
# filename: config.py

import ConfigParser as cp

cfg_file = "sys.cfg"
wechat = dict()

def loadCfg():
    cfg = cp.SafeConfigParser()
    cfg.read(cfg_file)
    for opt in cfg.options('wechat'):
        wechat[opt] = cfg.get('wechat',opt)

def saveCfg():
    cfg = cp.ConfigParser()
    cfg.add_section("wechat")
    for temp in wechat:
        cfg.set("wechat",temp,wechat[temp])
    cfg.write(open(cfg_file,'w'))

def updateValue(key,value):
    wechat[key] = value
    saveCfg()
