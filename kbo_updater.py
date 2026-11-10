"""
kbo_updater.py - KBO 최신 데이터를 매일 자동으로 수집하여 data/ 디렉토리에 저장하는 스크립트
GitHub Actions에서 주기적으로 실행되어 저장소 데이터를 항상 최신 상태로 유지합니다.
"""

import os
import json
import datetime
import kbo_data
import kbo_teams

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def update_all_data():
    ensure_data_dir()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = datetime.date.today().strftime("%Y-%m-%d")

    print(f"[{now_str}] Starting KBO automated data update...")

    # 1. KBO 순위표 업데이트
    print("[1/4] Fetching KBO Standings...")
    standings = kbo_data.fetch_kbo_standings()
    standings_path = os.path.join(DATA_DIR, "standings.json")
    with open(standings_path, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": now_str,
            "data": standings
        }, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved {len(standings)} teams to {standings_path}")

    # 2. 실시간 KBO 뉴스 업데이트
    print("[2/4] Fetching KBO News...")
    news = kbo_data.fetch_kbo_news("KBO 프로야구")
    news_path = os.path.join(DATA_DIR, "news.json")
    with open(news_path, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": now_str,
            "data": news
        }, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved {len(news)} articles to {news_path}")

    # 3. KBO 역대 최고 기록 (타자/투수)
    print("[3/4] Fetching Top Records...")
    batters = kbo_data.fetch_top_batters()
    pitchers = kbo_data.fetch_top_pitchers()
    records_path = os.path.join(DATA_DIR, "records.json")
    with open(records_path, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": now_str,
            "batters": batters,
            "pitchers": pitchers
        }, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved top records to {records_path}")

    # 4. 경기 스코어보드 & 최근 전적
    print("[4/4] Fetching Games & Scores...")
    today_games = kbo_data.fetch_games_by_date(today_str)
    team_games = {}
    for team_key in kbo_teams.KBO_TEAMS.keys():
        team_games[team_key] = kbo_data.fetch_recent_games(team_key)

    games_path = os.path.join(DATA_DIR, "games.json")
    with open(games_path, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": now_str,
            "today_games": today_games,
            "team_games": team_games
        }, f, ensure_ascii=False, indent=2)
    print(f"  -> Saved games data to {games_path}")

    # 메타 정보 기록
    meta_path = os.path.join(DATA_DIR, "meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": now_str,
            "status": "success",
            "teams_count": len(standings),
            "news_count": len(news)
        }, f, ensure_ascii=False, indent=2)

    print(f"[{now_str}] All KBO data successfully updated!")

if __name__ == "__main__":
    update_all_data()

