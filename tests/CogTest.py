#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, iohub, data, core, logging
from numpy import random
from datetime import datetime
from collections import OrderedDict


class FinishTest (Exception):
    pass


class GoOn (Exception):
    pass


# TODO: Ввести секретные клавиши для паузы и прерывания теста
class CogTest:
    # You are welcome to change this for CogTest instances
    name = 'CogTest'
    nreps = 75         # number of repeats within each trial dictionary
    
    maxtrials = 10000  # maximum number of trials in the main test
    mintrain = 5       # minimum number of training trials
    maxtrain = 20      # maximum number of training trials

    ndemo = 20         # number of trials in demo version of the test

    breaktrials = 40   # make a break after this number of trials
    breaktime = 6      # length of the break (sec)
    
    mincorrect = 0.7        # maximum percent of incorrect responses before test halts
                            # also, this is the minimum percent of correct responses
                            # to finish training series
    maxinvalidstrike = 10   # interrupt the test when the this number of consecutive responses is invalid
    nonresptime = 3         # maximum non-response time (sec)

    # This is trial dictionary passed to data.TrialHandler
    # Must contain training series
    # Each series must contain 'cor_resp' which is correct response
    # (key on a keyboard)
    trial_dict = OrderedDict(
        [('training', [{'target': None, 'cor_resp': None}]),
         ('main',     [{'target': None, 'cor_resp': None}])])

    # This is the key to interrupt the test between series,
    # kept for testers
    interruptkey = 'y'

    # Don't change this
    # Internal test components
    status = 'missing'
    start_time = None
    end_time = None 

    varnames = []
    vars = {}
    keys = None
    
    test_screen = None
    close_test_screen = False
    instr_stimuli = {}
    trial_stimuli = {}
    io = None
    keyboard = None
    data_file = None

    totalN = 0
    invalidstrike = 0
    ncorrect = 0
    nfailed = 0
    trial_seq = 0  # This one is to check percent of correct properly
                   # Is it the same as trial.thisN?
                   # No, because if we interrupt the test to show instruction,
                   # we have to count the trials from zero.
                   # If there were many errors before, it will interrupt again
                   # imidiately.
    training_trials = None
    
    def __init__(self):
        pass

    def init_devices(self):
        # Initialize test screen
        if self.test_screen is not None:
            self.close_test_screen = False
        else:
            self.test_screen = visual.Window(fullscr=True, units='pix',
                                             screen=0, winType='pyglet')
            self.test_screen.winHandle.activate()

        self.test_screen.mouseVisible = False

        # Initialize keyboard input
        self.io = iohub.launchHubServer()
        self.keyboard = self.io.devices.keyboard
        
    def init_attr(self):
        # Validity checks
        # Check that all keys in trial_dict are same
        trial_names = []
        for i in self.trial_dict.itervalues():
            for j in i:
                trial_names.append(j.keys())

        if not all([i == trial_names[0] for i in trial_names[1:]]):
            raise RuntimeError('trial_dict keys must be same within each series')
        
        # Initialize main attributes
        self.start_time = datetime.now()
        self.status = 'started'
        
        self.varnames = ['n', 'series', 'trial', 'status'] \
                 + trial_names[0] \
                 + ['response', 'accuracy', 'latency']
        
        self.vars = {i: None for i in self.varnames}
        
    def start(self, data_folder, mode=u'Демо', test_screen=None):
        logging.console.setLevel(logging.WARNING)
        log = logging.LogFile('data/' + data_folder + '/' + self.name + '.log',
                              level=logging.INFO, filemode='w')

        self.init_attr()
                
        # Make output folder
        DATA_FILE = 'data/' + data_folder + '/' + self.name + '.csv'
        self.data_file = open(DATA_FILE, mode='w')
        self.data_file.write(';'.join(self.varnames) + '\n')

        self.test_screen = test_screen
        self.init_devices()
        self.init_instr_stimuli()
        self.init_trial_stimuli()
        
        # --------------------------------------------------------------------
        # Start the test               
        # 1. Instruction
        self.vars['series'] = 'training'
        # We will need this for demonstration
        self.training_trials = self.trial_dict.pop('training')

        try:
            self.start_demonstration()
        except FinishTest:
            self.exit()
            return

        self.keys = [x['cor_resp'] for x in self.training_trials]
        trials = data.TrialHandler(self.training_trials,
                                   self.nreps, method='random')
        core.wait(1)
        
        maxtrials = self.maxtrain
        for trial in trials:
            if self.totalN > maxtrials:
                self.status = 'interrupted'
                self.exit()
            # Run trial
            self.trial_seq += 1
            self.totalN += 1
            self.vars['n'] = self.totalN
            self.vars['trial'] = trials.thisN + 1
            for i, v in trial.iteritems():
                self.vars[i] = v
                
            self.run_trial(trial)
            self.write_data()

            # Check status
            if self.trial_seq >= self.mintrain:
                if float(self.ncorrect) / self.trial_seq >= self.mincorrect:
                    break
                else:
                    try:
                        self.check_status()
                    except FinishTest:
                        self.exit()
                        return
            logging.flush()
        
        # --------------------------------------------------------------------
        # 2. Main series
        if mode == u'Демо':
            maxtrials = self.ndemo
        else:
            maxtrials = self.maxtrials
        self.totalN = 0

        try:
            self.instr_stimuli['start_main'].draw()
            self.test_screen.flip()
            self.suspend(wait=None)
        except FinishTest:
            self.exit()
            return
        except GoOn:
            pass
        
        for series in self.trial_dict:
            self.nfailed = 0
            self.invalidstrike = 0
            self.ncorrect = 0
            self.trial_seq = 0

            self.vars['series'] = series
            
            self.keys = [x['cor_resp'] for x in self.trial_dict[series]]
        
            trials = data.TrialHandler(self.trial_dict[series], self.nreps,
                                       method='random')
            core.wait(1)
            for trial in trials:
                if self.totalN + 1 > maxtrials:
                    self.status = 'complete'
                    break
                if self.trial_seq >= self.mintrain:
                    try:
                        self.check_status()
                    except FinishTest:
                        self.exit()
                        return
                
                # break after breaktrials number of trials
                if self.totalN > 0 and (self.totalN % self.breaktrials) == 0:
                    self.make_a_break(self.breaktime)

                self.trial_seq += 1
                self.totalN += 1
                self.vars['n'] = self.totalN
                self.vars['trial'] = trials.thisN + 1
                for i, v in trial.iteritems():
                    self.vars[i] = v
                
                self.run_trial(trial)
                self.write_data()
                logging.flush()
        else:
            self.status = 'complete'
        
        self.exit()
        return

    def check_status(self):
        # If last response was correct we don't perform check
        if self.vars['accuracy'] != 'correct':
            # Strike of invalid responses or too many incorrect
            if (self.invalidstrike >= self.maxinvalidstrike) or \
               (float(self.ncorrect)/self.trial_seq <= self.mincorrect):
                if self.nfailed >= 2:
                    self.status = 'interrupted'
                    raise FinishTest()
                    return
                else:
                    self.nfailed += 1
                    self.invalidstrike = 0
                    self.ncorrect = 0
                    self.trial_seq = 0
                    self.instr_stimuli['instr_fail'].draw()
                    self.test_screen.flip()
                    core.wait(3)
                    self.start_demonstration()
                
    def write_data(self):
        for x in self.varnames:
            self.data_file.write(str(self.vars[x]) + ';')
        self.data_file.write('\n')
 
    def exit(self):
        self.end_time = datetime.now()
        self.io.quit()
        self.data_file.close()
        if self.close_test_screen:
            self.test_screen.close()
        logging.flush()
    
    def init_instr_stimuli(self):
        # Instruction for each series from self.trial_dict
        self.instr_stimuli = {
            'start_main':
                visual.TextStim(self.test_screen, wrapWidth=600,
                                text=u'\
Тренировочная серия закончилась\n\n\
Для начала основной серии нажми любую клавишу'),
            # Feedback text used in the training series
            'feedback':
                visual.TextStim(self.test_screen, text=u'',
                                pos=[0, 0]),
            # Instruction shown when participant has to do smth to start
            # Not used here
            'instr_start':
                visual.TextStim(self.test_screen, text=u'',
                                pos=[0, 100]),
            # Instruction shown in case of non-response
            'instr_nonresp':
                visual.TextStim(self.test_screen, 
                                text=u'Слишком медленно!',
                                pos=[0, 100]),
            'instr_fail':
                visual.TextStim(self.test_screen, 
                                text=u'\
Слишком много ошибок!\n\
Внимательно посмотри инструкцию еще раз\n\n\
Нажми любую клавишу',
                                pos=[0, 0])}

    # You are welcome to change this for CogTest instances
    # Here you define all test stimuli
    # The fixation stimulus must be present
    def init_trial_stimuli(self):
        # TODO: Trial stimuli of fixed sizes
        self.trial_stimuli = {
            # Fixation stimulus indicating start of the trial
            'fixation':
                visual.ShapeStim(self.test_screen, units=None, lineWidth=4, 
                                 pos=[0, 0], lineColor='white',
                                 closeShape=False,
                                 vertices=((0, -10), (0, 10), (0, 0),
                                           (-10, 0), (10, 0)))}
        
    def suspend(self, keys=None, wait=3):
        self.keyboard.clearEvents()

        if keys is None:
            key_presses = self.keyboard.waitForPresses(clear=True, 
                                                       maxWait=wait)
        else:
            key_presses = self.keyboard.waitForPresses(keys=keys + [self.interruptkey],
                                                       clear=True, 
                                                       maxWait=wait)
        resp = [key.key for key in key_presses]
    
        if len(resp) > 0:
            if self.interruptkey in resp:
                self.status = 'interrupted'
                raise FinishTest()
            else:
                raise GoOn()

    # You are welcome to change this for CogTest instances
    # Here you define the test demonstration/instruction
    def start_demonstration(self):
        self.test_screen.flip()
        self.suspend(wait=None)
        
    def make_a_break(self, breaktime):
        for i in reversed(range(breaktime-1)):
            note = visual.TextStim(self.test_screen, text=u'\
Передышка!\n\
Тест продолжится через %d секунд' % (i + 1) ,
                                   pos=[0, 0], color='black')
            note.draw()
            self.test_screen.flip()
            core.wait(1)
        note = visual.TextStim(self.test_screen,
                               text=u'Тест сейчас продолжится, приготовься!',
                               pos=[0, 0], color='black')
        note.draw()
        self.test_screen.flip()
        core.wait(2)

    # You are welcome to change this for CogTest instances
    # Here you define the screen outlook
    def show_trial_screen(self):
        pass

    # You are welcome to change this for CogTest instances
    # Here you define how the trial information translates to stimuli
    def show_stim(self, trial):
        pass

    def run_trial(self, trial):
        wait_time = random.uniform(0.5, 2.5)
        self.vars['timestamp'] = datetime.now()
        self.vars['latency'] = None
        self.vars['response'] = None
        self.vars['accuracy'] = None
        self.vars['delay'] = wait_time
        
        # Start waiting, show fixation
        self.keyboard.clearEvents()
        self.show_trial_screen()
        self.trial_stimuli['fixation'].draw()
        self.test_screen.flip()
        wait_stim = self.keyboard.waitForPresses(maxWait=wait_time, 
                                                 keys=self.keys, 
                                                 clear=True)
        
        if wait_stim:
            self.vars['status'] = 'preterm'
        else:
            # Show stimuli
            self.show_trial_screen()
            self.show_stim(trial)
            self.test_screen.flip()
            trial_start = core.getTime()
            rel = self.keyboard.waitForPresses(keys=self.keys, 
                                               maxWait=self.nonresptime,
                                               clear=True)

            if len(rel) == 1:
                resp = rel.pop()
                self.vars['latency'] = resp.time - trial_start
                if resp.char == trial['cor_resp']:
                    self.vars['accuracy'] = 'correct'
                    self.ncorrect += 1
                else:
                    self.vars['accuracy'] = 'incorrect'
                self.vars['response'] = resp.char
                self.vars['status'] = 'valid'
                self.invalidstrike = 0
            else:
                self.invalidstrike += 1
                if len(rel) == 0:
                    self.vars['status'] = 'nonresponse'
                    self.instr_stimuli['instr_nonresp'].draw()
                else:
                    self.vars['status'] = 'invalid'

        if self.vars['series'] == 'training':
            self.instr_stimuli['feedback'].setText(text=self.feedback())
            self.instr_stimuli['feedback'].draw()
            self.show_trial_screen()
            self.test_screen.flip()
            core.wait(1)
        self.show_trial_screen()
        self.test_screen.flip()
        core.wait(0.7)

    def feedback(self):
        if self.vars['status'] == 'valid':
            if self.vars['accuracy'] == 'correct':
                return u'Верный ответ'
            else:
                return u'Неверный ответ'
        elif self.vars['status'] == 'preterm':
            return u'Преждевременный ответ'
        elif self.vars['status'] == 'nonresponse':
            return u'Слишком медленный ответ'
        elif self.vars['status'] == 'invalid':
            return u'Невалидный ответ'
