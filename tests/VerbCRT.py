#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from collections import OrderedDict
from random import choice
import os

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
    nreps = 1               # number of repeats within each trial dictionary

    mintrain = 10       # minimum number of training trials
    maxtrain = 30      # maximum number of training trials

    nonresptime = 5         # maximum non-response time (sec)

    # This is trial dictionary passed to data.TrialHandler
    # Must contain training series
    # Each series must contain 'cor_resp' which is correct response
    # (key on a keyboard)
    trial_dict = trial_dict

    # You are welcome to change this for CogTest instances
    # Here you define all test stimuli
    # The fixation stimulus must be present
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

    # You are welcome to change this for CogTest instances
    # Here you define the screen outlook
    def show_trial_screen(self):
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_animal'].draw()
            self.trial_stimuli['hint_plant'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the screen outlook
    def show_stim(self, trial):
        self.trial_stimuli['word'].setText(trial['target'])
        self.trial_stimuli['word'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the test demonstration/instruction
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
                self.suspend(wait=1.5)
            
                # Frame 2
                instruction.draw()
                self.show_trial_screen()
                key_0.draw()
                fixation.draw()
                self.test_screen.flip()
                self.suspend(wait=1)
            
                # Frame 3
                instruction.draw()
                self.show_trial_screen()
                key_0.draw()
                trial = choice(self.training_trials)
                self.show_stim(trial)
                self.test_screen.flip()
                self.suspend(wait=0.7)
            
                # Frame 4
                instruction.draw()
                self.show_trial_screen()
                self.show_stim(trial)
                keys[trial['cor_resp']].draw()
                self.test_screen.flip()
                self.suspend(wait=0.5)
            
                # Frame 5
                instruction.draw()
                self.show_trial_screen()
                keys[trial['cor_resp']].draw()
                self.test_screen.flip()
                self.suspend(wait=0.5)
            except GoOn:
                break


if __name__ == '__main__':
    if not os.access('data', os.F_OK):
        os.mkdir('data')
    VerbCRT().start('test', u'Демо')