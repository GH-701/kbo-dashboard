import streamlit as st
import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

import kbo_teams
from kbo_teams import KBO_TEAMS, resolve_team_key, get_team_info
import kbo_data
import kbo_stadiums

# 웹사이트 기본 설정
st.set_page_config(
    page_title="KBO 한국 프로야구 대시보드",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'my_team' not in st.session_state:
    st.session_state['my_team'] = "KIA"

if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

# 스타일 CSS
custom_css_light = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}
.main {
    background-color: #f8fafc;
}
.stMetric {
    background-color: white;
    padding: 14px 18px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    border: 1px solid #e2e8f0;
}
.game-card {
    background: white;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    transition: transform 0.2s, box-shadow 0.2s;
}
.game-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
}
.stadium-card {
    background: white;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
}
.badge-win {
    background-color: #10b981;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 9999px;
}
.badge-loss {
    background-color: #ef4444;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 9999px;
}
.badge-draw {
    background-color: #64748b;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 9999px;
}
</style>
"""

custom_css_dark = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}
.main {
    background-color: #0f172a;
    color: #f8fafc;
}
.stMetric {
    background-color: #1e293b;
    padding: 14px 18px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    border: 1px solid #334155;
    color: #f8fafc;
}
.game-card {
    background: #1e293b;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    border: 1px solid #334155;
    color: #f8fafc;
}
.stadium-card {
    background: #1e293b;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.2);
    border: 1px solid #334155;
    color: #f8fafc;
}
.badge-win {
    background-color: #059669;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 9999px;
}
.badge-loss {
    background-color: #dc2626;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 9999px;
}
.badge-draw {
    background-color: #475569;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 9999px;
}
</style>
"""

# 사이드바
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/ko/thumb/d/d1/KBO_League_logo.svg/300px-KBO_League_logo.svg.png", width=120)
    st.markdown("### ⚾ KBO 대시보드")
    
    # 최애 팀 빠른 선택
    team_list = list(KBO_TEAMS.keys())
    current_team_idx = team_list.index(st.session_state['my_team']) if st.session_state['my_team'] in team_list else 0
    selected_my_team = st.selectbox(
        "⭐ 나의 최애 구단 선택",
        options=team_list,
        index=current_team_idx,
        format_func=lambda x: f"{KBO_TEAMS[x]['name_full']}"
    )
    if selected_my_team != st.session_state['my_team']:
        st.session_state['my_team'] = selected_my_team

    st.markdown("---")
    st.markdown("### 🌓 화면 모드")
    dark_mode = st.toggle("다크 모드 활성화", value=st.session_state['dark_mode'])
    st.session_state['dark_mode'] = dark_mode

    st.markdown("---")
    st.markdown("### 🔗 구단별 공식 웹사이트")
    for t_key in team_list:
        t_data = KBO_TEAMS[t_key]
        st.markdown(f"[{t_data['name_full']}]({t_data['website']})")

# 테마 CSS 적용
if st.session_state['dark_mode']:
    st.markdown(custom_css_dark, unsafe_allow_html=True)
else:
    st.markdown(custom_css_light, unsafe_allow_html=True)

# 헤더 영역
fav_team = st.session_state['my_team']
fav_info = get_team_info(fav_team)

col_title, col_date = st.columns([2, 1])
with col_title:
    st.title("⚾ KBO 한국 프로야구 대시보드")
    st.caption(f"응원 구단: **{fav_info['name_full']}** | KBO 실시간 순위, 경기 일정 및 스코어, 선수 기록, 구장 정보")

with col_date:
    selected_date = st.date_input("📅 조회 날짜 선택", datetime.date.today())
    date_str = selected_date.strftime("%Y-%m-%d")

# 6개 메인 탭 생성
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "⚙️ 팀 설정 & 전적",
    "🔥 경기 결과 & 일정",
    "🏃‍♂️ 선수 상세 기록",
    "🏟️ 구장 및 구단 안내",
    "🏆 리그 순위표",
    "📰 주요 야구 뉴스"
])

