import streamlit as st
import pandas as pd

def display_meeting_history(worksheet):    
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    
    if not df.empty:
        df.columns = df.columns.str.strip().str.upper()
        df = df.sort_values(by='TANGGAL', ascending=False)
        
        for i, row in df.iterrows():
            with st.expander(f"📅 {row['TANGGAL']} | ⏰ {row['WAKTU MULAI']} - {row['WAKTU SELESAI']}"):
                st.markdown(f"**🗒️ Notulen:**\n{row['NOTULEN']}")
                
                if isinstance(row.get("LINK DOKUMENTASI"), str) and row["LINK DOKUMENTASI"].strip():
                    st.markdown(f"**📸 Dokumentasi:** [Buka Folder Foto]({row['LINK DOKUMENTASI']})")
    else:
        st.info("Belum ada notulen yang disimpan.")