#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from collections import OrderedDict
from random import choice

# import os
# HOME_FOLDER = '/home/ivanvoronin/P-files/2018-09-04-RT_grant/RT_tests'
# os.chdir(HOME_FOLDER)

'''
I adjust the colors for perceived luminocity using the formula:
def lum (R, G, B): 
    return sqrt(0.299*R*R + 0.587*G*G + 0.114*B*B)/255
I choose 0.338 as a baseline luminocity (red color)
red   = [255,   0,   0],
green = [  0, 200,   0],
blue  = [  0, 100, 255]}
Refs: 
 - http://alienryderflex.com/hsp.html
 - https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color
'''


class stroop3_1 (CogTest):
    name = 'stroop3_1'
    nreps = 40

    maxtrials = 10000 # maximum number of trials in the main test
    mintrain = 5      # number of correct training responses to start main test
    maxtrain = 20     # maximum length of training series

    ndemo = 20        # number of trials in demo version of the test

    breaktrials = 40  # make a break after this number of trials
    breaktime = 6     # length of the break (sec)
    
    mincorrect = 0.3      # maximum percent of incorrect responses
    maxinvalidstrike = 10   # interrupt the test when the this number of consecutive responses is invalid
    nonresptime = 5         # maximum nonresponse time (sec)
    
    colors = {'red':   [230,   0,   0],
              'green': [  0, 170,   0],
              'blue':  [  0, 100, 255]}
    
    trial_dict = OrderedDict(
        [('training', [{'word': u'ХХХХХХХ', 'color': 'red',   'cor_resp': 'd'},
                       {'word': u'ХХХХХХХ', 'color': 'green', 'cor_resp': 'l'},
                       {'word': u'ХХХХХХХ', 'color': 'blue',  'cor_resp': ' '}]),
         ('main',     [{'word': u'ХХХХХХХ', 'color': 'red',   'cor_resp': 'd'},
                       {'word': u'ХХХХХХХ', 'color': 'green', 'cor_resp': 'l'},
                       {'word': u'ХХХХХХХ', 'color': 'blue',  'cor_resp': ' '}])])

    def init_trial_stimuli(self):
        self.trial_stimuli = {
            # Fixation stimulus indicating start of the trial
            'fixation':
                visual.ShapeStim(self.test_screen, units=None, lineWidth=4,
                                 pos=[0, 0], lineColor = 'white',
                                 closeShape=False,
                                 vertices=((0, -10), (0, 10), (0, 0),
                                             (-10, 0), (10, 0))),
            # Trial stimuli
            'word':
                visual.TextStim(self.test_screen, 
                                text='', height=40,
                                pos=[0, 0], colorSpace='rgb255'),
            # Hints
            'hint_red':
                visual.TextStim(self.test_screen, 
                                text='D', height=30,
                                pos=[-200, 0], color='white'),
            'hint_green':
                visual.TextStim(self.test_screen, 
                                text='L', height=30,
                                pos=[200, 0], color='white'),
            'hint_blue':
                visual.TextStim(self.test_screen, 
                                text=u'ПРОБЕЛ', height=30,
                                pos=[0, -100], color='white'),
            'hint_red_key':
                visual.Rect(self.test_screen,
                            width=50, height=50,
                            fillColor=self.colors['red'],
                            fillColorSpace='rgb255',
                            lineColor='white',
                            pos=[-200, 0]),
            'hint_green_key':
                visual.Rect(self.test_screen,
                            width=50, height=50,
                            fillColor=self.colors['green'],
                            fillColorSpace='rgb255',
                            lineColor='white',
                            pos=[200, 0]),
            'hint_blue_key':
                visual.Rect(self.test_screen,
                            width=250, height=50,
                            fillColor=self.colors['blue'],
                            fillColorSpace='rgb255',
                            lineColor='white',
                            pos=[0, -100])}

    def show_stim(self, trial):
        # The translation from 'trial' to stimuli to be shown
        self.trial_stimuli['word'].setText(trial['word'])
        self.trial_stimuli['word'].setColor(self.colors[trial['color']])
        self.trial_stimuli['word'].draw()

    def show_trial_screen(self):
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_red_key'].draw()
            self.trial_stimuli['hint_red'].draw()
            self.trial_stimuli['hint_green_key'].draw()
            self.trial_stimuli['hint_green'].draw()
            self.trial_stimuli['hint_blue_key'].draw()
            self.trial_stimuli['hint_blue'].draw()
    
    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen,
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.35*self.test_screen.size[1]],
                                      text=u'\
Положи руки на стол, чтобы указательные пальцы располагались на клавишах L и D,\n\
а большой палец правой руки - на клавише ПРОБЕЛ (как на картинке)\n\
Как только в центре экрана появится белый крест, приготовься отвечать\n\
На экране появятся символы ХХХХХХХ\n\
Если символы написаны КРАСНЫМ цветом, как можно быстрее нажми D\n\
Если символы написаны ЗЕЛЕНЫМ цветом, как можно быстрее нажми L\n\
Если символы написаны ГОЛУБЫМ цветом, как можно быстрее нажми ПРОБЕЛ\n\
\n\
В начале будет серия тренировочных попыток\n\
\n\
Для продолжения нажми любую клавишу')
        # This is screen width-to-height ratio
        a2b = float(self.test_screen.size[0])/self.test_screen.size[1]
        # This is is picture width-to-height ration
        x2y = 1500.0/800
        # Pictures with keyboard
        key_0 = visual.ImageStim(self.test_screen, image='pics/stroop2_0.png',
                                 pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                 units='norm')
        keys = {
            'd': visual.ImageStim(self.test_screen, image='pics/stroop2_D.png',
                                  pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                  units='norm'),
            'l': visual.ImageStim(self.test_screen, image='pics/stroop2_L.png',
                                  pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                  units='norm'),
            ' ': visual.ImageStim(self.test_screen, image='pics/stroop2_space.png',
                                  pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                  units='norm')}
        # Stimuli
        fixation = self.trial_stimuli['fixation']

        while True:
            try:
                # Frame 1
                instruction.draw()
                self.show_trial_screen()
                key_0.draw()
                self.test_screen.flip()
                self.suspend(wait = 1.5)
            
                # Frame 2
                instruction.draw()
                self.show_trial_screen()
                key_0.draw()
                fixation.draw()
                self.test_screen.flip()
                self.suspend(wait = 1)
            
                # Frame 3
                instruction.draw()
                self.show_trial_screen()
                key_0.draw()
                trial = choice(self.trial_dict['training'])
                self.show_stim(trial)
                self.test_screen.flip()
                self.suspend(wait = 0.5)
            
                # Frame 4
                instruction.draw()
                self.show_trial_screen()
                self.show_stim(trial)
                keys[trial['cor_resp']].draw()
                self.test_screen.flip()
                self.suspend(wait = 0.5)
            
                # Frame 5
                instruction.draw()
                self.show_trial_screen()
                keys[trial['cor_resp']].draw()
                self.test_screen.flip()
                self.suspend(wait = 0.5)
            except GoOn:
                break

#stroop3_1().start('test', u'Демо')