#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import psutil
import platform
import psychopy
import wx
from datetime import datetime
from psychopy import gui, core
from testlist import test_battery
from setup_console import setup_console
from multiprocessing import freeze_support
from psychopy import logging

VERSION = 'v0.1'
BATTERY_ID = '000000'


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

    # Showing information dialog
    intro = u'''
Спасибо, что согласились поучаствовать в исследовании времени реакции!

Предлагаю Вам пройти набор тестов, в которых нужно как можно быстрее и точнее \
реагировать на стимулы (изображения или слова).

Время выполнения заданий составляет ~15 минут в демо-версии и ~60 минут в полной версии. \
Перед началом тестов программа соберет информацию о характеристиках Вашего компьютера:
    - Название операционной системы
    - Тип процессора
    - Количество оперативной памяти
    - Размер и частота обновления экрана
    - Используемую версию Питона

Данные и логи записываются в папке data. \
В данный момент батарея находится на стадии тестирования, \
поэтому я буду очень благодарен любой обратной связи. \
Отправляйте обратную связь и результаты из папки data по адресу:
ivan.a.voronin@gmail.com
Страница проекта на гитхабе: 
https://github.com/IvanVoronin/RT_tests

С уважением,
Иван Воронин'''

    app = wx.App()
    intro_dlg = wx.MessageDialog(None,
                                 intro, u'Добро пожаловать',
                                 wx.OK_DEFAULT | wx.CANCEL | wx.OK | wx.ALIGN_LEFT
                                 | wx.ICON_INFORMATION)

    resp = intro_dlg.ShowModal()
    if resp != wx.ID_OK:
        core.wait(1)
        core.quit()
        sys.exit(0)

    # Show the ID questionnaire
    info_dlg = gui.Dlg(title=u'Начать эксперимент')

    info_dlg.addField(u'ID:', u'0001')
    info_dlg.addField(u'Имя:', u'')
    info_dlg.addField(u'Дата рождения:', u'01.01.1990')
    info_dlg.addField(u'Пол:', choices=[u'Мужской',
                                        u'Женский'])

    info_dlg.addField(u'Режим теста:', choices=[u'Демо',
                                                u'Полный'])

    info_dlg.addField(u'Я согласен/согласна участвовать', True)

    info_dlg.addText(u'\nВыберите тесты для выполнения')
    for i in test_battery.keys():
        info_dlg.addField(i, True)

    info_dlg.addText(u'\nНе забудьте включить английскую расскладку клавиатуры!\n')
    info_dlg.show()

    if not info_dlg.OK:
        core.wait(1)
        core.quit()
        sys.exit(0)

    START_TIME = datetime.now()
    (ID, name, age, sex, test_mode, agr), run_tests = \
        info_dlg.data[0:6], info_dlg.data[6:]

    if not agr:
        core.wait(1)
        core.quit()
        sys.exit(0)

    out_file.write(test_mode + ';' +
                   ID + ';' +
                   name + ';' +
                   str(age) + ';' +
                   sex + ';')
    out_dir = START_TIME.strftime('%Y-%m-%d_%H%M__') + str(ID)
    os.mkdir('data/' + out_dir)

    for test, run in zip(test_battery.values(), run_tests):
        if not run:
            test.status = 'skipped'

    # Log the warnings
    # TODO: Log in-test warnings, log interruptions, pauses and demonstrations
    # TODO: Log test specifications
    logging.console.setLevel(logging.WARNING)
    log = logging.LogFile('data/' + out_dir + '/log.log',
                          level=logging.INFO, filemode='w')

    # The same window can be shared by tests
    # Here you can put window specifications
    test_screen = psychopy.visual.Window(fullscr=True, units='pix',
                                         monitor=0, winType='pyglet')
    test_screen.winHandle.activate()
    test_screen.mouseVisible = False

    screen_size = test_screen.size
    fps = test_screen.getActualFrameRate()
    frame_duration = test_screen.getMsPerFrame()

    logging.flush()
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

    # Run the tests, collect stats
    for test in test_battery.itervalues():
        log.write('\n======================================================================\n'
                + 'STARTING ' + test.name + '\n')
        if test.status != 'skipped':
            try:
                test.start(out_dir, mode=test_mode,
                           test_screen=test_screen)
            except Exception:
                test.status = 'failed'
                test.end_time = datetime.now()
                log.write('SOMETHING HAPPENED!\n')
                logging.flush()
                # If something went wrong we open the test screen again
                # FIXME: Probably not working as expected
                if test_screen not in locals() or test_screen._closed:
                    test_screen = psychopy.visual.Window(fullscr=True, units='pix',
                                                         monitor=0, winType='pyglet')
                    test_screen.winHandle.activate()
                    test_screen.mouseVisible = False
                    logging.flush()
        else:
            test.start_time = datetime.now()
            test.end_time = datetime.now()
            log.write(test.name + ' SKIPPED\n')
        logging.flush()
        log.write('FINISHING ' + test.name
                + '\n======================================================================\n')

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
