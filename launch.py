#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file starts the test

1. Ask for home directory
   Create 'data' dir
2. Show the blanc window: 
    - ID   - integer
    - Name - character
    - Age  - integer
    - Sex  - 'Male'/'Female'
   Make a folder 'data/id'
   Write into a file 'data/participants.dat
3. Start Test1
   Write the output into data/id/Test1.dat    
   (?) Write the log into log log/id/Test1.log
4. Start Test2
   ... 
'''

import os
import sys

import UserList, UserString
from datetime import datetime
from psychopy import gui, core
from testlist import test_battery

HOME_FOLDER = os.path.dirname(__file__)
os.chdir(HOME_FOLDER)

# Make folders and attach output table
if not os.access('data', os.F_OK):
    os.mkdir('data')
else:
    if (os.path.isfile('data/participants.csv')):
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

# background = visual.Window(fullscr=True, units='pix',
#                           screen=1, winType='pyglet')
# Show the ID questionnaire
info_dlg = gui.Dlg(title=u'Начать эксперимент')

# .decode('utf-8')
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
    # No need for a status here as there is no data record
    core.wait(1)
    #    background.close()
    core.quit()
    sys.exit(0)

START_TIME = datetime.now()
(ID, name, age, sex, test_mode, agr), run_tests = \
    info_dlg.data[0:6], info_dlg.data[6:]

if not agr:
    core.wait(1)
    #    background.close()
    core.quit()
    sys.exit(0)

out_file.write(test_mode + ';' + \
               ID + ';' + \
               name + ';' + \
               str(age) + ';' + \
               sex + ';')
out_dir = str(ID) + START_TIME.strftime('_%Y-%m-%d_%H%M')
os.mkdir('data/' + out_dir)

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
# TODO: Write log-file for each test

out_file.write(('complete' if BAT_STATUS else 'incomplete') + ';' + \
               START_TIME.strftime('%Y-%m-%d %H:%M:%S') + ';' + \
               END_TIME.strftime('%Y-%m-%d %H:%M:%S') + ';')
for test in test_battery.itervalues():
    out_file.write(test.status + ';' + \
                   test.start_time.strftime('%Y-%m-%d %H:%M:%S') + ';' + \
                   test.end_time.strftime('%Y-%m-%d %H:%M:%S') + ';')
out_file.write('\n')
out_file.close()

# debriefing = visual.TextStim(background,
#                             text = u'Благодарим за участие в исследовании!',
#                             pos = [0,0])
# debriefing.draw()
# background.flip()
core.wait(2)
# background.close()
core.quit()
