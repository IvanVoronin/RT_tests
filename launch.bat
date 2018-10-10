@ECHO off
TITLE Launch the RT test battery
python.exe launch.py
IF %ERRORLEVEL%==1 (
    ECHO It seems that PsychoPy is not installed on this machine
    ECHO Do you want to download and install PsychoPy?
    :: CHOICE
    SET /p resp="y=YES, n=NO "
    IF "%resp%"=="y" (
        START "" https://github.com/psychopy/psychopy/releases/download/1.90.3/StandalonePsychoPy2-1.90.3-win32.exe
        ECHO Install PsychoPy and start this script again
        PAUSE
    ) ELSE (
       ECHO Aborted!
       PAUSE
    )
