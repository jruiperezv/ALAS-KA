'''
Created on 19/03/2013

@author: Jose
'''
from __future__ import division
from google.appengine.ext.webapp import template

from viewer_code.profileviewer_models import UserProfile
from viewer_code.profileviewer_models import ViewerUser
from google.appengine.ext.db import GqlQuery
import viewer_code.viewer_consts
from viewer_code.classes_viewer import Utils
import webapp2
import os
import models

class ClassView(webapp2.RequestHandler):
    def get(self):
                 
        usuario = models.UserData.current()
        if(usuario):
            viewerUser = ViewerUser.get_by_key_name(usuario.user_id)
        else:
            viewerUser = None 
            
        if(viewerUser.professor == True):
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_viewer.html')
        else:
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/blank.html')
         
        template_values = {
                           'measureList': Utils().getMeasureList(),
                           'viewerUser': viewerUser
                          }
            
        self.response.out.write(template.render(path, template_values))

class DisplayClass(webapp2.RequestHandler):
    def get(self):
        
        # Se recogen los parametros para el perfil a mostrar
        measure = self.request.get('measure')
        
        usuario = models.UserData.current()
        if(usuario):
            viewerUser = ViewerUser.get_by_key_name(usuario.user_id)
        else:
            viewerUser = None
                    
        # Se comprueba que todos los campos estna completos
        if(measure and viewerUser.professor == True):                        
            if(int(measure)==1):
                self.useOfPlatformMeasure(measure)
            elif(int(measure)==2):
                self.correctProgress(measure)
            elif(int(measure)==3):
                self.timeDistribution(measure)
            elif(int(measure)==4):
                self.gamificationHabits(measure)
            elif(int(measure)==5):
                self.solvingExerciseHabits(measure)
            elif(int(measure)==6):
                self.evaluationMeasure(measure)
                
        # Si falta algun campo se pone un plantilla en blanco
        else:
            path = os.path.join(os.path.dirname(__file__), 'viewer_templates/blank.html')
            template_values = None
            self.response.out.write(template.render(path, template_values))
            
    def evaluationMeasureOLD(self, measure):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_profile_evaluation.html')
        
        userProfiles = GqlQuery("SELECT * FROM UserProfile") 
       
        exerciseThereshold = 50
        videoThereshold = 70
       
        exercisePass = 0
        videoPass = 0
        userPassCourse = 0
        
        pass_course_users = []
        fail_course_users = []
    
        for userProfile in userProfiles:
            if(userProfile.evaluation_exercise >= exerciseThereshold):
                exercisePass += 1
           
            if(userProfile.evaluation_video >= videoThereshold):
                videoPass += 1
               
            if(userProfile.evaluation_video >= videoThereshold and userProfile.evaluation_exercise >= exerciseThereshold):
                userPassCourse += 1
                pass_course_users.append(userProfile)
            else:
                fail_course_users.append(userProfile)
                
        template_values = {'exercisePass': exercisePass,
                           'exerciseFail': userProfiles.count() - exercisePass,
                           'videoPass': videoPass,
                           'videoFail': userProfiles.count() - videoPass,
                           'userPassCourse': userPassCourse,
                           'userFailCourse': userProfiles.count() - userPassCourse,
                           'measureList': Utils().getMeasureList(),
                           'passCourseUsers': pass_course_users,
                           'failCourseUsers': fail_course_users
                          }
        
        self.response.out.write(template.render(path, template_values))
        
    def evaluationMeasure(self, measure):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_profile_evaluation.html')
        
        userProfiles = GqlQuery("SELECT * FROM UserProfile") 
       
        rankingUsers = []
        ranking_groups = [0, 0, 0, 0, 0]
        for userProfile in userProfiles:
            userScore = ((userProfile.evaluation_ranking)/100)
                        
            rankingUsers.append((userProfile.user_id, userScore))
            
            if(userScore <= 2.0):
                ranking_groups[0] += 1      
            elif(userScore > 2.0 and userScore <= 4.0):
                ranking_groups[1] += 1  
            elif(userScore > 4.0 and userScore<= 6.0):
                ranking_groups[2] += 1     
            elif(userScore > 6.0 and userScore <= 8.0):
                ranking_groups[3] += 1    
            elif(userScore > 8.0):
                ranking_groups[4] += 1      
            
        rankingUsers.sort(key=lambda tup: tup[1], reverse=True)
                            
        template_values = {
                           'rankingUsers': rankingUsers,
                           'ranking_groups': ranking_groups
                          }
        
        self.response.out.write(template.render(path, template_values))
        
    def useOfPlatformMeasure(self, measure):
        
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_profile_use_platform.html')
        
        userProfiles = GqlQuery("SELECT * FROM UserProfile") 
        
        exercise_explorer_groups = [0, 0, 0, 0, 0]
        video_explorer_groups = [0, 0, 0, 0, 0]
        exercise_abandon_groups = [0, 0, 0, 0, 0]
        video_abandon_groups = [0, 0, 0, 0, 0]
        exercise_one_correct_groups = [0, 0, 0, 0, 0]
        optional_elements_groups = [0, 0]
        focus_groups = [0, 0, 0]
        
        for userProfile in userProfiles:
            if(userProfile.video_explorer < 20):
                video_explorer_groups[0] += 1      
            elif(userProfile.video_explorer >= 20 and userProfile.video_explorer <= 40):
                video_explorer_groups[1] += 1  
            elif(userProfile.video_explorer >= 41 and userProfile.video_explorer <= 60):
                video_explorer_groups[2] += 1     
            elif(userProfile.video_explorer >= 61 and userProfile.video_explorer <= 80):
                video_explorer_groups[3] += 1    
            elif(userProfile.video_explorer > 81):
                video_explorer_groups[4] += 1                     
                
            if(userProfile.exercise_explorer < 20):
                exercise_explorer_groups[0] += 1      
            elif(userProfile.exercise_explorer >= 20 and userProfile.exercise_explorer <= 40):
                exercise_explorer_groups[1] += 1  
            elif(userProfile.exercise_explorer >= 41 and userProfile.exercise_explorer <= 60):
                exercise_explorer_groups[2] += 1     
            elif(userProfile.exercise_explorer >= 61 and userProfile.exercise_explorer <= 80):
                exercise_explorer_groups[3] += 1    
            elif(userProfile.exercise_explorer > 81):
                exercise_explorer_groups[4] += 1                   
                
            if(userProfile.exercise_abandon < 20):
                exercise_abandon_groups[0] += 1      
            elif(userProfile.exercise_abandon >= 20 and userProfile.exercise_abandon <= 40):
                exercise_abandon_groups[1] += 1  
            elif(userProfile.exercise_abandon >= 41 and userProfile.exercise_abandon <= 60):
                exercise_abandon_groups[2] += 1     
            elif(userProfile.exercise_abandon >= 61 and userProfile.exercise_abandon <= 80):
                exercise_abandon_groups[3] += 1    
            elif(userProfile.exercise_abandon > 81):
                exercise_abandon_groups[4] += 1  
                
            if(userProfile.video_abandon < 20):
                video_abandon_groups[0] += 1      
            elif(userProfile.video_abandon >= 20 and userProfile.video_abandon <= 40):
                video_abandon_groups[1] += 1  
            elif(userProfile.video_abandon >= 41 and userProfile.video_abandon <= 60):
                video_abandon_groups[2] += 1     
            elif(userProfile.video_abandon >= 61 and userProfile.video_abandon <= 80):
                video_abandon_groups[3] += 1    
            elif(userProfile.video_abandon > 81):
                video_abandon_groups[4] += 1  
                
            if(userProfile.exercise_one_correct < 20):
                exercise_one_correct_groups[0] += 1      
            elif(userProfile.exercise_one_correct >= 20 and userProfile.exercise_one_correct <= 40):
                exercise_one_correct_groups[1] += 1  
            elif(userProfile.exercise_one_correct >= 41 and userProfile.exercise_one_correct <= 60):
                exercise_one_correct_groups[2] += 1     
            elif(userProfile.exercise_one_correct >= 61 and userProfile.exercise_one_correct <= 80):
                exercise_one_correct_groups[3] += 1    
            elif(userProfile.exercise_one_correct > 81):
                exercise_one_correct_groups[4] += 1  
                
            if(userProfile.optional_elements == 0):
                optional_elements_groups[0] += 1        
            elif(userProfile.optional_elements > 0):
                optional_elements_groups[1] += 1  
                
            if(userProfile.focus_videos >= 65):
                # Focus videos
                focus_groups[0] += 1        
            elif(userProfile.focus_exercises >= 65):
                # Focus exercises
                focus_groups[1] += 1  
            else:
                # No focus
                focus_groups[2] += 1  
                      
        template_values = {'exercise_explorer_groups': exercise_explorer_groups,
                           'video_explorer_groups': video_explorer_groups,
                           'video_abandon_groups': video_abandon_groups,
                           'exercise_abandon_groups': exercise_abandon_groups,
                           'exercise_one_correct_groups': exercise_one_correct_groups,
                           'optional_elements_groups': optional_elements_groups,
                           'focus_groups': focus_groups
                           }
        
        self.response.out.write(template.render(path, template_values))
        
    def correctProgress(self, measure):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_profile_correct_progress.html')
        
        userProfiles = GqlQuery("SELECT * FROM UserProfile") 
                
        exercise_progress_groups = [0, 0, 0, 0, 0]
        video_progress_groups = [0, 0, 0, 0, 0]  
        #exercise_efficiency_groups = [0, 0, 0, 0]  
        video_efficiency_groups = [0, 0, 0, 0, 0]
        #correct_exercises_groups = [0, 0, 0, 0]  
        #efficiency_proficiencies_groups = [0, 0, 0, 0]   
        solving_efficiency_groups = [0, 0, 0, 0, 0]  
        
        for userProfile in userProfiles:
            
            if(userProfile.exercise_progress < 20):
                exercise_progress_groups[0] += 1      
            elif(userProfile.exercise_progress >= 20 and userProfile.exercise_progress <= 40):
                exercise_progress_groups[1] += 1  
            elif(userProfile.exercise_progress >= 41 and userProfile.exercise_progress <= 60):
                exercise_progress_groups[2] += 1     
            elif(userProfile.exercise_progress >= 61 and userProfile.exercise_progress <= 80):
                exercise_progress_groups[3] += 1    
            elif(userProfile.exercise_progress > 81):
                exercise_progress_groups[4] += 1  

            if(userProfile.video_progress < 20):
                video_progress_groups[0] += 1      
            elif(userProfile.video_progress >= 20 and userProfile.video_progress <= 40):
                video_progress_groups[1] += 1  
            elif(userProfile.video_progress >= 41 and userProfile.video_progress <= 60):
                video_progress_groups[2] += 1     
            elif(userProfile.video_progress >= 61 and userProfile.video_progress <= 80):
                video_progress_groups[3] += 1    
            elif(userProfile.video_progress > 81):
                video_progress_groups[4] += 1     
            """   
            if(userProfile.correct_exercise_effiency < 50):
                exercise_efficiency_groups[0] += 1      
            elif(userProfile.correct_exercise_effiency >= 50 and userProfile.correct_exercise_effiency <= 100):
                exercise_efficiency_groups[1] += 1  
            elif(userProfile.correct_exercise_effiency >= 101 and userProfile.correct_exercise_effiency <= 200):
                exercise_efficiency_groups[2] += 1     
            elif(userProfile.correct_exercise_effiency > 200):
                exercise_efficiency_groups[3] += 1 
            """
            if(userProfile.video_efficiency < 20):
                video_efficiency_groups[0] += 1      
            elif(userProfile.video_efficiency >= 20 and userProfile.video_efficiency <= 40):
                video_efficiency_groups[1] += 1  
            elif(userProfile.video_efficiency >= 41 and userProfile.video_efficiency <= 60):
                video_efficiency_groups[2] += 1     
            elif(userProfile.video_efficiency >= 61 and userProfile.video_efficiency <= 80):
                video_efficiency_groups[3] += 1    
            elif(userProfile.video_efficiency > 81):
                video_efficiency_groups[4] += 1      
            """
            if(userProfile.correct_exercises < 40):
                correct_exercises_groups[0] += 1      
            elif(userProfile.correct_exercises >= 40 and userProfile.correct_exercises <= 65):
                correct_exercises_groups[1] += 1  
            elif(userProfile.correct_exercises >= 66 and userProfile.correct_exercises <= 85):
                correct_exercises_groups[2] += 1     
            elif(userProfile.correct_exercises > 85):
                correct_exercises_groups[3] += 1  
                
            if(userProfile.efficiency_proficiencies < 25):
                efficiency_proficiencies_groups[0] += 1      
            elif(userProfile.efficiency_proficiencies >= 25 and userProfile.efficiency_proficiencies <= 50):
                efficiency_proficiencies_groups[1] += 1  
            elif(userProfile.efficiency_proficiencies >= 51 and userProfile.efficiency_proficiencies <= 75):
                efficiency_proficiencies_groups[2] += 1     
            elif(userProfile.efficiency_proficiencies > 75):
                efficiency_proficiencies_groups[3] += 1   
            """   
            if(userProfile.correct_exercise_solving_efficiency < 15):
                solving_efficiency_groups[0] += 1      
            elif(userProfile.correct_exercise_solving_efficiency >= 15 and userProfile.correct_exercise_solving_efficiency <= 34):
                solving_efficiency_groups[1] += 1  
            elif(userProfile.correct_exercise_solving_efficiency >= 35 and userProfile.correct_exercise_solving_efficiency <= 54):
                solving_efficiency_groups[2] += 1     
            elif(userProfile.correct_exercise_solving_efficiency >= 53 and userProfile.correct_exercise_solving_efficiency <= 72):
                solving_efficiency_groups[3] += 1    
            elif(userProfile.correct_exercise_solving_efficiency > 73):
                solving_efficiency_groups[4] += 1                
                
        template_values = {
                           'exercise_progress_groups': exercise_progress_groups,
                           'video_progress_groups': video_progress_groups,
                           #'exercise_efficiency_groups': exercise_efficiency_groups,
                           'video_efficiency_groups': video_efficiency_groups,
                           #'correct_exercises_groups': correct_exercises_groups,
                           #'efficiency_proficiencies_groups': efficiency_proficiencies_groups,
                           'solving_efficiency_groups': solving_efficiency_groups               
                          }
        
        self.response.out.write(template.render(path, template_values))
                
    def timeDistribution(self, measure):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_profile_time_distribution.html')
        
        userProfiles = GqlQuery("SELECT * FROM UserProfile") 
                
        time_profiling_groups = [0, 0, 0, 0]
        
        morning_efficiency_groups = [0, 0, 0, 0, 0]
        afternoon_efficiency_groups = [0, 0, 0, 0, 0]
        night_efficiency_groups = [0, 0, 0, 0, 0]
        
        for userProfile in userProfiles:
            if(userProfile.time_schedule_morning >= 65):
                time_profiling_groups[0] += 1      
            elif(userProfile.time_schedule_afternoon >= 65):
                time_profiling_groups[1] += 1  
            elif(userProfile.time_schedule_night >= 65):
                time_profiling_groups[2] += 1       
            else:
                time_profiling_groups[3] += 1      
            
            if(userProfile.morning_schedule_efficiency != 0):
                if(userProfile.morning_schedule_efficiency < 50):
                    morning_efficiency_groups[0] += 1      
                elif(userProfile.morning_schedule_efficiency >= 50 and userProfile.morning_schedule_efficiency <= 65):
                    morning_efficiency_groups[1] += 1  
                elif(userProfile.morning_schedule_efficiency >= 65 and userProfile.morning_schedule_efficiency <= 80):
                    morning_efficiency_groups[2] += 1     
                elif(userProfile.morning_schedule_efficiency >= 81 and userProfile.morning_schedule_efficiency <= 92):
                    morning_efficiency_groups[3] += 1    
                elif(userProfile.morning_schedule_efficiency > 92):
                    morning_efficiency_groups[4] += 1   
                    
            if(userProfile.afternoon_schedule_efficiency != 0):
                if(userProfile.afternoon_schedule_efficiency < 50):
                    afternoon_efficiency_groups[0] += 1      
                elif(userProfile.afternoon_schedule_efficiency >= 50 and userProfile.afternoon_schedule_efficiency <= 65):
                    afternoon_efficiency_groups[1] += 1  
                elif(userProfile.afternoon_schedule_efficiency >= 65 and userProfile.afternoon_schedule_efficiency <= 80):
                    afternoon_efficiency_groups[2] += 1     
                elif(userProfile.afternoon_schedule_efficiency >= 81 and userProfile.afternoon_schedule_efficiency <= 92):
                    afternoon_efficiency_groups[3] += 1    
                elif(userProfile.afternoon_schedule_efficiency > 92):
                    afternoon_efficiency_groups[4] += 1     
                    
            if(userProfile.night_schedule_efficiency != 0):
                if(userProfile.night_schedule_efficiency < 50):
                    night_efficiency_groups[0] += 1
                elif(userProfile.night_schedule_efficiency >= 50 and userProfile.night_schedule_efficiency <= 65):
                    night_efficiency_groups[1] += 1  
                elif(userProfile.night_schedule_efficiency >= 65 and userProfile.night_schedule_efficiency <= 80):
                    night_efficiency_groups[2] += 1     
                elif(userProfile.night_schedule_efficiency >= 81 and userProfile.night_schedule_efficiency <= 92):
                    night_efficiency_groups[3] += 1    
                elif(userProfile.night_schedule_efficiency > 92):
                    night_efficiency_groups[4] += 1   
                
        template_values = {
                           'time_profiling_groups': time_profiling_groups,
                           'morning_efficiency_groups': morning_efficiency_groups,
                           'afternoon_efficiency_groups': afternoon_efficiency_groups,
                           'night_efficiency_groups': night_efficiency_groups         
                          }
        
        self.response.out.write(template.render(path, template_values))
                                    
    def solvingExerciseHabits(self, measure):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_profile_solving_exercise_habits.html')
        
        userProfiles = GqlQuery("SELECT * FROM UserProfile") 
                
        recommendation_listener_groups = [0, 0, 0, 0, 0]
        forgetful_user_group = [0, 0, 0, 0, 0]
        
        hint_avoidance_groups = [0, 0, 0, 0, 0]
        video_avoidance_groups = [0, 0, 0, 0, 0]
        unreflective_user_groups = [0, 0, 0, 0, 0]
        hint_abuser_groups = [0, 0, 0, 0, 0]
        
        for userProfile in userProfiles:
            if(userProfile.forgetful_exercises < 5):
                forgetful_user_group[0] += 1      
            elif(userProfile.forgetful_exercises >= 5 and userProfile.forgetful_exercises <= 14):
                forgetful_user_group[1] += 1  
            elif(userProfile.forgetful_exercises >= 15 and userProfile.forgetful_exercises <= 23):
                forgetful_user_group[2] += 1     
            elif(userProfile.forgetful_exercises >= 24 and userProfile.forgetful_exercises <= 32):
                forgetful_user_group[3] += 1     
            elif(userProfile.forgetful_exercises > 32):
                forgetful_user_group[4] += 1 
                
            if(userProfile.recommendation_listener < 15):
                recommendation_listener_groups[0] += 1      
            elif(userProfile.recommendation_listener >= 16 and userProfile.recommendation_listener <= 35):
                recommendation_listener_groups[1] += 1  
            elif(userProfile.recommendation_listener >= 36 and userProfile.recommendation_listener <= 53):
                recommendation_listener_groups[2] += 1   
            elif(userProfile.recommendation_listener >= 54 and userProfile.recommendation_listener <= 72):
                recommendation_listener_groups[3] += 1       
            elif(userProfile.recommendation_listener > 73):
                recommendation_listener_groups[4] += 1    
                
            if(userProfile.hint_avoidance < 6):
                hint_avoidance_groups[0] += 1      
            elif(userProfile.hint_avoidance >= 6 and userProfile.hint_avoidance <= 11):
                hint_avoidance_groups[1] += 1  
            elif(userProfile.hint_avoidance >= 12 and userProfile.hint_avoidance <= 17):
                hint_avoidance_groups[2] += 1     
            elif(userProfile.hint_avoidance >= 18 and userProfile.hint_avoidance <= 23):
                hint_avoidance_groups[3] += 1     
            elif(userProfile.hint_avoidance > 24):
                hint_avoidance_groups[4] += 1 
                
            if(userProfile.video_avoidance < 6):
                video_avoidance_groups[0] += 1      
            elif(userProfile.video_avoidance >= 6 and userProfile.video_avoidance <= 11):
                video_avoidance_groups[1] += 1  
            elif(userProfile.video_avoidance >= 12 and userProfile.video_avoidance <= 17):
                video_avoidance_groups[2] += 1     
            elif(userProfile.video_avoidance >= 18 and userProfile.video_avoidance <= 23):
                video_avoidance_groups[3] += 1     
            elif(userProfile.video_avoidance > 24):
                video_avoidance_groups[4] += 1 
                
            if(userProfile.unreflective_user < 6):
                unreflective_user_groups[0] += 1      
            elif(userProfile.unreflective_user >= 6 and userProfile.unreflective_user <= 11):
                unreflective_user_groups[1] += 1  
            elif(userProfile.unreflective_user >= 12 and userProfile.unreflective_user <= 17):
                unreflective_user_groups[2] += 1     
            elif(userProfile.unreflective_user >= 18 and userProfile.unreflective_user <= 23):
                unreflective_user_groups[3] += 1     
            elif(userProfile.unreflective_user > 24):
                unreflective_user_groups[4] += 1 
                
            if(userProfile.hint_abuser < 6):
                hint_abuser_groups[0] += 1      
            elif(userProfile.hint_abuser >= 6 and userProfile.hint_abuser <= 11):
                hint_abuser_groups[1] += 1  
            elif(userProfile.hint_abuser >= 12 and userProfile.hint_abuser <= 17):
                hint_abuser_groups[2] += 1     
            elif(userProfile.hint_abuser >= 18 and userProfile.hint_abuser <= 23):
                hint_abuser_groups[3] += 1     
            elif(userProfile.hint_abuser > 24):
                hint_abuser_groups[4] += 1      
                        
        template_values = {
                           'recommendation_listener_groups': recommendation_listener_groups,
                           'forgetful_user_group': forgetful_user_group,
                           'hint_avoidance_groups': hint_avoidance_groups, 
                           'video_avoidance_groups': video_avoidance_groups,
                           'unreflective_user_groups': unreflective_user_groups,
                           'hint_abuser_groups': hint_abuser_groups
                          }
        
        self.response.out.write(template.render(path, template_values))
        
    def gamificationHabits(self, measure):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/class_profile_gamification_habits.html')
        
        userProfiles = GqlQuery("SELECT * FROM UserProfile") 
                
        badges_hour_groups = [0, 0, 0, 0, 0]
        points_percentage_group = [0, 0, 0, 0, 0]
        
        for userProfile in userProfiles:
            if(userProfile.badge_over_time < 2):
                badges_hour_groups[0] += 1      
            elif(userProfile.badge_over_time >= 2 and userProfile.badge_over_time <= 3):
                badges_hour_groups[1] += 1  
            elif(userProfile.badge_over_time >= 4 and userProfile.badge_over_time <= 6):
                badges_hour_groups[2] += 1  
            elif(userProfile.badge_over_time >= 7 and userProfile.badge_over_time <= 10):
                badges_hour_groups[3] += 1  
            elif(userProfile.badge_over_time > 10):
                badges_hour_groups[4] += 1  
                
            if(userProfile.badge_point_percentage < 5):
                points_percentage_group[0] += 1      
            elif(userProfile.badge_point_percentage >= 5 and userProfile.badge_point_percentage <= 11):
                points_percentage_group[1] += 1  
            elif(userProfile.badge_point_percentage >= 12 and userProfile.badge_point_percentage <= 18):
                points_percentage_group[2] += 1     
            elif(userProfile.badge_point_percentage >= 19 and userProfile.badge_point_percentage <= 25):
                points_percentage_group[3] += 1     
            elif(userProfile.badge_point_percentage > 25):
                points_percentage_group[4] += 1                
                
        template_values = {
                           'badges_hour_groups': badges_hour_groups,
                           'points_percentage_group': points_percentage_group       
                          }
        
        self.response.out.write(template.render(path, template_values))
                                                            