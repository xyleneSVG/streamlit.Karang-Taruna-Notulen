from google import genai
from google.genai import types
import streamlit as st

def get_genai_client():
    api_key = st.secrets["google"]["api_key"]
    
    if not api_key:
        raise ValueError(
            "Google API key tidak ditemukan! "
            "Tambahkan ke .streamlit/secrets.toml atau environment variable."
        )
    
    return genai.Client(api_key=api_key)

def formatedWithAI(catatan: str) -> str:
    try:
        client = get_genai_client()
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[catatan],
            config=types.GenerateContentConfig(
                temperature=0.7,
                system_instruction="""
Kamu adalah asisten yang merapikan notulen rapat.

TUGAS:
1) Rapikan isi notulen
2) Format jadi poin-poin yang jelas
3) Jangan berikan pembuka atau judul
4) Keluarkan hanya isi notulen dalam bentuk poin
5) Jangan terlalu banyak mengubah notulennya sehingga menciptakan perbedaan maksud
6) Gunakan bullet points (•) atau numbering yang rapi

CONTOH OUTPUT:
- Pembahasan anggaran Q1 2025
- Tim marketing menyampaikan laporan campaign
- Keputusan: Alokasi budget ditambah 15%
- Action items: Buat proposal detail minggu depan
"""
            )
        )
        return response.text
    except Exception as e:
        st.warning(f"⚠️ AI tidak bisa memproses notulen: {e}")
        return catatan