import streamlit as st
from datetime import datetime

# 1. 設定版面
st.set_page_config(page_title="山海圳日記", page_icon="⛰️", layout="centered")
st.title("⛰️ 山海圳・行腳動態牆")

# --- 這是「暫存記憶體」的設定 ---
# 為了讓妳按按鈕後，舊的資料不會消失，要把它們存在 session_state 裡
if 'logs' not in st.session_state:
    st.session_state.logs = []

# ==========================================
#  輸入區 (Input Area)
# ==========================================
with st.container(border=True):
    st.subheader("📝 新增一筆紀錄")
    
    # 時間與地點
    current_time = datetime.now().strftime("%m/%d %H:%M")
    day_select = st.selectbox("目前進度", ["Day 1", "Day 2", "Day 3", "Day 4"])
    location = st.text_input("📍 地點", placeholder="例如：特富野古道 (可按鍵盤麥克風輸入)")
    
    # 心得文字 (用手機鍵盤麥克風輸入最快！)
    note = st.text_area("💬 心得筆記", placeholder="點擊手機鍵盤上的麥克風，直接把話轉成字...")

    # 多媒體輸入
    col1, col2 = st.columns(2)
    with col1:
        photo = st.camera_input("📸 拍一張")
    with col2:
        audio = st.audio_input("🎤 錄環境音")

    # === 送出按鈕 ===
    if st.button("➕ 加入動態牆", type="primary"):
        if location or photo or audio or note:
            # 把所有資料打包成一個「包裹 (Dictionary)」
            new_log = {
                "time": current_time,
                "day": day_select,
                "location": location,
                "note": note,
                "photo": photo,
                "audio": audio
            }
            # 塞進記憶體的第一個位置 (最新的在最上面)
            st.session_state.logs.insert(0, new_log)
            st.success("已新增！往下看 ↓")
        else:
            st.warning("請至少輸入一點內容喔！")

st.divider()

# ==========================================
#  展示區 (Display Area) - 這就是妳要的「並列」
# ==========================================
st.subheader("📅 旅程回顧")

if not st.session_state.logs:
    st.info("目前還沒有紀錄，快去上面新增第一筆吧！")

# 這裡用迴圈，把每一筆資料畫出來
for log in st.session_state.logs:
    with st.container(border=True):
        # 標題列：時間 + 地點
        st.markdown(f"### {log['day']} | {log['location']}")
        st.caption(f"🕒 {log['time']}")
        
        # 內容區
        if log['note']:
            st.info(f"💬 {log['note']}")
            
        # 影像與聲音並列
        if log['photo']:
            st.image(log['photo'])
            
        if log['audio']:
            st.write("🎵 環境錄音：")
            st.audio(log['audio'])
