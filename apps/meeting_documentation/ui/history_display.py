import streamlit as st
import pandas as pd
from ..services.gallery_service import GalleryService
from ..config import GAS_WEBAPP_URL

def display_meeting_history(worksheet):
    service = GalleryService(GAS_WEBAPP_URL)
    
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        st.info("Belum ada notulen yang disimpan.")
        return

    df.columns = df.columns.str.strip().str.upper()
    df = df.sort_values(by='TANGGAL', ascending=False)

    for i, row in df.iterrows():
        with st.expander(f"📅 {row['TANGGAL']} | ⏰ {row['WAKTU MULAI']} - {row['WAKTU SELESAI']}"):
            st.markdown(f"**🗒️ Notulen:**\n{row['NOTULEN']}")

            folder_link = row.get("LINK DOKUMENTASI")
            if isinstance(folder_link, str) and folder_link.strip():
                folder_id = folder_link.split("/")[-1]

                try:
                    files_data = service.list_files(folder_id)
                except Exception as e:
                    st.error(f"Gagal memuat file: {e}")
                    continue

                if files_data["status"] != "success" or files_data["count"] == 0:
                    continue

                st.markdown("**📸 Dokumentasi Foto:**")
                files = files_data["files"]
                cols = st.columns(3)

                for idx, file in enumerate(files):
                    if "image" in file["mimeType"]:
                        with cols[idx % 3]:
                            img_bytes = service.fetch_image_bytes(file["directUrl"])
                            st.image(img_bytes, width='stretch')
                    else:
                        st.write(f"📄 File lain: [{file['name']}]({file['url']})")
