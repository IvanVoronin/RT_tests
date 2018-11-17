@ECHO off
TITLE Launch the RT test battery
set gitdir="../Progs/git"
set path=%gitdir%/cmd;%path%
git checkout RT_tests_45min_2018
git pull
python.exe launch_win.py
rem Uncomment the next line if you have more than one Python distro installed
rem "C:\Program Files (x86)\PsychoPy2\python.exe" launch.py