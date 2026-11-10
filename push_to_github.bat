@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ================================================================
echo       KBO 한국프로야구 대시보드 - GitHub 원클릭 업로드 도구
echo ================================================================
echo.

git status > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git이 초기화되어 있지 않습니다.
    pause
    exit /b
)

echo [1/3] 변경 사항 스테이징 및 커밋...
git add .
git commit -m "update: KBO 대시보드 및 자동화 설정 최신화" > nul 2>&1

echo.
git remote get-url origin > nul 2>&1
if %errorlevel% neq 0 (
    echo [2/3] GitHub 리포지토리 URL이 등록되어 있지 않습니다.
    echo.
    echo GitHub에서 생성한 저장소 URL을 입력해주세요.
    echo (예: https://github.com/내아이디/kbo-dashboard.git)
    echo.
    set /p REPO_URL="저장소 URL 입력: "
    if "%REPO_URL%"=="" (
        echo URL이 입력되지 않아 종료합니다.
        pause
        exit /b
    )
    git remote add origin %REPO_URL%
    echo 원격 저장소가 등록되었습니다: %REPO_URL%
) else (
    echo [2/3] 원격 저장소 확인 완료.
)

echo.
echo [3/3] GitHub로 푸시 중 (main 브랜치)...
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo   [성공] GitHub에 코드가 성공적으로 업로드되었습니다!
    echo   이제 Streamlit Cloud 또는 GitHub Actions에서 계속 실행할 수 있습니다.
    echo ================================================================
) else (
    echo.
    echo [주의] 푸시 중 문제가 발생했습니다. GitHub 로그인 상태나 권한을 확인해주세요.
)

echo.
pause
