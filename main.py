# -*- coding: utf-8 -*-
# filename: main.py
import web
import src.messageHandler as mh
import src.token as tk
from src.handle import Handle


urls = (
    '/', 'Handle',
)

if __name__ == '__main__':
    mh.refresh()
    tk.post_url()
    app = web.application(urls, globals())
    app.run()
