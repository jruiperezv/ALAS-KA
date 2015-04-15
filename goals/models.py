# -*- coding: utf-8 -*-
from google.appengine.ext import db

from object_property import ObjectProperty


class Goal(db.Model):
    # data
    title = db.StringProperty(indexed=False)
    objectives = ObjectProperty()

    # a goal is 'completed' if it's finished or abandoned. This property is
    # indexed so that we can quickly fetch currently open goals
    completed = db.BooleanProperty(default=False)
    completed_on = db.DateTimeProperty(indexed=False)

    # we distinguish finished and abandoned goals with this property
    abandoned = db.BooleanProperty(indexed=False)

    created_on = db.DateTimeProperty(auto_now_add=True)
    updated_on = db.DateTimeProperty(auto_now=True)
