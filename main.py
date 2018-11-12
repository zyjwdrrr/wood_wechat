# -*- coding: utf-8 -*-
# filename: main.py
import web
import src.messageHandler as mh
from src.handle import Handle

urls = (
    '/', 'Handle',
)

if __name__ == '__main__':
    mh.refresh()
    app = web.application(urls, globals())
    app.run()
