"""
send_daily_briefing.py - GitHub Actions 등 주기적 자동화 배치용 단발성 실행 스크립트
KBO 실시간 순위, 주요 뉴스, 경기 일정을 요약하여 구독자들에게 텔레그램으로 전송
"""

import os
import asyncio
import datetime
from telegram import Bot
import kbo_data
import kbo_teams
from kbo_teams import KBO_TEAMS

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") # 특정 관리자/채널 ID

async def main():
    if not BOT_TOKEN:
        print("[SKIP] TELEGRAM_BOT_TOKEN is not set.")
        return

    bot = Bot(token=BOT_TOKEN)
    today_str = datetime.date.today().strftime("%Y-%m-%d")

    print(f"[INFO] Fetching KBO data for {today_str}...")
    standings = kbo_data.fetch_kbo_standings()
    news = kbo_data.fetch_kbo_news()

    # 메시지 작성
    msg = f"⚾ <b>[KBO 일일 브리핑] {today_str}</b> ⚾\n\n"
    
    if standings:
        msg += "🏆 <b>현재 KBO 정규리그 TOP 5:</b>\n"
        for s in standings[:5]:
            msg += f"• <b>{s['순위']}위: {s['팀명']}</b> ({s['승']}승 {s['무']}무 {s['패']}패, 승률 {s['승률']})\n"
        msg += "\n"

    if news:
        msg += "📰 <b>오늘의 주요 야구 뉴스:</b>\n"
        for it in news[:3]:
            msg += f"• <a href='{it['link']}'>{it['title']}</a> (<i>{it['press']}</i>)\n"
        msg += "\n"

    msg += "👉 자세한 전적 및 구장 정보는 웹 대시보드에서 확인하세요!"

    # 대상 chat_id로 전송
    targets = []
    if TARGET_CHAT_ID:
        targets.append(TARGET_CHAT_ID)

    # subscribers.json 파일이 존재할 경우 포함
    if os.path.exists("subscribers.json"):
        import json
        try:
            with open("subscribers.json", "r") as f:
                subs = json.load(f)
                targets.extend(subs)
        except Exception:
            pass

    targets = list(set(targets))
    if not targets:
        print("[INFO] No target chat IDs found to broadcast.")
        return

    print(f"[INFO] Sending briefing to {len(targets)} subscribers...")
    for chat_id in targets:
        try:
            await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML", disable_web_page_preview=True)
            print(f"[SUCCESS] Sent to {chat_id}")
        except Exception as e:
            print(f"[ERROR] Failed to send to {chat_id}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
