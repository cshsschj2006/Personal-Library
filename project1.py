import streamlit as st
import pandas as pd
import numpy as np
import time
import base64

# 1. 페이지 및 홍익대학교 테마 설정 (Hongik Deep Navy & Crimson Red)
st.set_page_config(
    page_title="Hongik University Personal Library", 
    page_icon="📖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 이미지 base64 변환 함수 (로컬 이미지를 HTML에 직접 주입하기 위함)
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

logo_base64 = get_base64_image("assets/hongik_logo.png")

# Streamlit Cloud 등 로컬 assets/hongik_logo.png 파일을 찾을 수 없는 배포 환경에서 로고가 깨지지 않도록 인터넷 URL 폴백 적용
if not logo_base64:
    logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Hongik_University_Logo.svg/1024px-Hongik_University_Logo.svg.png"
else:
    logo_url = f"data:image/png;base64,{logo_base64}"

# 홍익대학교 공식 색상 테마 주입
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; }
    .stApp { background-color: #f8f9fa; color: #212529; }
    
    /* 헤더 스타일 */
    .hongik-header {
        background: linear-gradient(90deg, #002C6C 0%, #001f4d 100%);
        color: white; padding: 2rem; border-radius: 12px;
        border-bottom: 5px solid #A50034; margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 44, 108, 0.15);
    }
    .hongik-header h1 { margin: 0; font-size: 2.2rem; font-weight: 800; color: white !important; }
    .hongik-header p { margin: 5px 0 0 0; color: rgba(255,255,255,0.75); font-size: 0.95rem; }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px; background-color: #ffffff;
        border-radius: 8px; padding: 6px; border: 1px solid #dee2e6;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.05rem; font-weight: 600; padding: 10px 22px;
        border-radius: 6px; color: #495057 !important; transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #002C6C !important;
        color: white !important; box-shadow: 0 4px 10px rgba(0, 44, 108, 0.25);
    }
    
    /* 버튼 스타일 및 흰색 텍스트 강제 지정 */
    .stButton > button, [data-testid="stFormSubmitButton"] button {
        background-color: #002C6C !important; color: #ffffff !important;
        border: none !important; border-radius: 6px !important;
        padding: 8px 16px !important; font-weight: 600 !important;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover {
        background-color: #A50034 !important; color: #ffffff !important;
        transform: translateY(-1px);
    }
    
    /* 뱃지 및 메트릭 */
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; color: #002C6C !important; }
    
    /* 박스 및 카드 공통 */
    .custom-card {
        background-color: white; border-radius: 10px; padding: 1.5rem;
        border: 1px solid #dee2e6; border-top: 4px solid #002C6C;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 1.5rem;
    }
    
    .genre-badge {
        display: inline-block; padding: 3px 8px; border-radius: 4px;
        font-size: 0.75rem; font-weight: 700; color: white; margin-right: 4px;
    }
    
    /* 데이터프레임 내부 검색창 및 돋보기 툴바 숨기기 (SASS 네스팅 제거하여 안전한 일반 CSS 사용) */
    div[data-testid="stDataFrame"] div[data-testid="stElementToolbar"] { display: none !important; }
    div[data-testid="stDataFrame"] button[title="Search table"] { display: none !important; }
    div[data-testid="stDataFrame"] [data-testid="stToolbar"] { display: none !important; }
    
    /* 로그아웃 버튼 스타일링 */
    .logout-btn-wrapper button {
        background-color: #A50034 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 700 !important;
        transition: background-color 0.2s;
    }
    .logout-btn-wrapper button:hover {
        background-color: #820028 !important;
    }
    
    /* 화면 고정 대출 순위 플로팅 버튼 */
    .floating-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #002C6C;
        color: white !important;
        padding: 12px 20px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        text-decoration: none !important;
        border: 2px solid #A50034;
        transition: background-color 0.2s, transform 0.2s;
    }
    .floating-btn:hover {
        background-color: #A50034;
        transform: scale(1.05);
    }
    .floating-btn-up {
        position: fixed;
        bottom: 90px;
        right: 30px;
        background-color: #A50034;
        color: white !important;
        padding: 12px 20px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        text-decoration: none !important;
        border: 2px solid #002C6C;
        transition: background-color 0.2s, transform 0.2s;
    }
    .floating-btn-up:hover {
        background-color: #002C6C;
        transform: scale(1.05);
    }
    </style>
""""", unsafe_allow_html=True)

# 로그인 화면의 stForm 전용 워터마크 CSS 분리 주입 (f-string 적용하여 logo_url 이미지 동적 결합)
st.markdown(f"""
    <style>
    div[data-testid="stForm"] {{
        max-width: 450px !important; margin: 4% auto !important; background-color: rgba(255, 255, 255, 0.96) !important;
        background-image: linear-gradient(rgba(255, 255, 255, 0.91), rgba(255, 255, 255, 0.91)), url('{logo_url}') !important;
        background-repeat: no-repeat !important;
        background-position: center 65% !important;
        background-size: 260px !important;
        padding: 2.5rem !important; border-radius: 12px !important; border: 1px solid #dee2e6 !important;
        border-top: 6px solid #002C6C !important; box-shadow: 0 10px 25px rgba(0,0,0,0.08) !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 로그인 제어부 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = ""
if 'user_dept' not in st.session_state:
    st.session_state['user_dept'] = ""
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = ""

# --- 로그인 화면 구성 ---
if not st.session_state['logged_in']:
    col_l1, col_l2, col_l3 = st.columns([1, 1.8, 1])
    with col_l2:
        # st.form으로 감싸서 레이아웃을 완전히 묶어줌으로써 여백 및 가상 필드 에러 차단
        with st.form("login_form", border=True):
            st.markdown(f"""
                <div style="text-align: center; margin-bottom: 1rem;">
                    <img src="{logo_url}" style="width: 140px; height: 140px; object-fit: contain;" />
                </div>
                <h3 style='text-align: center; color:#002C6C; font-weight:800; margin-bottom:0.2rem; margin-top:0;'>🏛️ 홍익대학교 개인 도서관</h3>
                <p style='text-align: center; color:#6c757d; font-size:0.85rem; margin-bottom:1.5rem;'>로그인 정보를 입력하여 접속해 주세요.</p>
            """, unsafe_allow_html=True)
            
            input_id = st.text_input("학번 (아이디)", placeholder="아이디 입력")
            input_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력")
            
            login_btn = st.form_submit_button("로그인", use_container_width=True)
            
            if login_btn:
                if not input_id:
                    st.error("학번을 입력해주세요.")
                else:
                    # 1. 조현준 계정 판정
                    if input_id == "C621062":
                        if input_pw == "ghdeodptjahdu12!":
                            st.session_state['logged_in'] = True
                            st.session_state['user_name'] = "조현준"
                            st.session_state['user_id'] = "C621062"
                            st.session_state['user_dept'] = "산업데이터공학과"
                            st.session_state['user_email'] = "cshsschj2006@g.hongik.ac.kr"
                            st.success("조현준 님, 로그인을 환영합니다!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
                    # 2. 홍길동 계정 판정
                    elif input_id == "C007007":
                        if input_pw == "ghdrlfehd!":
                            st.session_state['logged_in'] = True
                            st.session_state['user_name'] = "홍길동"
                            st.session_state['user_id'] = "C007007"
                            st.session_state['user_dept'] = "경제학과"
                            st.session_state['user_email'] = "lightningd@g.hongik.ac.kr"
                            st.success("홍길동 님, 로그인을 환영합니다!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
                    # 3. 그 외 임의 아이디 차단
                    else:
                        st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
    st.stop()

# ============================================================
# 메인 어플리케이션 영역 (로그인 성공 시)
# ============================================================

# Mock Book Database 생성 (100권으로 확장)
@st.cache_data
def load_bestsellers_db():
    genres = ["소설", "경영/경제", "자기계발", "인문/사회", "IT/과학"]
    books = [
        # 소설 (20권)
        ("해리포터와 마법사의 돌", "J.K. 롤링", "소설", "https://placehold.co/200x280/1a2a40/ffffff?text=Harry+Potter", 145),
        ("해리포터와 비밀의 방", "J.K. 롤링", "소설", "https://placehold.co/200x280/1a2a40/ffffff?text=Harry+Potter+2", 98),
        ("불편한 편의점", "김호연", "소설", "https://placehold.co/200x280/2e5e4e/ffffff?text=Convenience+Store", 220),
        ("메리골드 마음 세탁소", "윤정은", "소설", "https://placehold.co/200x280/5a3d7c/ffffff?text=Mind+Laundry", 112),
        ("구의 증명", "최진영", "소설", "https://placehold.co/200x280/7a2d3c/ffffff?text=Gu+Proof", 85),
        ("모순", "양귀자", "소설", "https://placehold.co/200x280/4a3c2c/ffffff?text=Contradiction", 195),
        ("노르웨이의 숲", "무라카미 하루키", "소설", "https://placehold.co/200x280/1a4a2c/ffffff?text=Norwegian+Wood", 130),
        ("작별인사", "김영하", "소설", "https://placehold.co/200x280/2a2a2a/ffffff?text=Farewell", 94),
        ("아몬드", "손원평", "소설", "https://placehold.co/200x280/8a6d3b/ffffff?text=Almond", 160),
        ("미드나잇 라이브러리", "매트 헤이그", "소설", "https://placehold.co/200x280/1c3c5a/ffffff?text=Midnight+Lib", 140),
        ("달러구트 꿈 백화점", "이미예", "소설", "https://placehold.co/200x280/3c5a7c/ffffff?text=Dream+Shop", 215),
        ("작별하지 않는다", "한강", "소설", "https://placehold.co/200x280/1e2e3e/ffffff?text=No+Farewell", 88),
        ("바리가데", "작가 A", "소설", "https://placehold.co/200x280/2e3e4e/ffffff?text=Barigade", 72),
        ("아침의 첫 빛", "작가 B", "소설", "https://placehold.co/200x280/3e4e5e/ffffff?text=First+Light", 65),
        ("파친코 1", "이민진", "소설", "https://placehold.co/200x280/4e5e6e/ffffff?text=Pachinko+1", 110),
        ("파친코 2", "이민진", "소설", "https://placehold.co/200x280/5e6e7e/ffffff?text=Pachinko+2", 95),
        ("모래알만 한 진실이라도", "박완서", "소설", "https://placehold.co/200x280/6e7e8e/ffffff?text=Sand+Truth", 83),
        ("밝은 밤", "최은영", "소설", "https://placehold.co/200x280/7e8e9e/ffffff?text=Bright+Night", 79),
        ("눈부신 안부", "백수린", "소설", "https://placehold.co/200x280/8e9eae/ffffff?text=Bright+Hello", 81),
        ("우리가 빛의 속도로 갈 수 없다면", "김초엽", "소설", "https://placehold.co/200x280/9eaebe/ffffff?text=If+We+Cannot", 125),

        # 경영/경제 (20권)
        ("트렌드 코리아 2026", "김난도", "경영/경제", "https://placehold.co/200x280/6c1c24/ffffff?text=Trend+Korea", 250),
        ("부자 아빠 가난한 아빠", "로버트 기요사키", "경영/경제", "https://placehold.co/200x280/6c5a1c/ffffff?text=Rich+Dad", 180),
        ("돈의 속성", "김승호", "경영/경제", "https://placehold.co/200x280/1c5a2c/ffffff?text=Money+Rules", 155),
        ("EBS 다큐프라임 자본주의", "EBS 자본주의 제작팀", "경영/경제", "https://placehold.co/200x280/1c3c3c/ffffff?text=Capitalism", 125),
        ("보도 섀퍼의 돈", "보도 섀퍼", "경영/경제", "https://placehold.co/200x280/2c3c5c/ffffff?text=Bodo+Schaefer", 110),
        ("역행자", "자청", "경영/경제", "https://placehold.co/200x280/5c2c5c/ffffff?text=Life+Hacker", 205),
        ("부의 시나리오", "오건영", "경영/경제", "https://placehold.co/200x280/2c5c6c/ffffff?text=Wealth+Scenario", 90),
        ("원칙", "레이 달리오", "경영/경제", "https://placehold.co/200x280/4c4c4c/ffffff?text=Principles", 115),
        ("피터 린치의 이기는 투자", "피터 린치", "경영/경제", "https://placehold.co/200x280/1c4c6c/ffffff?text=Peter+Lynch", 95),
        ("내 집 마련의 비밀", "부동산 전문가", "경영/경제", "https://placehold.co/200x280/3c3c3c/ffffff?text=Real+Estate", 75),
        ("돈의 시나리오", "홍진채", "경영/경제", "https://placehold.co/200x280/4c3c3c/ffffff?text=Money+Scenario", 68),
        ("부의 추월차선", "엠제이 드마코", "경영/경제", "https://placehold.co/200x280/5c3c3c/ffffff?text=Fastlane", 150),
        ("주식투자 무작정 따라하기", "이희선", "경영/경제", "https://placehold.co/200x280/6c3c3c/ffffff?text=Stock+Intro", 102),
        ("부의 본능", "브라운스톤", "경영/경제", "https://placehold.co/200x280/7c3c3c/ffffff?text=Wealth+Instinct", 89),
        ("배움의 발견", "타라 웨스트오버", "경영/경제", "https://placehold.co/200x280/8c3c3c/ffffff?text=Educated", 78),
        ("사장학개론", "김승호", "경영/경제", "https://placehold.co/200x280/9c3c3c/ffffff?text=CEO+Intro", 120),
        ("트레이딩의 기술", "금융 전문가", "경영/경제", "https://placehold.co/200x280/ac3c3c/ffffff?text=Trading+Art", 62),
        ("거인의 어깨", "홍진채", "경영/경제", "https://placehold.co/200x280/bc3c3c/ffffff?text=Giant+Shoulder", 91),
        ("스태그플레이션 서바이벌", "경제 리포트", "경영/경제", "https://placehold.co/200x280/cc3c3c/ffffff?text=Stagflation", 74),
        ("인플레이션에서 살아남기", "오건영", "경영/경제", "https://placehold.co/200x280/dc3c3c/ffffff?text=Inflation", 83),

        # 자기계발 (20권)
        ("아주 작은 습관의 힘", "제임스 습관", "자기계발", "assets/atomic_habits_cover.png", 230),
        ("데일 카네기 인간관계론", "데일 카네기", "자기계발", "https://placehold.co/200x280/1c3c2c/ffffff?text=Dale+Carnegie", 175),
        ("그릿(GRIT)", "앤절라 더크워스", "자기계발", "https://placehold.co/200x280/4c2c1c/ffffff?text=Grit", 140),
        ("원씽(The One Thing)", "게리 켈러", "자기계발", "https://placehold.co/200x280/5c1c1c/ffffff?text=One+Thing", 165),
        ("타이탄의 도구들", "팀 페리스", "자기계발", "https://placehold.co/200x280/2c2c2c/ffffff?text=Tools+of+Titans", 150),
        ("미움받을 용기", "기시미 이치로", "자기계발", "https://placehold.co/200x280/2c4c5c/ffffff?text=Courage", 190),
        ("루틴의 힘", "댄 아리엘리", "자기계발", "https://placehold.co/200x280/3c2c4c/ffffff?text=Routine+Power", 88),
        ("스토리텔링 비밀", "마케터", "자기계발", "https://placehold.co/200x280/4c4c2c/ffffff?text=Storytelling", 62),
        ("생각에 관한 생각", "대니얼 카너먼", "자기계발", "https://placehold.co/200x280/1c1c1c/ffffff?text=Thinking+Fast", 105),
        ("초집중", "니어 이얄", "자기계발", "https://placehold.co/200x280/2c5c3c/ffffff?text=Indistractable", 80),
        ("미라클 모닝", "할 엘로드", "자기계발", "https://placehold.co/200x280/3c5c3c/ffffff?text=Miracle+Morning", 135),
        ("퓨처 셀프", "벤저민 하디", "자기계발", "https://placehold.co/200x280/4c5c3c/ffffff?text=Future+Self", 118),
        ("시작의 기술", "개리 비숍", "자기계발", "https://placehold.co/200x280/5c5c3c/ffffff?text=Unfu%2Ak+Yourself", 95),
        ("신경 끄기의 기술", "마크 맨슨", "자기계발", "https://placehold.co/200x280/6c5c3c/ffffff?text=Subtle+Art", 128),
        ("킵고잉", "신사임당", "자기계발", "https://placehold.co/200x280/7c5c3c/ffffff?text=Keep+Going", 84),
        ("끝까지 해내는 힘", "성공 연구소", "자기계발", "https://placehold.co/200x280/8c5c3c/ffffff?text=Perseverance", 72),
        ("백만장자 메신저", "브렌든 버처드", "자기계발", "https://placehold.co/200x280/9c5c3c/ffffff?text=Messenger", 66),
        ("하버드 첫날 밤에 가르쳐준 것들", "하버드 에세이", "자기계발", "https://placehold.co/200x280/ac5c3c/ffffff?text=Harvard+Night", 59),
        ("말투 하나 바꿨을 뿐인데", "나이토 요시히토", "자기계발", "https://placehold.co/200x280/bc5c3c/ffffff?text=Speaking+Way", 77),
        ("정리하는 뇌", "대니얼 레비틴", "자기계발", "https://placehold.co/200x280/cc5c3c/ffffff?text=Organized+Mind", 143),

        # 인문/사회 (20권)
        ("사피엔스", "유발 하라리", "인문/사회", "https://placehold.co/200x280/5c3c1c/ffffff?text=Sapiens", 185),
        ("정의란 무엇인가", "마이클 샌델", "인문/사회", "https://placehold.co/200x280/1c2c5c/ffffff?text=What+Is+Justice", 160),
        ("코스모스", "칼 세이건", "인문/사회", "https://placehold.co/200x280/1c1c3c/ffffff?text=Cosmos", 142),
        ("총 균 쇠", "재레드 다이아몬드", "인문/사회", "https://placehold.co/200x280/3c4c2c/ffffff?text=Guns+Germs+Steel", 120),
        ("공정하다는 착각", "마이클 샌델", "인문/사회", "https://placehold.co/200x280/2c1c3c/ffffff?text=Tyranny+of+Merit", 98),
        ("설민석의 조선왕조실록", "설민석", "인문/사회", "https://placehold.co/200x280/5c1c2c/ffffff?text=Chosun+Dynasty", 135),
        ("역사의 쓸모", "최태성", "인문/사회", "https://placehold.co/200x280/4c3c1c/ffffff?text=Use+of+History", 110),
        ("도파민네이션", "애나 렘키", "인문/사회", "https://placehold.co/200x280/3c5c5c/ffffff?text=Dopaminnation", 148),
        ("지적 대화를 위한 넓고 얕은 지식 1", "채사장", "인문/사회", "https://placehold.co/200x280/2c2c3c/ffffff?text=Broad+Knowledge", 155),
        ("이기적 유전자", "리처드 도킨스", "인문/사회", "https://placehold.co/200x280/1c4c4c/ffffff?text=Selfish+Gene", 118),
        ("지적 대화를 위한 넓고 얕은 지식 2", "채사장", "인문/사회", "https://placehold.co/200x280/3c2c3c/ffffff?text=Broad+Knowledge+2", 122),
        ("호모 데우스", "유발 하라리", "인문/사회", "https://placehold.co/200x280/4c2c3c/ffffff?text=Homo+Deus", 113),
        ("21세기를 위한 21가지 제언", "유발 하라리", "인문/사회", "https://placehold.co/200x280/5c2c3c/ffffff?text=21+Lessons", 92),
        ("축의 시대", "카렌 암스트롱", "인문/사회", "https://placehold.co/200x280/6c2c3c/ffffff?text=Axial+Age", 71),
        ("역사란 무엇인가", "E.H. 카", "인문/사회", "https://placehold.co/200x280/7c2c3c/ffffff?text=What+Is+History", 86),
        ("자유론", "존 스튜어트 밀", "인문/사회", "https://placehold.co/200x280/8c2c3c/ffffff?text=On+Liberty", 69),
        ("소크라테스 익스프레스", "에릭 와이너", "인문/사회", "https://placehold.co/200x280/9c2c3c/ffffff?text=Socrates", 104),
        ("생각의 역사", "피터 왓슨", "인문/사회", "https://placehold.co/200x280/ac2c3c/ffffff?text=Idea+History", 80),
        ("국가란 무엇인가", "유시민", "인문/사회", "https://placehold.co/200x280/bc2c3c/ffffff?text=What+Is+State", 97),
        ("문명과 전쟁", "아자 가트", "인문/사회", "https://placehold.co/200x280/cc2c3c/ffffff?text=Civilization+War", 78),

        # IT/과학 (20권)
        ("클린 코드(Clean Code)", "로버트 C. 마틴", "IT/과학", "assets/clean_code_cover.png", 210),
        ("데이터 지향 애플리케이션 설계", "마틴 클레프만", "IT/과학", "assets/data_intensive_cover.png", 195),
        ("파이썬 알고리즘 인터뷰", "박상길", "IT/과학", "https://placehold.co/200x280/0f2d1e/ffffff?text=Python+Algo", 175),
        ("가상 면접 사례로 배우는 대규모 시스템 설계 기초", "알렉스 쉬", "IT/과학", "https://placehold.co/200x280/203c20/ffffff?text=System+Design", 188),
        ("Do it! 점프 투 파이썬", "박응용", "IT/과학", "https://placehold.co/200x280/3c4c2c/ffffff?text=Jump+To+Python", 240),
        ("밑바닥부터 시작하는 딥러닝", "사이토 고키", "IT/과학", "https://placehold.co/200x280/1c3c2c/ffffff?text=Deep+Learning", 150),
        ("혼자 공부하는 머신러닝+딥러닝", "박해선", "IT/과학", "https://placehold.co/200x280/2c3c4c/ffffff?text=HonGong+ML", 130),
        ("토비의 스프링 3.1", "이일민", "IT/과학", "https://placehold.co/200x280/4c3c2c/ffffff?text=Toby+Spring", 85),
        ("쿠버네티스 입문", "동욱", "IT/과학", "https://placehold.co/200x280/1c2c3c/ffffff?text=Kubernetes", 78),
        ("디자인 패턴: 재사용성을 높이는 객체지향 소프트웨어 핵심 요소", "에릭 감마", "IT/과학", "https://placehold.co/200x280/2c1c2c/ffffff?text=Design+Patterns", 95),
        ("쉽게 배우는 운영체제", "조성호", "IT/과학", "https://placehold.co/200x280/3c1c2c/ffffff?text=Operating+System", 102),
        ("이것이 코딩 테스트다", "나동빈", "IT/과학", "https://placehold.co/200x280/1c4c3c/ffffff?text=Coding+Test", 168),
        ("HTTP 완벽 가이드", "데이빗 고를리", "IT/과학", "https://placehold.co/200x280/2c2c4c/ffffff?text=HTTP+Guide", 74),
        ("모던 자바스크립트 Deep Dive", "이웅모", "IT/과학", "https://placehold.co/200x280/3c3c4c/ffffff?text=JS+Deep+Dive", 145),
        ("윤성우의 열혈 C 프로그래밍", "윤성우", "IT/과학", "https://placehold.co/200x280/4c4c4c/ffffff?text=C+Programming", 135),
        ("클린 아키텍처", "로버트 C. 마틴", "IT/과학", "https://placehold.co/200x280/5c5c5c/ffffff?text=Clean+Arch", 152),
        ("리팩터링 2판", "마틴 파울러", "IT/과학", "https://placehold.co/200x280/6c6c6c/ffffff?text=Refactoring", 118),
        ("쏙쏙 들어오는 함수형 코딩", "에릭 노먼", "IT/과학", "https://placehold.co/200x280/7c7c7c/ffffff?text=Functional", 84),
        ("스프링 입문", "최범균", "IT/과학", "https://placehold.co/200x280/8c8c8c/ffffff?text=Spring+Intro", 92),
        ("Rust 프로그래밍 공식 가이드", "스티브 클라브닉", "IT/과학", "https://placehold.co/200x280/9c9c9c/ffffff?text=Rust+Guide", 70)
    ]
    df = pd.DataFrame(books, columns=['도서명', '저자', '장르', '표지URL', '대출횟수'])
    
    np.random.seed(42)
    locations = ['중앙도서관 3층 과학기술실', '제1학술정보관 2층', '대학원도서관 2층', 'IT융합학부 자료실']
    df['청구기호'] = [f"{100 + idx:03d}.{idx}-홍{idx}ㅎ" for idx in range(len(df))]
    df['소장처'] = np.random.choice(locations, size=len(df))
    
    status_choices = ['대출가능', '대출중']
    df['상태'] = np.random.choice(status_choices, size=len(df), p=[0.8, 0.2])
    return df

df_books = load_bestsellers_db()

# 스크롤과 무관하게 고정되어 상단 대출 랭킹으로 스크롤 이동시켜주는 플로팅 미니 버튼 생성
st.markdown("""
    <div id="top-section"></div>
    <a href="#top-section" class="floating-btn-up">▲ 맨 위로 이동</a>
    <a href="#top10-section" class="floating-btn">▼ 대출 top10 도서</a>
""", unsafe_allow_html=True)

# --- 상단 헤더 영역 ---
st.markdown(f"""
    <div class="hongik-header" style="display: flex; justify-content: space-between; align-items: flex-end; padding: 1.5rem 2rem; margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 3rem;">🏛️</span>
            <div>
                <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; color: white !important;">HONGIK UNIVERSITY Personal LIBRARY</h1>
                <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.75); font-size: 0.95rem;">
                    홍익대학교 중앙도서관 연동형 <strong style="font-size: 1.55rem; color: #fbbf24; font-weight: 800;">{st.session_state['user_name']}</strong>의 개인 도서관 서버
                </p>
            </div>
        </div>
        <div class="logout-btn-wrapper">
""", unsafe_allow_html=True)

if st.button("로그아웃", key="header_logout"):
    st.session_state['logged_in'] = False
    st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# --- 메인 탭 구조 ---
tab1, tab2 = st.tabs([
    "🔍 통합 검색 & 대출 순위", 
    "👤 내 대출 서재 & AI 추천"
])

# --- TAB 1: 통합 검색 & 대출 순위 랭킹 ---
with tab1:
    st.markdown("### 🔍 도서 통합 검색")
    
    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ""
    if 'selected_genre' not in st.session_state:
        st.session_state['selected_genre'] = "전체"
        
    typed_query = st.text_input("도서명 또는 저자를 입력하세요 (자동 연관검색 지원)", value=st.session_state['search_query'], placeholder="예: 해리포터, 클린 코드, 유발 하라리")
    
    # 연관검색어 기능 (실시간 매칭 필터링)
    if typed_query:
        matches = df_books[
            df_books['도서명'].str.contains(typed_query, case=False) |
            df_books['저자'].str.contains(typed_query, case=False)
        ]
        if not matches.empty:
            st.markdown("<span style='font-size: 0.85rem; color:#A50034; font-weight: 700;'>💡 연관 도서 추천 (클릭 시 자동 완성 검색):</span>", unsafe_allow_html=True)
            cols = st.columns(min(len(matches), 5))
            for idx, row in matches.head(5).iterrows():
                with cols[idx % len(cols)]:
                    if st.button(row['도서명'], key=f"sug_{idx}"):
                        st.session_state['search_query'] = row['도서명']
                        st.rerun()

    # 장르별 빠른 검색 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 🏷️ 장르별 신속 검색")
    genres_list = ["전체", "소설", "경영/경제", "자기계발", "인문/사회", "IT/과학"]
    
    g_cols = st.columns(len(genres_list))
    for idx, g in enumerate(genres_list):
        with g_cols[idx]:
            btn_style = "primary" if st.session_state['selected_genre'] == g else "secondary"
            if st.button(g, key=f"genre_btn_{g}", use_container_width=True, type=btn_style):
                st.session_state['selected_genre'] = g
                st.rerun()

    df_filtered = df_books.copy()
    if st.session_state['selected_genre'] != "전체":
        df_filtered = df_filtered[df_filtered['장르'] == st.session_state['selected_genre']]
        
    search_term = st.session_state['search_query'] if st.session_state['search_query'] else typed_query
    if search_term:
        df_filtered = df_filtered[
            df_filtered['도서명'].str.contains(search_term, case=False) |
            df_filtered['저자'].str.contains(search_term, case=False)
        ]
        
    if search_term or st.session_state['selected_genre'] != "전체":
        if st.button("🔄 검색 조건 초기화"):
            st.session_state['search_query'] = ""
            st.session_state['selected_genre'] = "전체"
            st.rerun()

    st.markdown(f"##### 📚 검색 도서 목록 (필터 적용: {st.session_state['selected_genre']} / 결과: {len(df_filtered)}건)")
    if not df_filtered.empty:
        col_count = 4
        for r_idx in range(0, len(df_filtered), col_count):
            cols = st.columns(col_count, gap="medium")
            for c_idx, col in enumerate(cols):
                book_idx = r_idx + c_idx
                if book_idx < len(df_filtered):
                    row = df_filtered.iloc[book_idx]
                    status_badge = f"<span style='background-color:#198754; color:white; padding:2px 6px; border-radius:4px; font-size:0.75rem;'>{row['상태']}</span>" if row['상태'] == '대출가능' else f"<span style='background-color:#dc3545; color:white; padding:2px 6px; border-radius:4px; font-size:0.75rem;'>{row['상태']}</span>"
                    
                    with col:
                        st.markdown(f"""
                        <div class="custom-card" style="min-height: 440px; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <div style="display: flex; justify-content: center; margin-bottom: 0.8rem;">
                                    <img src="{row['표지URL']}" style="width: 130px; height: 180px; object-fit: cover; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
                                </div>
                                <span class="genre-badge" style="background-color: #002C6C;">{row['장르']}</span>
                                {status_badge}
                                <h5 style="margin: 8px 0 4px 0; font-size: 1.05rem; font-weight: 700; line-height: 1.3; color:#002C6C !important;">{row['도서명']}</h5>
                                <p style="margin: 0; font-size: 0.82rem; color: #6c757d;">✍️ 저자: {row['저자']}</p>
                            </div>
                            <div style="margin-top: 10px; border-top: 1px solid #eee; padding-top: 8px; font-size: 0.78rem; color:#495057;">
                                📍 청구기호: {row['청구기호']}<br>
                                🏢 소장처: {row['소장처']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("검색 조건에 맞는 도서가 존재하지 않습니다. 다른 검색어로 테스트해 보십시오.")

    st.markdown("---")
    
    st.markdown('<div id="top10-section"></div>', unsafe_allow_html=True)
    st.markdown("### 🏆 중앙도서관 종합 대출 랭킹 (Top 10)")
    df_ranking = df_books.sort_values(by="대출횟수", ascending=False).head(10).copy()
    df_ranking.insert(0, '순위', range(1, 11))
    
    st.dataframe(
        df_ranking[['순위', '도서명', '저자', '장르', '대출횟수', '상태']], 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "순위": st.column_config.NumberColumn("🥇 순위", format="%d"),
            "도서명": st.column_config.TextColumn("📖 도서명", width="large"),
            "저자": st.column_config.TextColumn("✍️ 저자"),
            "장르": st.column_config.TextColumn("🏷️ 장르"),
            "대출횟수": st.column_config.NumberColumn("📈 누적 대출수", format="%d회"),
            "상태": st.column_config.TextColumn("✅ 상태")
        }
    )


# --- TAB 2: 내 대출 서재 & AI 추천 도서 ---
with tab2:
    # 기획 요구사항 반영: '홍익대학교 구성원 정보' -> '나의 정보', 대출등급 열 삭제
    st.markdown("### 👤 나의 정보")
    
    user_info = pd.DataFrame({
        '항목': ['성명', '학번', '소속 학과', '이메일 주소'],
        '정보': [
            st.session_state['user_name'], 
            st.session_state['user_id'], 
            st.session_state['user_dept'], 
            st.session_state['user_email']
        ]
    })
    
    col_u1, col_u2 = st.columns([2, 1])
    with col_u1:
        st.dataframe(user_info, use_container_width=True, hide_index=True)
    with col_u2:
        # 로그인 사용자에 맞춰 대출 건수 다르게 표기 가능하도록 설정
        borrowed_count = 3 if st.session_state['user_name'] == "조현준" else (2 if st.session_state['user_name'] == "홍길동" else 1)
        st.markdown(f"""
        <div style="background-color: white; border: 1px solid #dee2e6; border-top: 4px solid #002C6C; border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="font-size: 0.95rem; color: #6c757d; font-weight: 700; margin-bottom: 8px;">현재 대출 상태</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #002C6C;">
                {borrowed_count}권
            </div>
            <div style="font-size: 1.3rem; color: #A50034; font-weight: 700; margin-top: 6px;">
                ({borrowed_count}/5권 대출중)
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📋 나의 현재 대출 도서 현황")
    
    # 로그인한 계정에 따라 가상 대출 목록 다르게 설정
    if st.session_state['user_name'] == "조현준":
        my_loans = pd.DataFrame({
            '도서명': ['파이썬 알고리즘 인터뷰', '가상 면접 사례로 배우는 대규모 시스템 설계 기초', '아주 작은 습관의 힘'],
            '저자': ['박상길', '알렉스 쉬', '제임스 클리어'],
            '대출일자': ['2026-06-01', '2026-05-28', '2026-06-03'],
            '반납기한': ['2026-06-15', '2026-06-11', '2026-06-17'],
            '연장가능여부': ['연장가능', '연장불가 (1회 연장완료)', '연장가능']
        })
    elif st.session_state['user_name'] == "홍길동":
        my_loans = pd.DataFrame({
            '도서명': ['트렌드 코리아 2026', '부자 아빠 가난한 아빠'],
            '저자': ['김난도', '로버트 기요사키'],
            '대출일자': ['2026-06-02', '2026-06-05'],
            '반납기한': ['2026-06-16', '2026-06-19'],
            '연장가능여부': ['연장가능', '연장가능']
        })
    else:
        my_loans = pd.DataFrame({
            '도서명': ['불편한 편의점'],
            '저자': ['김호연'],
            '대출일자': ['2026-06-07'],
            '반납기한': ['2026-06-21'],
            '연장가능여부': ['연장가능']
        })
    
    st.dataframe(
        my_loans, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "도서명": st.column_config.TextColumn("📖 대출 도서명", width="large"),
            "저자": st.column_config.TextColumn("✍️ 저자"),
            "대출일자": st.column_config.TextColumn("📅 대출일"),
            "반납기한": st.column_config.TextColumn("🚨 반납예정일"),
            "연장가능여부": st.column_config.TextColumn("🔄 연장 여부")
        }
    )

    st.markdown("---")
    
    # 빅데이터 & AI 맞춤형 도서 추천 영역 (로그인 사용자에 맞게 문구 변경)
    st.markdown(f"### 🎯 {st.session_state['user_name']} 님을 위한 빅데이터 기반 개인화 도서 추천")
    
    # 사용자별 선호 장르 텍스트 동적 변경
    if st.session_state['user_name'] == "조현준":
        genre_desc = "IT 기술서적 67%, 자기계발 33%"
        rec_intro = "최근 대출하신 전공 개발 도서와 인문 습관 서적을 융합 분석하여 조현준 님께 이 책들을 추천해요!"
    elif st.session_state['user_name'] == "홍길동":
        genre_desc = "경영/경제 100%"
        rec_intro = "경제학과 학과 트렌드 및 대출하신 자산 관리 서적을 연계 분석하여 홍길동 님께 이 책들을 추천해요!"
    else:
        genre_desc = "교양 소설 100%"
        rec_intro = f"대출하신 문학 도서 및 라이브러리 베스트셀러를 융합 분석하여 {st.session_state['user_name']} 님께 이 책들을 추천해요!"

    st.markdown(f"""
        <p style='color:#6c757d; font-size:0.92rem; margin-top:-0.5rem; font-weight:700;'>
            📢 "{rec_intro}"
        </p>
        <p style='color:#888; font-size:0.8rem; margin-top:-0.5rem;'>
            분석 카테고리 선호도: {genre_desc}
        </p>
    """, unsafe_allow_html=True)
    
    rec_cols2 = st.columns(3)
    
    # 조현준과 홍길동, 일반 사용자의 추천 풀 변경
    if st.session_state['user_name'] == "홍길동":
        rec_data = [
            {
                "title": "돈의 속성",
                "author": "김승호 | 스노우폭스북스",
                "image": "https://placehold.co/200x280/1c5a2c/ffffff?text=Money+Rules",
                "badge": "📈 경제 최적화",
                "reason": "대출하신 <strong>'부자 아빠 가난한 아빠'</strong>의 투자 철학과 연계하여, 실제 자산 운용가로서의 돈에 대한 태도와 경영 철학을 정립할 수 있는 최고의 지침서로 추천합니다."
            },
            {
                "title": "원칙",
                "author": "레이 달리오 | 한빛비즈",
                "image": "https://placehold.co/200x280/4c4c4c/ffffff?text=Principles",
                "badge": "💼 의사결정 모델",
                "reason": "경제학도로서 거시경쟁적 지표 분석 및 비즈니스 결정 원칙을 체계적으로 도식화한 거장 레이 달리오의 베스트셀러입니다."
            },
            {
                "title": "사피엔스",
                "author": "유발 하라리 | 김영사",
                "image": "https://placehold.co/200x280/5c3c1c/ffffff?text=Sapiens",
                "badge": "🏛️ 인문 융합 추천",
                "reason": "중앙도서관 경제/인문 분야 최다 대출 2위로, 화폐의 역사와 인류가 만든 신용(Credit)의 기원을 이해하기 위한 필독 인문 서적입니다."
            }
        ]
    else:
        # 조현준 및 기본 추천 풀
        rec_data = [
            {
                "title": "데이터 지향 애플리케이션 설계",
                "author": "마틴 클레프만 | 위키북스",
                "image": "assets/data_intensive_cover.png",
                "badge": "💡 기술 연계 추천",
                "reason": f"최근 대출하신 IT 아카이빙을 분석한 결과, 대규모 시스템의 백엔드 분산 아키텍처와 분산 데이터 모델의 물리 구조를 심도 있게 학습할 수 있는 {st.session_state['user_dept']} 전공 심화 필독서로 추천합니다."
            },
            {
                "title": "클린 코드(Clean Code)",
                "author": "로버트 C. 마틴 | 인사이트",
                "image": "assets/clean_code_cover.png",
                "badge": "🚀 역량 강화",
                "reason": f"{st.session_state['user_dept']} 전공 과정의 코딩 최적화를 돕기 위해, 전공자 최다 대출 도서이자 실무형 테스트와 클린 아키텍처 설계를 설계하는 법을 담은 바이블을 선정했습니다."
            },
            {
                "title": "트렌드 코리아 2026",
                "author": "김난도 | 미래의창",
                "image": "https://placehold.co/200x280/6c1c24/ffffff?text=Trend+Korea",
                "badge": "📈 융합 트렌드 추천",
                "reason": "중앙도서관 경제/경영 카테고리 최다 대출 1위 도서로, 산업 데이터 동향을 마케팅/기술 인프라 트렌드 관점에서 연계 분석할 수 있는 시야를 넓혀줄 것입니다."
            }
        ]

    for idx, col in enumerate(rec_cols2):
        rec = rec_data[idx]
        with col:
            st.markdown(f"""
            <div style="background-color: white; border: 1px solid #dee2e6; border-radius: 12px; padding: 1.25rem; height: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.06); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="text-align: center; margin-bottom: 0.8rem;">
                        <span style="background-color: #A50034; color: white; font-size: 0.72rem; font-weight: 700; padding: 4px 10px; border-radius: 20px;">
                            {rec['badge']}
                        </span>
                    </div>
                    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
                        <img src="{rec['image']}" style="width: 140px; height: 190px; object-fit: cover; border-radius: 6px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
                    </div>
                    <h5 style="text-align: center; margin: 0 0 4px 0; font-size: 1.05rem; font-weight: 700; color: #002C6C !important;">{rec['title']}</h5>
                    <p style="text-align: center; margin: 0 0 10px 0; font-size: 0.8rem; color: #6c757d;">✍️ {rec['author']}</p>
                </div>
                <div style="background-color: #f8f9fa; border-radius: 8px; padding: 0.75rem; font-size: 0.82rem; color: #495057; line-height: 1.45; border-left: 3px solid #A50034; min-height: 110px;">
                    💡 <strong>추천 사유:</strong><br>
                    {rec['reason']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- 하단 푸터 ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align: center; color: #6c757d; font-size: 0.8rem; padding: 1.5rem 0; border-top: 1px solid #dee2e6;">
        © 2026 홍익대학교 중앙도서관 · {st.session_state['user_name']}의 개인 도서관 서버<br>
        본 사이트는 교육 및 데모 연구용으로 제작되었습니다.
    </div>
""", unsafe_allow_html=True)
