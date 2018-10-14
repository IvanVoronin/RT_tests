#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_test_summary(test_battery):
    """Return the specifications of the tests in a test battery.

    This is to be called from the RT_test folder, otherwise some tests
    may not be loaded when they contain a reference to other resources
    (like the stimuli list in the VerbCRT).
    """
    with open('data/test_specifications.csv', mode='w') as f:
        f.write(';'.join([
            'name',
            'parent_class',
            'trial_dict',
            'nreps',
            'total_trials',
            'mintrain',
            'maxtrain',
            'mincorrect',
            'nonresptime',
            'maxinvalidstrike',
            'ndemo',
            'breaktrials',
            'breaktime'
        ]))
        f.write('\n')
        for name, test in test_battery.iteritems():
            parent_class = test.__class__.__bases__[0].__name__
            test.trial_dict.pop('training')
            trial_dict = [len(i) for i in test.trial_dict.values()]
            total_trials = min(test.nreps * sum(trial_dict), test.maxtrials)
            f.write(';'.join([
                name,
                parent_class,
                '+'.join(map(str, trial_dict)),
                str(test.nreps),
                str(total_trials),
                str(test.mintrain),
                str(test.maxtrain),
                str(test.mincorrect),
                str(test.nonresptime),
                str(test.maxinvalidstrike),
                str(test.ndemo),
                str(test.breaktrials),
                str(test.breaktime)
            ]))
            f.write('\n')


if __name__ == '__main__':
    from testlist import test_battery
    import os

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.access('data', os.F_OK):
        os.mkdir('data')

    get_test_summary(test_battery)
