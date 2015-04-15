'''
Created on 16/05/2013

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
from numpy.polynomial import Polynomial
from numpy import array

from goals.models import Goal

class CorrectProgress(webapp2.RequestHandler):

    def get(self):
        
        studentUsers = GqlQuery("SELECT * FROM ViewerUser WHERE student = True")
        
        logging.info("NOTE: Starting Correct Progress in the Platform cron job"); 
        for studentUser in studentUsers:
            taskqueue.add(queue_name='correct-progress', url='/admin/correct_progress', params={'userId': studentUser.key().name()})
            
        logging.info("NOTE: Calculating mean value of Correct Progress in the Platform");    
        
        taskqueue.add(queue_name='correct-progress', url='/admin/mean_calculator', params={'profileName': viewer_code.viewer_consts.CORRECT_PROGRESS})
        
        logging.info("NOTE: Finished Correct Progress in the Platform cron job");
        
    def post(self):  
        
        user_id = self.request.get('userId')
        usuario = ViewerUser.get_by_key_name(user_id)
        
        # Get measures
        video_efficiency_measure = self.video_efficiency(usuario)
        time_exercise_effiency_measure = self.correct_exercise_effiency_time(usuario)
        exercise_efficiency_measure = self.correct_exercise_efficiency(usuario)
        exercise_progress_measure = self.exercise_progress(usuario)
        video_progress_measure = self.video_progress(usuario)
        correct_exercises_measure = self.correct_exercises(usuario)
        efficiency_proficiencies = self.efficiency_proficiencies(usuario)                
            
        userProfile = UserProfile.get_by_key_name(user_id)
        
        if(userProfile == None):
            userProfile = UserProfile(key_name = user_id, user = usuario.user, user_nickname = usuario.user_nickname, 
                                      user_id = usuario.user_id,
                                      video_efficiency = video_efficiency_measure, correct_exercise_effiency = time_exercise_effiency_measure,
                                      exercise_progress = exercise_progress_measure, video_progress = video_progress_measure,
                                      correct_exercises = correct_exercises_measure, efficiency_proficiencies = efficiency_proficiencies,
                                      correct_exercise_solving_efficiency = exercise_efficiency_measure) 
        else:    
            userProfile.video_efficiency = video_efficiency_measure
            userProfile.correct_exercise_effiency = time_exercise_effiency_measure
            userProfile.exercise_progress = exercise_progress_measure
            userProfile.video_progress = video_progress_measure
            userProfile.correct_exercises = correct_exercises_measure
            userProfile.efficiency_proficiencies = efficiency_proficiencies
            userProfile.correct_exercise_solving_efficiency = exercise_efficiency_measure
            
        userProfile.put()   
        
    def video_efficiency(self, usuario):
        
        x_eff_video_1 = array([70.0, 85.0,  100.0])
        y_eff_video_1 = array([75.0, 85.0,  100.0])                 
        pol_eff_video_1 = Polynomial.fit(x_eff_video_1, y_eff_video_1, 2)
        
        x_eff_video_2 = array([100.0, 150.0, 200.0, 250.0, 300.0])
        y_eff_video_2 = array([100.0, 60.0, 30.0, 10.0, 0.0])                       
        pol_eff_video_2 = Polynomial.fit(x_eff_video_2, y_eff_video_2, 2)
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        
        videosAbove70 = 0
        videoPoints = 0
        
        for subject_video in subject_videos:
            
            userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
            
            if(userVideo != None):
                porcentajeVideo = (userVideo.seconds_watched/userVideo.duration)*100
                
                if(porcentajeVideo > 70):
                    videosAbove70 += 1
                    if(porcentajeVideo >= 100):
                        videoPoints += pol_eff_video_2(porcentajeVideo)
                    if(porcentajeVideo < 100):
                        videoPoints += pol_eff_video_1(porcentajeVideo)
                        
        if(videosAbove70 != 0):
            videoPoints = int(videoPoints/videosAbove70)
            
        return videoPoints
    
    #Eficiencia en tiempo
    def correct_exercise_effiency_time(self, usuario):
        
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        totalTime = 0
        totalCorrect = 0
        
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2", subject_exercise.name, usuario.user)
                
            for problemLog in problemLogs:
                if(problemLog.time_taken > 180):
                    totalTime += 180
                else:
                    totalTime += problemLog.time_taken
                if(problemLog.correct == True):
                    totalCorrect += 1          
        
        if(totalTime != 0):   
            return int( ((totalCorrect*30)/totalTime)*100 )
        else:
            return 0
    
    # Eficiencia hasta 1 ejercicio bien
    def correct_exercise_efficiency(self, usuario):
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        totalEfficiency = 0
        totalExercises= 0 
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2 ORDER BY time_done ASC", subject_exercise.name, usuario.user)
            
            if(problemLogs.count() > 0 ):
                totalExercises += 1
                problemsTime = 0
                problemsAttempt = 0
                exerciseCorrect = False
                
                for problemLog in problemLogs:
                    problemsTime += problemLog.time_taken
                    problemsAttempt += problemLog.count_attempts
                    if(problemLog.correct == True):
                        exerciseCorrect = True
                        break

                if(exerciseCorrect == True):
                    if(problemsTime < 10):
                        totalEfficiency += 50
                    elif(problemsTime > 100):
                        totalEfficiency += 0
                    else:
                        totalEfficiency += (1 - (problemsTime/100))*50
                        
                    if(problemsAttempt > 6):
                        totalEfficiency += 0
                    else:
                        totalEfficiency += (1 - ((problemsAttempt-1)/5))*50                    
        
        if (totalExercises == 0):
            totalEfficiency  = 0
        else:
            totalEfficiency = int(totalEfficiency/totalExercises) 
            
        return totalEfficiency               
                
    def video_progress(self, usuario):
        
        x_vid = array([0.0, 50.0, 75.0, 100.0])
        y_vid = array([0.0, 30.0, 55.0, 100.0])
        
        pol_video_progress = Polynomial.fit(x_vid, y_vid, 5)
        
        total_video_progress = 0
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        
        for subject_video in subject_videos:
                
            userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
            
            if(userVideo != None):
                porcentajeVideo = (userVideo.seconds_watched/userVideo.duration)*100
                if(porcentajeVideo >= 100):
                    total_video_progress += 100
                else:
                    total_video_progress += pol_video_progress(porcentajeVideo)
                        
        return int(total_video_progress/subject_videos.count())
    
    def exercise_progress(self, usuario):
        
        x_vid = array([0.0, 25.0, 50.0, 75.0, 100.0])
        y_vid = array([0.0, 40.0, 65.0, 85.0, 100.0])
        
        pol_exercise_progress = Polynomial.fit(x_vid, y_vid, 5)
        
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        exercise_progress = 0
        
        for subject_exercise in subject_exercises:
            userExercise = GqlQuery("SELECT * FROM UserExercise WHERE exercise_model = :1 AND user = :2", subject_exercise.exercise, usuario.user).get()
            
            if(userExercise != None):
                if(userExercise._progress == 1.0):
                    exercise_progress += 100
                else:
                    exercise_progress += pol_exercise_progress(userExercise._progress*100)
                    
        return int(exercise_progress/subject_exercises.count())
    
    # Considerando ejercicios correctos aquellos sin pistas ni intentos fallidos
    def correct_exercises(self, usuario):
        
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        totalExercisesAttempted = 0
        totalCorrectNoHintNoAttempt = 0
        
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2 ORDER BY time_done ASC", subject_exercise.name, usuario.user)
            counter = 0    
            for problemLog in problemLogs:
                counter += 1
                totalExercisesAttempted += 1
                if((problemLog.correct == True) and (problemLog.count_hints == 0) and (problemLog.count_attempts == 1) and (problemLog.time_taken < 60)):
                    totalCorrectNoHintNoAttempt += 1
                if(counter==10):
                    break
                    
        if(totalExercisesAttempted == 0):
            return 0
        else:
            return int((totalCorrectNoHintNoAttempt/totalExercisesAttempted)*100)
        
        
    def efficiency_proficiencies(self, usuario):
        
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        proficientExercises = 0
        efficiency_proficiency = 0
        
        for subject_exercise in subject_exercises:
            userExercise = GqlQuery("SELECT * FROM UserExercise WHERE exercise_model = :1 AND user = :2", subject_exercise.exercise, usuario.user).get()
            
            if(userExercise != None and userExercise.proficient_date != None):
                proficientExercises += 1
                if(userExercise.total_done < 8):
                    efficiency_proficiency += 1
                else:
                    efficiency_proficiency += 8/userExercise.total_done
                    
        if(proficientExercises == 0):
            return 0
        else:
            return int((efficiency_proficiency/proficientExercises)*100)