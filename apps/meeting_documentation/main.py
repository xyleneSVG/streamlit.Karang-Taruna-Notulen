import streamlit as st
from .config import get_google_sheets_client, GAS_WEBAPP_URL
from .services import GoogleSheetsService, UploadService
from .ui import render_meeting_form, display_meeting_history
from .utils.ai import formatedWithAI
from .utils.state_utils import reset_processing_state  
from auth import require_login

def run():
    st.set_page_config(page_title="KT. RW2 PEKUNDEN", layout="centered")
    st.title("📝 Notulen Pertemuan")

    tab_gallery, tab_upload = st.tabs(["📚 Riwayat Notulen", "📤 Upload Notulen"])
    
    worksheet = get_google_sheets_client()
    sheets_service = GoogleSheetsService(worksheet)
    upload_service = UploadService(GAS_WEBAPP_URL)
    
    with tab_gallery:
        display_meeting_history(worksheet)
    
    with tab_upload:
        if require_login():
            st.session_state.setdefault("is_processing", False)
            st.session_state.setdefault("form_data", None)

            if not st.session_state.is_processing:
                form_data = render_meeting_form()

                if form_data:
                    st.session_state.form_data = form_data
                    st.session_state.is_processing = True
                    st.rerun()

            if st.session_state.is_processing and st.session_state.form_data:
                with st.spinner("⏳ Sedang memproses... Jangan refresh halaman!"):
                    try:
                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        data = st.session_state.form_data
                        meeting_date_str = data['meeting_date'].strftime("%Y-%m-%d")

                        folder_link = upload_service.upload_photos(
                            data['photo_files'],
                            meeting_date_str,
                            progress_bar,
                            status_text
                        )

                        status_text.info("💬 Memproses notulen dengan AI...")
                        progress_bar.progress(0.90)
                        formatted_notes = formatedWithAI(data['notes'])

                        status_text.info("💾 Menyimpan ke Google Sheet...")
                        progress_bar.progress(0.95)
                        sheets_service.save_meeting_notes(
                            meeting_date_str,
                            data['start_time'],
                            data['end_time'],
                            formatted_notes,
                            folder_link
                        )

                        progress_bar.progress(1.0)
                        progress_bar.empty()
                        status_text.empty()

                        st.success("✅ Notulen berhasil disimpan!")
                        st.balloons()

                        reset_processing_state()

                    except Exception as e:
                        st.error(f"❌ Terjadi kesalahan: {e}")
                        reset_processing_state()


