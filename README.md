This is Reaction Time test battery
==================================

This test battery is implemented for assessment of the individual differences in response time across various decision tasks: simple and choice reaction time (SRT, CRT2, CRT4, SRT_rel, CRT2_rel), Stroop task with two and three colors (stroop2_1, stroop2_2, stroop3_1, stroop3_2), verbal classification (VerbCRT) and visuo-spatial classification (VisCRT).

_Quick start:_ 
bash/cmd: python launch.py
also: launch.bat (either starts an experiment or suggest to install PsychoPy2 if Python is not installed)

This battery aims to serve as a self-contained software to be used for assessment at school. At the same time it simplifies development of the tests and allows modification of test workflow across the whole test battery. It includes following functionality:
1. The user can select full or demo version of the test battery and the set of tests to execute. This is for the testing purpose. Demo version of the test includes 20 trials in main series.
2. Each test starts with demostration and training series.
3. The script checks if number of incorrect answers lies within 30%. When participant performs poorly, the script interrupts and shows the demonstration for a second time.
4. The same applies to 10 consecutive invalid answers. The script interrupts and repeats demonstration.
5. Each 40 trials the script pauses to let a participant have a short break (6s).
6. The timestamps and execution status are recorded for each test and for the whole test battery.

The specifications --- like number of trials, minimum number of correct answers, maximum subsequence of invalid answers and non response time --- are defined within parent classes and can be adjusted for each test separately. 

Description of tests
====================
_SRT:_ participant has to press SPACE bar as soon as stimulus appears in the middle of the screen.

_CRT2:_ participant has to press either D or L as a response to the stimulus appearing on the left or on the right.

_CRT4:_ participant has to press E, D, L or P as a response to the stimulus appearing in one of four possible positions.

_VerbCRT:_ participant has to reply whether a word on the screen means plant or animal.

_stroop2_1:_ participant has to reply whether a neutral stimulus (XXXXXXX) on the screen is red or green.

_stroop2_2:_ participant has to reply whether a word ('red' or 'green') on the screen is written in red or green.

_stroop3_1:_ participant has to reply whether a neutral stimulus (XXXXXXX) on the screen is red, green or blue.

_stroop3_2:_ participant has to reply whether a word ('red', 'green' or 'blue') on the screen is written in red, green or blue.

_VisCRT:_ participant has to compare two shapes on one feature, either shape or color depending on the cue (the arrow in the middle of the screen).

_SRT_rel:_ participant has to hold SPACE bar and release it as soon as stimulus appears in the middle of the screen.

_CRT2_rel:_ participant has to hold D or L and release one as a response to the stimulus appearing on the left or on the right.

Requirements
============
The implementation is based on PsychoPy. The stand-alone version of PsychoPy (v.1.90.3, or PsychoPy2) is supposedly sufficient. PsychoPy2 requires fully finctional OpenGL driver (details [here][requirements]).

[requirements]: http://psychopy.org/installation.html

To be implemented
=================
1. Encrypted storage of personal data.
2. Self-contained executable for Windows.
