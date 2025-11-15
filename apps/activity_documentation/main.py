import streamlit as st
from .services.upload_service import UploadService
from .ui.upload_form import render_upload_form
from .config import GAS_WEBAPP_URL
from .utils.state_utils import reset_upload_state
from .ui.gallery_ui import show_gallery
from auth import require_login

def run():
    st.set_page_config(page_title="KT. RW2 PEKUNDEN", layout="centered")
    st.title("📁 Dokumentasi Kegiatan")

    tab_gallery, tab_upload = st.tabs(["📸 Lihat Dokumentasi", "📤 Upload Dokumentasi"])

    upload_service = UploadService(GAS_WEBAPP_URL)

    with tab_gallery:
        show_gallery()

    with tab_upload:
        if require_login():
            st.session_state.setdefault("is_processing", False)
            st.session_state.setdefault("form_data", None)

            if not st.session_state.is_processing:
                form = render_upload_form()

                if form:
                    st.session_state.form_data = form
                    st.session_state.is_processing = True
                    st.rerun()

            if st.session_state.is_processing and st.session_state.form_data:
                with st.spinner("⏳ Mengupload... Harap tunggu..."):
                    try:
                        data = st.session_state.form_data
                        progress = st.progress(0)
                        status = st.empty()

                        link = upload_service.upload_photos(
                            data["activity_name"],
                            data["meeting_date"],
                            data["photos"],
                            progress,
                            status
                        )

                        progress.progress(1.0)
                        status.empty()

                        st.success("✅ Semua foto berhasil diupload!")
                        st.balloons()
                        st.write("📂 Folder Dokumentasi Google Drive:")
                        st.write(link)

                        reset_upload_state()

                    except Exception as e:
                        st.error(f"❌ Error: {e}")
                        reset_upload_state()