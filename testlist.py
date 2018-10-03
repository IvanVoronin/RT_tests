#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

import os
import sys
sys.path.append(os.path.dirname(__file__) + '/tests')

import SRT
import CRT2
import CRT4
import VerbCRT
import stroop2_1
import stroop2_2
import stroop3_1
import stroop3_2
import VisCRT
import SRT_rel
import CRT2_rel 

test_battery = OrderedDict([
    ('SRT', SRT.SRT()),
    ('CRT2', CRT2.CRT2()),
    ('CRT4', CRT4.CRT4()),
    ('VerbCRT', VerbCRT.VerbCRT()),
    ('stroop2_1',  stroop2_1.stroop2_1()),
    ('stroop2_2',  stroop2_2.stroop2_2()),
    ('stroop3_1',  stroop3_1.stroop3_1()),
    ('stroop3_2',  stroop3_2.stroop3_2()),
    ('VisCRT', VisCRT.VisCRT()),
    ('SRT_rel',  SRT_rel.SRT_rel()),
    ('CRT2_rel', CRT2_rel.CRT2_rel())])

# Вернуть тесты SRT и CRT2 с освобождением кнопки
# TODO: Validate instruction
# TODO: Gather statistics about number of trials, about test duration
