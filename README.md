This is Reaction Time test battery
==================================

This test battery is implemented to assess individual differences in response time across various decision tasks: simple and choice reaction time (SRT, CRT2, CRT4, SRT_rel, CRT2_rel), Stroop task with two and three colors (stroop2_1, stroop2_2, stroop3_1, stroop3_2), verbal classification (VerbCRT) and visuo-spatial classification (VisCRT).

_Quick start:_  
bash/cmd: `python launch.py`  
also: `launch.bat`

Description of test battery
===========================
This battery aims to serve as a self-contained software to be used for assessment at school. At the same time it simplifies development of the tests and allows modification of test workflow across the whole test battery. It includes following functionality:
1. The tests are implemented as instances of CogTest and CogTestRelease classes. This eases modification of the whole battery and separate tests. CogTest implements press responses, CogTestRelease - release responses. The list of tests is stored in `testlist.py`. The battery can be modified by commenting out or rearranging the tests in a test list.
2. Each test starts with instruction/demonstration, training session and one or several main sessions. 
3. The test battery has been developed to be used at school with minimum intervention from tester/teacher. This is why the script performs additional checks to help to ensure that the date are valid:
* The script checks that accuracy lies above certain level (default is 30%). When participant performs poor, the script interrupts and repeats demonstration. If performance remains low, the test interrupts execution and passes to the next.
* The logic applies when participant gives a sequence of invalid answers (e.g., preterm responses), 10 by default.
* At regular intervals (each 40 trials by default) the test pauses to let a participant have a short breal (6s by default).
* For each trial within the test and for the whole battery the detailed information is recorded (timestamp, execution status). The script also writes the log and computer specifications (CPU, RAM, screen resolution).
4. The script `test_summary.py` gathers specifications of test battery, including total number of trials.
5. The user can choose to pass either full or demo version of the test battery. Demo version сuts number of trials in ach test to 20 (let alone training session that remains unchanged).

Description of tests
====================
_SRT, CRT2, CRT4:_ participant has to respond to a stimulus appearing in one, two or four possible positions by pressing the key.

_VerbCRT:_ participant has to reply whether a word on the screen means plant or animal.

_stroop2_1:_ participant has to reply whether neutral stimulus (XXXXXXX) on the screen is red or green.

_stroop2_2:_ participant has to reply whether a word ('red' or 'green') on the screen is written in red or green.

_stroop3_1:_ participant has to reply whether neutral stimulus (XXXXXXX) on the screen is red, green or blue.

_stroop3_2:_ participant has to reply whether a word ('red', 'green' or 'blue') on the screen is written in red, green or blue.

_VisCRT:_ participant has to compare two shapes by either shape or color, depending on the cue (a word 'shape' or 'color').

_SRT_rel, CRT2_rel:_ participant has to respond to a stimulus appearing in one or two possible positions by releasing the key.


Requirements
============
The implementation is based on PsychoPy. The stand-alone version of PsychoPy (v.1.90.3, or PsychoPy2) is supposedly sufficient. PsychoPy2 requires fully finctional OpenGL 2.0 (details [here][requirements]).

[requirements]: http://psychopy.org/installation.html

To be implemented
=================
1. Encrypted storage of personal data.
2. Self-contained executable for OS Windows.
