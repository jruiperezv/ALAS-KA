#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import division

from google.appengine.ext.webapp import template
import webapp2
import os


# Import necesarios para el viewer
from viewer_code.profile_handlers import ProfileView
from viewer_code.profile_handlers import DisplayProfile
from viewer_code.class_handlers import ClassView
from viewer_code.class_handlers import DisplayClass
from viewer_code.menu_handlers import MenuHandler
from viewer_code.menu_handlers import AboutHandler
from viewer_code.viewer_cron.evaluation import EvaluationStats
from viewer_code.viewer_cron.use_of_platform import UseOfPlatform
from viewer_code.viewer_cron.mean_calculator import MeanCalculator
from viewer_code.viewer_cron.correct_progres import CorrectProgress
from viewer_code.viewer_cron.time_distribution import TimeDistribution
from viewer_code.viewer_cron.exercise_solving_habits import ExerciseSolvingHabits
from viewer_code.viewer_cron.gamification_habits import GamificationHabits

class MainHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'viewer_templates/menu.html')

        template_values = {
                          }
            
        self.response.out.write(template.render(path, template_values))

# Aqui recordar que habra que quitar la etiqueta de administrador en algunas URL e igualmente en los enlaces de los HTML
app = webapp2.WSGIApplication([('/', MenuHandler),
                               ('/menu_viewer', MenuHandler), 
                               ('/about_viewer', AboutHandler), 
                               ('/profile_viewer', ProfileView),
                               ('/class_viewer', ClassView),
                               ('/display_profile', DisplayProfile),
                               ('/display_class', DisplayClass),
                               ('/admin/evaluation_stats', EvaluationStats),
                               ('/admin/use_of_platform', UseOfPlatform),
                               ('/admin/mean_calculator', MeanCalculator),
                               ('/admin/correct_progress', CorrectProgress),
                               ('/admin/time_distribution', TimeDistribution),
                               ('/admin/exercise_solving', ExerciseSolvingHabits),
                               ('/admin/gamification_habits', GamificationHabits)
                               ], debug=True)
    