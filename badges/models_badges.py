#!/usr/bin/python
# -*- coding: utf-8 -*-


from google.appengine.ext import db


class UserBadge(db.Model):
    """Represents a single instance of a badge that a user has earned.

    Note that for any given badge type (e.g. a "streak" badge"), a user may
    earn multiple of them, and each instance will create an entity in the db.
    """

    user = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    badge_name = db.StringProperty()
    target_context = db.ReferenceProperty()
    target_context_name = db.StringProperty()
    points_earned = db.IntegerProperty(default=0)

    _serialize_blacklist = ["badge"]

