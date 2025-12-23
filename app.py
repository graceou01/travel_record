import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. 基礎設定
st.set_page_config(page_title="山海圳日記", page_icon="⛰️")
st.title("⛰️ 山海圳・行腳 (安全版)")

# 初始化暫存
if 'logs' not in st.session_state:
    st.session_state.logs = []

# 2. 輸入區
st.header("📝 新增紀錄")

# 時間地點
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
st.write(f"時間：{current_time}")

day_select = st.selectbox("目前進度", ["Day 1", "Day 2", "Day 3", "Day 4"])
location = st.text_input("📍 地點")
note = st.text_area("💬 心得筆記")

# 拍照 (這是最穩定的舊版寫法)
photo = st.camera_input("📸 拍一張")

# 暫時拿掉錄音功能，避免版本錯誤
st.write("---")

if st.button("➕ 加入紀錄"):
    if location or photo or note:
        new_log = {
            "time": current_time,
            "day": day_select,
            "location": location,
            "note": note,
            "photo": photo
        }
        st.session_state.logs.insert(0, new_log)
        st.success("已新增！")
    else:
        st.warning("請輸入內容")

st.write("---")

# 3. 顯示區
st.header("📅 紀錄列表")

if st.session_state.logs:
    for log in st.session_state.logs:
        # 用最簡單的方式顯示，不用 fancy 的容器
        st.markdown(f"### {log['day']} - {log['location']}")
        st.caption(log['time'])
        st.write(log['note'])
        if log['photo']:
            st.image(log['photo'])
        st.write("---")

    # 4. 下載區 (只留 CSV 下載，先確保不會 error)
    # 我們先把 ZIP 拿掉，因為那也需要額外模組，先求有！
    df = pd.DataFrame(st.session_state.logs)
    # 移除照片欄位
    csv_data = df.drop(columns=['photo']).to_csv(index=False).encode('utf-8-sig')
    
    st.download_button(
        label="📥 下載文字紀錄 (CSV)",
        data=csv_data,
        file_name="trip_log.csv",
        mime="text/csv"
    )

else:
    st.write("目前沒有資料")
