#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTestRelease import CogTestRelease, GoOn
from psychopy import visual
from collections import OrderedDict
import os

class SRT_rel (CogTestRelease):
    name = 'SRT_rel'
    nreps = 100

    trial_dict = OrderedDict(
        [('training', [{'target': 'center', 'cor_resp': ' '}]),
         ('main',     [{'target': 'center', 'cor_resp': ' '}])])
        
    def init_trial_stimuli(self):
        self.trial_stimuli = {
            # Fixation stimulus indicating start of the trial
            'fixation':
                visual.Circle(self.test_screen, units=None, radius=50, pos=[0, 0],
                              lineWidth=5, lineColor='red'),
            # Trial stimuli
            'center':
                visual.Circle(self.test_screen, units=None, radius=25, pos=[0, 0], 
                              lineWidth=3, fillColor='white')}
        
    def show_stim(self, trial):
        # The translation from 'trial' to stimuli to be shown
        self.trial_stimuli[trial['target']].draw()

    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen, 
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.35*self.test_screen.size[1]],
                                      text=u'\
Положи руку на стол, чтобы большой палец располагался на клавише ПРОБЕЛ\n\
Когда в центре экрана появится белый круг, приготовься отвечать\n\
Как только в центре круга появится белая точка, как можно быстрее нажми на ПРОБЕЛ\n\
В начале будет серия тренировочных попыток\n\
\n\
Для продолжения нажми любую клавишу')
        # This is screen width-to-height ratio
        a2b = float(self.test_screen.size[0])/self.test_screen.size[1]
        # This is is picture width-to-height ration
        x2y = 1500.0/800
        # Pictures with keyboard
        key_0 = visual.ImageStim(self.test_screen, image='pics/SRT_0.png',
                                 pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                 units='norm')
        key_press = visual.ImageStim(self.test_screen, image='pics/SRT_press.png',
                                     pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                     units='norm')
        # Stimuli
        fixation = self.trial_stimuli['fixation']
        stim = self.trial_stimuli['center']

        while True:
            try:
                # Frame 1
                instruction.draw()
                key_0.draw()
                self.show_trial_screen()
                self.test_screen.flip()
                self.suspend(wait = 1.5)
            
                # Frame 2
                instruction.draw()
                key_press.draw()
                fixation.setLineColor('green')
                self.show_trial_screen()
                self.test_screen.flip()
                self.suspend(wait = 1)
            
                # Frame 3
                instruction.draw()
                key_press.draw()
                self.show_trial_screen()
                stim.draw()
                self.test_screen.flip()
                self.suspend(wait = 0.2)
            
                # Frame 4
                instruction.draw()
                key_0.draw()            
                fixation.setLineColor('red')
                self.show_trial_screen()
                self.test_screen.flip()
                self.suspend(wait = 0.3)

            except GoOn:
                break
         

if __name__ == '__main__':
    if not os.access('data', os.F_OK):
        os.mkdir('data')
    SRT_rel().start('test', u'Демо')