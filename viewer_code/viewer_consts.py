'''
Created on 06/04/2013

File with constants needed for the viewer code

@author: Jose
'''

# Bloques de medidas

EXERCISE_VIDEO_EVALUATION = "EXERCISE_VIDEO_EVALUATION"
USE_OF_PLATFORM = "USE_OF_PLATFORM"
CORRECT_PROGRESS = "CORRECT_PROGRESS"
TIME_DISTRIBUTION = "TIME_DISTRIBUTION"
GAMIFICATION_HABITS = "GAMIFICATION HABITS"
EXERCISE_SOLVING_HABITS = "EXERCISE_SOLVING_HABITS"

# Measures

EVALUATION_EXERCISE = 'evaluation_exercise'
EVALUATION_VIDEO = 'evaluation_video'

VIDEO_EXPLORER = 'video_explorer'
EXERCISE_EXPLORER = 'exercise_explorer'
VIDEO_ABANDON = 'video_abandon'
EXERCISE_ABANDON = 'exercise_abandon'
OPTIONAL_ELEMENTS = 'optional_elements'
EXERCISE_ONE_CORRECT = 'exercise_one_correct'
FOCUS_VIDEOS = 'focus_videos'
FOCUS_EXERCISES = 'focus_exercises'

CORRECT_EXERCISE_EFFICIENCY = 'correct_exercise_efficiency'
CORRECT_SOLVING_EXERCISE_EFFICIENCY = 'correct_solving_exercise_efficiency'
VIDEO_EFFICIENCY = 'video_efficiency'
EXERCISE_PROGRESS = 'exercise_progress'
VIDEO_PROGRESS = 'video_progress'
CORRECT_EXERCISES = 'correct_exercises'
EFFICIENCY_PROFICIENCIES = 'efficiency_proficiencies'

TIME_SCHEDULE_MORNING = 'time_schedule_morning'
TIME_SCHEDULE_AFTERNOON = 'time_schedule_afternoon'
TIME_SCHEDULE_NIGHT = 'time_schedule_night'
EFFICIENCY_SCHEDULE_MORNING = 'efficiency_schedule_morning'
EFFICIENCY_SCHEDULE_AFTERNOON = 'efficiency_schedule_afternoon'
EFFICIENCY_SCHEDULE_NIGHT = 'efficiency_schedule_night'
CONSTANCY_MEAN = 'constancy_mean'
CONSTANCY_VARIANCE = 'constancy_variance'

RECOMMENDATION_LISTENER = 'recommendation_listener'
FORGETFUL_EXERCISES = 'forgetful_exercises'
HINT_AVOIDANCE = 'hint_avoidance'
VIDEO_AVOIDANCE = 'video_avoidance'
UNREFLECTIVE_USER = 'unreflective_user'
HINT_ABUSER = 'hint_abuser'

BADGE_POINTS_PERCENTAGE = 'badge_points_percentage'
BADGES_OVER_TIME = 'badges_over_time'
# CODIGOS DE Las ASIGNATURAS


ACTIVE_COURSE_CODE = 1
ACTIVE_COURSE_STRING = "physics"

#ACTIVE_COURSE_CODE = 2
#ACTIVE_COURSE_STRING = "chemistry"

#ACTIVE_COURSE_CODE = 3
#ACTIVE_COURSE_STRING = "mathematics"

PHYSICS_CODE = 1
CHEMISTRY_CODE = 2
MATHEMATICS_CODE = 3

PHYSICS_STRING = "physics"
CHEMISTRY_STRING = "chemistry"
MATHEMATICS_STRING = "mathematics"


