@echo off
REM LegalBot+ Setup Script for Windows
REM Automates the installation and setup process

echo ======================================================================
echo                     LegalBot+ Setup Script
echo ======================================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found! Please install Python 3.10 or higher
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo √ Dependencies installed successfully

REM Build FAISS index
echo.
echo ======================================================================
echo Building FAISS index from legal documents...
echo ======================================================================
echo.

python core\build_faiss_index.py

if %errorlevel% neq 0 (
    echo X Failed to build FAISS index
    pause
    exit /b 1
)

echo.
echo √ FAISS index built successfully

REM Final instructions
echo.
echo ======================================================================
echo √ Setup Complete!
echo ======================================================================
echo.
echo Next steps:
echo.
echo 1. Get a Telegram Bot Token from @BotFather:
echo    - Open Telegram and message @BotFather
echo    - Send /newbot and follow instructions
echo    - Copy your bot token
echo.
echo 2. Set the token as environment variable:
echo    set TELEGRAM_BOT_TOKEN=your_token_here
echo.
echo 3. Run the bot:
echo    venv\Scripts\activate.bat
echo    python bot\main.py
echo.
echo Or run in demo mode (no Telegram token needed):
echo    python bot\main.py
echo.
echo ======================================================================
echo Documentation:
echo   - README.md - Full documentation
echo   - EXAMPLES.md - Example conversations
echo   - test_system.py - System verification
echo ======================================================================
echo.

pause

