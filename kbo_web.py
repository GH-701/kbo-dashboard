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
import kbo_players
from kbo_players import KBO_BATTERS, KBO_PITCHERS

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
    st.subheader("🏃‍♂️ KBO 10개 구단 선수 상세 기록 및 능력치 비교")

    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "👥 구단별 선수 명단 및 성적",
        "📊 선수 스탯 비교 시뮬레이터 (Radar)",
        "🏆 KBO 역대 레전드 TOP 10"
    ])

    # ----------------------------------------------------
    # [서브탭 1] 10개 구단별 선수 명단 및 성적
    # ----------------------------------------------------
    with sub_tab1:
        st.markdown("#### 10개 구단별 대표 타자 및 투수 라인업")
        col_team_filter, col_pos_filter = st.columns([1, 1])
        with col_team_filter:
            team_filter_options = ["전체 10개 구단"] + list(KBO_TEAMS.keys())
            selected_team_filter = st.selectbox(
                "구단 선택",
                options=team_filter_options,
                format_func=lambda x: f"{KBO_TEAMS[x]['name_full']}" if x != "전체 10개 구단" else "전체 10개 구단 (모든 선수)"
            )
        with col_pos_filter:
            pos_choice = st.radio("포지션 선택", ["타자 (Hitter)", "투수 (Pitcher)"], horizontal=True)

        if pos_choice == "타자 (Hitter)":
            batters_list = []
            for k, v in KBO_BATTERS.items():
                if selected_team_filter == "전체 10개 구단" or v["team"] == selected_team_filter:
                    batters_list.append({
                        "선수명": v["name"],
                        "구단": KBO_TEAMS.get(v["team"], {}).get("name_full", v["team"]),
                        "포지션": v["pos"],
                        "타율 (AVG)": f"{v['타율']:.3f}",
                        "홈런 (HR)": v["홈런"],
                        "타점 (RBI)": v["타점"],
                        "안타 (H)": v["안타"],
                        "도루 (SB)": v["도루"],
                        "출루율 (OBP)": f"{v['출루율']:.3f}",
                        "장타율 (SLG)": f"{v['장타율']:.3f}",
                        "OPS": f"{v['OPS']:.3f}"
                    })
            df_filtered_batters = pd.DataFrame(batters_list)
            st.dataframe(df_filtered_batters, use_container_width=True, hide_index=True)

            # 상위 홈런 타자 바 차트
            if not df_filtered_batters.empty:
                df_hr_top = df_filtered_batters.sort_values(by="홈런 (HR)", ascending=False).head(8)
                fig_hr = go.Figure(go.Bar(
                    x=df_hr_top["선수명"] + " (" + df_hr_top["구단"] + ")",
                    y=df_hr_top["홈런 (HR)"],
                    marker_color="#ea0029",
                    text=df_hr_top["홈런 (HR)"].astype(str) + "개",
                    textposition='auto'
                ))
                fig_hr.update_layout(
                    title="선택된 구단 홈런 순위",
                    yaxis_title="홈런 수",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#f8fafc" if st.session_state['dark_mode'] else "#1e293b"),
                    height=300
                )
                st.plotly_chart(fig_hr, use_container_width=True)

        else: # 투수
            pitchers_list = []
            for k, v in KBO_PITCHERS.items():
                if selected_team_filter == "전체 10개 구단" or v["team"] == selected_team_filter:
                    pitchers_list.append({
                        "선수명": v["name"],
                        "구단": KBO_TEAMS.get(v["team"], {}).get("name_full", v["team"]),
                        "보직": v["role"],
                        "평균자책점 (ERA)": f"{v['ERA']:.2f}",
                        "승리 (W)": v["승"],
                        "패배 (L)": v["패"],
                        "세이브 (SV)": v["세이브"],
                        "홀드 (HLD)": v["홀드"],
                        "이닝 (IP)": v["이닝"],
                        "탈삼진 (SO)": v["탈삼진"],
                        "WHIP": f"{v['WHIP']:.2f}"
                    })
            df_filtered_pitchers = pd.DataFrame(pitchers_list)
            st.dataframe(df_filtered_pitchers, use_container_width=True, hide_index=True)

            # 평균자책점 바 차트
            if not df_filtered_pitchers.empty:
                df_era_top = df_filtered_pitchers.sort_values(by="평균자책점 (ERA)", ascending=True).head(8)
                fig_era = go.Figure(go.Bar(
                    x=df_era_top["선수명"] + " (" + df_era_top["구단"] + ")",
                    y=pd.to_numeric(df_era_top["평균자책점 (ERA)"]),
                    marker_color="#0066b3",
                    text=df_era_top["평균자책점 (ERA)"],
                    textposition='auto'
                ))
                fig_era.update_layout(
                    title="선택된 구단 평균자책점(ERA) 순위 (낮을수록 우수)",
                    yaxis_title="ERA",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="#f8fafc" if st.session_state['dark_mode'] else "#1e293b"),
                    height=300
                )
                st.plotly_chart(fig_era, use_container_width=True)

    # ----------------------------------------------------
    # [서브탭 2] 선수 스탯 비교 시뮬레이터 (Radar Chart)
    # ----------------------------------------------------
    with sub_tab2:
        st.markdown("#### 📊 KBO 대표 타자 스탯 비교 시뮬레이터")
        st.caption("구단별 대표 타자 2명을 선택하여 6대 핵심 지표(타율, 홈런, 타점, 안타, 출루율, 장타율)를 레이더 차트로 직접 비교해보세요.")

        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            st.markdown("##### 👤 첫 번째 타자")
            sim_team1 = st.selectbox("구단 필터 (타자 1)", options=["전체"] + list(KBO_TEAMS.keys()), key="sim_team1")
            candidates1 = [k for k, v in KBO_BATTERS.items() if (sim_team1 == "전체" or v["team"] == sim_team1)]
            player1_key = st.selectbox("선수 선택 (타자 1)", options=candidates1, index=0, key="sim_p1")

        with col_sim2:
            st.markdown("##### 👤 두 번째 타자")
            sim_team2 = st.selectbox("구단 필터 (타자 2)", options=["전체"] + list(KBO_TEAMS.keys()), index=2 if len(KBO_TEAMS) > 2 else 0, key="sim_team2")
            candidates2 = [k for k, v in KBO_BATTERS.items() if (sim_team2 == "전체" or v["team"] == sim_team2)]
            def_idx = 1 if len(candidates2) > 1 else 0
            player2_key = st.selectbox("선수 선택 (타자 2)", options=candidates2, index=def_idx, key="sim_p2")

        p1_info = KBO_BATTERS[player1_key]
        p2_info = KBO_BATTERS[player2_key]

        # 6대 지표 정규화 (0~100 스케일)
        # 지표 최대 기준: 타율 0.400, 홈런 50, 타점 140, 안타 210, 출루율 0.460, 장타율 0.700
        METRIC_SPECS = {
            "타율": {"max": 0.400, "unit": ""},
            "홈런": {"max": 50, "unit": "개"},
            "타점": {"max": 140, "unit": "점"},
            "안타": {"max": 210, "unit": "개"},
            "출루율": {"max": 0.460, "unit": ""},
            "장타율": {"max": 0.700, "unit": ""}
        }

        cats = list(METRIC_SPECS.keys())
        cats_closed = cats + [cats[0]]

        def norm_val(val, cat):
            mx = METRIC_SPECS[cat]["max"]
            return min(100.0, max(0.0, (val / mx) * 100.0))

        p1_r = [norm_val(p1_info[c], c) for c in cats] + [norm_val(p1_info[cats[0]], cats[0])]
        p2_r = [norm_val(p2_info[c], c) for c in cats] + [norm_val(p2_info[cats[0]], cats[0])]

        p1_hover = [f"{c}: {p1_info[c]}{METRIC_SPECS[c]['unit']}" for c in cats] + [f"{cats[0]}: {p1_info[cats[0]]}"]
        p2_hover = [f"{c}: {p2_info[c]}{METRIC_SPECS[c]['unit']}" for c in cats] + [f"{cats[0]}: {p2_info[cats[0]]}"]

        col_radar_chart, col_radar_table = st.columns([1.2, 1])

        with col_radar_chart:
            fig_radar = go.Figure()

            # Player 1 Radar
            fig_radar.add_trace(go.Scatterpolar(
                r=p1_r,
                theta=cats_closed,
                fill='toself',
                name=player1_key,
                hoverinfo='text',
                text=p1_hover,
                line=dict(color=p1_info["color"], width=3),
                fillcolor=p1_info["color"],
                opacity=0.35
            ))

            # Player 2 Radar
            fig_radar.add_trace(go.Scatterpolar(
                r=p2_r,
                theta=cats_closed,
                fill='toself',
                name=player2_key,
                hoverinfo='text',
                text=p2_hover,
                line=dict(color=p2_info["color"], width=3),
                fillcolor=p2_info["color"],
                opacity=0.35
            ))

            text_c = "#f8fafc" if st.session_state['dark_mode'] else "#0f172a"
            grid_c = "#334155" if st.session_state['dark_mode'] else "#cbd5e1"
            bg_c = "rgba(30, 41, 59, 0.4)" if st.session_state['dark_mode'] else "rgba(241, 245, 249, 0.5)"

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor=grid_c),
                    angularaxis=dict(gridcolor=grid_c, tickfont=dict(size=12, color=text_c)),
                    bgcolor=bg_c
                ),
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color=text_c),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                height=420,
                margin=dict(t=30, b=40, l=40, r=40)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_radar_table:
            st.markdown("##### 📋 세부 스탯 비교표")
            compare_rows = []
            for c in ["포지션", "타율", "홈런", "타점", "안타", "도루", "출루율", "장타율", "OPS"]:
                v1 = p1_info[c]
                v2 = p2_info[c]
                if isinstance(v1, float):
                    v1_str = f"{v1:.3f}"
                    v2_str = f"{v2:.3f}"
                    diff_sym = "◀ 우세" if v1 > v2 else ("우세 ▶" if v2 > v1 else "=")
                elif isinstance(v1, int):
                    v1_str = str(v1)
                    v2_str = str(v2)
                    diff_sym = "◀ 우세" if v1 > v2 else ("우세 ▶" if v2 > v1 else "=")
                else:
                    v1_str = str(v1)
                    v2_str = str(v2)
                    diff_sym = "-"

                compare_rows.append({
                    "지표": c,
                    f"{p1_info['name']} ({p1_info['team']})": v1_str,
                    "비교": diff_sym,
                    f"{p2_info['name']} ({p2_info['team']})": v2_str
                })
            df_compare = pd.DataFrame(compare_rows)
            st.dataframe(df_compare, use_container_width=True, hide_index=True)

    # ----------------------------------------------------
    # [서브탭 3] KBO 역대 레전드 TOP 10
    # ----------------------------------------------------
    with sub_tab3:
        st.markdown("#### 🏆 KBO 리그 역대 최고 기록 TOP 10")
        stat_choice = st.radio("역대 기록 부문", ["역대 최고 타율 TOP 10", "단일시즌 최다승 투수 TOP 10"], horizontal=True)

        if stat_choice == "역대 최고 타율 TOP 10":
            b_data = kbo_data.fetch_top_batters()
            df_b = pd.DataFrame(b_data)
            st.dataframe(df_b, use_container_width=True, hide_index=True)
        else:
            p_data = kbo_data.fetch_top_pitchers()
            df_p = pd.DataFrame(p_data)
            st.dataframe(df_p, use_container_width=True, hide_index=True)

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

