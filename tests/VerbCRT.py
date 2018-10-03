#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from collections import OrderedDict
from random import choice

# import os
# HOME_FOLDER = '/home/ivanvoronin/P-files/2018-09-04-RT_grant/RT_tests'
# os.chdir(HOME_FOLDER)

trial_dict = OrderedDict()
for i in ['training', 'series1', 'series2', 'series3']:
    animals = []
    plants  = []
    
    with open('stimuli/VCRT/' + i, 'r') as File:
        for line in File:
            line = line.translate(None, '\n').decode('utf-8')
            animal, plant = line.split('\t')
            animals.append(animal)
            plants.append(plant)

    series_trial_dict = []
    for j in animals:
        series_trial_dict.append({'target': j, 'cor_resp': 'd'})
    for j in plants:
        series_trial_dict.append({'target': j, 'cor_resp': 'l'})
    trial_dict[i] = series_trial_dict


class VerbCRT (CogTest):
    name = 'VerbCRT'
    nreps = 1
    maxtrials = 10000 # maximum number of trials in the main test
    mintrain = 5      # number of correct training responses to start main test
    maxtrain = 20     # maximum length of training series

    ndemo = 20        # number of trials in demo version of the test

    breaktrials = 40  # make a break after this number of trials
    breaktime = 6     # length of the break (sec)
    
    mincorrect = 0.3      # maximum percent of incorrect responses
    maxinvalidstrike = 10   # interrupt the test when the this number of consecutive responses is invalid
    nonresptime = 5         # maximum nonresponse time (sec)
    
    trial_dict = trial_dict

    def init_trial_stimuli(self):
        self.trial_stimuli = {
            # Fixation stimulus indicating start of the trial
            'fixation':
                visual.ShapeStim(self.test_screen, units=None, lineWidth=4,
                                 pos=[0, 0], lineColor='white',
                                 closeShape=False,
                                 vertices=((0, -10), (0, 10), (0, 0),
                                             (-10, 0), (10, 0))),
            # Trial stimuli
            'word':
                visual.TextStim(self.test_screen, 
                                text='', height=35,
                                pos=[0, 0], color='white'),
            # Hints
            'hint_animal':
                visual.TextStim(self.test_screen, 
                                text=u'D <- животное', height=35,
                                pos=[-270, 0], color='white'),
            'hint_plant':
                visual.TextStim(self.test_screen, 
                                text=u'растение -> L', height=35,
                                pos=[270, 0], color='white')}

    def show_trial_screen(self):
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_animal'].draw()
            self.trial_stimuli['hint_plant'].draw()

    def show_stim(self, trial):
        # The translation from 'trial' to stimuli to be shown
        self.trial_stimuli['word'].setText(trial['target'])
        self.trial_stimuli['word'].draw()
        
    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen, 
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.35*self.test_screen.size[1]],
                                      text=u'\
Положи руки на стол, чтобы указательные пальцы располагались на клавишах L и D\n\
Когда в центре экрана появится крестик, приготовься отвечать\n\
На экране появится слово, обозначающее животное или растение\n\
Если слово на экране обозначает РАСТЕНИЕ, как можно быстрее нажми L\n\
Если слово на экране обозначает ЖИВОТНОЕ, как можно быстрее нажми D\n\
В начале будет серия тренировочных попыток\n\
\n\
Для продолжения нажми любую клавишу')
        # This is screen width-to-height ratio
        a2b = float(self.test_screen.size[0])/self.test_screen.size[1]
        # This is is picture width-to-height ration
        x2y = 1500.0/800
        # Pictures with keyboard
        key_0 = visual.ImageStim(self.test_screen, image='pics/VerbCRT_0.png',
                                 pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                 units='norm')
        keys = {
            'd': visual.ImageStim(self.test_screen, image='pics/VerbCRT_D.png',
                                  pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                  units='norm'),
            'l': visual.ImageStim(self.test_screen, image='pics/VerbCRT_L.png',
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
                self.suspend(wait = 0.7)
            
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

#VerbCRT().start('test', 'Демо') 