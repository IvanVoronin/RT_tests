#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from collections import OrderedDict
from psychopy.tools.coordinatetools import pol2cart
import itertools
from random import choice

# import os
# HOME_FOLDER = '/home/ivanvoronin/P-files/2018-09-04-RT_grant/RT_tests'
# os.chdir(HOME_FOLDER)

shape = ['circle', 'triangle']
color = ['red', 'green']
fill  = ['solid', 'contour']
cue   = ['shape', 'color']

# Series 1: all shapes filled
figure1 = list(itertools.product(shape, color, ['solid']))
figures1 = list(itertools.product(figure1, figure1))
figures1cue = list(itertools.product(figures1, cue))

trial_dict1 = []
for i in figures1cue:
    trial = dict(zip(
        ['shape1', 'color1', 'fill1', 'shape2', 'color2', 'fill2', 'cue'], 
        i[0][0] + i[0][1] + (i[1],)))
    if trial['cue'] == 'shape':
        if trial['shape1'] == trial['shape2']:
            trial['cor_resp'] = 'l'
        else:
            trial['cor_resp'] = 'd'
    elif trial['cue'] == 'color':
        if trial['color1'] == trial['color2']:
            trial['cor_resp'] = 'l'
        else:
            trial['cor_resp'] = 'd'
    trial_dict1.append(trial)
    
# Series 2: filled an contoured shapes
figure2 = list(itertools.product(shape, color, fill))
figures2 = list(itertools.product(figure2, figure2))
figures2cue = list(itertools.product(figures2, cue))

trial_dict2 = []
for i in figures2cue:
    trial = dict(zip(
        ['shape1', 'color1', 'fill1', 'shape2', 'color2', 'fill2', 'cue'], 
        i[0][0] + i[0][1] + (i[1],)))
    if trial['cue'] == 'shape':
        if trial['shape1'] == trial['shape2']:
            trial['cor_resp'] = 'l'
        else:
            trial['cor_resp'] = 'd'
    elif trial['cue'] == 'color':
        if trial['color1'] == trial['color2']:
            trial['cor_resp'] = 'l'
        else:
            trial['cor_resp'] = 'd'
    trial_dict2.append(trial)


