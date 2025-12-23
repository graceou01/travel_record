import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 手機版面設定 (讓網頁在手機上看起來像 App)
st.set_page_config(page_title="山海圳日記", page_icon="⛰️", layout="centered")

# 標題與當下時間
st.title("⛰️ 山海圳・行腳記錄")
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
st.caption(f"📅 現在時間：{current_time}")

# 2. 只有一個簡單的問題：現在在哪？
day_select = st.selectbox("行程進度", ["Day 1: 內海到大圳", "Day 2: 大圳到原鄉", "Day 3: 原鄉到聖山", "Day 4: 聖山攻頂"], index=0)
location_note = st.text_input("📍 地標/位置 (例如：曾文水庫)", placeholder="輸入地標...")

# 3. 核心功能：語音筆記 (Streamlit 新功能！)
# 累的時候用講的，不用打字
audio_value = st.audio_input("🎤 錄下妳的心情")

if audio_value:
    st.success("收到語音筆記！(回來後可用 AI 轉成文字)")

# 4. 核心功能：拍照 (直接呼叫手機相機)
img_file = st.camera_input("📸 拍一張當下")

# 5. 情緒大按鈕 (直覺紀錄)
mood = st.radio("😤 現在的體感指數", ["超爽", "微累", "快掛了", "腳要在地上拖了"], horizontal=True)

st.divider()

# 6. 產生「日記卡片」區 (這區是為了讓妳截圖用的)
# 因為山上訊號不好，連資料庫太慢，直接把結果秀出來讓妳截圖最保險
if img_file or audio_value or location_note:
    st.markdown("### 📸 截圖保存區")
    st.info("💡 因山區訊號不穩，建議直接截圖這張卡片保存！")
    
    with st.container(border=True):
        st.write(f"**{day_select}** | {current_time}")
        st.write(f"📍 {location_note} | 體感：{mood}")
        
        if img_file:
            st.image(img_file)
            
        if audio_value:
            st.write("🎵 (已附上語音檔)")
            
# 7. (進階) 臨時暫存按鈕
# 這會把資料變成一個 CSV 讓妳下載，但手機操作可能沒截圖快
if st.button("📥 下載本次紀錄 (CSV)"):
    # 這裡做一個簡單的 DataFrame 範例
    data = {
        "Time": [current_time],
        "Day": [day_select],
        "Location": [location_note],
        "Mood": [mood]
    }
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    
    st.download_button(
        "點我儲存檔案",
        csv,
        "shanhai_log.csv",
        "text/csv",
        key='download-csv'
    )
