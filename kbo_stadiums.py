"""
kbo_stadiums.py - KBO 구장 상세 규격 및 인터랙티브 지도/시각화 모듈
"""

import math
import folium
import plotly.graph_objects as go
from kbo_teams import KBO_TEAMS

# KBO 구장 상세 정보
STADIUM_DETAILS = {
    "KIA": {
        "stadium_name": "광주-기아 챔피언스 필드",
        "opened_year": 2014,
        "capacity": "20,500석",
        "turf": "천연잔디",
        "left_m": 99.0,
        "center_m": 121.0,
        "right_m": 99.0,
        "fence_height": "2.6m",
        "address": "광주광역시 북구 서림로 10 (임동)",
        "lat": 35.168128,
        "lon": 126.889104,
        "features": "국내 최초 개방형 메이저리그식 야구장, 쾌적한 관람 시야 및 가족석 특화"
    },
    "삼성": {
        "stadium_name": "대구 삼성 라이온즈 파크",
        "opened_year": 2016,
        "capacity": "24,000석",
        "turf": "천연잔디",
        "left_m": 99.5,
        "center_m": 122.5,
        "right_m": 99.5,
        "fence_height": "3.6m",
        "address": "대구광역시 수성구 야구전설로 1 (연호동)",
        "lat": 35.841170,
        "lon": 128.681534,
        "features": "국내 유일의 팔각형 다이아몬드 구장, 짧은 좌우중간 펜스로 홈런 친화적 구조"
    },
    "LG": {
        "stadium_name": "서울종합운동장 야구장 (잠실)",
        "opened_year": 1982,
        "capacity": "23,750석",
        "turf": "천연잔디",
        "left_m": 100.0,
        "center_m": 125.0,
        "right_m": 100.0,
        "fence_height": "2.6m",
        "address": "서울특별시 송파구 올림픽로 25 (잠실동)",
        "lat": 37.512257,
        "lon": 127.071901,
        "features": "한국 프로야구의 성지, 국내 최대 규모의 광활한 외야 펜스를 자랑하는 투수 친화 구장"
    },
    "두산": {
        "stadium_name": "서울종합운동장 야구장 (잠실)",
        "opened_year": 1982,
        "capacity": "23,750석",
        "turf": "천연잔디",
        "left_m": 100.0,
        "center_m": 125.0,
        "right_m": 100.0,
        "fence_height": "2.6m",
        "address": "서울특별시 송파구 올림픽로 25 (잠실동)",
        "lat": 37.512257,
        "lon": 127.071901,
        "features": "LG 트윈스와 함께 홈으로 사용하는 대한민국 대표 야구장"
    },
    "KT": {
        "stadium_name": "수원 케이티 위즈 파크",
        "opened_year": 2015,
        "capacity": "18,700석",
        "turf": "천연잔디",
        "left_m": 95.0,
        "center_m": 120.0,
        "right_m": 95.0,
        "fence_height": "4.0m",
        "address": "경기도 수원시 장안구 경수대로 893 (조원동)",
        "lat": 37.299710,
        "lon": 127.009703,
        "features": "스마트 첨단 ICT 구장, 맛있는 먹거리(진미통닭, 보영만두 등)로 유명"
    },
    "SSG": {
        "stadium_name": "인천 SSG 랜더스필드",
        "opened_year": 2002,
        "capacity": "23,000석",
        "turf": "천연잔디",
        "left_m": 95.0,
        "center_m": 120.0,
        "right_m": 95.0,
        "fence_height": "2.4m",
        "address": "인천광역시 미추홀구 매소홀로 618 (문학동)",
        "lat": 37.437042,
        "lon": 126.693262,
        "features": "국내 최초 메이저리그식 포수 후면석, 빅보드 초대형 전광판 및 바비큐존 명소"
    },
    "롯데": {
        "stadium_name": "부산 사직 야구장",
        "opened_year": 1985,
        "capacity": "22,990석",
        "turf": "천연잔디",
        "left_m": 95.0,
        "center_m": 120.5,
        "right_m": 95.0,
        "fence_height": "6.0m",
        "address": "부산광역시 동래구 사직로 45 (사직동)",
        "lat": 35.194032,
        "lon": 129.061518,
        "features": "‘구도 부산’의 열정적인 응원 문화의 요람, 6m 사직몬스터 펜스 보유"
    },
    "한화": {
        "stadium_name": "대전 한화생명 이글스파크",
        "opened_year": 1964,
        "capacity": "12,000석",
        "turf": "천연잔디",
        "left_m": 100.0,
        "center_m": 122.0,
        "right_m": 100.0,
        "fence_height": "4.0m",
        "address": "대전광역시 중구 대종로 373 (부사동)",
        "lat": 36.317070,
        "lon": 127.429134,
        "features": "유서 깊은 역사를 자랑하며, 육성응원과 뜨거운 팬덤으로 유명한 대전 야구의 심장"
    },
    "NC": {
        "stadium_name": "창원 NC 파크",
        "opened_year": 2019,
        "capacity": "17,891석",
        "turf": "천연잔디",
        "left_m": 101.0,
        "center_m": 122.0,
        "right_m": 101.0,
        "fence_height": "3.3m",
        "address": "경상남도 창원시 마산회원구 삼호로 63 (양덕동)",
        "lat": 35.222533,
        "lon": 128.582375,
        "features": "360도 개방형 콘코스, 완만한 경사로 무장애 설계가 적용된 최신식 명품 구장"
    },
    "키움": {
        "stadium_name": "서울 고척 스카이돔",
        "opened_year": 2015,
        "capacity": "16,000석",
        "turf": "인조잔디",
        "left_m": 99.0,
        "center_m": 122.0,
        "right_m": 99.0,
        "fence_height": "4.0m",
        "address": "서울특별시 구로구 경인로 430 (고척동)",
        "lat": 37.498233,
        "lon": 126.867107,
        "features": "대한민국 최초의 돔 야구장, 우천 취소 없이 사계절 쾌적한 냉난방 관람 환경 제공"
    }
}