class VisCRT (CogTest):
    name = 'VisCRT'
    nreps = 1

    maxtrials = 10000 # maximum number of trials in the main test
    mintrain = 5      # number of correct training responses to start main test
    maxtrain = 20     # maximum length of training series

    ndemo = 20        # number of trials in demo version of the test

    breaktrials = 40  # make a break after this number of trials
    breaktime = 6     # length of the break (sec)
    
    mincorrect = 0.3      # maximum percent of incorrect responses
    maxinvalidstrike = 10   # interrupt the test when the this number of consecutive responses is invalid
    nonresptime = 7         # maximum nonresponse time (sec)
    
    trial_dict = OrderedDict([
        ('training', trial_dict1),
        ('main', trial_dict2)])

    colors = {'red':   [230,   0,   0],
              'green': [  0, 170,   0],
              'blue':  [  0, 100, 255]}

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
            'circle1':
                visual.Circle(self.test_screen, units=None, radius=40, 
                              pos=[-130, 0], lineWidth=6, 
                              lineColorSpace='rgb255',
                              fillColorSpace='rgb255'),
            'circle2':
                visual.Circle(self.test_screen, units=None, radius=40, 
                              pos=[130, 0], lineWidth=6, 
                              lineColorSpace='rgb255',
                              fillColorSpace='rgb255'),
            'triangle1':
                visual.ShapeStim(self.test_screen, units=None,
                                 pos=[-130, -0.33*40], lineWidth=6,
                                 closeShape=True,
                                 vertices=(pol2cart(90,  1.17*40, units='deg'),
                                           pol2cart(210, 1.17*40, units='deg'),
                                           pol2cart(330, 1.17*40, units='deg')),
                                 lineColorSpace='rgb255',
                                 fillColorSpace='rgb255'),
            'triangle2':
                visual.ShapeStim(self.test_screen, units=None,
                                 pos=[130, -0.33*40], lineWidth=6,
                                 closeShape=True,
                                 vertices=(pol2cart(90,  1.17*40, units='deg'),
                                           pol2cart(210, 1.17*40, units='deg'),
                                           pol2cart(330, 1.17*40, units='deg')),
                                 lineColorSpace='rgb255',
                                 fillColorSpace='rgb255'),
            # Cues
            'cue1':
                visual.ShapeStim(self.test_screen, units=None, lineWidth=4,
                                 pos = [0, 0], lineColor = 'white', 
                                 closeShape=False,
                                 vertices = ((0,-10), (0,10), 
                                             (-10,0), (0,10), (10,0))),
            'cue2':
                visual.ShapeStim(self.test_screen, units=None, lineWidth=4,
                                 pos = [0, 0], lineColor = 'white', 
                                 closeShape=False,
                                 vertices = ((0,10), (0,-10), 
                                             (-10,0), (0,-10), (10,0))),
            # Hints
            'hint_cue1':
                visual.TextStim(self.test_screen, 
                                text=u'сравнить по форме', height=25,
                                pos=[0, 100], color='white'),
            'hint_cue2':
                visual.TextStim(self.test_screen, 
                                text=u'сравнить по цвету', height=25,
                                pos=[0, -100], color='white'),
            'hint_D':
                visual.TextStim(self.test_screen, 
                                text=u'D <- разные', height=25,
                                pos=[-330, 0], color='white'),
            'hint_L':
                visual.TextStim(self.test_screen, 
                                text=u'одинаковые -> L', height=25,
                                pos=[330, 0], color='white')    
            }

    def show_stim(self, trial):
        # The translation from 'trial' to stimuli to be shown
        if trial['cue'] == 'shape':
            self.trial_stimuli['cue1'].draw()
        elif trial['cue'] == 'color':
            self.trial_stimuli['cue2'].draw()
            
        # Left stimulus
        if trial['shape1'] == 'circle':
            if trial['color1'] == 'red':
                if trial['fill1'] == 'solid':
                    self.trial_stimuli['circle1'].setFillColor(self.colors['red'])
                    self.trial_stimuli['circle1'].setLineColor(self.colors['red'])
                elif trial['fill1'] == 'contour':
                    self.trial_stimuli['circle1'].setFillColor(None)
                    self.trial_stimuli['circle1'].setLineColor(self.colors['red'])
            elif trial['color1'] == 'green':
                if trial['fill1'] == 'solid':
                    self.trial_stimuli['circle1'].setFillColor(self.colors['green'])
                    self.trial_stimuli['circle1'].setLineColor(self.colors['green'])
                elif trial['fill1'] == 'contour':
                    self.trial_stimuli['circle1'].setFillColor(None)
                    self.trial_stimuli['circle1'].setLineColor(self.colors['green'])
            self.trial_stimuli['circle1'].draw()
        elif trial['shape1'] == 'triangle':
            if trial['color1'] == 'red':
                if trial['fill1'] == 'solid':
                    self.trial_stimuli['triangle1'].setFillColor(self.colors['red'])
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['red'])
                elif trial['fill1'] == 'contour':
                    self.trial_stimuli['triangle1'].setFillColor(None)
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['red'])
            elif trial['color1'] == 'green':
                if trial['fill1'] == 'solid':
                    self.trial_stimuli['triangle1'].setFillColor(self.colors['green'])
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['green'])
                elif trial['fill1'] == 'contour':
                    self.trial_stimuli['triangle1'].setFillColor(None)
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['green'])   
            self.trial_stimuli['triangle1'].draw()
            
        # Right stimulus
        if trial['shape2'] == 'circle':
            if trial['color2'] == 'red':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['circle2'].setFillColor(self.colors['red'])
                    self.trial_stimuli['circle2'].setLineColor(self.colors['red'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['circle2'].setFillColor(None)
                    self.trial_stimuli['circle2'].setLineColor(self.colors['red'])
            elif trial['color2'] == 'green':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['circle2'].setFillColor(self.colors['green'])
                    self.trial_stimuli['circle2'].setLineColor(self.colors['green'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['circle2'].setFillColor(None)
                    self.trial_stimuli['circle2'].setLineColor(self.colors['green'])
            self.trial_stimuli['circle2'].draw()
        elif trial['shape2'] == 'triangle':
            if trial['color2'] == 'red':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['triangle2'].setFillColor(self.colors['red'])
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['red'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['triangle2'].setFillColor(None)
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['red'])
            elif trial['color2'] == 'green':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['triangle2'].setFillColor(self.colors['green'])
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['green'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['triangle2'].setFillColor(None)
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['green'])   
            self.trial_stimuli['triangle2'].draw()
            
    def show_trial_screen(self):    
        # Hint
        if self.vars['series'] == 'training':
            self.trial_stimuli['hint_cue1'].draw()
            self.trial_stimuli['hint_cue2'].draw()
            self.trial_stimuli['hint_D'].draw()
            self.trial_stimuli['hint_L'].draw()

    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen, 
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.30*self.test_screen.size[1]],
                                      text=u'\
Положи руки на стол, чтобы указательные пальцы располагались на клавишах L и D\n\
Когда в центре экрана появится крестик, приготовься отвечать\n\
На экране появятся две фигуры и стрелка\n\
Если стрелка показывает НАВЕРХ, необходимо сравнить фигуры ПО ФОРМЕ\n\
Если стрелка показывает ВНИЗ, необходимо сравнить фигуры ПО ЦВЕТУ\n\
\n\
Если фигуры СХОДНЫ, как можно быстрее нажми L\n\
Если фигуры РАЗЛИЧАЮТСЯ, как можно быстрее нажми D\n\
\n\
В начале будет серия тренировочных попыток\n\
\n\
Для продолжения нажми любую клавишу')
        # This is screen width-to-height ratio
        a2b = float(self.test_screen.size[0])/self.test_screen.size[1]
        # This is is picture width-to-height ration
        x2y = 1500.0/800
        # Pictures with keyboard
        key_0 = visual.ImageStim(self.test_screen, image='pics/VisCRT_0.png',
                                 pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                 units='norm')
        keys = {
            'd': visual.ImageStim(self.test_screen, image='pics/VisCRT_D.png',
                                  pos=[0, -0.7], size=[0.6 * x2y/a2b, 0.6], 
                                  units='norm'),
            'l': visual.ImageStim(self.test_screen, image='pics/VisCRT_L.png',
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

# VisCRT().start('test', u'Демо')