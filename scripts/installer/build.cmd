@echo off
setlocal

set "SCRIPT_DIRECTORY=%~dp0"
set "PYTHON=%SCRIPT_DIRECTORY%..\..\.venv3\Scripts\python.exe"

if not exist "%PYTHON%" (
   echo Python virtual environment not found:
   echo "%PYTHON%"
   pause
   endlocal
   exit /b 1
)

pushd "%SCRIPT_DIRECTORY%"
if errorlevel 1 (
   echo Failed to change to the installer directory.
   pause
   endlocal
   exit /b 1
)

"%PYTHON%" -m PyInstaller --clean "installer.spec"
set "BUILD_EXIT_CODE=%ERRORLEVEL%"

popd

if "%BUILD_EXIT_CODE%" NEQ "0" (
   echo.
   echo Build failed with exit code %BUILD_EXIT_CODE%.
   pause
)

endlocal
exit /b %BUILD_EXIT_CODE%