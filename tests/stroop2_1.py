#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from collections import OrderedDict
from random import choice
import os

# I adjust the colors for perceived luminocity using the formula:
# def lum (R, G, B):
#     return sqrt(0.299*R*R + 0.587*G*G + 0.114*B*B)/255
# I choose 0.338 as a baseline luminocity (red color)
# red   = [255,   0,   0],
# green = [  0, 200,   0],
# blue  = [  0, 100, 255]}
# Refs:
#  - http://alienryderflex.com/hsp.html
#  - https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color


class stroop2_1 (CogTest):
    name = 'stroop2_1'
    nreps = 20          # number of repeats within each trial dictionary

    mintrain = 10       # minimum number of training trials
    maxtrain = 30       # maximum number of training trials

    nonresptime = 5     # maximum non-response time (sec)
    
    colors = {'red':   [230,   0,   0],
              'green': [  0, 130,   0],
              'blue':  [  0, 100, 255]}

    # This is trial dictionary passed to data.TrialHandler
    # Must contain training series
    # Each series must contain 'cor_resp' which is correct response
    # (key on a keyboard)
    trial_dict = OrderedDict(
        [('training', [{'word': u'XXXXXXX', 'color': 'red',   'cor_resp': 'd'},
                       {'word': u'XXXXXXX', 'color': 'green', 'cor_resp': 'l'},
                       {'word': u'XXXXXXX', 'color': 'red', 'cor_resp': 'd'},
                       {'word': u'XXXXXXX', 'color': 'green', 'cor_resp': 'l'}]),
         ('main',     [{'word': u'XXXXXXX', 'color': 'red',   'cor_resp': 'd'},
                       {'word': u'XXXXXXX', 'color': 'green', 'cor_resp': 'l'},
                       {'word': u'XXXXXXX', 'color': 'red', 'cor_resp': 'd'},
                       {'word': u'XXXXXXX', 'color': 'green', 'cor_resp': 'l'}])])

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
                            pos=[200, 0])}

    # You are welcome to change this for CogTest instances
    # Here you define how the trial information translates to stimuli
    def show_stim(self, trial):
        self.trial_stimuli['word'].setText(trial['word'])
        self.trial_stimuli['word'].setColor(self.colors[trial['color']])
        self.trial_stimuli['word'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the screen outlook
    def show_trial_screen(self):
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_red_key'].draw()
            self.trial_stimuli['hint_red'].draw()
            self.trial_stimuli['hint_green_key'].draw()
            self.trial_stimuli['hint_green'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the test demonstration/instruction
    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen,
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.35*self.test_screen.size[1]],
                                      text=u'\
Положи руки на стол, чтобы указательные пальцы располагались на клавишах L и D.\n\
Как только в центре экрана появится белый крест, приготовься отвечать.\n\
На экране появятся символы ХХХХХХХ.\n\
Если символы написаны КРАСНЫМ цветом, как можно быстрее нажми D.\n\
Если символы написаны ЗЕЛЕНЫМ цветом, как можно быстрее нажми L.\n\
В начале будет серия тренировочных попыток.\n\
\n\
Для продолжения нажми любую клавишу')
        # This is screen width-to-height ratio
        a2b = float(self.test_screen.size[0])/self.test_screen.size[1]
        # This is is picture width-to-height ration
        x2y = 1500.0/800
        # Pictures with keyboard
        key_0 = visual.ImageStim(self.test_screen, image='pics/stroop0_0.png',
                                 pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                 units='norm')
        keys = {
            'd': visual.ImageStim(self.test_screen, image='pics/stroop0_D.png',
                                  pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                  units='norm'),
            'l': visual.ImageStim(self.test_screen, image='pics/stroop0_L.png',
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
                self.suspend(wait=0.5)
            
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
    stroop2_1().start('test', u'Демо')