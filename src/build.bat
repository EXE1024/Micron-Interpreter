@echo off
title build.bat
echo ===================================================
echo   Building Micron 2.0 into .exe file
echo ===================================================

pip install pyinstaller --quiet
pyinstaller --onefile --distpath . micron2.0.py
rmdir /s /q build
del /q micron2.0.spec

pause
