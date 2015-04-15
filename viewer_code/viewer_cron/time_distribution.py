'''
Created on 24/05/2013

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
from numpy.polynomial import polynomial
from numpy import array
import datetime

from goals.models import Goal

class TimeDistribution(webapp2.RequestHandler):

    def get(self):
        
        studentUsers =  GqlQuery("SELECT * FROM ViewerUser WHERE student = True")
        
        logging.info("NOTE: Starting Time Distribution of Use of the Platform cron job"); 
        for studentUser in studentUsers:
            taskqueue.add(queue_name='time-distribution', url='/admin/time_distribution', params={'userId': studentUser.key().name()})
            
        logging.info("NOTE: Calculating mean value of Time Distribution of Use of the Platform");    
        
        taskqueue.add(queue_name='time-distribution', url='/admin/mean_calculator', params={'profileName': viewer_code.viewer_consts.TIME_DISTRIBUTION})
        
        logging.info("NOTE: Finished Use of Platform cron job");
        
    def post(self):        
        user_id = self.request.get('userId')
        usuario = ViewerUser.get_by_key_name(user_id)
        
        time_schedule_measure = self.time_schedule(usuario)
        efficiency_schedule_measure = self.efficiency_schedule(usuario)
        constancy = self.constancy_meanvar(usuario)    
            
        userProfile = UserProfile.get_by_key_name(user_id)
        
        if(userProfile == None):
            userProfile = UserProfile(key_name = user_id, user = usuario.user, user_nickname = usuario.user_nickname, 
                                      user_id = usuario.user_id,
                                      time_schedule_morning = time_schedule_measure[0], time_schedule_afternoon = time_schedule_measure[1], time_schedule_night = time_schedule_measure[2],
                                      morning_schedule_efficiency = efficiency_schedule_measure[0], afternoon_schedule_efficiency = efficiency_schedule_measure[1], night_schedule_efficiency = efficiency_schedule_measure[2], average_schedule_efficiency = efficiency_schedule_measure[3], 
                                      constancy_mean = constancy[0], constancy_variance = constancy[1]) 
        else:    
            userProfile.time_schedule_morning = time_schedule_measure[0]
            userProfile.time_schedule_afternoon = time_schedule_measure[1]
            userProfile.time_schedule_night = time_schedule_measure[2]
            userProfile.morning_schedule_efficiency = efficiency_schedule_measure[0] 
            userProfile.afternoon_schedule_efficiency = efficiency_schedule_measure[1] 
            userProfile.night_schedule_efficiency = efficiency_schedule_measure[2]
            userProfile.average_schedule_efficiency = efficiency_schedule_measure[3]
            userProfile.constancy_mean = constancy[0] 
            userProfile.constancy_variance = constancy[1]
            
        userProfile.put()  
        
    def time_schedule(self, usuario):
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
                
        morningTimeExercises = 0
        afternoonTimeExercises = 0
        nightTimeExercises = 0
        morningTimeVideos = 0
        afternoonTimeVideos = 0
        nightTimeVideos = 0
        
        totalTime = 0
        
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2", subject_exercise.name, usuario.user)
            for problemLog in problemLogs:
                hour = problemLog.backup_timestamp.hour
                totalTime += problemLog.time_taken
                if( 6 < hour and hour < 14 ):
                    morningTimeExercises += problemLog.time_taken
                elif( 14 <= hour and hour < 21):
                    afternoonTimeExercises += problemLog.time_taken
                elif( hour <= 6 or hour == 21 or hour == 22 or hour == 23 or hour == 0):
                    nightTimeExercises += problemLog.time_taken
                else:
                    print "WRONG HOUR EXERCISE"
            
        for subject_video in subject_videos:
            videoLogs = GqlQuery("SELECT * FROM VideoLog WHERE video = :1 AND user = :2", subject_video.video, usuario.user)
            for videoLog in videoLogs:
                hour = videoLog.backup_timestamp.hour
                totalTime += videoLog.seconds_watched
                if( 6 < hour and hour < 14 ):
                    morningTimeVideos += videoLog.seconds_watched
                elif( 14 <= hour and hour < 21):
                    afternoonTimeVideos += videoLog.seconds_watched
                elif( hour <= 6 or hour == 21 or hour == 22 or hour == 23 or hour == 0):
                    nightTimeVideos += videoLog.seconds_watched
                else:
                    print "WRONG HOUR VIDEO"
                                        
        totalTimeMorning = morningTimeExercises + morningTimeVideos
        totalTimeAfternoon = afternoonTimeExercises + afternoonTimeVideos
        totalTimeNight = nightTimeExercises + nightTimeVideos
        
        if(totalTime == 0):
            return [0, 0, 0]
        else:
            morningPercentage = int((totalTimeMorning/totalTime)*100)
            afternoonPercentage = int((totalTimeAfternoon/totalTime)*100)
            nightPercentage = 100 - morningPercentage - afternoonPercentage
            return [morningPercentage, afternoonPercentage, nightPercentage]
        
        
    def efficiency_schedule(self, usuario):

        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
                
        morningExercises = 0
        afternoonExercises = 0
        nightExercises = 0
        correctMorningExercises = 0
        correctAfternoonExercises = 0
        correctNightExercises = 0        
        
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2", subject_exercise.name, usuario.user)
            for problemLog in problemLogs:
                hour = problemLog.backup_timestamp.hour
                if( 6 < hour and hour < 14 ):
                    morningExercises += 1
                    if((problemLog.correct == True) and (problemLog.count_hints == 0) and (problemLog.count_attempts == 1) and (problemLog.time_taken < 60)):
                        correctMorningExercises += 1
                elif( 14 <= hour and hour < 21):
                    afternoonExercises += 1
                    if((problemLog.correct == True) and (problemLog.count_hints == 0) and (problemLog.count_attempts == 1) and (problemLog.time_taken < 60)):
                        correctAfternoonExercises += 1
                elif( hour <= 6 or hour == 21 or hour == 22 or hour == 23 or hour == 0):
                    nightExercises += 1
                    if((problemLog.correct == True) and (problemLog.count_hints == 0) and (problemLog.count_attempts == 1) and (problemLog.time_taken < 60)):
                        correctNightExercises += 1
                else:
                    print "WRONG HOUR EXERCISE"
                    
        if(morningExercises == 0):
            morningPercentage = 0
        else:
            morningPercentage = (correctMorningExercises/morningExercises)*100
            
        if(afternoonExercises == 0):
            afternoonPercentage = 0
        else:
            afternoonPercentage = (correctAfternoonExercises/afternoonExercises)*100
            
        if(nightExercises == 0):
            nightPercentage = 0
        else:
            nightPercentage = (correctNightExercises/nightExercises)*100
            
        totalExercises = morningExercises + afternoonExercises + nightExercises
        totalCorrectExercises = correctMorningExercises + correctAfternoonExercises + correctNightExercises
        if(totalExercises == 0):
            averagePercentage = 0
        else:
            averagePercentage = (totalCorrectExercises/totalExercises)*100
            
        return [int(morningPercentage), int(afternoonPercentage), int(nightPercentage), int(averagePercentage)]
    
    
    # Constancia para las pruebas con periodo temporal prefijado
    def constancy_meanvar(self, usuario): 
            
        userDayList = []
        startDate = datetime.datetime(2012,8,1,0,0,1)
        endDate = datetime.datetime(2012,8,2,0,0,1)
        numberOfDays = 0
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        while(numberOfDays < 40):  
            
            timeSpentThisDay = 0
                  
            for subject_exercise in subject_exercises:
                problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2 AND time_done >= :3 AND time_done < :4", subject_exercise.name, usuario.user, startDate, endDate)
                for problemLog in problemLogs:
                    timeSpentThisDay += problemLog.time_taken
                                        
            for subject_video in subject_videos:
                videoLogs = GqlQuery("SELECT * FROM VideoLog WHERE video = :1 AND user = :2 AND time_watched >= :3 AND time_watched < :4", subject_video.video, usuario.user, startDate, endDate)
                for videoLog in videoLogs:
                    timeSpentThisDay += videoLog.seconds_watched
                    
            startDate += datetime.timedelta(days=1)
            endDate += datetime.timedelta(days=1)
            numberOfDays += 1
            userDayList.append(timeSpentThisDay/60)
            
        # Mean calculation    
        suma = 0        
        for userDay in userDayList:
            suma += userDay
                        
        userMean = int(suma/numberOfDays)
        
        std = 0        
        for userDay in userDayList:
            std += (userDay-userMean)**2
            
        userVar = int(std/(numberOfDays-1))
    
        return [userMean, userVar]
    
    """
    # Constancia con fecha actual como fecha final
    def constancy_meanvar(self, usuario): 
            
        userDayList = []
        startDate = datetime.datetime(2013,7,25,0,0,1)
        endDate = startDate + datetime.timedelta(days=1)
        numberOfDays = 0
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        todayDate = datetime.datetime.now()
        
        while(endDate < todayDate):  
            
            timeSpentThisDay = 0
                  
            for subject_exercise in subject_exercises:
                problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2 AND time_done >= :3 AND time_done < :4", subject_exercise.name, usuario.user, startDate, endDate)
                for problemLog in problemLogs:
                    timeSpentThisDay += problemLog.time_taken
                                        
            for subject_video in subject_videos:
                videoLogs = GqlQuery("SELECT * FROM VideoLog WHERE video = :1 AND user = :2 AND time_watched >= :3 AND time_watched < :4", subject_video.video, usuario.user, startDate, endDate)
                for videoLog in videoLogs:
                    timeSpentThisDay += videoLog.seconds_watched
                    
            startDate += datetime.timedelta(days=1)
            endDate += datetime.timedelta(days=1)
            numberOfDays += 1
            userDayList.append(timeSpentThisDay/60)
            
        # Mean calculation    
        suma = 0        
        for userDay in userDayList:
            suma += userDay
                        
        userMean = int(suma/numberOfDays)
        
        std = 0        
        for userDay in userDayList:
            std += (userDay-userMean)**2
            
        userVar = int(std/(numberOfDays-1))
    
        return [userMean, userVar]

    """
    
    def constancy(self, usuario): 
            
        userDayList = []
        startDate = datetime.datetime(2012,8,1,0,0,1)
        endDate = datetime.datetime(2012,8,2,0,0,1)
        numberOfDays = 0
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        while(numberOfDays < 40):  
            
            timeSpentThisDay = 0
                  
            for subject_exercise in subject_exercises:
                problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2 AND time_done >= :3 AND time_done < :4", subject_exercise.name, usuario.user, startDate, endDate)
                for problemLog in problemLogs:
                    timeSpentThisDay += problemLog.time_taken
                                        
            for subject_video in subject_videos:
                videoLogs = GqlQuery("SELECT * FROM VideoLog WHERE video = :1 AND user = :2 AND time_watched >= :3 AND time_watched < :4", subject_video.video, usuario.user, startDate, endDate)
                for videoLog in videoLogs:
                    timeSpentThisDay += videoLog.seconds_watched
                    
            startDate += datetime.timedelta(days=1)
            endDate += datetime.timedelta(days=1)
            numberOfDays += 1
            userDayList.append(timeSpentThisDay/60)
            
        # Mean calculation    
        suma = 0        
        for userDay in userDayList:
            suma += userDay
                        
        userMean = int(suma/numberOfDays)
        
        constancy = 0
        
        if(userMean != 0):
            for userDay in userDayList:
                constancy += abs((userDay-userMean)/userMean)            
            return constancy/len(userDayList)
        else:
            return 0
        