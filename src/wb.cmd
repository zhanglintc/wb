@echo off
REM plan to use in Windows platform \
REM by useing this, we can call xiaobawang.py \
REM just like: wb -p1 -p2 ... -pN

REM new parameter and set it as None
set parameter=

REM concatenate all input parameters
:loop
if "%1" neq "" set parameter=%parameter% %1 & shift & goto loop

REM call main Python file
python xiaobawang.py %parameter%