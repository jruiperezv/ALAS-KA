'''
Created on 14/03/2013

@author: Jose Antonio Ruiperez Valiente
'''

from models import Video
from models import Exercise

from google.appengine.ext import db

class ViewerUser(db.Model):
    
    user = db.UserProperty()
    user_id = db.StringProperty()
    user_nickname = db.StringProperty()    
    professor = db.BooleanProperty(default = False)
    student = db.BooleanProperty(default = False)
    
# Modelo que representa a todos los perfiles de medidas de un usuario
class UserProfile(db.Model):

    user = db.UserProperty()
    user_id = db.StringProperty()
    user_nickname = db.StringProperty()
    
    evaluation_exercise = db.IntegerProperty(default = -1, indexed=False)
    evaluation_video = db.IntegerProperty(default = -1, indexed=False)
    evaluation_ranking = db.IntegerProperty(default =-1 ,indexed=False)
    
    video_explorer = db.IntegerProperty(default = -1, indexed=False)
    exercise_explorer = db.IntegerProperty(default = -1, indexed=False)
    video_abandon = db.IntegerProperty(default = -1, indexed=False)
    exercise_abandon = db.IntegerProperty(default = -1, indexed=False)
    optional_elements = db.IntegerProperty(default = -1, indexed=False)
    exercise_one_correct = db.IntegerProperty(default = -1, indexed=False)
    focus_videos = db.IntegerProperty(default = -1, indexed=False)
    focus_exercises = db.IntegerProperty(default = -1, indexed=False)
    
    video_efficiency = db.IntegerProperty(default = -1, indexed=False)
    correct_exercise_effiency = db.IntegerProperty(default = -1, indexed=False)
    correct_exercise_solving_efficiency = db.IntegerProperty(default = -1, indexed=False)
    exercise_progress = db.IntegerProperty(default = -1, indexed=False)
    video_progress = db.IntegerProperty(default = -1, indexed=False)
    correct_exercises = db.IntegerProperty(default = -1, indexed=False)
    efficiency_proficiencies = db.IntegerProperty(default = -1, indexed=False)
    
    time_schedule_morning = db.IntegerProperty(default = -1, indexed=False)
    time_schedule_afternoon = db.IntegerProperty(default = -1, indexed=False)
    time_schedule_night = db.IntegerProperty(default = -1, indexed=False)
    morning_schedule_efficiency = db.IntegerProperty(default = -1, indexed=False)
    afternoon_schedule_efficiency = db.IntegerProperty(default = -1, indexed=False)
    night_schedule_efficiency = db.IntegerProperty(default = -1, indexed=False)
    average_schedule_efficiency = db.IntegerProperty(default = -1, indexed=False)
    constancy_mean = db.IntegerProperty(default = -1, indexed=False)
    constancy_variance = db.IntegerProperty(default = -1, indexed=False)
    
    recommendation_listener = db.IntegerProperty(default = -1, indexed=False)
    forgetful_exercises = db.IntegerProperty(default = -1, indexed=False)
    hint_avoidance = db.IntegerProperty(default = -1, indexed=False)
    video_avoidance = db.IntegerProperty(default = -1, indexed=False)
    unreflective_user = db.IntegerProperty(default = -1, indexed=False)
    hint_abuser = db.IntegerProperty(default = -1, indexed=False)
    
    badge_over_time = db.IntegerProperty(default = -1, indexed=False)
    badge_point_percentage = db.IntegerProperty(default = -1, indexed=False)
    
# Valor medio de los perfiles para las visualizaciones de clase   
class ClassMeanProfile(db.Model):
    
    profile_name = db.StringProperty(indexed=True)
    mean_value = db.IntegerProperty(default = 0, indexed=False)
    
class ViewerVideo(db.Model):
    
    youtube_id = db.StringProperty()
    video = db.ReferenceProperty(Video)
    
class ViewerExercise(db.Model):
    
    name = db.StringProperty()
    exercise = db.ReferenceProperty(Exercise)
    