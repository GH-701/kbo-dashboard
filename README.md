# ⚾ KBO 한국 프로야구 실시간 대시보드 & 텔레그램 알림 봇

> **한국 프로야구(KBO) 10개 구단의 실시간 순위, 경기 결과/스코어보드, 선수 상세 기록, 전국 야구장 지도 및 시설 안내, 최신 뉴스를 제공하는 올인원(All-in-One) 야구 데이터 플랫폼입니다.**  
> Streamlit 기반의 인터랙티브 웹 대시보드와 Telegram 알림 봇, 그리고 GitHub Actions 자동화 워크플로우를 완벽 지원합니다.

---

## 🌟 주요 기능

### 1. 🖥️ KBO 웹 대시보드 (`kbo_web.py`)
* **⚙️ 팀 설정 & 전적**: 나의 최애 구단을 등록하고 최근 5경기 전적(승/무/패 뱃지 및 스코어), 홈구장 정보 확인
* **🔥 경기 결과 & 일정**: 날짜별 경기 스코어카드, 홈/원정 대진, 주요 경기 하이라이트 제공 (비시즌 기간에는 주요 명승부 제공)
* **🏃‍♂️ 선수 상세 기록 & 라인업**:
  * 10개 구단 전체 대표 타자/투수 상세 스탯 및 라인업 조회 (타율, 홈런, 타점, OPS / 평균자책점, 승, 세이브, 탈삼진, WHIP)
  * **2인 선수 스탯 비교 시뮬레이터 (Plotly Radar 방사형 차트 시각화)**
  * KBO 역대 최고 타율 TOP 10, 단일 시즌 최다승 투수 TOP 10
* **🏟️ 구장 및 구단 안내**: KBO 10개 구단 9개 홈구장 정보(펜스 거리, 수용인원, 좌석 규격), 공식 유튜브/굿즈샵 링크, Folium 인터랙티브 전국 야구장 지도, Plotly 2D 그라운드/펜스 규격도
* **🏆 리그 순위표**: 실시간 KBO 정규리그 순위표(경기, 승, 무, 패, 승률, 게임차, 최근10경기, 연속 승패, 홈/방문 성적) 및 승률 비교 차트
* **📰 주요 야구 뉴스**: 실시간 KBO 뉴스 크롤링 및 구단별 맞춤형 필터링 지원

### 2. 🤖 텔레그램 알림 봇 (`kbo_bot.py` / `한국프로야구.py`)
* `/start` : 봇 환영 메시지 및 사용법 안내
* `/team <구단명>` : 나의 최애 구단 등록 (예: `/team KIA`, `/team 삼성`, `/team LG`)
* `/my` : 등록한 최애 팀의 최근 전적 및 홈구장 확인
* `/games` 또는 `/today` : 오늘/최근 경기 스코어카드 브리핑
* `/rank` 또는 `/standings` : KBO 정규리그 실시간 순위표 출력
* `/news` : 실시간 KBO 주요 야구 뉴스 TOP 5 링크 전송
* `/stat` : KBO 리그 역대 레전드 기록 TOP 5
* `/subscribe` / `/unsubscribe` : 일일 야구 브리핑 알림 구독/해제

---

## 📁 프로젝트 구조

```text
├── kbo_web.py                  # Streamlit 웹 대시보드 메인 프로그램
├── kbo_bot.py                  # KBO 텔레그램 알림 봇 메인 프로그램
├── 한국프로야구.py              # 텔레그램 봇 실행 진입점 (한글 파일명 호환)
├── kbo_data.py                 # KBO 순위, 뉴스, 일정, 선수 기록 크롤링 모듈
├── kbo_teams.py                # 10개 구단 정보, 로고, 대표 컬러, 별칭 매핑
├── kbo_stadiums.py             # 9개 홈구장 규격, Folium 지도, Plotly 평면도
├── send_daily_briefing.py      # GitHub Actions 자동 발송용 스크립트
├── run_kbo_web.bat             # 웹 대시보드 윈도우 원클릭 실행 배치 파일
├── run_kbo_bot.bat             # 텔레그램 봇 윈도우 원클릭 실행 배치 파일
├── requirements.txt            # 필수 파이썬 패키지 목록
├── .gitignore                  # Git 추적 제외 설정
└── .github/
    └── workflows/
        └── kbo_daily_notification.yml  # GitHub Actions 무중단 일일 알림 워크플로우
```

