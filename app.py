# ==========================================
#  在最下面加上這段：強力 ZIP 打包下載區
# ==========================================
import zipfile
import io

st.divider()
st.subheader("📥 超級備份 (文字+照片)")

if st.session_state.logs:
    # 1. 準備一個記憶體裡的 ZIP 檔
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # A. 處理文字檔 (CSV)
        df = pd.DataFrame(st.session_state.logs)
        # 只留文字欄位轉 CSV
        csv_data = df.drop(columns=['photo', 'audio']).to_csv(index=False).encode('utf-8-sig')
        zf.writestr("trip_log.csv", csv_data)
        
        # B. 處理每一張照片
        for i, log in enumerate(st.session_state.logs):
            if log['photo']:
                # 幫照片取名：DayX_地點_編號.jpg
                img_name = f"{log['day']}_{log['location']}_{i}.jpg"
                # 把照片的內容讀出來，寫入 ZIP
                zf.writestr(img_name, log['photo'].getvalue())
                
            # (進階) 如果想連錄音檔都打包，可以把下面這兩行 # 拿掉
            # if log['audio']:
            #     audio_name = f"{log['day']}_{log['location']}_{i}.wav"
            #     zf.writestr(audio_name, log['audio'].getvalue())

    # 2. 完成打包，準備下載
    st.download_button(
        label="📦 點我打包下載 (ZIP壓縮檔)",
        data=zip_buffer.getvalue(),
        file_name="山海圳全紀錄.zip",
        mime="application/zip",
        type="primary"  # 讓按鈕變顯眼的紅色
    )
    
    st.caption("💡 下載後，在手機「檔案」App 點一下該檔案就會自動解壓縮囉！")

else:
    st.write("目前沒有資料可以打包")
