@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul
cd /d "%~dp0"

echo ========================================
echo  포트폴리오 리밸런싱 도구 - 실행 준비
echo ========================================
echo.

REM ---- 1) Python 실행기 찾기 (python / py) ----
set "PYEXE="
where python >nul 2>nul
if not errorlevel 1 (
    set "PYEXE=python"
) else (
    where py >nul 2>nul
    if not errorlevel 1 set "PYEXE=py -3"
)

if "!PYEXE!"=="" (
    echo [ERROR] Python을 찾을 수 없습니다.
    echo  - https://www.python.org/downloads/ 에서 Python 3.10 이상 설치
    echo  - 설치 시 "Add python.exe to PATH" 옵션 반드시 체크
    echo.
    pause
    exit /b 1
)

echo [1/4] Python 확인됨: !PYEXE!
!PYEXE! --version
echo.

REM ---- 2) 가상환경 생성 ----
if not exist ".venv\Scripts\python.exe" (
    echo [2/4] 가상환경 생성 중... (.venv)
    !PYEXE! -m venv .venv
    if errorlevel 1 (
        echo [ERROR] 가상환경 생성 실패
        pause
        exit /b 1
    )
) else (
    echo [2/4] 가상환경 이미 존재
)
echo.

REM ---- 3) 패키지 설치 확인 ----
set "VENV_PY=.venv\Scripts\python.exe"
echo [3/4] 패키지 확인 중...
"%VENV_PY%" -c "import streamlit, pandas, plotly, FinanceDataReader, yfinance" 2>nul
if errorlevel 1 (
    echo     패키지 미설치 - 설치 시작 (최초 1회, 수 분 소요)
    "%VENV_PY%" -m pip install --upgrade pip
    "%VENV_PY%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] 패키지 설치 실패. 위 로그를 확인하세요.
        pause
        exit /b 1
    )
) else (
    echo     패키지 모두 설치됨
)
echo.

REM ---- 4) Streamlit 실행 ----
echo [4/4] Streamlit 앱 실행
echo  - 브라우저가 자동으로 열립니다
echo  - 종료하려면 이 창에서 Ctrl+C
echo ========================================
echo.

"%VENV_PY%" -m streamlit run app.py

echo.
echo === 앱이 종료되었습니다 ===
pause
