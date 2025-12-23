import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 設定 App 版面
st.set_page_config(page_title="山海圳日記", page_icon="⛰️", layout="centered")

# --- CSS 魔法：強制標題不換行 ---
st.markdown("""
    <style>
    .nowrap-title {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0px;
    }
    </style>
    <div class="nowrap-title">⛰️ 山海圳第一回・行腳記錄</div>
    """, unsafe_allow_html=True)

# 建立背包
if 'logs' not in st.session_state:
    st.session_state['logs'] = []

# --- 2. 行程資訊小抄 (加碼功能) ---
# 把妳提供的詳細資訊藏在這裡，隨時可查
with st.expander("ℹ️ 點我查看：住宿、集合、注意事項"):
    st.markdown("""
    **📅 活動日期：12/25(四) ~ 12/28(日)**
    
    **🚩 集合資訊**
    * 08:00 台南火車站
    * 08:30 山海圳起點

    **🏠 每日行程 & 住宿**
    * **D1 (12/25)**: 內海起點 ➔ 南科 (27k) | 宿: 南科宇田商旅
    * **D2 (12/26)**: 南科 ➔ 烏山頭 (16k) | 宿: 烏山頭飯店
    * **D3 (12/27)**: 烏山頭 ➔ 曾文活動中心 (26k) | 宿: 曾文青年活動中心
    * **D4 (12/28)**: 曾文活動中心 ➔ 曾文水庫 (9k) | 搭船遊湖 (13:30開船)

    **⚠️ 注意事項**
    1. 帶盥洗用品 (牙膏牙刷毛巾)
    2. 保暖衣物、雨衣、頭燈
    3. 備用行動水/糧食
    4. 回程高鐵建議買 18:30 後

    🔗 [Google 地圖請點我](https://goo.gl/maps/dbxW4jsQwgzNqDDk8?g_st=al)
    """)

st.divider()

# --- 3. 輸入區 ---
current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
st.caption(f"📅 現在時間：{current_time}")

# 更新後的行程選單 (依照妳的規劃)
day_options = [
    "D1 (12/25): 內海起點 ➔ 南科 (27k)",
    "D2 (12/26): 南科 ➔ 烏山頭 (16k)",
    "D3 (12/27): 烏山頭 ➔ 曾文中心 (26k)",
    "D4 (12/28): 曾文中心 ➔ 水庫搭船 (9k)"
]
day_select = st.selectbox("📌 目前進度", day_options)

location_note = st.text_input("📍 地標/位置", placeholder="例如：剛過善化啤酒廠...")
mood = st.select_slider("😤 體感指數", options=["超爽", "舒服", "微累", "快掛了", "腳已廢"])
audio_value = st.audio_input("🎤 語音筆記")
img_file = st.camera_input("📸 拍一張當下")

# --- 4. 即時確認與截圖區 ---
if location_note or img_file or audio_value:
    st.markdown("### 📸 預覽確認 (請在此截圖)")
    with st.container(border=True):
        st.markdown(f"**🕒 {current_time}**")
        st.markdown(f"**🚩 {day_select}**")
        st.markdown(f"**📍 地點**：{location_note if location_note else '(未填寫)'}")
        st.markdown(f"**😤 心情**：{mood}")
        
        if img_file:
            st.image(img_file, caption="附圖")
        
        if audio_value:
            st.audio(audio_value)
            st.caption("🎵 語音已錄製")
            
    st.info("👆 確認內容無誤後，建議先截圖，再按下方按鈕儲存。")

# --- 5. 按鈕動作 ---
if st.button("📝 確認無誤，加入紀錄", use_container_width=True, type="primary"):
    new_record = {
        "時間": current_time,
        "行程": day_select,
        "地點": location_note,
        "心情": mood,
        "有照片": "有" if img_file else "無",
        "有錄音": "有" if audio_value else "無"
    }
    st.session_state['logs'].append(new_record)
    st.success("✅ 已成功加入下方清單！")

st.divider()

# --- 6. 歷史清單 ---
st.subheader(f"📋 歷史紀錄 (目前 {len(st.session_state['logs'])} 筆)")

if len(st.session_state['logs']) > 0:
    # 下載按鈕
    df = pd.DataFrame(st.session_state['logs'])
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載所有紀錄 (CSV)",
        data=csv,
        file_name=f"shanhai_log_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # 顯示過往紀錄
    for i, log in enumerate(reversed(st.session_state['logs'])):
        with st.expander(f"#{len(st.session_state['logs'])-i} {log['時間']} @ {log['地點']}"):
            st.write(f"行程: {log['行程']}")
            st.write(f"心情: {log['心情']}")
else:
    st.info("目前還沒有紀錄，準備出發囉！")
