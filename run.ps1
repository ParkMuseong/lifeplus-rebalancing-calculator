# PowerShell 런처 (run.bat가 안 될 때 대안)
# 사용법: 파일 우클릭 → "PowerShell로 실행" 또는 PowerShell에서 .\run.ps1

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " 포트폴리오 리밸런싱 도구 - 실행 준비" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 1) Python 찾기
$pyCmd = $null
foreach ($candidate in @("python", "py")) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd) {
        try {
            $ver = & $candidate --version 2>&1
            if ($ver -match "Python 3") {
                $pyCmd = $candidate
                Write-Host "[1/4] Python 확인: $candidate ($ver)" -ForegroundColor Green
                break
            }
        } catch {}
    }
}

if (-not $pyCmd) {
    Write-Host "[ERROR] Python 3.10+ 가 필요합니다. https://www.python.org/downloads/" -ForegroundColor Red
    Read-Host "Enter 키를 누르면 종료"
    exit 1
}

# 2) venv 생성
$venvPy = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) {
    Write-Host "`n[2/4] 가상환경 생성 중..." -ForegroundColor Yellow
    & $pyCmd -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] venv 생성 실패" -ForegroundColor Red
        Read-Host "Enter 키를 누르면 종료"
        exit 1
    }
} else {
    Write-Host "`n[2/4] 가상환경 이미 존재" -ForegroundColor Green
}

# 3) 패키지 설치 확인
Write-Host "`n[3/4] 패키지 확인 중..." -ForegroundColor Yellow
$check = & $venvPy -c "import streamlit, pandas, plotly, FinanceDataReader, yfinance" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "     패키지 미설치 - 설치 시작 (수 분 소요)" -ForegroundColor Yellow
    & $venvPy -m pip install --upgrade pip
    & $venvPy -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] 패키지 설치 실패" -ForegroundColor Red
        Read-Host "Enter 키를 누르면 종료"
        exit 1
    }
} else {
    Write-Host "     모두 설치됨" -ForegroundColor Green
}

# 4) 실행
Write-Host "`n[4/4] Streamlit 실행 (브라우저 자동 열림, 종료는 Ctrl+C)" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

& $venvPy -m streamlit run app.py

Write-Host "`n=== 앱이 종료되었습니다 ===" -ForegroundColor Cyan
Read-Host "Enter 키를 누르면 창 닫기"
