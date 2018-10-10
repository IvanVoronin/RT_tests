#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import psutil
import platform
import psychopy
from datetime import datetime
from psychopy import gui, core
from testlist import test_battery
from multiprocessing import freeze_support

VERSION = '0.1'
BATTERY_ID = '000000'


def launch():
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
    info_dlg = gui.Dlg(title=u'Начать эксперимент')

    info_dlg.addField(u'ID:', u'0001')
    info_dlg.addField(u'Имя:', u'Иван Дурак')
    info_dlg.addField(u'Дата рождения:', '01.01.1990')
    info_dlg.addField(u'Пол:', choices=[u'Мужской',
                                        u'Женский'])

    info_dlg.addField(u'Режим теста:', choices=[u'Демо',
                                                u'Полный'])

    info_dlg.addField(u'Я согласен/согласна участвовать', True)

    info_dlg.addText(u'\nВыберите тесты для выполнения')
    for i in test_battery.keys():
        info_dlg.addField(i, True)

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

    out_file.write(test_mode + ';' + \
                   ID + ';' + \
                   name + ';' + \
                   str(age) + ';' + \
                   sex + ';')
    out_dir = str(ID) + START_TIME.strftime('_%Y-%m-%d_%H%M')
    os.mkdir('data/' + out_dir)

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
        specs.write('Python version: %s\n' % platform.python_version())
        specs.write('Python implementation: %s\n' % platform.python_implementation())
        specs.write('PsychoPy version: %s\n' % psychopy.__version__)
        specs.write('Battery version: %s\n' % VERSION)
        specs.write('Battery ID: %s\n' % BATTERY_ID)

    for test, run in zip(test_battery.values(), run_tests):
        if not run:
            test.status = 'skipped'

    # Run the tests, collect stats
    for test in test_battery.itervalues():
        if test.status != 'skipped':
            try:
                test.start(out_dir, mode=test_mode)
            except Exception:
                test.status = 'failed'
                test.end_time = datetime.now()
        else:
            test.start_time = datetime.now()
            test.end_time = datetime.now()

    END_TIME = datetime.now()

    BAT_STATUS = all([test.status == 'complete' for test in test_battery.values()])

    # TODO: Ввести секретную комбинацию клавиш для определения набора тестов

    out_file.write(('complete' if BAT_STATUS else 'incomplete') + ';' + \
                   START_TIME.strftime('%Y-%m-%d %H:%M:%S') + ';' + \
                   END_TIME.strftime('%Y-%m-%d %H:%M:%S') + ';')
    for test in test_battery.itervalues():
        out_file.write(test.status + ';' + \
                       test.start_time.strftime('%Y-%m-%d %H:%M:%S') + ';' + \
                       test.end_time.strftime('%Y-%m-%d %H:%M:%S') + ';')
    out_file.write('\n')
    out_file.close()

    debriefing = gui.Dlg(title=u'Спасибо за участие!',
                         labelButtonOK=u'Закончить',
                         labelButtonCancel=u'Закончить')
    debriefing.addText(u'Благодарим за участие в эксперименте!')
    debriefing.show()
    core.quit()


if __name__ == '__main__':
    freeze_support()
    launch()