---

## 🚀 로컬 실행 방법

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 웹 대시보드 실행
윈도우 탐색기에서 **`run_kbo_web.bat`** 파일을 더블클릭하거나 터미널에서 다음 명령어를 실행합니다:
```bash
streamlit run kbo_web.py
```
> 브라우저가 자동으로 열리며 `http://localhost:8501`에서 대시보드가 실행됩니다.

### 3. 텔레그램 봇 실행 (선택 사항)
텔레그램 BotFather에게 발급받은 봇 토큰이 있는 경우:
```bash
set TELEGRAM_BOT_TOKEN="내_봇_토큰"
python kbo_bot.py
```
*(또는 `kbo_bot.py` 파일 상단의 `BOT_TOKEN` 변수에 직접 입력 후 `run_kbo_bot.bat` 실행)*

---

## 🌐 깃허브(GitHub)에 넣어 24시간 계속 작동시키는 방법

컴퓨터가 꺼져 있어도 프로그램이 중단 없이 계속 실행되도록 2가지 방법을 모두 제공합니다.

### 방법 1: Streamlit Community Cloud (웹 대시보드 24/7 무료 호스팅)
GitHub에 올리면 무료로 언제 어디서나 웹 대시보드에 접속할 수 있습니다:

1. 본인의 **GitHub에 새 저장소(Repository)** 생성 (예: `kbo-dashboard`)
2. 아래 **Git 업로드 가이드**를 따라 코드를 Push
3. **[streamlit.io/cloud](https://streamlit.io/cloud)** 접속 후 GitHub 계정으로 로그인
4. **[Create app]** 클릭 -> 내 GitHub 저장소(`kbo-dashboard`) 선택
5. Main file path에 **`kbo_web.py`** 입력 후 **[Deploy]** 클릭!
6. 잠시 후 전 세계 어디서든 모바일/PC로 접속 가능한 나만의 고유 웹 주소(`https://<내앱이름>.streamlit.app`)가 생성되어 **365일 24시간 계속 작동**합니다!

---

### 방법 2: GitHub Actions (컴퓨터가 꺼져 있어도 자동 실행되는 알림)
저장소에 포함된 `.github/workflows/kbo_daily_notification.yml`에 의해 동작합니다:

1. GitHub 저장소의 **Settings** -> **Secrets and variables** -> **Actions** 메뉴로 이동
2. **[New repository secret]** 클릭하여 다음 시크릿 등록:
   * `TELEGRAM_BOT_TOKEN` : BotFather에게 발급받은 봇 토큰
   * `TELEGRAM_CHAT_ID` : 알림을 받을 본인의 텔레그램 Chat ID (User ID)
3. 이제 GitHub 서버가 **매일 오전 9시, 오후 9시**에 자동으로 Python 스크립트를 실행하여 최신 KBO 순위와 뉴스를 텔레그램으로 자동 전송합니다!
4. GitHub 저장소의 **Actions** 탭에서 언제든 **[Run workflow]**를 눌러 수동으로 즉시 실행할 수도 있습니다.

---

## 📤 GitHub에 코드 올리기 (Git 명령어 가이드)

터미널(PowerShell 또는 CMD)에서 다음 명령어를 순서대로 실행하세요:

```bash
# 1. git 초기화
git init

# 2. 파일 추가 및 첫 커밋
git add .
git commit -m "feat: KBO 한국프로야구 대시보드 및 텔레그램 봇 완성"

# 3. 브랜치명을 main으로 설정
git branch -M main

# 4. 내 GitHub 저장소 원격 주소 연결 (본인의 GitHub 리포지토리 URL로 변경)
git remote add origin https://github.com/사용자아이디/저장소이름.git

# 5. GitHub에 업로드
git push -u origin main
```

