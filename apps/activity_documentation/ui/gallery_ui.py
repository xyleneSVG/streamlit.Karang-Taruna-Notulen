import streamlit as st
from ..services.gallery_service import GalleryService
from ..config import GAS_WEBAPP_URL
from ..utils.parse_folder import parse_folder_name

def show_gallery():
    service = GalleryService(GAS_WEBAPP_URL)

    try:
        folders_data = service.list_folders()
    except Exception as e:
        st.error(f"Error memuat folder: {e}")
        return

    if folders_data["status"] != "success" or folders_data["count"] == 0:
        st.info("Belum ada dokumentasi kegiatan.")
        return

    folders = folders_data["folders"]

    for folder in folders:
        folder_id = folder["id"]
        folder_name = folder["name"]
        folder_url = folder["url"]

        activity, date = parse_folder_name(folder_name)

        with st.expander(f"📁 {activity} — {date}"):
            st.markdown(f"**📂 Folder Google Drive:** [Buka Folder]({folder_url})")

            try:
                files_data = service.list_files(folder_id)
            except Exception as e:
                st.error(f"Gagal memuat file: {e}")
                continue

            if files_data["status"] != "success" or files_data["count"] == 0:
                st.warning("Tidak ada foto di folder ini.")
                continue

            files = files_data["files"]
            cols = st.columns(3)

            for idx, file in enumerate(files):
                if "image" in file["mimeType"]:
                    with cols[idx % 3]:
                        img_bytes = service.fetch_image_bytes(file["directUrl"])
                        st.image(img_bytes, width='stretch')

                else:
                    st.write(f"📄 File lain: [{file['name']}]({file['url']})")