# ==========================================
# [탭 1] 팀 설정 및 최근 전적
# ==========================================
with tab1:
    st.subheader(f"👑 {fav_info['name_full']} 팀 현황 및 최근 전적")
    
    col_fav1, col_fav2, col_fav3 = st.columns([1, 1, 1])
    with col_fav1:
        st.metric("홈 구장", fav_info['stadium_name'])
    with col_fav2:
        st.metric("공식 대표 컬러", fav_info['color_primary'])
    with col_fav3:
        st.metric("구단 웹사이트", "공식 홈페이지", fav_info['website'])

    st.markdown("---")
    st.markdown(f"### 📈 {fav_info['name_full']} 최근 경기 전적")

    recent_games = kbo_data.fetch_recent_games(fav_team)
    if recent_games:
        wins = sum(1 for g in recent_games if g['결과'] == "승리")
        losses = sum(1 for g in recent_games if g['결과'] == "패배")
        draws = sum(1 for g in recent_games if g['결과'] == "무승부")

        # 전적 원형 뱃지 바
        trend_html = "<div style='display:flex; gap:10px; align-items:center; margin-bottom:18px;'>"
        for g in recent_games:
            if g['결과'] == "승리":
                bg = "#10b981"
                txt = "승"
            elif g['결과'] == "패배":
                bg = "#ef4444"
                txt = "패"
            else:
                bg = "#64748b"
                txt = "무"
            trend_html += f"""
            <div style='background-color:{bg}; color:white; font-weight:800; font-size:0.9rem;
                        width:36px; height:36px; border-radius:50%; display:flex; align-items:center;
                        justify-content:center; box-shadow:0 2px 4px rgba(0,0,0,0.1);'>{txt}</div>
            """
        trend_html += f"<span style='margin-left:14px; font-weight:700; font-size:1.15rem;'>최근 5경기: {wins}승 {losses}패{f' {draws}무' if draws else ''}</span></div>"
        st.markdown(trend_html, unsafe_allow_html=True)

        # 경기 목록 테이블
        df_games = pd.DataFrame(recent_games)
        st.dataframe(df_games[['날짜', '상대팀', '결과', '스코어', '구장', '하이라이트']], use_container_width=True, hide_index=True)

