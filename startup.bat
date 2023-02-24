@echo off

REM **************************************************
REM author:Mingliang Wang
REM brief:launch the main.py
REM date:2023.2.24
REM version:1.0
REM **************************************************

SETLOCAL ENABLEDELAYEDEXPANSION

set "parentDir=..\"
set "excludeDir=%cd%"

REM Get all directories of the previous level.
set "dirs_list="
for /d %%D in (%parentDir%*) do (
    set "dir=%%~fD"
    if not "!dir!" == "%excludeDir%" (
        set "dirs_list=!dirs_list! "%%~nxD""
    )
)

REM Display all directories.
set /a count=0
for %%D in (%dirs_list%) do (
    echo [!count!]:    !parentDir!%%~D
    set /a count+=1
)

:RESTART
REM Get input of the user.
set /p input=input the index of data directory:
set i=0
set /a ok=0
for %%f in (%dirs_list%) do (
    if !i! equ %input% (
        echo enter dir: %parentDir%%%~f
        set data_dir=%parentDir%%%~f
        set /a ok=1
    )
    set /a i+=1
)

if !ok! equ 0 (
    echo Your input: !input! is invalid, restart now...
    goto RESTART
)

set out_data_dir=%data_dir%_out

python main.py %data_dir% %out_data_dir%

ENDLOCAL

:END