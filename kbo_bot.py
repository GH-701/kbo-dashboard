"""
kbo_bot.py - KBO 한국프로야구 텔레그램 봇
실시간 순위, 경기 일정 및 스코어 알림, 최애 팀 전적, 야구 뉴스 제공
"""

import asyncio
import os
import json
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import kbo_teams
from kbo_teams import KBO_TEAMS, resolve_team_key, get_team_info
import kbo_data

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
SUBSCRIBERS_FILE = "subscribers.json"
FAVORITE_TEAMS_FILE = "favorite_teams.json"

# 최애 팀 설정 저장 및 로드
def load_favorite_teams():
    if os.path.exists(FAVORITE_TEAMS_FILE):
        try:
            with open(FAVORITE_TEAMS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_favorite_teams(favs):
    try:
        with open(FAVORITE_TEAMS_FILE, "w", encoding="utf-8") as f:
            json.dump(favs, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to save favorite teams: {e}")

# 구독자 저장 및 로드
def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        try:
            with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_subscribers(subs):
    try:
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(subs), f)
    except Exception as e:
        print(f"[ERROR] Failed to save subscribers: {e}")

# /start 명령어
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
⚾ <b>KBO 한국프로야구 알림 봇에 오신 것을 환영합니다!</b> ⚾

KBO 리그의 실시간 순위, 경기 일정 및 스코어, 최신 뉴스, 최애 구단 전적을 한눈에 확인할 수 있습니다.

📌 <b>사용 가능한 명령어:</b>
• <code>/team &lt;팀명&gt;</code> - 나의 최애 구단 등록 (예: <code>/team KIA</code>, <code>/team 삼성</code>, <code>/team LG</code>)
• <code>/my</code> - 등록한 최애 구단의 전적 및 정보 확인
• <code>/games</code> (또는 <code>/today</code>) - 오늘/최근 경기 스코어보드 확인
• <code>/rank</code> (또는 <code>/standings</code>) - KBO 정규리그 실시간 순위표
• <code>/news</code> - KBO 최신 야구 뉴스 TOP 5
• <code>/stat</code> - KBO 타자/투수 역대 최고 기록 TOP 5
• <code>/subscribe</code> - 경기 소식 및 알림 구독
• <code>/unsubscribe</code> - 알림 구독 취소
• <code>/help</code> - 도움말 보기

지금 바로 <code>/team &lt;구단명&gt;</code>으로 최애 팀을 설정해보세요! 🚀
"""
    await update.message.reply_text(welcome_text, parse_mode="HTML")

# /team 명령어: 최애 팀 등록
async def team_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if not context.args:
        teams_str = ", ".join([KBO_TEAMS[k]['name_full'] for k in KBO_TEAMS.keys()])
        await update.message.reply_text(
            f"⚠️ 팀명을 입력해주세요!\n예: <code>/team KIA</code>, <code>/team 삼성</code>, <code>/team LG</code>\n\n📌 지원 구단:\n{teams_str}",
            parse_mode="HTML"
        )
        return

    team_input = " ".join(context.args)
    team_key = resolve_team_key(team_input)
    if not team_key:
        await update.message.reply_text(f"❌ '{team_input}'은(는) 올바른 KBO 구단명이 아닙니다. 다시 확인해주세요.")
        return

    favs = load_favorite_teams()
    favs[user_id] = team_key
    save_favorite_teams(favs)

    info = KBO_TEAMS[team_key]
    await update.message.reply_text(
        f"👑 최애 팀이 <b>{info['name_full']}</b>(으)로 등록되었습니다!\n이제 <code>/my</code> 명령어로 최근 전적을 간편하게 확인해보세요.",
        parse_mode="HTML"
    )

# /my 명령어: 최애 팀 정보 및 전적
async def my_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    favs = load_favorite_teams()
    team_key = favs.get(user_id, "KIA")
    info = KBO_TEAMS[team_key]

    recent = kbo_data.fetch_recent_games(team_key)
    wins = sum(1 for g in recent if g['결과'] == "승리")
    losses = sum(1 for g in recent if g['결과'] == "패배")
    draws = sum(1 for g in recent if g['결과'] == "무승부")

    msg = f"👑 <b>나의 최애 팀: {info['name_full']}</b>\n"
    msg += f"🏟️ 홈 구장: {info['stadium_name']}\n"
    msg += f"📈 최근 5경기 전적: <b>{wins}승 {losses}패{f' {draws}무' if draws else ''}</b>\n\n"
    msg += "📋 <b>최근 경기 목록:</b>\n"
    for g in recent:
        result_icon = "🟢" if g['결과'] == "승리" else ("🔴" if g['결과'] == "패배" else "⚪")
        msg += f"{result_icon} {g['날짜']} vs {g['상대팀']} ({g['결과']} {g['스코어']}) - {g['구장']}\n"

    await update.message.reply_text(msg, parse_mode="HTML")

# /games 명령어: 오늘/최근 경기 스코어카드
async def games_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    games = kbo_data.fetch_games_by_date(today_str)

    msg = f"⚾ <b>KBO 경기 스코어보드</b> ({today_str})\n"
    msg += "<i>(비시즌 기간에는 주요 포스트시즌/한국시리즈 명승부를 안내합니다.)</i>\n\n"

    for g in games:
        msg += f"🏟️ <b>{g['구장']}</b> [{g['상태']}]\n"
        msg += f"  ▶ <b>{g['홈팀']}</b> {g['스코어']} <b>{g['원정팀']}</b>\n"
        if g.get('하이라이트'):
            msg += f"  💬 {g['하이라이트']}\n"
        msg += "\n"

    await update.message.reply_text(msg, parse_mode="HTML")

# /rank 명령어: KBO 리그 실시간 순위표
async def rank_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    standings = kbo_data.fetch_kbo_standings()

    msg = "🏆 <b>KBO 정규리그 순위표</b>\n"
    msg += "<code>순위  팀명    경기  승  무  패  승률   게임차</code>\n"
    msg += "----------------------------------------\n"

    for s in standings:
        team_display = f"{s['팀명']:<4}"
        msg += f"<code>{s['순위']:>2}위  {team_display}  {s['경기']:>3}  {s['승']:>2}  {s['무']:>1}  {s['패']:>2}  {s['승률']:<5}  {s['게임차']:>4}</code>\n"

    await update.message.reply_text(msg, parse_mode="HTML")

# /news 명령어: 최신 KBO 야구 뉴스
async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_items = kbo_data.fetch_kbo_news("KBO 프로야구")

    msg = "📰 <b>KBO 실시간 주요 뉴스 TOP 5</b>\n\n"
    for i, it in enumerate(news_items[:5], start=1):
        msg += f"<b>{i}. <a href='{it['link']}'>{it['title']}</a></b>\n"
        msg += f"   <i>{it['press']} | {it['time']}</i>\n\n"

    await update.message.reply_text(msg, parse_mode="HTML", disable_web_page_preview=True)

# /stat 명령어: KBO 역대 최고 기록
async def stat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    batters = kbo_data.fetch_top_batters()[:5]
    pitchers = kbo_data.fetch_top_pitchers()[:5]

    msg = "📊 <b>KBO 리그 역대 레전드 기록 TOP 5</b>\n\n"
    msg += "🏏 <b>[타자] 역대 최고 타율 TOP 5:</b>\n"
    for b in batters:
        msg += f"• {b['순위']}위: <b>{b['선수명']}</b> ({b['팀명']}, {b['연도']}) - <code>{b['기록']}</code>\n"

    msg += "\n⚾ <b>[투수] 단일시즌 최다승 TOP 5:</b>\n"
    for p in pitchers:
        msg += f"• {p['순위']}위: <b>{p['선수명']}</b> ({p['팀명']}, {p['연도']}) - <code>{p['기록']}승</code>\n"

    await update.message.reply_text(msg, parse_mode="HTML")

# /subscribe 및 /unsubscribe
async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subs = load_subscribers()
    subs.add(chat_id)
    save_subscribers(subs)
    await update.message.reply_text("✅ KBO 야구 경기 소식 및 알림을 구독하였습니다!")

async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subs = load_subscribers()
    if chat_id in subs:
        subs.remove(chat_id)
        save_subscribers(subs)
    await update.message.reply_text("❎ 알림 구독이 해제되었습니다.")

# 알림 브로드캐스트 함수 (GitHub Actions 워크플로우나 주기적 스케줄에서 사용 가능)
async def broadcast_daily_briefing(bot):
    subs = load_subscribers()
    if not subs:
        return

    today_str = datetime.date.today().strftime("%Y-%m-%d")
    standings = kbo_data.fetch_kbo_standings()
    news = kbo_data.fetch_kbo_news()

    briefing = f"⚾ <b>[{today_str}] 오늘의 KBO 브리핑</b> ⚾\n\n"
    briefing += f"🥇 <b>현재 리그 1위:</b> {standings[0]['팀명']} ({standings[0]['승']}승 {standings[0]['패']}패, 승률 {standings[0]['승률']})\n\n"
    briefing += "📰 <b>오늘의 주요 헤드라인:</b>\n"
    for it in news[:3]:
        briefing += f"• <a href='{it['link']}'>{it['title']}</a>\n"

    for chat_id in subs:
        try:
            await bot.send_message(chat_id=chat_id, text=briefing, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            print(f"[ERROR] Failed to send to {chat_id}: {e}")

def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
        print("[INFO] Telegram Bot Token이 설정되지 않았습니다.")
        print("[INFO] 환경변수 TELEGRAM_BOT_TOKEN을 설정하거나 파일 상단 BOT_TOKEN에 입력해주세요.")
        print("[INFO] (웹 대시보드는 텔레그램 봇 토큰 없이도 완벽히 작동합니다: python -m streamlit run kbo_web.py)")
        return

    print("[INFO] KBO 텔레그램 봇 시작 중...")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", start_command))
    app.add_handler(CommandHandler("team", team_command))
    app.add_handler(CommandHandler("my", my_command))
    app.add_handler(CommandHandler("games", games_command))
    app.add_handler(CommandHandler("today", games_command))
    app.add_handler(CommandHandler("rank", rank_command))
    app.add_handler(CommandHandler("standings", rank_command))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("stat", stat_command))
    app.add_handler(CommandHandler("subscribe", subscribe_command))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe_command))

    print("[SUCCESS] KBO 봇이 성공적으로 실행되었습니다! (Polling 대기 중)")
    app.run_polling()

if __name__ == "__main__":
    main()
