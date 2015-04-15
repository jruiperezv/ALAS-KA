'''
Created on 29/05/2013

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
import math
import datetime

from goals.models import Goal

class ExerciseSolvingHabits(webapp2.RequestHandler):

    def get(self):
        
        studentUsers =  GqlQuery("SELECT * FROM ViewerUser WHERE student = True")
        
        logging.info("NOTE: Starting Exercise Solving Habits cron job"); 
        for studentUser in studentUsers:
            taskqueue.add(queue_name='exercise-solving-habits', url='/admin/exercise_solving', params={'userId': studentUser.key().name()})
        
        logging.info("NOTE: Calculating mean value of Exercise Solving Habits");    
        
        taskqueue.add(queue_name='exercise-solving-habits', url='/admin/mean_calculator', params={'profileName': viewer_code.viewer_consts.EXERCISE_SOLVING_HABITS})
        
        logging.info("NOTE: Finished Exercise Solving Habits cron job");
        
    def post(self):  
        
        user_id = self.request.get('userId')
        usuario = ViewerUser.get_by_key_name(user_id)
        
        # Get measures
        recommendation_listener_measure = self.recommendation_listener(usuario)
        forgetful_measure = self.forgetful_exercises(usuario)
        cognitive_model_measure = self.cognitiveModel(usuario)                
            
        userProfile = UserProfile.get_by_key_name(user_id)
        
        if(userProfile == None):
            userProfile = UserProfile(key_name = user_id, user = usuario.user, user_nickname = usuario.user_nickname, 
                                      user_id = usuario.user_id,
                                      recommendation_listener = recommendation_listener_measure, forgetful_exercises = forgetful_measure,
                                      hint_avoidance = cognitive_model_measure[0], video_avoidance = cognitive_model_measure[1],
                                      unreflective_user = cognitive_model_measure[2], hint_abuser = cognitive_model_measure[3]) 
        else:    
            userProfile.recommendation_listener = recommendation_listener_measure
            userProfile.forgetful_exercises = forgetful_measure
            userProfile.hint_avoidance = cognitive_model_measure[0] 
            userProfile.video_avoidance = cognitive_model_measure[1]
            userProfile.unreflective_user = cognitive_model_measure[2] 
            userProfile.hint_abuser = cognitive_model_measure[3]
                        
        userProfile.put()   
        
    def recommendation_listener(self, usuario):
        
        totalProblems = 0
        totalSuggested = 0
        
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2", subject_exercise.name, usuario.user)
            for problemLog in problemLogs:
                totalProblems += 1
                if(problemLog.suggested == True):
                    totalSuggested += 1
                    
        if(totalProblems == 0):
            suggestedPercentage = 0
        else:
            suggestedPercentage = int((totalSuggested/totalProblems)*100)
            
        return suggestedPercentage
    
    def forgetful_exercises(self, usuario):
        
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        exercisesAfterOneCorrect = 0
        wrongExercisesAfterOneCorrect = 0
        
        for subject_exercise in subject_exercises:
            
            previouslyCorrect = False
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2", subject_exercise.name, usuario.user)
            for problemLog in problemLogs:
                if(previouslyCorrect == False):
                    if(problemLog.correct == True):
                        previouslyCorrect = True
                    else:
                        continue
                elif(previouslyCorrect == True):
                    exercisesAfterOneCorrect += 1            
                    if((problemLog.correct == False) or (problemLog.count_hints > 0) or (problemLog.count_attempts > 1) or (problemLog.time_taken > 60)):
                        wrongExercisesAfterOneCorrect += 1   
                
        if(exercisesAfterOneCorrect==0):
            forgetful_percentage = 0
        else:
            forgetful_percentage = int((wrongExercisesAfterOneCorrect/exercisesAfterOneCorrect)*100)
            
        return forgetful_percentage
    
    def cognitiveModel(self, usuario):
        
        hintAvoidance = 0
        videoAvoidance = 0
        unreflectiveUser = 0
        hintAbuser = 0
        
        totalDifferentExercises = 0
        
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        for subject_exercise in subject_exercises:
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2 ORDER BY time_done ASC", subject_exercise.name, usuario.user)
            
            if(problemLogs.count() > 0 ):
                
                totalDifferentExercises += 1
                
                exercisesSameKind = 0
                hintAvoidPoints = 0
                videoAvoidPoints = 0
                unreflectivePoints = 0
                hintAbusePoints = 0
            
                exerciseVideo = GqlQuery("SELECT * FROM ExerciseVideo WHERE exercise = :1", subject_exercise.exercise).get()                
                userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user= :2", exerciseVideo.video, usuario.user).get()
                videoDate = datetime.datetime.now()
                if(userVideo != None):
                    videoDate = userVideo.backup_timestamp
                
                
                for problemLog in problemLogs:
                    
                    exercisesSameKind += 1
                    
                    # Video Avoidance
                    if(problemLog.correct == False and (problemLog.time_done < videoDate)):
                        videoAvoidPoints += 1
                                                
                    # Hint Avoidance                    
                    if(problemLog.correct == False and problemLog.count_hints == 0):
                        hintAvoidPoints += 1
                    if(problemLog.correct == False and problemLog.count_hints == 1):    
                        hintAvoidPoints += 0.5
                        
                    # Calculamos el no reflexionador
                    if(problemLog.correct == False):
                        intentoAnterior = 0
                        listaIntentos = problemLog.time_taken_attempts
                        listaIntentos.sort()
                        
                        for intento in listaIntentos:
                            diferenciaTemporal = math.fabs(intento-intentoAnterior)
                            intentoAnterior = intento
                            #Comprobamos que sea menor de 10 segundos para considerar abuso
                            if(diferenciaTemporal < 10):
                                unreflectivePoints += 1
                                break
                    #Fin no reflexionador
                    
                    #Calculo pide pistas demasiado rapido
                    if(problemLog.count_hints > 0):
                        pistaAnterior = 0
                        listaPistas = problemLog.hint_time_taken_list
                        listaPistas.sort()
                        
                        for pista in listaPistas:
                            diferenciaTemporal = math.fabs(pista-pistaAnterior)
                            pistaAnterior = pista
                            #Comprobamos que sea menor de 10 segundos para considerar abuso
                            if(diferenciaTemporal < 10):
                                hintAbusePoints += 1
                                break
                    #Fin abusor pistas
                    
                    if(problemLog.correct == True):
                        break
                    else:
                        continue
                                        
                hintAvoidance += ((hintAvoidPoints/exercisesSameKind)*100)
                videoAvoidance += ((videoAvoidPoints/exercisesSameKind)*100)
                unreflectiveUser += ((unreflectivePoints/exercisesSameKind)*100)
                hintAbuser += ((hintAbusePoints/exercisesSameKind)*100)
                
        if(totalDifferentExercises != 0):
            hintAvoidanceFinal = int(hintAvoidance/totalDifferentExercises)
            videoAvoidanceFinal = int(videoAvoidance/totalDifferentExercises)
            unreflectiveUserFinal = int(unreflectiveUser/totalDifferentExercises)
            hintAbuserFinal = int(hintAbuser/totalDifferentExercises)
            
            return [hintAvoidanceFinal, videoAvoidanceFinal,
                    unreflectiveUserFinal, hintAbuserFinal]
        else:
            return [0,0,0,0]
                