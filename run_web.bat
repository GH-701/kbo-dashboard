@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo ===================================================
echo     KBO 한국 프로야구 웹 대시보드 실행 중...
echo ===================================================
streamlit run kbo_web.py
pause
