@echo off
REM Launch PolyArcStereoND in nDisplay cluster runtime mode.
REM
REM CRITICAL: must use UnrealEditor-Cmd.exe (NOT UnrealEditor.exe) with -game
REM so that UDisplayClusterGameEngine::Init fires and the -dc_cluster flag
REM gets parsed. UnrealEditor.exe ignores -dc_cluster silently.
REM
REM CRITICAL: -dc_cfg= must be a path to the .ndisplay JSON file (NOT a
REM /Game/.../AssetName UE asset path). nDisplay's config validator
REM only accepts files with .ndisplay or .cfg extension.
REM
REM CRITICAL: the .ndisplay file's "AssetPath" field must point to the
REM DCRA blueprint asset, e.g. "/Game/nDisplay/BP_PolyArcStereo.BP_PolyArcStereo"
REM Without it the engine creates an empty default DCRA and you see
REM the level's PlayerStart view instead of the sweet-spot cluster view.

setlocal
set UE_CMD="D:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
set PROJ="D:\Claude\UE5\PolyArcStereoND\PolyArcStereoND.uproject"
set MAP=/Game/NewMap
set CFG="D:\Claude\UE5\PolyArcStereoND\Config\PolyArcStereo.ndisplay"
set NODE=node_main

set RESX=%1
if "%RESX%"=="" set RESX=1280
set RESY=%2
if "%RESY%"=="" set RESY=720

%UE_CMD% %PROJ% %MAP% -game -dc_cluster -dc_cfg=%CFG% -dc_node=%NODE% ^
    -windowed -resx=%RESX% -resy=%RESY% ^
    -log -NoSplash ^
    -AbsLog=D:\Claude\UE5\PolyArcStereoND\Saved\Logs\cluster_launch.log
endlocal
