# -*- coding: utf-8 -*-
# filename: main.py
import web
from src.handle import Handle

urls = (
    '/', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
