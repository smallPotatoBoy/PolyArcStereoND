@echo off
REM Launch PolyArcStereoND in nDisplay cluster runtime mode.
REM This is the ONLY way to get the actual 4-viewport cluster output —
REM editor preview / PIE don't run cluster runtime in 5.5.
REM
REM Window size defaults to 1280x720 for desktop. For real LED splicer
REM output, set RESX=3612 RESY=2236 (or pass them as args).

setlocal
set UE="D:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe"
set PROJ="D:\Claude\UE5\PolyArcStereoND\PolyArcStereoND.uproject"
set MAP=/Game/NewMap
set CFG=/Game/nDisplay/BP_PolyArcStereo.BP_PolyArcStereo
set NODE=node_main

set RESX=%1
if "%RESX%"=="" set RESX=1280
set RESY=%2
if "%RESY%"=="" set RESY=720

%UE% %PROJ% %MAP% -game -dc_cluster -dc_cfg=%CFG% -dc_node=%NODE% ^
    -windowed -resx=%RESX% -resy=%RESY% ^
    -log -NoSplash ^
    -AbsLog=D:\Claude\UE5\PolyArcStereoND\Saved\Logs\cluster_launch.log
endlocal
