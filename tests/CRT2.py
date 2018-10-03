#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from collections import OrderedDict
from random import choice

# import os
# HOME_FOLDER = '/home/ivanvoronin/P-files/2018-09-04-RT_grant/RT_tests'
# os.chdir(HOME_FOLDER)


class CRT2 (CogTest):
    name = 'CRT2'
    nreps = 75

    maxtrials = 10000 # maximum number of trials in the main test
    mintrain = 5      # number of correct training responses to start main test
    maxtrain = 20     # maximum length of training series

    ndemo = 20        # number of trials in demo version of the test

    breaktrials = 40  # make a break after this number of trials
    breaktime = 6     # length of the break (sec)
    
    mincorrect = 0.3      # maximum percent of incorrect responses
    maxinvalidstrike = 10   # interrupt the test when the this number of consecutive responses is invalid
    nonresptime = 3         # maximum nonresponse time (sec)
    
    trial_dict = OrderedDict(
        [('training', [{'target': 'left', 'cor_resp': 'd'},
                       {'target': 'right', 'cor_resp': 'l'}]),
         ('main',     [{'target': 'left', 'cor_resp': 'd'},
                       {'target': 'right', 'cor_resp': 'l'}])])
    
    def init_trial_stimuli(self):
        self.trial_stimuli = {
            # Fixation stimulus indicating start of the trial
            'fixation':
                visual.ShapeStim(self.test_screen, units=None, lineWidth=4,
                                 pos = [0, 0], lineColor = 'white', 
                                 closeShape=False,
                                 vertices = ((0,-10), (0,10), (0,0), 
                                             (-10,0), (10,0))),            
            # Trial stimuli
            'blanc_left':
                visual.Circle(self.test_screen, units=None, radius=50, 
                              pos=[-160, 0], lineWidth=5, lineColor='white'),
            'blanc_right':
                visual.Circle(self.test_screen, units=None, radius=50, 
                              pos=[160, 0], lineWidth=5, lineColor='white'),
            
            'left':
                visual.Circle(self.test_screen, units=None, radius=25, 
                              pos=[-160, 0], lineWidth=3, fillColor='white'),
            'right':
                visual.Circle(self.test_screen, units=None, radius=25, 
                              pos=[160, 0], lineWidth=3, fillColor='white'),
            'hint_left': visual.TextStim(self.test_screen, text='D',
                                         pos=[-160, 0], color='white',
                                         height=30),
            'hint_right': visual.TextStim(self.test_screen, text='L',
                                          pos=[160, 0], color='white',
                                          height=30)}
    
    def show_trial_screen(self):
        self.trial_stimuli['blanc_left'].draw()
        self.trial_stimuli['blanc_right'].draw()
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_left'].draw()
            self.trial_stimuli['hint_right'].draw()

    def show_stim(self, trial):
        # The translation from 'trial' to stimuli to be shown
        self.trial_stimuli[trial['target']].draw()
    
    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen, 
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.35*self.test_screen.size[1]],
                                      text=u'\
Положи руки на клавиатуру, чтобы указательные пальцы располагались на клавишах L и D\n\
Когда в центре экрана появится крестик, приготовься отвечать\n\
В одном из кругов появится белая точка\n\
Если точка появилась в ПРАВОМ круге, как можно быстрее нажми L\n\
Если точка появилась в ЛЕВОМ круге, как можно быстрее нажми D\n\
В начале будет серия тренировочных попыток\n\
\n\
Для продолжения нажми любую клавишу')
        # This is screen width-to-height ratio
        a2b = float(self.test_screen.size[0])/self.test_screen.size[1]
        # This is is picture width-to-height ration
        x2y = 1500.0/800

        # Pictures with keyboard
        key_0 = visual.ImageStim(self.test_screen, image='pics/CRT2_0.png',
                                 pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                 units='norm')
        keys = {
            'left': visual.ImageStim(self.test_screen, image='pics/CRT2_D.png',
                                     pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                     units='norm'),
            'right': visual.ImageStim(self.test_screen, image='pics/CRT2_L.png',
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
                ch = choice(['right', 'left'])
                self.trial_stimuli[ch].draw()
                self.test_screen.flip()
                self.suspend(wait = 0.2)
            
                # Frame 4
                instruction.draw()
                self.show_trial_screen()
                keys[ch].draw()
                self.trial_stimuli[ch].draw()
                self.test_screen.flip()
                self.suspend(wait = 0.3)
            
                # Frame 5
                instruction.draw()
                self.show_trial_screen()
                self.trial_stimuli[ch].draw()
                keys[ch].draw()
                self.test_screen.flip()
                self.suspend(wait = 0.5)
            except GoOn:
                break

#CRT2().start('test', u'Демо')
        