# ==========================================
# [탭 2] 경기 결과 및 일정
# ==========================================
with tab2:
    st.subheader(f"🔥 {date_str} KBO 경기 스코어보드 & 일정")
    st.info("💡 비시즌 기간에는 최근 포스트시즌 / 한국시리즈 주요 명승부 스코어카드를 제공합니다.")

    day_games = kbo_data.fetch_games_by_date(date_str)
    
    col_g1, col_g2 = st.columns(2)
    for i, g in enumerate(day_games):
        target_col = col_g1 if i % 2 == 0 else col_g2
        with target_col:
            home_key = resolve_team_key(g["홈팀"]) or g["홈팀"]
            away_key = resolve_team_key(g["원정팀"]) or g["원정팀"]
            home_color = KBO_TEAMS.get(home_key, {}).get("color_primary", "#333333")
            away_color = KBO_TEAMS.get(away_key, {}).get("color_primary", "#333333")

            card_html = f"""
            <div class="game-card" style="border-left: 6px solid {home_color};">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span style="font-size:0.85rem; color:#64748b; font-weight:600;">🏟️ {g['구장']}</span>
                    <span class="badge-win">{g['상태']}</span>
                </div>
                <div style="display:flex; justify-content:space-around; align-items:center; padding:12px 0;">
                    <div style="text-align:center; flex:1;">
                        <h4 style="margin:0; font-size:1.25rem; font-weight:800; color:{home_color};">{g['홈팀']}</h4>
                        <span style="font-size:0.75rem; color:#888;">(홈)</span>
                    </div>
                    <div style="text-align:center; font-size:1.8rem; font-weight:900; letter-spacing:2px; padding:0 15px;">
                        {g['스코어']}
                    </div>
                    <div style="text-align:center; flex:1;">
                        <h4 style="margin:0; font-size:1.25rem; font-weight:800; color:{away_color};">{g['원정팀']}</h4>
                        <span style="font-size:0.75rem; color:#888;">(원정)</span>
                    </div>
                </div>
                <div style="margin-top:10px; font-size:0.85rem; color:#555; background:rgba(0,0,0,0.03); padding:8px 12px; border-radius:8px;">
                    ⚾ <b>경기 내용:</b> {g.get('하이라이트', '정규 경기')}
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

# ==========================================
# [탭 3] 선수 상세 기록
# ==========================================
with tab3:
    st.subheader("🏃‍♂️ KBO 선수 상세 순위 및 통계")
    
    stat_type = st.radio("포지션 부문 선택", ["타자 부문 TOP 10", "투수 부문 TOP 10"], horizontal=True)
    
    if stat_type == "타자 부문 TOP 10":
        batters_data = kbo_data.fetch_top_batters()
        st.markdown("#### 🏏 KBO 역대 최고 타율 TOP 10")
        df_batters = pd.DataFrame(batters_data)
        st.dataframe(df_batters, use_container_width=True, hide_index=True)
        
        # 상위 5명 바 차트 시각화
        df_top5 = df_batters.head(5).copy()
        df_top5['기록_num'] = pd.to_numeric(df_top5['기록'], errors='coerce')
        fig_bar = go.Figure(go.Bar(
            x=df_top5['선수명'] + " (" + df_top5['팀명'] + ")",
            y=df_top5['기록_num'],
            marker_color='#ea0029',
            text=df_top5['기록'],
            textposition='auto'
        ))
        fig_bar.update_layout(
            title="KBO 역대 타율 상위 5걸",
            yaxis_title="타율 (AVG)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#f8fafc" if st.session_state['dark_mode'] else "#1e293b"),
            height=320
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        pitchers_data = kbo_data.fetch_top_pitchers()
        st.markdown("#### ⚾ KBO 역대 최다승 투수 TOP 10")
        df_pitchers = pd.DataFrame(pitchers_data)
        st.dataframe(df_pitchers, use_container_width=True, hide_index=True)
        
        # 상위 5명 바 차트
        df_top5_p = df_pitchers.head(5).copy()
        df_top5_p['기록_num'] = pd.to_numeric(df_top5_p['기록'], errors='coerce')
        fig_bar_p = go.Figure(go.Bar(
            x=df_top5_p['선수명'] + " (" + df_top5_p['팀명'] + ")",
            y=df_top5_p['기록_num'],
            marker_color='#0066b3',
            text=df_top5_p['기록'] + "승",
            textposition='auto'
        ))
        fig_bar_p.update_layout(
            title="KBO 단일 시즌 최다승 투수 상위 5걸",
            yaxis_title="승리 수 (W)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#f8fafc" if st.session_state['dark_mode'] else "#1e293b"),
            height=320
        )
        st.plotly_chart(fig_bar_p, use_container_width=True)

# ==========================================
# [탭 4] 구장 및 구단 안내
# ==========================================
with tab4:
    st.subheader("🏟️ KBO 10개 구단 홈구장 및 시설 안내")

    col_select, col_stadium_info = st.columns([1, 2])
    with col_select:
        selected_stadium_team = st.selectbox(
            "조회할 구단을 선택하세요",
            options=list(KBO_TEAMS.keys()),
            format_func=lambda x: f"{KBO_TEAMS[x]['name_full']} ({KBO_TEAMS[x]['stadium_name']})"
        )

    stadium_cfg = kbo_stadiums.STADIUM_DETAILS[selected_stadium_team]
    team_cfg = KBO_TEAMS[selected_stadium_team]

    col_details, col_visual = st.columns([1, 1.2])
    with col_details:
        card_html = f"""
        <div class="stadium-card" style="border-left: 6px solid {team_cfg['color_primary']};">
            <h3 style="margin-top:0; color:{team_cfg['color_primary']};">{team_cfg['name_full']}</h3>
            <h4 style="margin:4px 0 16px 0;">🏟️ {stadium_cfg['stadium_name']}</h4>
            <p><b>개장 연도:</b> {stadium_cfg['opened_year']}년 | <b>수용 인원:</b> {stadium_cfg['capacity']}</p>
            <p><b>잔디 종류:</b> {stadium_cfg['turf']} | <b>펜스 높이:</b> {stadium_cfg['fence_height']}</p>
            <p><b>펜스 거리:</b> 좌/우 {stadium_cfg['left_m']}m, 중앙 {stadium_cfg['center_m']}m</p>
            <p><b>주소:</b> {stadium_cfg['address']}</p>
            <p style="font-size:0.9rem; color:#666; margin-top:12px;">{stadium_cfg['features']}</p>
            <div style="margin-top:18px;">
                <a href="{team_cfg['website']}" target="_blank" style="display:inline-block; padding:8px 16px; background:{team_cfg['color_primary']}; color:white; border-radius:8px; text-decoration:none; font-weight:700;">공식 웹사이트 바로가기 →</a>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        # Plotly 외야 및 그라운드 규격도
        fig_stadium = kbo_stadiums.create_stadium_field_chart(selected_stadium_team, st.session_state['dark_mode'])
        st.plotly_chart(fig_stadium, use_container_width=True)

    with col_visual:
        st.markdown("#### 🗺️ 전국 KBO 야구장 위치 지도")
        st_map = kbo_stadiums.create_kbo_stadium_map(selected_stadium_team)
        st_folium(st_map, width=700, height=580)

