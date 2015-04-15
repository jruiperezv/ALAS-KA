'''
Created on 06/04/2013

@author: Jose
'''
from __future__ import division
import webapp2
import viewer_code.viewer_consts
import logging
from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from viewer_code.profileviewer_models import ClassMeanProfile

class MeanCalculator(webapp2.RequestHandler):
    
    def post(self):
        
        profileName = self.request.get('profileName')
        
        if(profileName == viewer_code.viewer_consts.EXERCISE_VIDEO_EVALUATION):
                            
            mean_values = self.get_profile_mean(profileName)
                       
            classMeanProfileExercise = ClassMeanProfile(key_name=viewer_code.viewer_consts.EVALUATION_EXERCISE, profile_name=viewer_code.viewer_consts.EVALUATION_EXERCISE,
                                                     mean_value=mean_values[0])
            classMeanProfileVideo = ClassMeanProfile(key_name=viewer_code.viewer_consts.EVALUATION_VIDEO, profile_name=viewer_code.viewer_consts.EVALUATION_VIDEO,
                                                     mean_value=mean_values[1])
            
            db.put([classMeanProfileExercise, classMeanProfileVideo])
            
        elif(profileName == viewer_code.viewer_consts.USE_OF_PLATFORM):
            
            mean_values = self.get_profile_mean(profileName)
            
            classMeanExerciseExplorer = ClassMeanProfile(key_name=viewer_code.viewer_consts.EXERCISE_EXPLORER, profile_name=viewer_code.viewer_consts.EXERCISE_EXPLORER,
                                                     mean_value=mean_values[0])
            classMeanVideoExplorer = ClassMeanProfile(key_name=viewer_code.viewer_consts.VIDEO_EXPLORER, profile_name=viewer_code.viewer_consts.VIDEO_EXPLORER,
                                                     mean_value=mean_values[1])
            classMeanExerciseAbandon = ClassMeanProfile(key_name=viewer_code.viewer_consts.EXERCISE_ABANDON, profile_name=viewer_code.viewer_consts.EXERCISE_ABANDON,
                                                     mean_value=mean_values[2])
            classMeanVideoAbandon = ClassMeanProfile(key_name=viewer_code.viewer_consts.VIDEO_ABANDON, profile_name=viewer_code.viewer_consts.VIDEO_ABANDON,
                                                     mean_value=mean_values[3])
            classMeanOptional = ClassMeanProfile(key_name=viewer_code.viewer_consts.OPTIONAL_ELEMENTS, profile_name=viewer_code.viewer_consts.OPTIONAL_ELEMENTS,
                                                     mean_value=mean_values[4])
            classMeanOneCorrect = ClassMeanProfile(key_name=viewer_code.viewer_consts.EXERCISE_ONE_CORRECT, profile_name=viewer_code.viewer_consts.EXERCISE_ONE_CORRECT,
                                                     mean_value=mean_values[5])
            classMeanFocusExercise = ClassMeanProfile(key_name=viewer_code.viewer_consts.FOCUS_EXERCISES, profile_name=viewer_code.viewer_consts.FOCUS_EXERCISES,
                                                     mean_value=mean_values[6])
            classMeanFocusVideo = ClassMeanProfile(key_name=viewer_code.viewer_consts.FOCUS_VIDEOS, profile_name=viewer_code.viewer_consts.FOCUS_VIDEOS,
                                                     mean_value=mean_values[7])
            
            db.put([classMeanExerciseExplorer, classMeanVideoExplorer,
                    classMeanExerciseAbandon, classMeanVideoAbandon,
                    classMeanOptional, classMeanOneCorrect,
                    classMeanFocusExercise, classMeanFocusVideo])
            
        elif(profileName == viewer_code.viewer_consts.CORRECT_PROGRESS):
            
            mean_values = self.get_profile_mean(profileName)        
            
            classMeanExerciseEfficiency = ClassMeanProfile(key_name=viewer_code.viewer_consts.CORRECT_EXERCISE_EFFICIENCY, profile_name=viewer_code.viewer_consts.CORRECT_EXERCISE_EFFICIENCY,
                                                 mean_value=mean_values[0])
            classMeanVideoEfficiency = ClassMeanProfile(key_name=viewer_code.viewer_consts.VIDEO_EFFICIENCY, profile_name=viewer_code.viewer_consts.VIDEO_EFFICIENCY,
                                                 mean_value=mean_values[1])
            classMeanExerciseProgress = ClassMeanProfile(key_name=viewer_code.viewer_consts.EXERCISE_PROGRESS, profile_name=viewer_code.viewer_consts.EXERCISE_PROGRESS,
                                                 mean_value=mean_values[2])
            classMeanVideoProgress = ClassMeanProfile(key_name=viewer_code.viewer_consts.VIDEO_PROGRESS, profile_name=viewer_code.viewer_consts.VIDEO_PROGRESS,
                                                 mean_value=mean_values[3])
            classMeanCorrectExercises = ClassMeanProfile(key_name=viewer_code.viewer_consts.CORRECT_EXERCISES, profile_name=viewer_code.viewer_consts.CORRECT_EXERCISES,
                                                 mean_value=mean_values[4])
            classMeanEfficiencyProficiencies = ClassMeanProfile(key_name=viewer_code.viewer_consts.EFFICIENCY_PROFICIENCIES, profile_name=viewer_code.viewer_consts.EFFICIENCY_PROFICIENCIES,
                                                 mean_value=mean_values[5])
            classMeanCorrectSolvingEfficiency = ClassMeanProfile(key_name=viewer_code.viewer_consts.CORRECT_SOLVING_EXERCISE_EFFICIENCY, profile_name=viewer_code.viewer_consts.CORRECT_SOLVING_EXERCISE_EFFICIENCY,
                                                 mean_value=mean_values[6])
           
            db.put([classMeanExerciseEfficiency, classMeanVideoEfficiency,
                    classMeanExerciseProgress, classMeanVideoProgress,
                    classMeanCorrectExercises, classMeanEfficiencyProficiencies,
                    classMeanCorrectSolvingEfficiency])
            
        elif(profileName == viewer_code.viewer_consts.TIME_DISTRIBUTION):
            
            mean_values = self.get_profile_mean(profileName)            
            
            classMeanTimeMorning = ClassMeanProfile(key_name=viewer_code.viewer_consts.TIME_SCHEDULE_MORNING, profile_name=viewer_code.viewer_consts.TIME_SCHEDULE_MORNING,
                                                 mean_value=mean_values[0])
            classMeanTimeAfternoon = ClassMeanProfile(key_name=viewer_code.viewer_consts.TIME_SCHEDULE_AFTERNOON, profile_name=viewer_code.viewer_consts.TIME_SCHEDULE_AFTERNOON,
                                                 mean_value=mean_values[1])
            classMeanTimeNight = ClassMeanProfile(key_name=viewer_code.viewer_consts.TIME_SCHEDULE_NIGHT, profile_name=viewer_code.viewer_consts.TIME_SCHEDULE_NIGHT,
                                                 mean_value=mean_values[2])
            classMeanConstancyMean = ClassMeanProfile(key_name=viewer_code.viewer_consts.CONSTANCY_MEAN, profile_name=viewer_code.viewer_consts.CONSTANCY_MEAN,
                                                 mean_value=mean_values[3])
            classMeanConstancyVariance = ClassMeanProfile(key_name=viewer_code.viewer_consts.CONSTANCY_VARIANCE, profile_name=viewer_code.viewer_consts.CONSTANCY_VARIANCE,
                                                 mean_value=mean_values[4])
            classMeanEfficiencyMorning = ClassMeanProfile(key_name=viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_MORNING, profile_name=viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_MORNING,
                                                 mean_value=mean_values[5])
            classMeanEfficiencyAfternoon = ClassMeanProfile(key_name=viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_AFTERNOON, profile_name=viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_AFTERNOON,
                                                 mean_value=mean_values[6])
            classMeanEfficiencyNight = ClassMeanProfile(key_name=viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_NIGHT, profile_name=viewer_code.viewer_consts.EFFICIENCY_SCHEDULE_NIGHT,
                                                 mean_value=mean_values[7])
           
            db.put([classMeanTimeMorning, classMeanTimeAfternoon, classMeanTimeNight,
                    classMeanConstancyMean, classMeanConstancyVariance,
                    classMeanEfficiencyMorning, classMeanEfficiencyAfternoon, classMeanEfficiencyNight])
            
            
        elif(profileName == viewer_code.viewer_consts.EXERCISE_SOLVING_HABITS):
            
            mean_values = self.get_profile_mean(profileName)
           
            classMeanRecommendationListener = ClassMeanProfile(key_name=viewer_code.viewer_consts.RECOMMENDATION_LISTENER, profile_name=viewer_code.viewer_consts.RECOMMENDATION_LISTENER,
                                                  mean_value=mean_values[0])
            classMeanForgetfulExercises = ClassMeanProfile(key_name=viewer_code.viewer_consts.FORGETFUL_EXERCISES, profile_name=viewer_code.viewer_consts.FORGETFUL_EXERCISES,
                                                  mean_value=mean_values[1])
            classMeanHintAvoidance = ClassMeanProfile(key_name=viewer_code.viewer_consts.HINT_AVOIDANCE, profile_name=viewer_code.viewer_consts.HINT_AVOIDANCE,
                                                  mean_value=mean_values[2])
            classMeanVideoAvoidance = ClassMeanProfile(key_name=viewer_code.viewer_consts.VIDEO_AVOIDANCE, profile_name=viewer_code.viewer_consts.VIDEO_AVOIDANCE,
                                                  mean_value=mean_values[3])
            classMeanUnreflectiveUser = ClassMeanProfile(key_name=viewer_code.viewer_consts.UNREFLECTIVE_USER, profile_name=viewer_code.viewer_consts.UNREFLECTIVE_USER,
                                                  mean_value=mean_values[4])
            classMeanHintAbuser = ClassMeanProfile(key_name=viewer_code.viewer_consts.HINT_ABUSER, profile_name=viewer_code.viewer_consts.HINT_ABUSER,
                                                  mean_value=mean_values[5])
           
            db.put([classMeanRecommendationListener, classMeanForgetfulExercises,
                    classMeanHintAvoidance, classMeanVideoAvoidance,
                    classMeanUnreflectiveUser, classMeanHintAbuser])
            
        elif(profileName == viewer_code.viewer_consts.GAMIFICATION_HABITS):
            
            mean_values = self.get_profile_mean(profileName)
            
            classMeanBadgeOverTime = ClassMeanProfile(key_name=viewer_code.viewer_consts.BADGES_OVER_TIME, profile_name=viewer_code.viewer_consts.BADGES_OVER_TIME,
                                                  mean_value=mean_values[0])
            classMeanBadgePointPercentage = ClassMeanProfile(key_name=viewer_code.viewer_consts.BADGE_POINTS_PERCENTAGE, profile_name=viewer_code.viewer_consts.BADGE_POINTS_PERCENTAGE,
                                                  mean_value=mean_values[1])
           
            db.put([classMeanBadgeOverTime, classMeanBadgePointPercentage])
                                                
        else:
        
            logging.info("NOTE: Mean calculator error, profile does not match.");
             
    def get_profile_mean(self, profileName):
        
        queryUserProfile = GqlQuery("SELECT * FROM UserProfile")       

        if(profileName == viewer_code.viewer_consts.EXERCISE_VIDEO_EVALUATION):
            evaluation_exercise_suma = 0
            evaluation_video_suma = 0
            
            for userProfile in queryUserProfile:
                evaluation_exercise_suma += userProfile.evaluation_exercise
                evaluation_video_suma += userProfile.evaluation_video
            
            evaluation_exercise_mean = int(evaluation_exercise_suma / (queryUserProfile.count()))
            evaluation_video_mean = int(evaluation_video_suma / (queryUserProfile.count()))
            
            return [evaluation_exercise_mean, evaluation_video_mean]
        
        elif(profileName == viewer_code.viewer_consts.USE_OF_PLATFORM):
            exercise_explorer_suma = 0
            video_explorer_suma = 0
            exercise_abandon_suma = 0
            video_abandon_suma = 0
            optional_suma = 0
            one_correct_suma = 0
            focus_videos_suma = 0
            focus_exercises_suma = 0
            
            for userProfile in queryUserProfile:
                exercise_explorer_suma += userProfile.exercise_explorer
                video_explorer_suma += userProfile.video_explorer
                exercise_abandon_suma += userProfile.exercise_abandon
                video_abandon_suma += userProfile.video_abandon
                optional_suma += userProfile.optional_elements
                one_correct_suma += userProfile.exercise_one_correct
                focus_videos_suma += userProfile.focus_videos
                focus_exercises_suma += userProfile.focus_exercises
            
            exercise_explorer_mean = int(exercise_explorer_suma / (queryUserProfile.count()))
            video_explorer_mean = int(video_explorer_suma / (queryUserProfile.count()))
            exercise_abandon_mean = int(exercise_abandon_suma / (queryUserProfile.count()))
            video_abandon_mean = int(video_abandon_suma / (queryUserProfile.count()))
            optional_mean = int(optional_suma / (queryUserProfile.count()))
            one_correct_mean = int(one_correct_suma / (queryUserProfile.count()))
            focus_exercises_mean = int(focus_exercises_suma / (queryUserProfile.count()))
            focus_videos_mean = int(focus_videos_suma / (queryUserProfile.count()))
            
            return [exercise_explorer_mean, video_explorer_mean,
                    exercise_abandon_mean, video_abandon_mean,
                    optional_mean, one_correct_mean,
                    focus_exercises_mean, focus_videos_mean]
            
        elif(profileName == viewer_code.viewer_consts.CORRECT_PROGRESS):
            
            video_efficiency_suma = 0
            exercise_efficiency_suma = 0
            video_progress_suma = 0
            exercise_progress_suma = 0
            correct_exercise_suma = 0
            efficiency_proficiencies_suma = 0
            correct_solving_efficiency_suma = 0
            
            for userProfile in queryUserProfile:
                video_efficiency_suma += userProfile.video_efficiency
                exercise_efficiency_suma += userProfile.correct_exercise_effiency
                video_progress_suma += userProfile.video_progress
                exercise_progress_suma += userProfile.exercise_progress
                correct_exercise_suma += userProfile.correct_exercises
                efficiency_proficiencies_suma += userProfile.efficiency_proficiencies
                correct_solving_efficiency_suma += userProfile.correct_exercise_solving_efficiency
                
            video_efficiency_mean = int(video_efficiency_suma / (queryUserProfile.count()))
            exercise_efficiency_mean = int(exercise_efficiency_suma / (queryUserProfile.count()))
            video_progress_mean = int(video_progress_suma / (queryUserProfile.count()))
            exercise_progress_mean = int(exercise_progress_suma / (queryUserProfile.count()))
            correct_exercise_mean = int(correct_exercise_suma / (queryUserProfile.count()))
            efficiency_proficiencies_mean = int(efficiency_proficiencies_suma / (queryUserProfile.count()))
            correct_solving_efficiency_mean = int(correct_solving_efficiency_suma / (queryUserProfile.count()))
            
            return [exercise_efficiency_mean, video_efficiency_mean,
                    exercise_progress_mean, video_progress_mean,
                    correct_exercise_mean, efficiency_proficiencies_mean,
                    correct_solving_efficiency_mean]
                        
        elif(profileName == viewer_code.viewer_consts.TIME_DISTRIBUTION):
            
            time_morning_suma = 0
            time_afternoon_suma = 0
            time_night_suma = 0
            morning_efficiency_suma = 0
            afternoon_efficiency_suma = 0
            night_efficiency_suma = 0
            
            constancy_mean_suma = 0
            constancy_var_suma = 0
            
            morning_efficiency_counter = 0
            afternoon_efficiency_counter = 0
            night_efficiency_counter = 0
            
            for userProfile in queryUserProfile:
                time_morning_suma += userProfile.time_schedule_morning
                time_afternoon_suma += userProfile.time_schedule_afternoon
                time_night_suma += userProfile.time_schedule_night
                constancy_mean_suma += userProfile.constancy_mean
                constancy_var_suma += userProfile.constancy_variance
                if(userProfile.morning_schedule_efficiency != 0):                    
                    morning_efficiency_suma += userProfile.morning_schedule_efficiency
                    morning_efficiency_counter += 1
                    
                if(userProfile.afternoon_schedule_efficiency != 0):                    
                    afternoon_efficiency_suma += userProfile.afternoon_schedule_efficiency
                    afternoon_efficiency_counter += 1
                    
                if(userProfile.night_schedule_efficiency != 0):                    
                    night_efficiency_suma += userProfile.night_schedule_efficiency
                    night_efficiency_counter += 1
                 
            time_morning_mean = int(time_morning_suma / (queryUserProfile.count()))
            #time_afternoon_mean = int(time_afternoon_suma / (queryUserProfile.count()))
            time_night_mean = int(time_night_suma / (queryUserProfile.count()))
            time_afternoon_mean = 100 - time_morning_mean - time_night_mean
            constancy_mean_mean = int(constancy_mean_suma / (queryUserProfile.count()))
            constancy_var_mean = int(constancy_var_suma / (queryUserProfile.count()))
            
            if(morning_efficiency_counter == 0):
                morning_efficiency_mean = 0
            else:
                morning_efficiency_mean = int(morning_efficiency_suma/morning_efficiency_counter)
                
            if(afternoon_efficiency_counter == 0):
                afternoon_efficiency_mean = 0
            else:
                afternoon_efficiency_mean = int(afternoon_efficiency_suma/afternoon_efficiency_counter)
            
            if(night_efficiency_counter == 0):
                night_efficiency_mean = 0
            else:
                night_efficiency_mean = int(night_efficiency_suma/night_efficiency_counter)
            
            return [time_morning_mean, time_afternoon_mean, time_night_mean,
                    constancy_mean_mean, constancy_var_mean,
                    morning_efficiency_mean, afternoon_efficiency_mean, night_efficiency_mean]
              
        elif(profileName == viewer_code.viewer_consts.EXERCISE_SOLVING_HABITS):
            
            recommendation_listener_suma = 0
            forgetful_exercises_suma = 0
            hint_avoidance_suma = 0
            video_avoidance_suma = 0
            unreflective_user_suma = 0
            hint_abuser_suma = 0
            
            for userProfile in queryUserProfile:
                recommendation_listener_suma += userProfile.recommendation_listener
                forgetful_exercises_suma += userProfile.forgetful_exercises
                hint_avoidance_suma += userProfile.hint_avoidance
                video_avoidance_suma += userProfile.video_avoidance
                unreflective_user_suma += userProfile.unreflective_user
                hint_abuser_suma += userProfile.hint_abuser
                
            recommendation_listener_mean = int(recommendation_listener_suma / (queryUserProfile.count()))
            forgetful_exercises_mean = int(forgetful_exercises_suma / (queryUserProfile.count()))
            hint_avoidance_mean = int(hint_avoidance_suma / (queryUserProfile.count()))
            video_avoidance_mean = int(video_avoidance_suma / (queryUserProfile.count()))
            unreflective_user_mean = int(unreflective_user_suma / (queryUserProfile.count()))
            hint_abuser_mean = int(hint_abuser_suma / (queryUserProfile.count()))
            
            return [recommendation_listener_mean, forgetful_exercises_mean,
                    hint_avoidance_mean, video_avoidance_mean,
                    unreflective_user_mean, hint_abuser_mean]
            
        elif(profileName == viewer_code.viewer_consts.GAMIFICATION_HABITS):
            
            badge_over_time_suma = 0
            badge_percentage_suma = 0
            
            for userProfile in queryUserProfile:
                badge_over_time_suma += userProfile.badge_over_time
                badge_percentage_suma += userProfile.badge_point_percentage
                
            badge_over_time_mean = int(badge_over_time_suma / (queryUserProfile.count()))
            badge_percentage_mean = int(badge_percentage_suma / (queryUserProfile.count()))
            
            return [badge_over_time_mean, badge_percentage_mean]