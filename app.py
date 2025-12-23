import streamlit as st
from datetime import datetime

# 1. 版面設定
st.set_page_config(page_title="山海圳日記", page_icon="⛰️", layout="centered")
st.title("⛰️ 山海圳・行腳記錄")

# 2. 顯示現在時間
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
st.caption(f"📅 時間：{current_time}")

# 3. 選單與文字
day_select = st.selectbox("行程", ["Day 1: 內海-大圳", "Day 2: 大圳-原鄉", "Day 3: 原鄉-聖山", "Day 4: 聖山攻頂"])
location = st.text_input("📍 地點", placeholder="例如：曾文水庫")

st.divider()

# --- 關鍵修正區：語音 ---
st.subheader("1. 語音筆記")
audio_data = st.audio_input("🎤 按下錄音")

if audio_data:
    # 修正 A: 讓妳可以立刻聽
    st.audio(audio_data) 
    # 修正 B: 直接給妳下載按鈕 (存到手機檔案夾)
    st.download_button(
        label="💾 下載這個錄音檔 (WAV)",
        data=audio_data,
        file_name=f"voice_{current_time.replace(':','')}.wav",
        mime="audio/wav"
    )

st.divider()

# --- 關鍵修正區：照片 ---
st.subheader("2. 現場照片")
photo_data = st.camera_input("📸 拍照")

if photo_data:
    # 修正 C: 給妳下載按鈕 (存到手機相簿/檔案夾)
    st.download_button(
        label="💾 下載這張照片 (JPG)",
        data=photo_data,
        file_name=f"photo_{current_time.replace(':','')}.jpg",
        mime="image/jpeg"
    )

st.divider()

# --- 截圖保存區 (最後一道防線) ---
if location or audio_data or photo_data:
    with st.container(border=True):
        st.write(f"**{day_select}** | {location}")
        if audio_data: st.info("🎵 語音已錄製")
        if photo_data: st.image(photo_data)
        st.caption("💡 建議直接「截圖」這張卡片最快！")
