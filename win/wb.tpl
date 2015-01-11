@echo off
REM plan to use in Windows platform \
REM by useing this, we can call wb.py \
REM just like: wb -p1 -p2 ... -pN

REM set your wb directory here
set wbDIR=to_be_replaced
set wbFILE=%wbDIR%\wb.py

REM new parameter and set it as None
set parameter=

REM concatenate all input parameters
:loop
if "%~1" neq "" set parameter=%parameter% %1 & shift & goto loop
REM (%1) -> (%~1), strip the quotation mark
REM see if (%1) is ("a b"), thus ("%1") is (""a b"") means ("") and (a b) and ("")
REM change (%1) to (%~1) means ("a b") become (a b), then ("%1") means ("a b")
REM well, it's ok now

REM call main Python file
pushd "%wbDIR%"
python "%wbFILE%" %parameter%
popd