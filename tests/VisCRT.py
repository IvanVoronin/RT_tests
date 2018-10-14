#!/usr/bin/env python
# -*- coding: utf-8 -*-

from CogTest import CogTest, GoOn
from psychopy import visual
from collections import OrderedDict
from psychopy.tools.coordinatetools import pol2cart
import itertools
from random import choice
import os

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
            trial['cor_resp'] = 'd'
        else:
            trial['cor_resp'] = 'l'
    elif trial['cue'] == 'color':
        if trial['color1'] == trial['color2']:
            trial['cor_resp'] = 'd'
        else:
            trial['cor_resp'] = 'l'
    trial_dict1.append(trial)
    
# Series 2: filled an contoured shapes
figure2 = list(itertools.product(shape, color, fill))
figures2 = list(itertools.product(figure2, figure2))
figures2cue = list(itertools.product(figures2, cue))

# FIXME: Exclude identical shapes
trial_dict2 = []
for i in figures2cue:
    trial = dict(zip(
        ['shape1', 'color1', 'fill1', 'shape2', 'color2', 'fill2', 'cue'], 
        i[0][0] + i[0][1] + (i[1],)))
    if trial['cue'] == 'shape':
        if trial['shape1'] == trial['shape2']:
            trial['cor_resp'] = 'd'
        else:
            trial['cor_resp'] = 'l'
    elif trial['cue'] == 'color':
        if trial['color1'] == trial['color2']:
            trial['cor_resp'] = 'd'
        else:
            trial['cor_resp'] = 'l'
    trial_dict2.append(trial)

trial_dict2mod = []
for i in trial_dict2:
    if i['color1'] == i['color1'] and \
       i['shape1'] == i['shape2'] and \
       i['fill1'] == i['fill2']:
        pass
    else:
        trial_dict2mod.append(i)


class VisCRT (CogTest):
    name = 'VisCRT'
    nreps = 2           # number of repeats within each trial dictionary

    maxtrials = 120     # maximum number of trials in the main test
    mintrain = 10       # minimum number of training trials
    maxtrain = 30       # maximum number of training trials

    nonresptime = 7     # maximum non-response time (sec)

    # This is trial dictionary passed to data.TrialHandler
    # Must contain training series
    # Each series must contain 'cor_resp' which is correct response
    # (key on a keyboard)
    trial_dict = OrderedDict([
        ('training', trial_dict1),
        ('main', trial_dict2mod)])

    colors = {'red':   [230,   0,   0],
              'green': [  0, 170,   0],
              'blue':  [  0, 100, 255]}

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
            # FIXME: Почему-то все треугольники белые
            # TODO: Исключить совпадающие формы
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
                visual.TextStim(self.test_screen, text=u'ФОРМА'),
            'cue2':
                visual.TextStim(self.test_screen, text=u'ЦВЕТ'),

            'hint_D':
                visual.TextStim(self.test_screen, 
                                text=u'D <- одинаковые', height=25,
                                pos=[-330, 0], color='white'),
            'hint_L':
                visual.TextStim(self.test_screen, 
                                text=u'разные -> L', height=25,
                                pos=[330, 0], color='white')    
            }

    # You are welcome to change this for CogTest instances
    # Here you define how the trial information translates to stimuli
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
                    self.trial_stimuli['circle1'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['circle1'].setLineColor(self.colors['red'])
            elif trial['color1'] == 'green':
                if trial['fill1'] == 'solid':
                    self.trial_stimuli['circle1'].setFillColor(self.colors['green'])
                    self.trial_stimuli['circle1'].setLineColor(self.colors['green'])
                elif trial['fill1'] == 'contour':
                    self.trial_stimuli['circle1'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['circle1'].setLineColor(self.colors['green'])
            self.trial_stimuli['circle1'].draw()
        elif trial['shape1'] == 'triangle':
            if trial['color1'] == 'red':
                if trial['fill1'] == 'solid':
                    self.trial_stimuli['triangle1'].setFillColor(self.colors['red'])
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['red'])
                elif trial['fill1'] == 'contour':
                    self.trial_stimuli['triangle1'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['red'])
            elif trial['color1'] == 'green':
                if trial['fill1'] == 'solid':
                    self.trial_stimuli['triangle1'].setFillColor(self.colors['green'])
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['green'])
                elif trial['fill1'] == 'contour':
                    self.trial_stimuli['triangle1'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['triangle1'].setLineColor(self.colors['green'])   
            self.trial_stimuli['triangle1'].draw()
            
        # Right stimulus
        if trial['shape2'] == 'circle':
            if trial['color2'] == 'red':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['circle2'].setFillColor(self.colors['red'])
                    self.trial_stimuli['circle2'].setLineColor(self.colors['red'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['circle2'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['circle2'].setLineColor(self.colors['red'])
            elif trial['color2'] == 'green':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['circle2'].setFillColor(self.colors['green'])
                    self.trial_stimuli['circle2'].setLineColor(self.colors['green'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['circle2'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['circle2'].setLineColor(self.colors['green'])
            self.trial_stimuli['circle2'].draw()
        elif trial['shape2'] == 'triangle':
            if trial['color2'] == 'red':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['triangle2'].setFillColor(self.colors['red'])
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['red'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['triangle2'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['red'])
            elif trial['color2'] == 'green':
                if trial['fill2'] == 'solid':
                    self.trial_stimuli['triangle2'].setFillColor(self.colors['green'])
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['green'])
                elif trial['fill2'] == 'contour':
                    self.trial_stimuli['triangle2'].setFillColor(None, colorSpace='rgb255')
                    self.trial_stimuli['triangle2'].setLineColor(self.colors['green'])   
            self.trial_stimuli['triangle2'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the screen outlook
    def show_trial_screen(self):    
        # Hint
        if self.vars['series'] == 'training':
#            self.trial_stimuli['hint_cue1'].draw()
#            self.trial_stimuli['hint_cue2'].draw()
            self.trial_stimuli['hint_D'].draw()
            self.trial_stimuli['hint_L'].draw()

    # You are welcome to change this for CogTest instances
    # Here you define the test demonstration/instruction
    def start_demonstration(self):
        instruction = visual.TextStim(self.test_screen, 
                                      wrapWidth=1.8*self.test_screen.size[0],
                                      pos=[0, 0.30*self.test_screen.size[1]],
                                      text=u'\
Положи руки на стол, чтобы указательные пальцы располагались на клавишах L и D\n\
Когда в центре экрана появится крестик, приготовься отвечать\n\
На экране появятся две фигуры и слово\n\
Если в центре экрана слово ФОРМА, необходимо сравнить фигуры ПО ФОРМЕ\n\
Если в центре экрана слово ЦВЕТ, необходимо сравнить фигуры ПО ЦВЕТУ\n\
\n\
Если фигуры СХОДНЫ, как можно быстрее нажми D\n\
Если фигуры РАЗЛИЧАЮТСЯ, как можно быстрее нажми L\n\
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
    VisCRT().start('test', u'Демо')