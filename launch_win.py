#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import psutil
import platform
import psychopy
import wx
import traceback
import win32api
import win32con
from datetime import datetime
from psychopy import gui, core
from testlist import test_battery, TIME_LIMIT
from setup_console import setup_console
from multiprocessing import freeze_support
from psychopy import logging

VERSION = 'v0.1'
BATTERY_ID = 'RT_tests_45min_2018'


def launch():
    """Launch a test battery.

    The test battery is stored in testlist.py.
    This is to be called from the RT_test folder, otherwise some tests
    may not be loaded when they contain a reference to other resources
    (like the stimuli list in the VerbCRT).
    """
    setup_console()

    # This part aims to fix the problem with multitasking when making
    # executable using pyinstaller
    if getattr(sys, 'frozen', False):
            # we are running in a bundle
            HOME_FOLDER = os.path.dirname(sys.executable)
    else:
            # we are running in a normal Python environment
            HOME_FOLDER = os.path.dirname(os.path.abspath(__file__))

    os.chdir(HOME_FOLDER)

    # Make folders and attach output table
    if not os.access('data', os.F_OK):
        os.mkdir('data')

    if os.path.isfile('data/participants.csv'):
        try:
            out_file = open('data/participants.csv', mode='a')
        except:
            print('The directory is not writable, cannot write the data')
    else:
        out_file = open('data/participants.csv', mode='w')
        out_file.write('test_mode;id;name;age;sex;status;start_time;end_time;')
        for i in test_battery:
            out_file.write(i + '_status;' + \
                           i + '_start_time;' + \
                           i + '_end_time;')
        out_file.write('\n')

    # Show the ID questionnaire
    info_dlg = gui.Dlg(title=u'Добро пожаловать в эксперимент')

    info_dlg.addField(u'ID:', u'')
    info_dlg.addField(u'Имя:', u'')
    info_dlg.addField(u'Дата рождения:', u'01.01.1995')
    info_dlg.addField(u'Пол:', choices=[u'Женский',
                                        u'Мужской'])
    info_dlg.addField(u'Какой рукой ты пишешь?',
                      choices=[u'Правой',
                               u'Левой'])

    info_dlg.show()

    if not info_dlg.OK:
        core.wait(1)
        core.quit()
        sys.exit(0)

    START_TIME = datetime.now()
    (ID, name, age, sex, handedness) = info_dlg.data

    out_file.write(ID + ';' +
                   name + ';' +
                   str(age) + ';' +
                   sex + ';')
    out_dir = START_TIME.strftime('%Y-%m-%d_%H%M__') + str(ID)
    os.mkdir('data/' + out_dir)

    # Showing information dialog
    intro = u'''
Спасибо, что %s поучаствовать в эксперименте на скорость реакции!

Эксперимент состоит из нескольких тестов разной сложности. \
В каждом тесте надо отвечать как можно быстрее и как можно точнее. \
В начале каждого теста будет инструкция и серия тренировочных попыток. \
Прежде чем начинать тест, внимательно прочти инструкцию и посмотри, \
как положить руку на клавиатуру.''' \
            % (u'согласился' if sex == u'Мужской' else u'согласилась').decode('utf-8')

    app = wx.App()
    intro_dlg = wx.MessageDialog(None,
                                 intro, u'Добро пожаловать в эксперимент',
                                 wx.OK_DEFAULT | wx.OK | wx.ALIGN_LEFT
                                 | wx.ICON_INFORMATION)

    resp = intro_dlg.ShowModal()
    if resp != wx.ID_OK:
        core.wait(1)
        core.quit()
        sys.exit(0)

    # Log the warnings
    # TODO: Log in-test warnings, log interruptions, pauses and demonstrations
    logging.console.setLevel(logging.WARNING)
    log = logging.LogFile('data/' + out_dir + '/log.log',
                          level=logging.INFO, filemode='w',
                          encoding='utf8')

    # The same window can be shared by tests
    # Here you can put window specifications
    test_screen = psychopy.visual.Window(size=(1024, 768),
                                         fullscr=True,
                                         units='pix',
                                         monitor=0, winType='pyglet')
    test_screen.winHandle.activate()
    test_screen.mouseVisible = False
    win32api.LoadKeyboardLayout('00000409', win32con.KLF_ACTIVATE | win32con.KLF_REORDER)
    # FIXME: This still not working when each app has its own keyboard layout

    try:
        screen_size = test_screen.size
        fps = test_screen.getActualFrameRate()
        frame_duration = test_screen.getMsPerFrame(msg=u'Тест сейчас начнётся')
        test_screen.flip()

        # Gather system information
        with open('data/' + out_dir + '/specs.txt', mode='w') as specs:
            specs.write('Platform: %s\n' % platform.platform())
            specs.write('Machine: %s\n' % platform.machine())
            specs.write('Processor: %s\n' % platform.processor())
            specs.write('Number of CPUs: %d\n' % psutil.cpu_count(logical=False))
            specs.write('Available CPUs: %d\n' % len(psutil.Process().cpu_affinity()))
            specs.write('Current CPU load: %0.1f%%\n' % psutil.cpu_percent())
            specs.write('Total RAM: %dMb\n' % int(psutil.virtual_memory().total / (1024 * 1024)))
            specs.write('Available RAM: %dMb\n' % int(psutil.virtual_memory().available / (1024 * 1024)))
            specs.write('Screen size: %dx%d\n' % tuple(screen_size))
            specs.write('FPS: %0.1f\n' % fps)
            specs.write('Frame duration: mean=%0.1fms, SD=%0.1fms, median=%0.1fms\n' % frame_duration)
            specs.write('Python version: %s\n' % platform.python_version())
            specs.write('Python implementation: %s\n' % platform.python_implementation())
            specs.write('PsychoPy version: %s\n' % psychopy.__version__)
            specs.write('Battery version: %s\n' % VERSION)
            specs.write('Battery ID: %s\n' % BATTERY_ID)
    except Exception as e:
        log.write('EXCEPTION: %s\n' % e)

    logging.flush()

    # Run the tests, collect stats
    # TODO: Remove opening test screen after failure
    # TODO: Introduce total interruption
    skip_the_rest = False
    for test in test_battery.itervalues():
        if skip_the_rest:
            test.status = 'skipped'
        if test.status != 'skipped':
            log.write('\n======================================================================\n'
                      + 'STARTING ' + test.name + '\n')
            exc_info = sys.exc_info()
            try:
                test.start(out_dir, mode='Full',
                           test_screen=test_screen)
            except Exception as e:
                test.status = 'failed'
                test.end_time = datetime.now()
                log.write('SOMETHING HAPPENED!\n')
                log.write('EXCEPTION: %s\n' % e)
                logging.flush()

                # # If something went wrong we open the test screen again
                # # FIXME: Probably not working as expected
                # if test_screen not in locals() or test_screen._closed:
                #     log.write('OPENING A NEW WINDOW\n')
                #     test_screen = psychopy.visual.Window(size=(1024, 768),
                #                                          fullscr=True,
                #                                          units='pix',
                #                                          monitor=0, winType='pyglet')
                #     test_screen.winHandle.activate()
                #     test_screen.mouseVisible = False
                #     win32api.LoadKeyboardLayout('00000409', 1)
                #     logging.flush()

            finally:
                log.write(traceback.format_exc(exc_info))
                del exc_info
            log.write('FINISHING ' + test.name
                      + '\n======================================================================\n')
        else:
            test.start_time = datetime.now()
            test.end_time = datetime.now()
            log.write(test.name + ' SKIPPED\n')
        current_dur = test.end_time - START_TIME
        if current_dur.seconds/60.0 > TIME_LIMIT:
            skip_the_rest = True
            log.write('TIME LIMIT REACHED\n')

    END_TIME = datetime.now()

    BAT_STATUS = all([test.status == 'complete' for test in test_battery.values()])
    # TODO: Ввести секретную комбинацию клавиш для определения набора тестов

    out_file.write(('complete' if BAT_STATUS else 'incomplete') + ';' +
                   START_TIME.strftime('%Y-%m-%d %H:%M:%S') + ';' +
                   END_TIME.strftime('%Y-%m-%d %H:%M:%S') + ';')
    for test in test_battery.itervalues():
        out_file.write(test.status + ';' +
                       test.start_time.strftime('%Y-%m-%d %H:%M:%S') + ';' +
                       test.end_time.strftime('%Y-%m-%d %H:%M:%S') + ';')
    out_file.write('\n')
    out_file.close()

    debriefing = psychopy.visual.TextStim(test_screen,
                                          text=u'\
Благодарим за участие в эксперименте!\n\n\
Окно закроется автоматически')
    debriefing.draw()
    test_screen.flip()
    core.wait(3)
    test_screen.close()
    core.quit()


if __name__ == '__main__':
    freeze_support()
    launch()
