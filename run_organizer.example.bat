@echo off
REM ========================================================================
REM Batch file to run the download organizer with Task Scheduler
REM ========================================================================
REM
REM SETUP INSTRUCTIONS:
REM 1. Copy this file to "run_organizer.bat"
REM 2. If Python is in your PATH, you can use this file as-is
REM 3. If Python is NOT in your PATH, uncomment Option B below and update
REM    the path to your Python installation
REM
REM ========================================================================

REM Change directory to where this batch file is located
cd /d "%~dp0"

REM ========================================================================
REM OPTION A: Use Python from PATH (default)
REM ========================================================================
REM This works if Python is in your system PATH
python organizer.py

REM ========================================================================
REM OPTION B: Use specific Python installation
REM ========================================================================
REM If Option A doesn't work, comment out the line above and uncomment
REM and customize the line below with your Python path:
REM
REM "C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\python.exe" organizer.py
REM
REM To find your Python path, run this in PowerShell:
REM   where.exe python
REM ========================================================================

REM Optional: Uncomment the line below to see output before closing
REM pause
