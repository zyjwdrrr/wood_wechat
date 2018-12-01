# -*- coding: utf-8 -*-
# filename: express.py
import web
render=web.template.render('templates/')

class Express(object):
    def GET(self):
        name = 'test'
        return render.express(name)
    def POST(self):
        return "71"
     