def create_stadium_field_chart(team_key: str, dark_mode: bool = False) -> go.Figure:
    """
    야구장 펜스 및 내야 다이아몬드 규격을 시각화한 인터랙티브 Plotly 차트 생성
    """
    stadium = STADIUM_DETAILS.get(team_key, STADIUM_DETAILS["KIA"])
    team = KBO_TEAMS.get(team_key, KBO_TEAMS["KIA"])
    team_color = team["color_primary"]

    left = stadium["left_m"]
    center = stadium["center_m"]
    right = stadium["right_m"]

    # 외야 호 생성 (좌측폴 -45도 ~ 중앙 0도 ~ 우측폴 +45도)
    theta_deg = [i for i in range(-45, 46, 2)]
    r_vals = []
    for th in theta_deg:
        # 각도에 따른 거리 보간 (포물선 형태)
        ratio = (45 - abs(th)) / 45.0
        dist = (left + (center - left) * ratio) if th <= 0 else (right + (center - right) * ratio)
        r_vals.append(dist)

    # 닫힌 외야 폴리곤 (홈플레이트 0에서 시작)
    poly_theta = [-45] + theta_deg + [45, -45]
    poly_r = [0] + r_vals + [0, 0]

    bg_color = "rgba(30, 41, 59, 0.7)" if dark_mode else "rgba(241, 245, 249, 0.8)"
    text_color = "#f8fafc" if dark_mode else "#1e293b"
    turf_color = "rgba(34, 197, 94, 0.35)" if not dark_mode else "rgba(22, 101, 52, 0.45)"

    fig = go.Figure()

    # 그라운드 영역 (잔디)
    fig.add_trace(go.Scatterpolar(
        r=poly_r,
        theta=poly_theta,
        fill='toself',
        fillcolor=turf_color,
        line=dict(color=team_color, width=3),
        name=stadium["stadium_name"],
        hoverinfo='text',
        text=[f"외야 펜스 라인<br>중앙: {center}m, 좌: {left}m, 우: {right}m"] * len(poly_theta)
    ))

    # 내야 다이아몬드 (베이스 거리: 약 27.43m)
    diamond_theta = [0, -45, 0, 45, 0]
    diamond_r = [0, 27.4, 38.8, 27.4, 0] # 홈 -> 3루 -> 2루 -> 1루 -> 홈
    fig.add_trace(go.Scatterpolar(
        r=diamond_r,
        theta=diamond_theta,
        mode='lines+markers',
        line=dict(color="#f59e0b", width=2),
        marker=dict(size=8, color=["#ffffff", "#ef4444", "#3b82f6", "#ef4444", "#ffffff"]),
        name="내야 다이아몬드",
        hoverinfo='text',
        text=["홈플레이트", "3루 베이스", "2루 베이스", "1루 베이스", "홈플레이트"]
    ))

    fig.update_layout(
        title=dict(
            text=f"🏟️ {stadium['stadium_name']} 외야 및 그라운드 규격도",
            font=dict(color=text_color, size=15)
        ),
        polar=dict(
            sector=[-55, 55],
            radialaxis=dict(
                visible=True,
                range=[0, center + 15],
                tickfont=dict(color=text_color, size=10),
                ticksuffix="m"
            ),
            angularaxis=dict(
                direction="clockwise",
                rotation=90,
                tickfont=dict(color=text_color, size=11),
                tickmode="array",
                tickvals=[-45, -22.5, 0, 22.5, 45],
                ticktext=["좌측 폴", "좌중간", "중앙 (백스크린)", "우중간", "우측 폴"]
            ),
            bgcolor=bg_color
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=380,
        margin=dict(t=40, b=20, l=40, r=40)
    )

    return fig

def create_kbo_stadium_map(selected_team: str = "KIA") -> folium.Map:
    """
    KBO 10개 구단 홈구장을 표시하는 Folium 지도 생성
    """
    info = STADIUM_DETAILS.get(selected_team, STADIUM_DETAILS["KIA"])
    m = folium.Map(
        location=[info["lat"], info["lon"]],
        zoom_start=14,
        tiles="OpenStreetMap"
    )

    for team_k, s_data in STADIUM_DETAILS.items():
        team_cfg = KBO_TEAMS.get(team_k, {})
        color = team_cfg.get("color_primary", "#ea0029")
        is_selected = (team_k == selected_team)

        popup_html = f"""
        <div style="font-family: 'Noto Sans KR', sans-serif; min-width: 200px;">
            <h4 style="margin: 0 0 5px 0; color: {color};">{s_data['stadium_name']}</h4>
            <p style="margin: 0; font-size: 12px; color: #555;"><b>구단:</b> {team_cfg.get('name_full', team_k)}</p>
            <p style="margin: 3px 0; font-size: 12px; color: #555;"><b>규모:</b> {s_data['capacity']} ({s_data['turf']})</p>
            <p style="margin: 3px 0; font-size: 12px; color: #555;"><b>펜스:</b> 좌우 {s_data['left_m']}m / 중앙 {s_data['center_m']}m</p>
            <p style="margin: 3px 0; font-size: 11px; color: #888;">{s_data['address']}</p>
            <a href="{team_cfg.get('website', '#')}" target="_blank" style="display:inline-block; margin-top:6px; font-size:11px; color:{color}; font-weight:bold;">공식 웹사이트 바로가기 →</a>
        </div>
        """

        folium.CircleMarker(
            location=[s_data["lat"], s_data["lon"]],
            radius=12 if is_selected else 8,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9 if is_selected else 0.6,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{s_data['stadium_name']} ({team_cfg.get('name_full', team_k)})"
        ).add_to(m)

    return m
