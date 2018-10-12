#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from psychopy.tools.coordinatetools import pol2cart
from collections import OrderedDict
from random import choice
import os

class CRT4 (CogTest):
    name = 'CRT4'
    nreps = 30

    mintrain = 7       # minimum number of training trials
    maxtrain = 20      # maximum number of training trials

    # This is trial dictionary passed to data.TrialHandler
    # Must contain training series
    # Each series must contain 'cor_resp' which is correct response
    # (key on a keyboard)
    trial_dict = OrderedDict(
        [('training', [{'target': 'stim1', 'cor_resp': 'p'},
                       {'target': 'stim2', 'cor_resp': 'l'},
                       {'target': 'stim3', 'cor_resp': 'd'},
                       {'target': 'stim4', 'cor_resp': 'e'}]),
         ('main',     [{'target': 'stim1', 'cor_resp': 'p'},
                       {'target': 'stim2', 'cor_resp': 'l'},
                       {'target': 'stim3', 'cor_resp': 'd'},
                       {'target': 'stim4', 'cor_resp': 'e'}])])

    # You are welcome to change this for CogTest instances
    # Here you define all test stimuli
    # The fixation stimulus must be present
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
            'blanc1':
                visual.Circle(self.test_screen, units=None, radius=50, 
                              pos=pol2cart(15, 160, units='deg'),
                              lineWidth=5, lineColor='white'),
            'blanc2':
                visual.Circle(self.test_screen, units=None, radius=50, 
                              pos=pol2cart(-55, 160, units='deg'),
                              lineWidth=5, lineColor='white'),
            'blanc3':
                visual.Circle(self.test_screen, units=None, radius=50, 
                              pos=pol2cart(-125, 160, units='deg'),
                              lineWidth=5, lineColor='white'),
            'blanc4':
                visual.Circle(self.test_screen, units=None, radius=50, 
                              pos=pol2cart(-195, 160, units='deg'),
                              lineWidth=5, lineColor='white'),
            
            'stim1':
                visual.Circle(self.test_screen, units=None, radius=25, 
                              pos=pol2cart(15, 160, units='deg'),
                              lineWidth=3, fillColor='white'),
            'stim2':
                visual.Circle(self.test_screen, units=None, radius=25, 
                              pos=pol2cart(-55, 160, units='deg'),
                              lineWidth=3, fillColor='white'),
            'stim3':
                visual.Circle(self.test_screen, units=None, radius=25, 
                              pos=pol2cart(-125, 160, units='deg'),
                              lineWidth=3, fillColor='white'),
            'stim4':
                visual.Circle(self.test_screen, units=None, radius=25, 
                              pos=pol2cart(-195, 160, units='deg'),
                              lineWidth=3, fillColor='white'),
            'hint_1': visual.TextStim(self.test_screen, text='P',
                                      pos=pol2cart(15, 160, units='deg'),
                                      color='white', height=30),
            'hint_2': visual.TextStim(self.test_screen, text='L',
                                      pos=pol2cart(-55, 160, units='deg'),
                                      color='white', height=30),
            'hint_3': visual.TextStim(self.test_screen, text='D',
                                      pos=pol2cart(-125, 160, units='deg'),
                                      color='white', height=30),
            'hint_4': visual.TextStim(self.test_screen, text='E',
                                      pos=pol2cart(-195, 160, units='deg'),
                                      color='white', height=30)}

    # You are welcome to change this for CogTest instances
    # Here you define the screen outlook
    def show_trial_screen(self):
        self.trial_stimuli['blanc1'].draw()
        self.trial_stimuli['blanc2'].draw()
        self.trial_stimuli['blanc3'].draw()
        self.trial_stimuli['blanc4'].draw()
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_1'].draw()
            self.trial_stimuli['hint_2'].draw()
            self.trial_stimuli['hint_3'].draw()
            self.trial_stimuli['hint_4'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define how the trial information translates to stimuli
    def show_stim(self, trial):
        self.trial_stimuli[trial['target']].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the test demonstration/instruction
    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen, 
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.3*self.test_screen.size[1]],
                                      text=u'\
Положи руки на стол, чтобы указательные пальцы располагались на клавишах L и D,\n\
а средние пальцы - на клавишах P и E (как на рисунке)\n\
Когда в центре экрана появится крестик, приготовься отвечать\n\
В одном из кругов появится белая точка\n\
Если точка появилась в ПРАВОМ ВЕРХНЕМ круге, как можно быстрее нажми P\n\
Если точка появилась в ПРАВОМ НИЖНЕМ круге, как можно быстрее нажми L\n\
Если точка появилась в ЛЕВОМ ВЕРХНЕМ круге, как можно быстрее нажми E\n\
Если точка появилась в ЛЕВОМ НИЖНЕМ круге, как можно быстрее нажми D\n\
В начале будет серия тренировочных попыток\n\
\n\
Для продолжения нажми любую клавишу')
        # This is screen width-to-height ratio
        a2b = float(self.test_screen.size[0])/self.test_screen.size[1]
        # This is is picture width-to-height ration
        x2y = 1500.0/800
        # Pictures with keyboard
        key_0 = visual.ImageStim(self.test_screen, image='pics/CRT4_0.png',
                                 pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                 units='norm')
        keys = {
            'stim1': visual.ImageStim(self.test_screen, image='pics/CRT4_1.png',
                                     pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                     units='norm'),
            'stim2': visual.ImageStim(self.test_screen, image='pics/CRT4_2.png',
                                      pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                      units='norm'),
            'stim3': visual.ImageStim(self.test_screen, image='pics/CRT4_3.png',
                                      pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                      units='norm'),
            'stim4': visual.ImageStim(self.test_screen, image='pics/CRT4_4.png',
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
                ch = choice(['stim1', 'stim2',
                             'stim3', 'stim4'])
                self.trial_stimuli[ch].draw()
                self.test_screen.flip()
                self.suspend(wait=0.5)
            
                # Frame 4
                instruction.draw()
                self.show_trial_screen()
                keys[ch].draw()
                self.trial_stimuli[ch].draw()
                self.test_screen.flip()
                self.suspend(wait=0.3)
            
                # Frame 5
                instruction.draw()
                self.show_trial_screen()
                keys[ch].draw()
                self.test_screen.flip()
                self.suspend(wait=0.3)
            except GoOn:
                break


if __name__ == '__main__':
    if not os.access('data', os.F_OK):
        os.mkdir('data')
    CRT4().start('test', u'Демо')