DESCRIPTION_LIST = [
                    #0 Use of Platform
                    "This block of metrics gives information about how much the student has used the platform, but it does not take into account if the student did it correctly or incorrectly. ",
                    #1 Correct Progress in the Platform
                    "This block of metrics shows if students progressed in a proper way when watching videos and solving exercises in the platform. In addition, it includes the efficiency of them during this process.",
                    #2 Time Distribution of Use of the Platform
                    "This section presents an analysis of the times when the user has interacted with the platform.",
                    #3 Gamification Habits
                    "This block gives information about whether a student is motivated by the gamification elements.",
                    #4 Exercise Solving Habits
                    "This block of metrics analyzes the interaction of a student when solving exercises and provides information related to the students habits.",
                    #5 Course Evaluation
                    "This is a customized measure by the course professors to see how well the student has done in the platform.",
                    #6 Different Exercise Accessed
                    "This metric gives a percentage of the number of different types of exercises accessed (It is not necessary that they have been solved correctly). Each parametric exercise is only taken into account 1 time (i.e if accessed several times the same parametric exercise, it is only taken into account once).",
                    #7 Exercise at Least 1 Correct
                    "This metric is a percentage of the number of different types of exercises that have been solved correctly at least once.",                   
                    #8 Exercise Abandon
                    "This metric is a percentage of the number of exercises that were started, but the student never achieved proficiency in them, so they abandoned that type of exercise without mastering it. To achieve the proficiency in a parametric exercise the students must solve it correctly several times.",
                    #9 Video Abandon
                    "This metric is a percentage of the number of videos that have been started but never finished. ",
                    #10 Different Videos Accessed
                    "This metric is a percentage of the number of different videos accessed (It is not necessary that they have been fully watched)",
                    #11 Exercise Over Video Focus
                    "This metric gives insight about if a student focuses his learning more on watching videos or doing exercises.  We represent Exercise Over Videos as (ExerciseTime/(VideoTime+ExerciseTime)), so the higher is the percentage, the more focus is on Exercises, and the lower the more focus is on Videos.",
                    #12 Optional Elements
                    "This metric represents the level of optional elements the student interacted with in the platform. Optional items considered are e.g. the setting of goals. A level of 100% would mean that the student used all non-mandatory elements available in the platform.",
                    #13 Exercise Correct Progress
                    "This metric shows how much the student has progressed in doing exercises correctly.",
                    #14 Exercise Solving Efficiency
                    "This metric shows the efficiency of the user when solving exercises, it is related with the time needed to answer correctly and the number of attempts.",
                    #15 Video Correct Progress
                    "This metric shows how much the student has progressed in watching videos.",
                    #16 Video Efficiency
                    "This measure shows the efficiency of the user when watching videos. It is related with if the students watch the video several times.",
                    #17 Time Schedule
                    "These parameters show at what time users watch their videos and solve exercises. We set three time schedules by time intervals: morning [7:00 to 13:59], afternoon [14:00 to 20:59] and night [21:00 to 06:59]",
                    #18 Efficiency Schedule
                    "These efficiencies use the same interval as the Time Schedule metric, but in this case we show the efficiency of the student doing exercises in each time interval.",
                    #19 Constancy 
                    "This parameter checks if a user was studying in a constant way during many days or was studying strongly only for a few days. The sample mean and variance of time spent on the platform by day are calculated",
                    #20 Gamification Motivation
                    "This metric gives information about if the user is interested in earning badges and it is related to the time invest on the platform and the number of badges earned.",
                    #21 Badge Points Percentage
                    "We show the percentage of points that have been earned due to winning badges (BadgePoints/TotalPoints), this gives information about if a student is more or less motivated by badges",
                    #22 Recommendation Listener
                    "Khan Academy includes an exercise recommender; therefore checking whether the user has accessed a certain number of recommended exercises gives an indication about if the user follows the recommended path. ",
                    #23 Forgetful Exercises
                    "This metric analyzes if students that have already solved a parametric exercise correctly, fail later to solve it, so they have forgotten how to solve it.",
                    #24 Hint Avoidance
                    "A student is classified as hint avoider whenever he cannot solve an exercise correctly but he does not ask hints either.",
                    #25 Hint Abuse
                    "A student is classified as hint abuser whenever he asks for too many hints without reflecting on previous hints or the exercise statement.",
                    #26 Video Avoidance
                    "A student is classified as video avoider whenever he cannot solve an exercise correctly and he did not watched the related video previously.",
                    #27 Unreflective User
                    "A student is classified as unreflective whenever he submits answers to fast without reflecting in what could have been his previous mistakes.",
                    #28 Evaluation Score
                    "This metric is in the range [0-10] and it is related to the number of correct exercises and the number of attempts required."           
                    ]

