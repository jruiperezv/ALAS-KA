'''
Created on 07/06/2013

@author: jruiperezv
'''
from __future__ import division
import webapp2
import logging
from viewer_code.profileviewer_models import UserProfile
from viewer_code.profileviewer_models import ViewerUser
from viewer_code.profileviewer_models import ViewerVideo
from viewer_code.profileviewer_models import ViewerExercise
from google.appengine.ext.db import GqlQuery
import viewer_code.viewer_consts
from google.appengine.api import taskqueue
from models import UserData
from models import ProblemLog
from badges.models_badges import UserBadge
from numpy.polynomial import polynomial
from numpy import array
import datetime

from goals.models import Goal

class GamificationHabits(webapp2.RequestHandler):

    def get(self):
        
        studentUsers =  GqlQuery("SELECT * FROM ViewerUser WHERE student = True")
        
        logging.info("NOTE: Starting Gamification Habits cron job"); 
        for studentUser in studentUsers:
            taskqueue.add(queue_name='gamification-habits', url='/admin/gamification_habits', params={'userId': studentUser.key().name()})
            
        logging.info("NOTE: Calculating mean value of Gamification Habits");    
        
        taskqueue.add(queue_name='gamification-habits', url='/admin/mean_calculator', params={'profileName': viewer_code.viewer_consts.GAMIFICATION_HABITS})
        
        logging.info("NOTE: Finished Gamification Habits cron job");
        
    def post(self):        
        user_id = self.request.get('userId')
        usuario = ViewerUser.get_by_key_name(user_id)
        
        badge_time_points_measure = self.badges_over_time_and_points(usuario)
            
        userProfile = UserProfile.get_by_key_name(user_id)
        
        if(userProfile == None):
            userProfile = UserProfile(key_name = user_id, user = usuario.user, user_nickname = usuario.user_nickname, 
                                      user_id = usuario.user_id,
                                      badge_over_time = badge_time_points_measure[0], badge_point_percentage = badge_time_points_measure[1]) 
        else:    
            userProfile.badge_over_time = badge_time_points_measure[0]
            userProfile.badge_point_percentage = badge_time_points_measure[1]
            
        userProfile.put()          
        
    def badges_over_time_and_points(self, usuario):
                
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
            
        videoTime = 0
        exerciseTime = 0
        numberOfBadges = 0
        
        exercisePoints = 0
        videoPoints = 0
        badgePoints = 0
        
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2", subject_exercise.name, usuario.user)
            for problemLog in problemLogs:
                exerciseTime += problemLog.time_taken
                exercisePoints += problemLog.points_earned
                            
        for subject_video in subject_videos:
            videoLogs = GqlQuery("SELECT * FROM VideoLog WHERE video = :1 AND user = :2", subject_video.video, usuario.user)
            for videoLog in videoLogs:
                videoTime += videoLog.seconds_watched     
                videoPoints += videoLog.points_earned    
                
        userBadges = GqlQuery("SELECT * FROM UserBadge WHERE user = :1", usuario.user)
        for userBadge in userBadges:
            badgePoints += userBadge.points_earned
            numberOfBadges += 1
                
        totalTime = (exerciseTime + videoTime)/3600
        totalPoints = (exercisePoints + videoPoints + badgePoints)
        
        if(totalTime == 0):      
            badgesPerHour = 0                  
        else:
            badgesPerHour = int(round((numberOfBadges/totalTime),0))
            
        if(totalPoints == 0):
            badgePointsPercentage = 0
        else:
            badgePointsPercentage = int((badgePoints/totalPoints)*100)
         
        return [badgesPerHour, badgePointsPercentage]  