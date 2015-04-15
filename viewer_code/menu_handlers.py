'''
Created on 19/03/2013

@author: Jose
'''

from __future__ import division
from google.appengine.ext.webapp import template
import viewer_code.viewer_consts
import webapp2
import models
from profileviewer_models import ViewerUser
import os
from google.appengine.ext.db import GqlQuery
from google.appengine.ext import gql

class MenuHandler(webapp2.RequestHandler):
    def get(self):
                
        usuario = models.UserData.current()
        if(usuario):
            viewerUser = ViewerUser.get_by_key_name(usuario.user_id)
        else:
            viewerUser = None
            
        if(viewerUser.professor == True):
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/menu.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/blank.html')
        
        template_values = {
                           "viewerUser": viewerUser,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                          }
            
        self.response.out.write(template.render(path, template_values))
        
        
class AboutHandler(webapp2.RequestHandler):
    def get(self):
        
        usuario = models.UserData.current()
        if(usuario):
            viewerUser = ViewerUser.get_by_key_name(usuario.user_id)
        else:
            viewerUser = None
            
        if(viewerUser.professor == True):
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/about.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/blank.html')
        
        template_values = {
                           "viewerUser": viewerUser,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                          }
            
        self.response.out.write(template.render(path, template_values))
        
