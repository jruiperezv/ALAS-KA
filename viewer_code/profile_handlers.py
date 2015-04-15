'''
Created on 19/03/2013

@author: Jose
'''
from __future__ import division
from google.appengine.ext.webapp import template

from google.appengine.ext.db import GqlQuery
from viewer_code.profileviewer_models import UserProfile
from viewer_code.profileviewer_models import ViewerUser
from viewer_code.profileviewer_models import ClassMeanProfile
import viewer_code.viewer_consts
from viewer_code.classes_viewer import Utils
from google.appengine.ext import db
import webapp2
import os
import logging
import models

class ProfileView(webapp2.RequestHandler):
    def get(self):                
        usuario = models.UserData.current()
        if(usuario):
            viewerUser = ViewerUser.get_by_key_name(usuario.user_id)
        else:
            viewerUser = None
            
        if(viewerUser.professor == True):
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/profile_viewer.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/blank.html')
        
        template_values = {'viewerUsers': ViewerUser.all(),
                           'studentUsers': GqlQuery("SELECT * FROM ViewerUser WHERE student = True"),
                           'measureList': Utils().getMeasureList(),
                           'viewerUser': viewerUser
                          }
            
        self.response.out.write(template.render(path, template_values))
        
class DisplayProfile(webapp2.RequestHandler):    
    def get(self):
        # Se recogen los parametros para el perfil a mostrar
        userKeyName = self.request.get('userKeyName')
        measure = self.request.get('measure')
        
        usuario = models.UserData.current()
        if(usuario):
            viewerUser = ViewerUser.get_by_key_name(usuario.user_id)
        else:
            viewerUser = None
        # Se comprueba que todos los campos estna completos
        
        if(viewerUser.professor == True):
            if(userKeyName and measure):            
                if(int(measure)==1):
                    self.useOfPlatformMeasure(viewerUser, userKeyName)
                elif(int(measure)==2):
                    self.correctProgressMeasure(viewerUser, userKeyName)
                elif(int(measure)==3):
                    self.timeDistribution(viewerUser, userKeyName)
                elif(int(measure)==4):
                    self.gamificationHabits(viewerUser, userKeyName)
                elif(int(measure)==5):
                    self.solvingExerciseHabits(viewerUser, userKeyName)
                elif(int(measure)==6):
                    self.evaluationMeasure(viewerUser, userKeyName)
        # Cambiar cuando se quiera dejar entrar a estudiantes
        elif(viewerUser.professor == True):
            if(measure):            
                if(int(measure)==1):
                    self.useOfPlatformMeasure(viewerUser, userKeyName)
                elif(int(measure)==2):
                    self.correctProgressMeasure(viewerUser, userKeyName)
                elif(int(measure)==3):
                    self.timeDistribution(viewerUser, userKeyName)
                elif(int(measure)==4):
                    self.gamificationHabits(viewerUser, userKeyName)
                elif(int(measure)==5):
                    self.solvingExerciseHabits(viewerUser, userKeyName)
                elif(int(measure)==6):
                    self.evaluationMeasure(viewerUser, userKeyName)
                
        # Si falta algun campo se pone un plantilla en blanco
        else:
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/blank.html')
            template_values = {
                               'viewerUser': viewerUser
                               }
            self.response.out.write(template.render(path, template_values))

        # Funcion para la representacion del perfil evaluacion            
    def evaluationMeasure(self, viewerUser, userKeyName):   
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/user_profile_evaluation.html')
           
        if(viewerUser.professor == True):            
            userProfile = UserProfile.get_by_key_name(userKeyName)
        elif(viewerUser.student == True):    
            userProfile = UserProfile.get_by_key_name(viewerUser.user_id)
            
        textClusterization = []
        
        userScore = ((userProfile.evaluation_ranking)/100)    
            
        if(userScore <= 2.0):
            textClusterization.append("The student has a very low evaluation score")      
        elif(userScore > 2.0 and userScore <= 4.0):
            textClusterization.append("The student has a low evaluation score")  
        elif(userScore > 4.0 and userScore<= 6.0):
            textClusterization.append("The student has a medium evaluation score")     
        elif(userScore > 6.0 and userScore <= 8.0):
            textClusterization.append("The student has a high evaluation score")    
        elif(userScore > 8.0):
            textClusterization.append("The student has a very high evaluation score")      
            
        ranking_thereshold = 5
        
        template_values = {'userKeyName': viewerUser.user_id,
                           'userID': userProfile.user,
                           'evaluation_ranking': (userProfile.evaluation_ranking)/100,
                           'ranking_thereshold': ranking_thereshold,
                           'viewerUser': viewerUser,
                           'textClusterization': textClusterization,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                           }
        
        self.response.out.write(template.render(path, template_values))
        
        
    def useOfPlatformMeasure(self, viewerUser, userKeyName):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/user_profile_use_platform.html')
        
        if(viewerUser.professor == True):            
            userProfile = UserProfile.get_by_key_name(userKeyName)
        elif(viewerUser.student == True):    
            userProfile = UserProfile.get_by_key_name(viewerUser.user_id)
            
        textClusterization = []
        
        if(userProfile.exercise_explorer < 20):
            textClusterization.append("The student has accesed a few exercise types")       
        elif(userProfile.exercise_explorer >= 20 and userProfile.exercise_explorer <= 40):
            textClusterization.append("The student has accesed several exercise types") 
        elif(userProfile.exercise_explorer >= 41 and userProfile.exercise_explorer <= 60):
            textClusterization.append("The student has accesed a middle number of the exercise types")     
        elif(userProfile.exercise_explorer >= 61 and userProfile.exercise_explorer <= 80):
            textClusterization.append("The student has accesed many exercise types")   
        elif(userProfile.exercise_explorer > 81):
            textClusterization.append("The student has accesed the majority of the exercise types")           
            
        if(userProfile.exercise_one_correct < 20):
            textClusterization.append("The student has solved correctly a few exercise types")      
        elif(userProfile.exercise_one_correct >= 20 and userProfile.exercise_one_correct <= 40):
            textClusterization.append("The student has solved correctly several exercise types")  
        elif(userProfile.exercise_one_correct >= 41 and userProfile.exercise_one_correct <= 60):
            textClusterization.append("The student has solved correctly a middle number of the exercise types")     
        elif(userProfile.exercise_one_correct >= 61 and userProfile.exercise_one_correct <= 80):
            textClusterization.append("The student has solved correctly many exercise types")    
        elif(userProfile.exercise_one_correct > 81):
            textClusterization.append("The student has solved correctly the majority exercise types")                     
                                         
        if(userProfile.exercise_abandon < 20):
            textClusterization.append("The student has abandoned a few exercises without achieving proficiency")      
        elif(userProfile.exercise_abandon >= 20 and userProfile.exercise_abandon <= 40):
            textClusterization.append("The student has abandoned several exercises without achieving proficiency")  
        elif(userProfile.exercise_abandon >= 41 and userProfile.exercise_abandon <= 60):
            textClusterization.append("The student has abandoned a middle number of the exercises without achieving proficiency")     
        elif(userProfile.exercise_abandon >= 61 and userProfile.exercise_abandon <= 80):
            textClusterization.append("The student has abandoned many exercises without achieving proficiency")    
        elif(userProfile.exercise_abandon > 81):
            textClusterization.append("The student has abandoned the majority of the exercises without achieving proficiency")
                        
        if(userProfile.video_explorer < 20):
            textClusterization.append("The student has accesed a few videos")
        elif(userProfile.video_explorer >= 20 and userProfile.video_explorer <= 40):
            textClusterization.append("The student has accesed several videos")
        elif(userProfile.video_explorer >= 41 and userProfile.video_explorer <= 60):
            textClusterization.append("The student has accesed a middle number of the videos")     
        elif(userProfile.video_explorer >= 61 and userProfile.video_explorer <= 80):
            textClusterization.append("The student has accesed many videos")    
        elif(userProfile.video_explorer > 81):
            textClusterization.append("The student has accesed the majority of the videos")    
            
        if(userProfile.video_abandon < 20):
            textClusterization.append("The student has abandoned a few videos without finishing them")      
        elif(userProfile.video_abandon >= 20 and userProfile.video_abandon <= 40):
            textClusterization.append("The student has abandoned several videos without finishing them")  
        elif(userProfile.video_abandon >= 41 and userProfile.video_abandon <= 60):
            textClusterization.append("The student has abandoned around half of the videos without finishing them")   
        elif(userProfile.video_abandon >= 61 and userProfile.video_abandon <= 80):
            textClusterization.append("The student has abandoned many videos without finishing them")  
        elif(userProfile.video_abandon > 81):
            textClusterization.append("The student has abandoned the majority of the videos without finishing them")   
                   
        if(userProfile.focus_videos >= 65):
            textClusterization.append("The student focus his/her learning on watching videos")       
        elif(userProfile.focus_exercises >= 65):
            textClusterization.append("The student focus his/her learning on making exercises")
        else:                
            textClusterization.append("The user does not have a clear focus profile on videos or exercises")            
                        
        if(userProfile.optional_elements == 0):
            textClusterization.append("The student has not used optional elements")        
        elif(userProfile.optional_elements > 0):
            textClusterization.append("The student has made use of optional elements")        
                            
        classMean_exercise_explorer = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EXERCISE_EXPLORER)                        
        classMean_video_explorer = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.VIDEO_EXPLORER)
        classMean_exercise_abandon = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EXERCISE_ABANDON)
        classMean_video_abandon = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.VIDEO_ABANDON)
        classMean_optional = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.OPTIONAL_ELEMENTS)
        classMean_one_correct = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EXERCISE_ONE_CORRECT)
        classMean_focus_exercise = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.FOCUS_EXERCISES)
        classMean_focus_video = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.FOCUS_VIDEOS)

        template_values = {'userKeyName': viewerUser.user_id,
                           'userID': viewerUser.user,
                           'userProfile': userProfile,
                           'video_explorer_mean': classMean_video_explorer.mean_value,
                           'exercise_explorer_mean': classMean_exercise_explorer.mean_value,
                           'video_abandon_mean': classMean_video_abandon.mean_value,
                           'exercise_abandon_mean': classMean_exercise_abandon.mean_value,
                           'optional_elements_mean': classMean_optional.mean_value,
                           'one_correct_mean': classMean_one_correct.mean_value,
                           'focus_exercise_mean': classMean_focus_exercise.mean_value,
                           'focus_video_mean': classMean_focus_video.mean_value,
                           'viewerUser': viewerUser,
                           'textClusterization': textClusterization,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                           }
    
        self.response.out.write(template.render(path, template_values))
        
    def correctProgressMeasure(self, viewerUser, userKeyName):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/user_profile_correct_progress.html')
        
        if(viewerUser.professor == True):            
            userProfile = UserProfile.get_by_key_name(userKeyName)
        elif(viewerUser.student == True):    
            userProfile = UserProfile.get_by_key_name(viewerUser.user_id)
            
        textClusterization = []
            
        if(userProfile.exercise_progress < 20):
            textClusterization.append("The student has made a very low progress on solving exercises")
        elif(userProfile.exercise_progress >= 20 and userProfile.exercise_progress <= 40):
            textClusterization.append("The student has made a low progress on solving exercises")
        elif(userProfile.exercise_progress >= 41 and userProfile.exercise_progress <= 60):
            textClusterization.append("The student has made a medium progress on solving exercises")     
        elif(userProfile.exercise_progress >= 61 and userProfile.exercise_progress <= 80):
            textClusterization.append("The student has made a high progress on solving exercises")    
        elif(userProfile.exercise_progress > 81):
            textClusterization.append("The student has made a very high progress on solving exercises") 
            
        if(userProfile.correct_exercise_solving_efficiency < 15):
            textClusterization.append("The student has a very low efficiency solving exercise correctly")      
        elif(userProfile.correct_exercise_solving_efficiency >= 15 and userProfile.correct_exercise_solving_efficiency <= 34):
            textClusterization.append("The student has a low efficiency solving exercise correctly")  
        elif(userProfile.correct_exercise_solving_efficiency >= 35 and userProfile.correct_exercise_solving_efficiency <= 54):
            textClusterization.append("The student has a medium efficiency solving exercise correctly")     
        elif(userProfile.correct_exercise_solving_efficiency >= 53 and userProfile.correct_exercise_solving_efficiency <= 72):
            textClusterization.append("The student has a high efficiency solving exercise correctly")    
        elif(userProfile.correct_exercise_solving_efficiency > 73):
            textClusterization.append("The student has a very high efficiency solving exercise correctly")   

        if(userProfile.video_progress < 20):
            textClusterization.append("The student has made a very low progress on watching videos")      
        elif(userProfile.video_progress >= 20 and userProfile.video_progress <= 40):
            textClusterization.append("The student has made a low progress on watching videos")  
        elif(userProfile.video_progress >= 41 and userProfile.video_progress <= 60):
            textClusterization.append("The student has made a medium progress on watching videos")     
        elif(userProfile.video_progress >= 61 and userProfile.video_progress <= 80):
            textClusterization.append("The student has made a high progress on watching videos")    
        elif(userProfile.video_progress > 81):
            textClusterization.append("The student has made a very high progress on watching videos")
                    
        if(userProfile.video_efficiency < 20):
            textClusterization.append("The student has a very low efficiency watching videos")      
        elif(userProfile.video_efficiency >= 20 and userProfile.video_efficiency <= 40):
            textClusterization.append("The student has a low efficiency watching videos")  
        elif(userProfile.video_efficiency >= 41 and userProfile.video_efficiency <= 60):
            textClusterization.append("The student has a medium efficiency watching videos")     
        elif(userProfile.video_efficiency >= 61 and userProfile.video_efficiency <= 80):
            textClusterization.append("The student has a high efficiency watching videos")    
        elif(userProfile.video_efficiency > 81):
            textClusterization.append("The student has a very high efficiency watching videos")    
                                
        classMean_video_efficiency = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.VIDEO_EFFICIENCY)                        
        classMean_exercise_efficiency = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.CORRECT_EXERCISE_EFFICIENCY)
        classMean_exercise_progress = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EXERCISE_PROGRESS)
        classMean_video_progress = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.VIDEO_PROGRESS)
        classMean_correct_exercise = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.CORRECT_EXERCISES)
        classMean_efficiency_proficiencies = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EFFICIENCY_PROFICIENCIES)
        classMean_solving_efficiency= ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.CORRECT_SOLVING_EXERCISE_EFFICIENCY)
        
       
        template_values = {'userKeyName': viewerUser.user_id,
                           'userID': viewerUser.user,
                           'userProfile': userProfile,
                           'classMean_video_efficiency': classMean_video_efficiency.mean_value,
                           'classMean_exercise_efficiency': classMean_exercise_efficiency.mean_value,
                           'classMean_exercise_progress': classMean_exercise_progress.mean_value,
                           'classMean_video_progress': classMean_video_progress.mean_value,
                           'classMean_correct_exercise': classMean_correct_exercise.mean_value,
                           'classMean_efficiency_proficiencies': classMean_efficiency_proficiencies.mean_value,
                           'classMean_solving_efficiency': classMean_solving_efficiency.mean_value,
                           'viewerUser': viewerUser,
                           'textClusterization': textClusterization,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                           }
    
        self.response.out.write(template.render(path, template_values))
                
    def timeDistribution(self, viewerUser, userKeyName):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/user_profile_time_distribution.html')
        
        if(viewerUser.professor == True):            
            userProfile = UserProfile.get_by_key_name(userKeyName)
        elif(viewerUser.student == True):    
            userProfile = UserProfile.get_by_key_name(viewerUser.user_id)
            
        textClusterization = []   
            
        if(userProfile.time_schedule_morning >= 65):
            textClusterization.append("The student has a morning schedule profile")     
        elif(userProfile.time_schedule_afternoon >= 65):
            textClusterization.append("The student has a afternoon schedule profile")  
        elif(userProfile.time_schedule_night >= 65):
            textClusterization.append("The student has a night schedule profile")       
        else:
            textClusterization.append("The student does not have a clear schedule profile")      
        
        scheduleEfficiency = ""
        
        if(userProfile.morning_schedule_efficiency == 0):
            scheduleEfficiency += ("The student does not have a morning efficiency, ")
        elif(userProfile.morning_schedule_efficiency < 50):
            scheduleEfficiency += ("The student has a very low morning efficiency, ")      
        elif(userProfile.morning_schedule_efficiency >= 50 and userProfile.morning_schedule_efficiency <= 65):
            scheduleEfficiency += ("The student has a low morning efficiency, ")  
        elif(userProfile.morning_schedule_efficiency >= 65 and userProfile.morning_schedule_efficiency <= 80):
            scheduleEfficiency += ("The student has a medium morning efficiency, ")     
        elif(userProfile.morning_schedule_efficiency >= 81 and userProfile.morning_schedule_efficiency <= 92):
            scheduleEfficiency += ("The student has a high morning efficiency, ")    
        elif(userProfile.morning_schedule_efficiency > 92):
            scheduleEfficiency += ("The student has a very high morning efficiency, ")   
                
        if(userProfile.afternoon_schedule_efficiency == 0):
            scheduleEfficiency += ("no afternoon efficiency and ")
        elif(userProfile.afternoon_schedule_efficiency < 50):
            scheduleEfficiency += ("a very low afternoon efficiency and ")      
        elif(userProfile.afternoon_schedule_efficiency >= 50 and userProfile.afternoon_schedule_efficiency <= 65):
            scheduleEfficiency += ("a low afternoon efficiency and ")  
        elif(userProfile.afternoon_schedule_efficiency >= 65 and userProfile.afternoon_schedule_efficiency <= 80):
            scheduleEfficiency += ("a medium afternoon efficiency and ")     
        elif(userProfile.afternoon_schedule_efficiency >= 81 and userProfile.afternoon_schedule_efficiency <= 92):
            scheduleEfficiency += ("a high afternoon efficiency and ")    
        elif(userProfile.afternoon_schedule_efficiency > 92):
            scheduleEfficiency += ("a very high afternoon efficiency and ")     
                
        if(userProfile.night_schedule_efficiency == 0):
            scheduleEfficiency += ("no night efficiency")
        elif(userProfile.night_schedule_efficiency < 50):
            scheduleEfficiency += ("a very low night efficiency")
        elif(userProfile.night_schedule_efficiency >= 50 and userProfile.night_schedule_efficiency <= 65):
            scheduleEfficiency += ("a low night efficiency")  
        elif(userProfile.night_schedule_efficiency >= 65 and userProfile.night_schedule_efficiency <= 80):
            scheduleEfficiency += ("a medium night efficiency")     
        elif(userProfile.night_schedule_efficiency >= 81 and userProfile.night_schedule_efficiency <= 92):
            scheduleEfficiency += ("a high night efficiency")    
        elif(userProfile.night_schedule_efficiency > 92):
            scheduleEfficiency += ("a very high night efficiency")  
            
        textClusterization.append(scheduleEfficiency)
                    
        classMean_time_morning = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.TIME_SCHEDULE_MORNING)                        
        classMean_time_afternoon = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.TIME_SCHEDULE_AFTERNOON)
        classMean_time_night = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.TIME_SCHEDULE_NIGHT)    
        classMean_constancy_mean = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.CONSTANCY_MEAN)
        classMean_constancy_var = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.CONSTANCY_VARIANCE)
        classMean_efficiency_morning = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_MORNING)
        classMean_efficiency_afternoon = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_AFTERNOON)
        classMean_efficiency_night = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_NIGHT)
        classMean_efficiency_average = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.CORRECT_EXERCISES)
        
        template_values = {'userKeyName': viewerUser.user_id,
                           'userID': viewerUser.user,
                           'userProfile': userProfile,
                           'classMean_time_morning': classMean_time_morning.mean_value,
                           'classMean_time_afternoon': classMean_time_afternoon.mean_value,
                           'classMean_time_night': classMean_time_night.mean_value,
                           'classMean_constancy_mean': classMean_constancy_mean.mean_value,
                           'classMean_constancy_var': classMean_constancy_var.mean_value,
                           'classMean_efficiency_morning': classMean_efficiency_morning.mean_value,
                           'classMean_efficiency_afternoon': classMean_efficiency_afternoon.mean_value,
                           'classMean_efficiency_night': classMean_efficiency_night.mean_value,
                           'classMean_efficiency_average': classMean_efficiency_average.mean_value,
                           'viewerUser': viewerUser,
                           'textClusterization': textClusterization,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                           }
    
        self.response.out.write(template.render(path, template_values))
        
        
    def solvingExerciseHabits(self, viewerUser, userKeyName):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/user_profile_solving_exercise_habits.html')
        
        if(viewerUser.professor == True):            
            userProfile = UserProfile.get_by_key_name(userKeyName)
        elif(viewerUser.student == True):    
            userProfile = UserProfile.get_by_key_name(viewerUser.user_id)
            
        textClusterization = []
            
        if(userProfile.recommendation_listener < 15):
            textClusterization.append("The student has a very low recommendation listener profile")      
        elif(userProfile.recommendation_listener >= 16 and userProfile.recommendation_listener <= 35):
            textClusterization.append("The student has a low recommendation listener profile")  
        elif(userProfile.recommendation_listener >= 36 and userProfile.recommendation_listener <= 53):
            textClusterization.append("The student has a medium recommendation listener profile")   
        elif(userProfile.recommendation_listener >= 54 and userProfile.recommendation_listener <= 72):
            textClusterization.append("The student has a high recommendation listener profile")       
        elif(userProfile.recommendation_listener > 73):
            textClusterization.append("The student has a very high recommendation listener profile")        
            
        if(userProfile.forgetful_exercises < 5):
            textClusterization.append("The student has a very low forgetful exercises profile")      
        elif(userProfile.forgetful_exercises >= 5 and userProfile.forgetful_exercises <= 14):
            textClusterization.append("The student has a low forgetful exercises profile")  
        elif(userProfile.forgetful_exercises >= 15 and userProfile.forgetful_exercises <= 23):
            textClusterization.append("The student has a medium forgetful exercises profile")     
        elif(userProfile.forgetful_exercises >= 24 and userProfile.forgetful_exercises <= 32):
            textClusterization.append("The student has a high forgetful exercises profile")     
        elif(userProfile.forgetful_exercises > 32):
            textClusterization.append("The student has a very high forgetful exercises profile")             
            
        if(userProfile.hint_avoidance < 6):
            textClusterization.append("The student has a very low hint avoidance profile")      
        elif(userProfile.hint_avoidance >= 6 and userProfile.hint_avoidance <= 11):
            textClusterization.append("The student has a low hint avoidance profile")  
        elif(userProfile.hint_avoidance >= 12 and userProfile.hint_avoidance <= 17):
            textClusterization.append("The student has a medium hint avoidance profile")     
        elif(userProfile.hint_avoidance >= 18 and userProfile.hint_avoidance <= 23):
            textClusterization.append("The student has a high hint avoidance profile")     
        elif(userProfile.hint_avoidance > 24):
            textClusterization.append("The student has a very high hint avoidance profile") 
            
        if(userProfile.video_avoidance < 6):
            textClusterization.append("The student has a very low video avoidance profile")      
        elif(userProfile.video_avoidance >= 6 and userProfile.video_avoidance <= 11):
            textClusterization.append("The student has a low video avoidance profile")  
        elif(userProfile.video_avoidance >= 12 and userProfile.video_avoidance <= 17):
            textClusterization.append("The student has a medium video avoidance profile")     
        elif(userProfile.video_avoidance >= 18 and userProfile.video_avoidance <= 23):
            textClusterization.append("The student has a high video avoidance profile")     
        elif(userProfile.video_avoidance > 24):
            textClusterization.append("The student has a very high video avoidance profile") 
            
        if(userProfile.unreflective_user < 6):
            textClusterization.append("The student has a very low unreflective user profile")      
        elif(userProfile.unreflective_user >= 6 and userProfile.unreflective_user <= 11):
            textClusterization.append("The student has a low unreflective user profile")  
        elif(userProfile.unreflective_user >= 12 and userProfile.unreflective_user <= 17):
            textClusterization.append("The student has a medium unreflective user profile")     
        elif(userProfile.unreflective_user >= 18 and userProfile.unreflective_user <= 23):
            textClusterization.append("The student has a high unreflective user profile")     
        elif(userProfile.unreflective_user > 24):
            textClusterization.append("The student has a very high unreflective user profile") 
            
        if(userProfile.hint_abuser < 6):
            textClusterization.append("The student has a very low hint abuser profile")      
        elif(userProfile.hint_abuser >= 6 and userProfile.hint_abuser <= 11):
            textClusterization.append("The student has a low hint abuser profile")  
        elif(userProfile.hint_abuser >= 12 and userProfile.hint_abuser <= 17):
            textClusterization.append("The student has a medium hint abuser profile")     
        elif(userProfile.hint_abuser >= 18 and userProfile.hint_abuser <= 23):
            textClusterization.append("The student has a high hint abuser profile")     
        elif(userProfile.hint_abuser > 24):
            textClusterization.append("The student has a very high hint abuser profile")      
                    
        classMean_recommendation_listener = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.RECOMMENDATION_LISTENER)                        
        classMean_forgetful_exercises = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.FORGETFUL_EXERCISES)
        classMean_hint_avoidance = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.HINT_AVOIDANCE)
        classMean_video_avoidance = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.VIDEO_AVOIDANCE)
        classMean_unreflective_user = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.UNREFLECTIVE_USER)
        classMean_hint_abuser = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.HINT_ABUSER)
                    
        template_values = {'userKeyName': viewerUser.user_id,
                           'userID': viewerUser.user,
                           'userProfile': userProfile,
                           'classMean_recommendation_listener': classMean_recommendation_listener.mean_value,
                           'classMean_forgetful_exercises': classMean_forgetful_exercises.mean_value,
                           'classMean_hint_avoidance': classMean_hint_avoidance.mean_value,
                           'classMean_video_avoidance': classMean_video_avoidance.mean_value,
                           'classMean_unreflective_user': classMean_unreflective_user.mean_value,
                           'classMean_hint_abuser': classMean_hint_abuser.mean_value,
                           'viewerUser': viewerUser,
                           'textClusterization': textClusterization,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                           }
    
        self.response.out.write(template.render(path, template_values))
        
    def gamificationHabits(self, viewerUser, userKeyName):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/user_profile_gamification_habits.html')
        
        if(viewerUser.professor == True):            
            userProfile = UserProfile.get_by_key_name(userKeyName)
        elif(viewerUser.student == True):    
            userProfile = UserProfile.get_by_key_name(viewerUser.user_id)
           
        textClusterization = []     
            
        if(userProfile.badge_over_time < 2):
            textClusterization.append("The student has a very low motivation on winning badges")   
        elif(userProfile.badge_over_time >= 2 and userProfile.badge_over_time <= 3):
            textClusterization.append("The student has a low motivation on winning badges")  
        elif(userProfile.badge_over_time >= 4 and userProfile.badge_over_time <= 6):
            textClusterization.append("The student has a medium motivation on winning badges")  
        elif(userProfile.badge_over_time >= 7 and userProfile.badge_over_time <= 10):
            textClusterization.append("The student has a high motivation on winning badges")  
        elif(userProfile.badge_over_time > 10):
            textClusterization.append("The student has a very high motivation on winning badges")  
            
        if(userProfile.badge_point_percentage < 5):
            textClusterization.append("The student has a very low point percentage of badges")      
        elif(userProfile.badge_point_percentage >= 5 and userProfile.badge_point_percentage <= 11):
            textClusterization.append("The student has a low point percentage of badges")  
        elif(userProfile.badge_point_percentage >= 12 and userProfile.badge_point_percentage <= 18):
            textClusterization.append("The student has a medium point percentage of badges")     
        elif(userProfile.badge_point_percentage >= 19 and userProfile.badge_point_percentage <= 25):
            textClusterization.append("The student has a high point percentage of badges")     
        elif(userProfile.badge_point_percentage > 25):
            textClusterization.append("The student has a very high point percentage of badges")  
                    
        classMean_badge_over_time = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.BADGES_OVER_TIME)                        
        classMean_point_percentage = ClassMeanProfile.get_by_key_name(viewer_code.viewer_consts.BADGE_POINTS_PERCENTAGE)
                    
        template_values = {'userKeyName': viewerUser.user_id,
                           'userID': viewerUser.user,
                           'userProfile': userProfile,
                           'classMean_badge_over_time': classMean_badge_over_time.mean_value,
                           'classMean_point_percentage': classMean_point_percentage.mean_value,
                           'viewerUser': viewerUser,
                           'textClusterization': textClusterization,
                           'descriptionList': viewer_code.viewer_consts.DESCRIPTION_LIST
                           }
    
        self.response.out.write(template.render(path, template_values))        
        