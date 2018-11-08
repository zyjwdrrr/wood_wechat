# -*- coding: utf-8 -*-
# filename: index.wsgi
import sae
import web

from handle import Handle

urls = (
    '/wx', 'Handle',
)
    
app = web.application(urls, globals()).wsgifunc()  
application = sae.create_wsgi_app(app)