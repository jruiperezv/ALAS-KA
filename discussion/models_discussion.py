#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import db


class FeedbackType:
    Question="question"
    Answer="answer"
    Comment="comment"

    @staticmethod
    def is_valid(type):
        return (type == FeedbackType.Question or 
                type == FeedbackType.Answer or 
                type == FeedbackType.Comment)

class FeedbackFlag:

    # 2 or more flags immediately hides feedback
    HIDE_LIMIT = 2

    Inappropriate="inappropriate"
    LowQuality="lowquality"
    DoesNotBelong="doesnotbelong"
    Spam="spam"

    @staticmethod
    def is_valid(flag):
        return (flag == FeedbackFlag.Inappropriate or 
                flag == FeedbackFlag.LowQuality or 
                flag == FeedbackFlag.DoesNotBelong or 
                flag == FeedbackFlag.Spam)

class Feedback(db.Model):
    author = db.UserProperty()
    author_nickname = db.StringProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    deleted = db.BooleanProperty(default=False)
    targets = db.ListProperty(db.Key)
    types = db.StringListProperty()
    is_flagged = db.BooleanProperty(default=False)
    is_hidden_by_flags = db.BooleanProperty(default=False)
    flags = db.StringListProperty(default=None)
    flagged_by = db.StringListProperty(default=None)
    sum_votes = db.IntegerProperty(default=0)
    inner_score = db.FloatProperty(default=0.0)


class FeedbackNotification(db.Model):
    feedback = db.ReferenceProperty(Feedback)
    user = db.UserProperty()

class FeedbackVote(db.Model):
    DOWN = -1
    ABSTAIN = 0
    UP = 1

    # Feedback reference stored in parent property
    video = db.ReferenceProperty()
    user = db.UserProperty()
    vote_type = db.IntegerProperty(default=0)



