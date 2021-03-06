#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from tests import SRT, CRT2, CRT4, VerbCRT
from tests import stroop2_1, stroop2_2, stroop3_1, stroop3_2
from tests import VisCRT, SRT_rel, CRT2_rel

# Total time limit
TIME_LIMIT = 180

# This is the list of the tests to launch
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

