# This is the Reaction Time test battery

This test battery is implemented for the assessment of the individual differences in response time 
across various decision tasks: simple and choice reaction time (SRT, CRT2, CRT4), 
Stroop task with two colors (stroop2_1, stroop2_2) and three colors (stroop3_1, stroop3_2), verbal classification (VerbCRT)
and visuo-spatial classification (VisCRT). The tests are implemented as instances of CogTest class.
Additionally, SRT and CRT2 are implemented in Jensen paradigm (hold -> release) as instances of CogTestRelease class.

The test battery includes following functionality:
1. The user can select full or demo version of the test battery and the set of tests to execute. 
This is for the testing purpose.
2. Each test starts with demostration and training series.
3. The script checks if number of incorrect answers lies within some reasonable limit (e.g., 20%, can be set up for each test).
When participant performs poorly, he/she is shown with a demonstration repeatedly (up to two times).
4. The same applied to the sublequent invalid answers.
5. From time to time the script pauses to let a participant have a break and 

