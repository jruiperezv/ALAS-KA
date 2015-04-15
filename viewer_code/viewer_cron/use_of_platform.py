'''
Created on 07/05/2013

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

class UseOfPlatform(webapp2.RequestHandler):

    def get(self):
        
        studentUsers =  GqlQuery("SELECT * FROM ViewerUser WHERE student = True")
        
        logging.info("NOTE: Starting Use of Platform cron job"); 
        for studentUser in studentUsers:
            taskqueue.add(queue_name='use-of-platform', url='/admin/use_of_platform', params={'userId': studentUser.key().name()})
            
        logging.info("NOTE: Calculating mean value of Use of Platform");    
        
        taskqueue.add(queue_name='use-of-platform', url='/admin/mean_calculator', params={'profileName': viewer_code.viewer_consts.USE_OF_PLATFORM})
        
        logging.info("NOTE: Finished Use of Platform cron job");
        
    def post(self):        
        user_id = self.request.get('userId')
        usuario = ViewerUser.get_by_key_name(user_id)
        
        explorer_measure = self.exercise_video_explorer(usuario)
        leaver_measure = self.exercise_video_abandon(usuario)
        optional_measure = self.optional_elements(usuario)
        exercise_one_correct_measure = self.exercise_one_correct(usuario)
        focus_videos_exercises_measure = self.focus_videos_exercises(usuario)
            
        userProfile = UserProfile.get_by_key_name(user_id)
        
        if(userProfile == None):
            userProfile = UserProfile(key_name = user_id, user = usuario.user, user_nickname = usuario.user_nickname,
                                      user_id = usuario.user_id,
                                      exercise_explorer = explorer_measure[0], video_explorer = explorer_measure[1],
                                      exercise_abandon = leaver_measure[0], video_abandon = leaver_measure[1],
                                      optional_elements = optional_measure, exercise_one_correct = exercise_one_correct_measure,
                                      focus_exercises = focus_videos_exercises_measure[0], focus_videos = focus_videos_exercises_measure[1]) 
        else:    
            userProfile.exercise_explorer = explorer_measure[0]
            userProfile.video_explorer = explorer_measure[1]
            userProfile.exercise_abandon = leaver_measure[0] 
            userProfile.video_abandon = leaver_measure[1]
            userProfile.optional_elements = optional_measure
            userProfile.exercise_one_correct = exercise_one_correct_measure
            userProfile.focus_exercises = focus_videos_exercises_measure[0]
            userProfile.focus_videos = focus_videos_exercises_measure[1]
            
        userProfile.put()   
 
    def exercise_video_explorer(self, usuario):
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        exercises_accessed = 0
        videos_started = 0
        
        for subject_exercise in subject_exercises:
            userExercise = GqlQuery("SELECT * FROM UserExercise WHERE exercise_model = :1 AND user = :2", subject_exercise.exercise, usuario.user).get()
            
            if(userExercise != None):
                exercises_accessed += 1
                
        for subject_video in subject_videos:       
            userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
            
            if(userVideo != None):
                videos_started += 1
        
        videoPercentage = int((videos_started/subject_videos.count())*100)
        exercisePercentage = int((exercises_accessed/subject_exercises.count())*100)
        
        return [exercisePercentage, videoPercentage]
    
    def exercise_video_abandon(self, usuario):
        
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        
        exercises_accessed = 0
        videos_started = 0
        
        non_finished_videos = 0
        non_achieved_proficiencies = 0
        
        for subject_exercise in subject_exercises:
            userExercise = GqlQuery("SELECT * FROM UserExercise WHERE exercise_model = :1 AND user = :2", subject_exercise.exercise, usuario.user).get()
            
            if(userExercise != None):
                exercises_accessed += 1
                if(userExercise.proficient_date == None):
                    non_achieved_proficiencies += 1
                
        for subject_video in subject_videos:       
            userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
            
            if(userVideo != None):
                videos_started += 1
                if(userVideo.completed == False):
                    non_finished_videos += 1
        
        if(videos_started == 0):
            videoPercentage = 0
        else:
            videoPercentage = int((non_finished_videos/videos_started)*100)
            
        if(exercises_accessed == 0):
            exercisePercentage = 0
        else:
            exercisePercentage = int((non_achieved_proficiencies/exercises_accessed)*100)
        
        return [exercisePercentage, videoPercentage]
    
    def optional_elements(self, usuario):
        
        userData = GqlQuery("SELECT * FROM UserData WHERE user_id = :1", usuario.user_id).get()
        goals = GqlQuery("SELECT * FROM Goal WHERE ANCESTOR IS :1", userData)
        
        optionalPoints = 0
        
        for goal in goals:
            optionalPoints += 0.5
            if(goal.completed == True):
                optionalPoints += 0.5
                
        if(optionalPoints > 3):
            optionalPoints = 3
        if(userData.avatar_name != None):
            optionalPoints += 1
        if(len(userData.public_badges) > 0):
            optionalPoints += 1
          
        return int((optionalPoints/5)*100)
    
    def exercise_one_correct(self, usuario):

        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        correct_exercises = 0
        
        for subject_exercise in subject_exercises:
            userExercise = GqlQuery("SELECT * FROM UserExercise WHERE exercise_model = :1 AND user = :2", subject_exercise.exercise, usuario.user).get()
            
            if(userExercise != None and userExercise.total_correct >= 1):
                correct_exercises += 1
                
        return int((correct_exercises/subject_exercises.count())*100)
    
    def focus_videos_exercises(self, usuario):
        
        # Ejercicios y videos de la asignatura
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        
        focusVideos = 0
        focusExercise = 0
        numberTopics = 0
        # Para cada video de la asignatura
        for subject_video in subject_videos:
            # Coge los ejercicios asociados a dicho video
            exerciseVideos = GqlQuery("SELECT * FROM ExerciseVideo where video = :1", subject_video.video)
            
            # Si encuentra el ejercicio asociado a dicho video
            if(exerciseVideos != None):
                
                videoPoints = 0
                exercisePoints = 0
                
                userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
                
                if(userVideo != None):
                    porcentajeVideo = (userVideo.seconds_watched/userVideo.duration)
                    
                    if(porcentajeVideo > 1):
                        porcentajeVideo = 1
                        
                    videoPoints = round(36*porcentajeVideo,0)
                
                for exerciseVideo in exerciseVideos:
                    puntosTiempoEjercicio = 0
                    puntosIntentosEjercicio = 0
                    # Coge el UserExercise de dicho ejercicio
                    problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2", exerciseVideo.exercise.name, usuario.user)
                    
                    for problemLog in problemLogs:
                        if(problemLog.correct == True):
                            puntosTiempoEjercicio += 2
                            puntosIntentosEjercicio += 2
                        else:
                            # Calculo por tiempo
                            if(problemLog.time_taken > 100):
                                puntosTiempoEjercicio += 2
                            else:
                                puntosTiempoEjercicio += 2*(problemLog.time_taken/100)
                                
                            if(problemLog.count_attempts > 5):
                                puntosIntentosEjercicio += 2
                            else:
                                puntosIntentosEjercicio += 2*(problemLog.count_attempts/5)
                                                                                                                                        
                    if(puntosTiempoEjercicio > 18):
                        puntosTiempoEjercicio = 18
                    if(puntosIntentosEjercicio > 18):
                        puntosIntentosEjercicio = 18  
                        
                    exercisePoints += puntosTiempoEjercicio + puntosIntentosEjercicio
                    
                if(exercisePoints != 0):
                    exercisePoints = (exercisePoints/exerciseVideos.count())
                               
                if(exercisePoints != 0 or videoPoints !=0):
                    numberTopics += 1
                    focusExercise += (exercisePoints/(exercisePoints + videoPoints))*100
                    focusVideos += (videoPoints/(exercisePoints + videoPoints))*100
            else:
                print "Video no tiene ejercicio. No usamos."
        
        if(numberTopics != 0): 
            focusVideos = int(round(focusVideos/numberTopics,0))
            focusExercise = int(round(focusExercise/numberTopics,0))
        
        return [focusExercise, focusVideos]    