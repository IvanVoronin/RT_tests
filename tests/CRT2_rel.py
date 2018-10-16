#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTestRelease import CogTestRelease, GoOn
from psychopy import visual
from collections import OrderedDict
from random import choice
import os


class CRT2_rel (CogTestRelease):
    name = 'CRT2_rel'
    nreps = 30         # number of repeats within each trial dictionary

    mintrain = 7       # minimum number of training trials
    maxtrain = 20      # maximum number of training trials

    # This is trial dictionary passed to data.TrialHandler
    # Must contain training series
    # Each series must contain 'cor_resp' which is correct response
    # (key on a keyboard)
    trial_dict = OrderedDict(
        [('training', [{'target': 'left', 'cor_resp': 'd'},
                       {'target': 'right', 'cor_resp': 'l'}]),
         ('main',     [{'target': 'left', 'cor_resp': 'd'},
                       {'target': 'right', 'cor_resp': 'l'}])])

    # You are welcome to change this for CogTest instances
    # Here you define all test stimuli
    # The fixation stimulus must be present
    def init_trial_stimuli(self):
        self.trial_stimuli = {
            # Fixation stimulus indicating start of the trial
            'fixation':
                visual.ShapeStim(self.test_screen, units=None, lineWidth=4,
                                 pos=[0, 0], lineColor='red',
                                 closeShape=False,
                                 vertices=((0, -10), (0, 10), (0, 0),
                                           (-10, 0), (10, 0))),
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
            'hint_left': 
                visual.TextStim(self.test_screen, text='D',
                                pos=[-160, 0], color='white',
                                height=30),
            'hint_right': 
                visual.TextStim(self.test_screen, text='L',
                                pos=[160, 0], color='white',
                                height=30)}

    # You are welcome to change this for CogTest instances
    # Here you define the screen outlook
    def show_trial_screen(self):
        self.trial_stimuli['fixation'].draw()
        self.trial_stimuli['blanc_left'].draw()
        self.trial_stimuli['blanc_right'].draw()
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_left'].draw()
            self.trial_stimuli['hint_right'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define how the trial information is translated to stimuli
    def show_stim(self, trial):
        self.trial_stimuli[trial['target']].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the test demonstration/instruction
    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen, 
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.35*self.test_screen.size[1]],
                                      text=u'\
Положи руки на стол, чтобы указательные пальцы располагались на клавишах L и D\n\
Нажми и удерживай клавиши L и D, чтобы крестик в середине экрана стал зеленый\n\
В одном из кругов появится белая точка\n\
Если точка появилась в ПРАВОМ круге, как можно быстрее отпусти L\n\
Если точка появилась в ЛЕВОМ круге, как можно быстрее отпусти D\n\
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
            'right': visual.ImageStim(self.test_screen, image='pics/CRT2_D.png',
                                     pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                     units='norm'),
            'left': visual.ImageStim(self.test_screen, image='pics/CRT2_L.png',
                                      pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                      units='norm'),
            'both': visual.ImageStim(self.test_screen, image='pics/CRT2_both.png',
                                      pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                      units='norm')}
        # Stimuli
        fixation = self.trial_stimuli['fixation']

        # Frame 0
        instruction.draw()
        key_0.draw()
        self.show_trial_screen()
        self.test_screen.flip()
        self.suspend(wait=2)
        
        while True:
            try:
                # Frame 1
                instruction.draw()
                keys['both'].draw()
                fixation.setLineColor('green')
                self.show_trial_screen()
                self.test_screen.flip()
                self.suspend(wait=1.5)
            
                # Frame 2
                instruction.draw()
                self.show_trial_screen()
                keys['both'].draw()
                ch = choice(['right', 'left'])
                self.trial_stimuli[ch].draw()
                self.test_screen.flip()
                self.suspend(wait=0.5)
            
                # Frame 3
                instruction.draw()
                keys[ch].draw()
                fixation.setLineColor('red')
                self.show_trial_screen()
                self.test_screen.flip()
                self.suspend(wait=0.5)
            except GoOn:
                break


if __name__ == '__main__':
    if not os.access('data', os.F_OK):
        os.mkdir('data')
    CRT2_rel().start('test', u'Демо')