# ==========================================
# [탭 5] 리그 순위표
# ==========================================
with tab5:
    st.subheader("🏆 KBO 정규리그 실시간 순위표")

    with st.spinner("최신 리그 순위표를 조회하는 중..."):
        standings = kbo_data.fetch_kbo_standings()

    df_standings = pd.DataFrame(standings)
    cols_display = ["순위", "팀명", "경기", "승", "무", "패", "승률", "게임차", "최근10경기", "연속", "홈", "방문"]
    st.dataframe(df_standings[cols_display], use_container_width=True, hide_index=True)

    # 상위권 승률 바 차트 시각화
    fig_winrate = go.Figure(go.Bar(
        x=df_standings['팀명'],
        y=pd.to_numeric(df_standings['승률'], errors='coerce'),
        marker_color=[s.get('color', '#3b82f6') for s in standings],
        text=df_standings['승률'],
        textposition='auto'
    ))
    fig_winrate.update_layout(
        title="구단별 시즌 승률 비교",
        yaxis_title="승률",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#f8fafc" if st.session_state['dark_mode'] else "#1e293b"),
        height=350
    )
    st.plotly_chart(fig_winrate, use_container_width=True)

# ==========================================
# [탭 6] 주요 야구 뉴스
# ==========================================
with tab6:
    st.subheader("📰 실시간 KBO 주요 야구 뉴스")

    col_news_filter, _ = st.columns([1, 2])
    with col_news_filter:
        news_query = st.selectbox(
            "뉴스 키워드 / 구단 필터",
            options=["KBO 프로야구"] + [f"KBO {KBO_TEAMS[k]['name_full']}" for k in KBO_TEAMS.keys()]
        )

    with st.spinner("최신 뉴스를 불러오는 중..."):
        news_list = kbo_data.fetch_kbo_news(news_query)

    for item in news_list:
        with st.container():
            col_img, col_text = st.columns([1, 4])
            with col_img:
                if item.get("image"):
                    st.image(item["image"], use_container_width=True)
                else:
                    st.markdown("⚾ **KBO NEWS**")
            with col_text:
                st.markdown(f"#### [{item['title']}]({item['link']})")
                st.caption(f"**{item['press']}** · {item['time']}")
                if item.get('desc'):
                    st.write(item['desc'])
            st.divider()
