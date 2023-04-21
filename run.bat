@echo off

setlocal

set "PYTHON_INSTALL_URL=https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe"
set "PYTHON_INSTALL_EXE=python-3.10.9-amd64.exe"
set "PYTHON_INSTALL_OPTIONS=/quiet PrependPath=1"
set "REQUIRED_MODULE=pytest-playwright"

echo Checking for installed version of Python...

for /f "delims=" %%i in ('py --version') do set "PYTHON=%%i" 
if defined PYTHON (  
    goto :found_python 
)
    echo Python is not installed. Installing the recommended version...
    curl -L -o %PYTHON_INSTALL_EXE% %PYTHON_INSTALL_URL%
    %PYTHON_INSTALL_EXE% %PYTHON_INSTALL_OPTIONS%
    del %PYTHON_INSTALL_EXE%
    echo Python has been installed and added to the system PATH. Please re-open ""run.bat"" to register Python.
    pause
    exit
    :found_python
    


echo Checking if %REQUIRED_MODULE% is installed...

for /f "delims=" %%i in ('%REQUIRED_MODULE:~7% --version ^| findstr /r /c:"^Version"') do set "INSTALLED_VERSION=%%i"
if defined INSTALLED_VERSION (
    echo %REQUIRED_MODULE% version %INSTALLED_VERSION:~8% is already installed.
) else (
    echo %REQUIRED_MODULE% is not installed. Installing...
    pip install %REQUIRED_MODULE%
)
echo playwright install 1>nul 2>nul

echo Installation of %REQUIRED_MODULE% is complete.

echo All required modules are installed.

echo.

py loophole.py

echo.
pause

endlocal