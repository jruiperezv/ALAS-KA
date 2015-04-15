# -*- coding: utf-8 -*-
from __future__ import division
from google.appengine.api import taskqueue
import viewer_code.viewer_consts
import webapp2

from viewer_code.profileviewer_models import UserProfile
from viewer_code.profileviewer_models import ViewerUser
from models import ExerciseVideo
import logging
from google.appengine.ext.db import GqlQuery




class EvaluationStats(webapp2.RequestHandler):
    
    # This is called by the cron job
    def get(self):
        
        logging.info("NOTE: Starting evaluation cron job"); 
        
        studentUsers =  GqlQuery("SELECT * FROM ViewerUser WHERE student = True")
    
        for studentUser in studentUsers:
            taskqueue.add(queue_name='evaluation-stats', url='/admin/evaluation_stats', params={'userId': studentUser.key().name()})
                     
        #logging.info("NOTE: Calculating mean value of evaluation");    
        #taskqueue.add(queue_name='evaluation-stats', url='/admin/mean_calculator', params={'profileName': viewer_code.viewer_consts.EXERCISE_VIDEO_EVALUATION})
        
        #logging.info("NOTE: Finished evaluation cron job");
        
    # This is called by the task queue
    def post(self):
        
        user_id = self.request.get('userId')
        usuario = ViewerUser.get_by_key_name(user_id)
        
        # Los de fisica curso 2012
        
        exerciseList1 =  ['d_ejercicio_corriente_electrica', 'd_ejercicio_voltaje','d_ejercicio_ley_de_ohm',
                          'd_ejercicio_de_magnetismo', 'd_ejercicio_fuerza_de_lorentz','d_ejercicio_radio_de_Larmor' ,
                          'd_ejercicio_ley_de_faraday_1','d_ejercicio_ley_de_faraday_2', 'd_ejercicio_ley_de_faraday_3', 
                          'd_ejercicio_producto_escalar','d_ejercicio_movimiento_armonico_simple','d_ejercicio_ondas_armonicas_1a',
                          'd_ejercicio_ondas_armonicas_1b','d_ejercicio_ondas_armonicas_1c','d_ejercicio_ondas_armonicas_2a',
                          'd_ejercicio_ondas_armonicas_2c','d_ejercicio_ondas_armonicas_2d','d_ejercicio_ondas_armonicas_2b']
                          
        
        exerciseList2 = ['d_ejercicio_carga_electrica','d_ejercicio_principio_de_superposicion','d_ejercicio_ley_de_gauss_1',
                          'd_ejercicio_ley_de_gauss_2','d_ejercicio_ley_de_gauss_3','d_ejercicio_sistemas_unidades',
                          'd_ejercicio_producto_vectorial','d_ejercicio_escalares_y_vectores','d_ejercicio_tiro_parabolico',
                          'd_ejercicio_movimiento_circular' ,'d_ejercicio_fuerza_rozamiento','d_ejercicio_plano_inclinado_a',
                          'd_ejercicio_plano_inclinado_b','d_ejercicio_fuerza_centripeta','d_ejercicio_trabajo_y_energia_2',
                          'd_ejercicio_trabajo_y_energia_3','d_ejercicio_trabajo_y_energia_1']
        
        
        subject_exercises1 = GqlQuery("SELECT * FROM ViewerExercise WHERE name IN :1", exerciseList1)
        subject_exercises2 = GqlQuery("SELECT * FROM ViewerExercise WHERE name IN :1", exerciseList2)
        
        subject_exercises = list(subject_exercises1) + list(subject_exercises2)
        #subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")
        points = 0
        for subject_exercise in subject_exercises:
            
            problemLogs = GqlQuery("SELECT * FROM ProblemLog WHERE exercise = :1 AND user = :2 ORDER BY time_done ASC", subject_exercise.name, usuario.user)
            correct = False
            numberAttempts = 0
                                                
            for problemLog in problemLogs:
                
                numberAttempts += problemLog.count_attempts  
                              
                if(problemLog.correct == True):
                    correct = True
                    break
                else:
                    continue
                
            if(correct):
                points += 10/numberAttempts
    
        ranking = int((points*100)/len(subject_exercises))
        
        userProfile = UserProfile.get_by_key_name(user_id)
        
        if(userProfile == None):
            userProfile = UserProfile(key_name = user_id, user = usuario.user, user_nickname = usuario.user_nickname, 
                                      user_id = usuario.user_id, evaluation_ranking = ranking)
        else:    
            userProfile.evaluation_ranking = ranking

        userProfile.put()   
              
    #This is called by the task queue
    def oldEvaluation(self):
        
        user_id = self.request.get('userId')
        usuario = ViewerUser.get_by_key_name(user_id)
        
        ejerciciosMin3 = 0
        videosMin50 = 0
        
        # Ejercicios y videos de la asignatura
        subject_videos = GqlQuery("SELECT * FROM ViewerVideo")
        subject_exercises = GqlQuery("SELECT * FROM ViewerExercise")

        # Para cada video de la asignatura
        for subject_video in subject_videos:
            # Coge los ejercicios asociados a dicho video
            exerciseVideos = GqlQuery("SELECT * FROM ExerciseVideo where video = :1", subject_video.video)
            
            # Si encuentra el ejercicio asociado a dicho video
            if(exerciseVideos != None):
                for exerciseVideo in exerciseVideos:
                    # Coge el UserExercise de dicho ejercicio
                    userExercise = GqlQuery("SELECT * FROM UserExercise WHERE exercise_model = :1 AND user = :2", exerciseVideo.exercise, usuario.user).get()
                    
                    # Si no ha encontrado el ejercicio asociado al video, mira directamente el video
                    if(userExercise == None):
                        
                        userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
                        
                        if(userVideo != None):
                            porcentaje = userVideo.seconds_watched/userVideo.duration
                            if(porcentaje >= 0.5):                
                                if(subject_video.youtube_id == 'WKR3h7vBxtU' or subject_video.youtube_id == 'NwZqpCAf6o8' or subject_video.youtube_id == 'ESSg3pdsSqA'):
                                    videosMin50 += 1/3
                                elif(subject_video.youtube_id == 'EQ4JVdRLxlU'):
                                    videosMin50 += 1/4
                                elif(subject_video.youtube_id == '7jj6zSWEEgk'):
                                    videosMin50 += 1/2
                                else:
                                    videosMin50 += 1
                            
                    # Si ha encontrado el ejercicio asociado al video, comprueba primero si el ejercicio esta bien hecho
                    else:
                        # Si tiene mas de 3 correctos, sumamos directamente ejercicio y video
                        if(userExercise.total_correct >= 3):
                            ejerciciosMin3 += 1
                            if(subject_video.youtube_id == 'WKR3h7vBxtU' or subject_video.youtube_id == 'NwZqpCAf6o8' or subject_video.youtube_id == 'ESSg3pdsSqA'):
                                videosMin50 += 1/3
                            elif(subject_video.youtube_id == 'EQ4JVdRLxlU'):
                                videosMin50 += 1/4
                            elif(subject_video.youtube_id == '7jj6zSWEEgk'):
                                videosMin50 += 1/2
                            else:
                                videosMin50 += 1  
                        # Si tiene menos de 3 correctos, NO sumamos ejercicio y miramos video                  
                        else:
                            userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
                        
                            if(userVideo != None):
                                porcentaje = userVideo.seconds_watched/userVideo.duration
                                if(porcentaje >= 0.5):                
                                    if(subject_video.youtube_id == 'WKR3h7vBxtU' or subject_video.youtube_id == 'NwZqpCAf6o8' or subject_video.youtube_id == 'ESSg3pdsSqA'):
                                        videosMin50 += 1/3
                                    elif(subject_video.youtube_id == 'EQ4JVdRLxlU'):
                                        videosMin50 += 1/4
                                    elif(subject_video.youtube_id == '7jj6zSWEEgk'):
                                        videosMin50 += 1/2
                                    else:
                                        videosMin50 += 1
                
            # Si el video no tiene un ejercicio asociado, mira directamente el video
            else:
                userVideo = GqlQuery("SELECT * FROM UserVideo WHERE video = :1 AND user = :2", subject_video.video, usuario.user).get()
                    
                if(userVideo != None):
                    porcentaje = userVideo.seconds_watched/userVideo.duration
                    if(porcentaje >= 0.5):                
                        videosMin50 += 1
        
        ejerciciosMin3 = int((ejerciciosMin3/subject_exercises.count())*100)
        videosMin50 = int((videosMin50/subject_videos.count())*100)
                 
        userProfile = UserProfile.get_by_key_name(user_id)
        
        if(userProfile == None):
            userProfile = UserProfile(key_name = user_id, user = usuario.user, user_nickname = usuario.user_nickname, 
                                      user_id = usuario.user_id,
                                      evaluation_exercise = ejerciciosMin3,  evaluation_video = videosMin50)
        else:    
            userProfile.evaluation_exercise = ejerciciosMin3
            userProfile.evaluation_video = videosMin50

        userProfile.put()        
        