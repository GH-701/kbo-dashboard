"""
kbo_teams.py - KBO 10개 구단 및 홈구장 상세 정보 (공식 웹사이트, 유튜브, 굿즈샵 포함)
"""

# 각 팀의 한국어 명칭, 대표 컬러, 홈구장, 공식 사이트, 유튜브 채널 및 굿즈샵 정보
KBO_TEAMS = {
    "KIA": {
        "name_full": "KIA 타이거즈",
        "short_name": "KIA",
        "aliases": ["kia", "기아", "타이거즈", "기아 타이거즈", "KIA 타이거즈", "호랑이"],
        "color_primary": "#EA0029",
        "color_secondary": "#06141F",
        "stadium_name": "광주-기아 챔피언스 필드",
        "stadium_address": "광주광역시 북구 서림로 10 (임동)",
        "website": "https://tigers.co.kr/",
        "youtube": "https://www.youtube.com/@kiatigerstv",
        "shop": "https://www.tigersshop.kr/",
        "lat": 35.168128,
        "lon": 126.889104,
        "outfield": {"left": 99, "center": 121, "right": 99, "fence_height": 2.6}
    },
    "삼성": {
        "name_full": "삼성 라이온즈",
        "short_name": "삼성",
        "aliases": ["삼성", "라이온즈", "삼성 라이온즈", "삼라", "samsung"],
        "color_primary": "#0066B3",
        "color_secondary": "#C0C0C0",
        "stadium_name": "대구 삼성 라이온즈 파크",
        "stadium_address": "대구광역시 수성구 야구전설로 1 (연호동)",
        "website": "https://www.samsunglions.com/",
        "youtube": "https://www.youtube.com/@lionstv1982",
        "shop": "https://samsunglionsmall.com/",
        "lat": 35.841170,
        "lon": 128.681534,
        "outfield": {"left": 99.5, "center": 122.5, "right": 99.5, "fence_height": 3.6}
    },
    "LG": {
        "name_full": "LG 트윈스",
        "short_name": "LG",
        "aliases": ["lg", "LG", "엘지", "트윈스", "LG 트윈스", "엘지 트윈스", "쌍둥이"],
        "color_primary": "#C30037",
        "color_secondary": "#000000",
        "stadium_name": "서울종합운동장 야구장 (잠실)",
        "stadium_address": "서울특별시 송파구 올림픽로 25 (잠실동)",
        "website": "https://www.lgtwins.com/",
        "youtube": "https://www.youtube.com/@LGTwinsTV",
        "shop": "https://www.lgtwinsshop.com/",
        "lat": 37.512257,
        "lon": 127.071901,
        "outfield": {"left": 100, "center": 125, "right": 100, "fence_height": 2.6}
    },
    "두산": {
        "name_full": "두산 베어스",
        "short_name": "두산",
        "aliases": ["두산", "베어스", "두산 베어스", "돐", "곰", "doosan"],
        "color_primary": "#131230",
        "color_secondary": "#ED1C24",
        "stadium_name": "서울종합운동장 야구장 (잠실)",
        "stadium_address": "서울특별시 송파구 올림픽로 25 (잠실동)",
        "website": "https://www.doosanbears.com/",
        "youtube": "https://www.youtube.com/@bearstv",
        "shop": "https://www.wefan.co.kr/",
        "lat": 37.512257,
        "lon": 127.071901,
        "outfield": {"left": 100, "center": 125, "right": 100, "fence_height": 2.6}
    },
    "KT": {
        "name_full": "KT 위즈",
        "short_name": "KT",
        "aliases": ["kt", "KT", "케이티", "위즈", "KT 위즈", "케이티 위즈", "콱"],
        "color_primary": "#000000",
        "color_secondary": "#EC1C24",
        "stadium_name": "수원 케이티 위즈 파크",
        "stadium_address": "경기도 수원시 장안구 경수대로 893 (조원동)",
        "website": "https://www.ktwiz.co.kr/",
        "youtube": "https://www.youtube.com/@ktwiztv",
        "shop": "https://www.ktwizstore.co.kr/",
        "lat": 37.299710,
        "lon": 127.009703,
        "outfield": {"left": 95, "center": 120, "right": 95, "fence_height": 4.0}
    },
    "SSG": {
        "name_full": "SSG 랜더스",
        "short_name": "SSG",
        "aliases": ["ssg", "SSG", "쓱", "랜더스", "SSG 랜더스", "에스에스지", "sk"],
        "color_primary": "#CE0E2D",
        "color_secondary": "#C49A45",
        "stadium_name": "인천 SSG 랜더스필드",
        "stadium_address": "인천광역시 미추홀구 매소홀로 618 (문학동)",
        "website": "https://www.ssglanders.com/",
        "youtube": "https://www.youtube.com/@ssglanderstv",
        "shop": "https://ssglandersstore.com/",
        "lat": 37.437042,
        "lon": 126.693262,
        "outfield": {"left": 95, "center": 120, "right": 95, "fence_height": 2.4}
    },
    "롯데": {
        "name_full": "롯데 자이언츠",
        "short_name": "롯데",
        "aliases": ["롯데", "자이언츠", "롯데 자이언츠", "꼴데", "거인", "lotte"],
        "color_primary": "#041E42",
        "color_secondary": "#DC032A",
        "stadium_name": "부산 사직 야구장",
        "stadium_address": "부산광역시 동래구 사직로 45 (사직동)",
        "website": "https://www.giantsclub.com/",
        "youtube": "https://www.youtube.com/@giants_tv",
        "shop": "https://www.lottegiantsshop.com/",
        "lat": 35.194032,
        "lon": 129.061518,
        "outfield": {"left": 95, "center": 120.5, "right": 95, "fence_height": 6.0}
    },
    "한화": {
        "name_full": "한화 이글스",
        "short_name": "한화",
        "aliases": ["한화", "이글스", "한화 이글스", "칟", "독수리", "hanwha"],
        "color_primary": "#FF6600",
        "color_secondary": "#222222",
        "stadium_name": "대전 한화생명 이글스파크",
        "stadium_address": "대전광역시 중구 대종로 373 (부사동)",
        "website": "https://www.hanwhaeagles.co.kr/",
        "youtube": "https://www.youtube.com/@eaglestv",
        "shop": "https://eagles.lockerdium.com/",
        "lat": 36.317070,
        "lon": 127.429134,
        "outfield": {"left": 100, "center": 122, "right": 100, "fence_height": 4.0}
    },
    "NC": {
        "name_full": "NC 다이노스",
        "short_name": "NC",
        "aliases": ["nc", "NC", "엔씨", "다이노스", "NC 다이노스", "엔씨 다이노스", "공룡"],
        "color_primary": "#315288",
        "color_secondary": "#AF9165",
        "stadium_name": "창원 NC 파크",
        "stadium_address": "경상남도 창원시 마산회원구 삼호로 63 (양덕동)",
        "website": "https://www.ncdinos.com/",
        "youtube": "https://www.youtube.com/@ncdinos",
        "shop": "https://shop.ncdinos.com/",
        "lat": 35.222533,
        "lon": 128.582375,
        "outfield": {"left": 101, "center": 122, "right": 101, "fence_height": 3.3}
    },
    "키움": {
        "name_full": "키움 히어로즈",
        "short_name": "키움",
        "aliases": ["키움", "히어로즈", "키움 히어로즈", "넥센", "영웅", "kiwoom"],
        "color_primary": "#570514",
        "color_secondary": "#B0915B",
        "stadium_name": "서울 고척 스카이돔",
        "stadium_address": "서울특별시 구로구 경인로 430 (고척동)",
        "website": "https://www.heroesbaseball.co.kr/",
        "youtube": "https://www.youtube.com/@heroestv",
        "shop": "https://interpark.com/",
        "lat": 37.498233,
        "lon": 126.867107,
        "outfield": {"left": 99, "center": 122, "right": 99, "fence_height": 4.0}
    }
}

# 팀 별칭 -> 표준 팀 키 (예: "LG", "KIA", "삼성")
TEAM_ALIAS_MAP = {}
for key, data in KBO_TEAMS.items():
    TEAM_ALIAS_MAP[key.lower()] = key
    TEAM_ALIAS_MAP[data["name_full"].lower()] = key
    for alias in data["aliases"]:
        TEAM_ALIAS_MAP[alias.lower()] = key

def resolve_team_key(input_str: str) -> str:
    """사용자가 입력한 팀 이름을 KBO 표준 키로 변환"""
    if not input_str:
        return "KIA"
    clean = input_str.strip().lower()
    return TEAM_ALIAS_MAP.get(clean, None)

def get_team_info(team_key_or_name: str) -> dict:
    """팀 표준 키나 이름으로 팀 정보 딕셔너리 반환"""
    key = resolve_team_key(team_key_or_name)
    if key and key in KBO_TEAMS:
        return KBO_TEAMS[key]
    return KBO_TEAMS["KIA"]
