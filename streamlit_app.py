# streamlit_app.py

import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
from PIL import Image
import io

# --- Fungsi Helper ---
def get_file_parts(uploaded_file):
    """Mengubah file yang diunggah menjadi format 'parts' yang dimengerti oleh Gemini."""
    if uploaded_file is None:
        return None
    
    file_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type
    
    if mime_type == "application/pdf":
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        parts = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text().strip()
            if page_text:
                parts.append(f"--- Teks dari Halaman PDF {page_num + 1} ---\n{page_text}")
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                parts.append(Image.open(io.BytesIO(image_bytes)))
        return parts
    
    elif mime_type in ["image/jpeg", "image/png"]:
        return [Image.open(uploaded_file)]
        
    elif mime_type == "text/plain":
        return [file_bytes.decode("utf-8")]
        
    return None

# --- Konfigurasi Halaman & Judul ---
st.set_page_config(page_title="Tutor Eureka", page_icon="🤖")
st.title("💬 Tutor Eureka")
st.caption("Asisten belajar cerdas untuk Matematika, Fisika, dan Kimia.")

# --- Sidebar (Panel Kontrol) ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    try:
        google_api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ API Key ditemukan!")
    except (KeyError, FileNotFoundError):
        google_api_key = st.text_input("Gemini API Key", type="password")

    selected_model_name = st.radio(
        "Pilih Model Gemini:",
        ["Gemini 2.5 Flash", "Gemini 2.5 Pro"],
        horizontal=True,
    )
    
    if st.button("🔄 Reset Percakapan", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- Inisialisasi Model & Riwayat Chat ---
if not google_api_key:
    st.info("🗝️ Masukkan Gemini API Key Anda di sidebar untuk memulai.")
    st.stop()

try:
    genai.configure(api_key=google_api_key)
    # --- PERUBAHAN DI SINI ---
    model_id = "gemini-2.5-flash" if selected_model_name == "Gemini 2.5 Flash" else "gemini-2.5-pro"
    # --- AKHIR PERUBAHAN ---
    model = genai.GenerativeModel(model_id)
except Exception as e:
    st.error(f"Gagal mengonfigurasi model: {e}")
    st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- Tampilkan Riwayat Percakapan ---
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- Area Input & Unggah File ---
uploaded_file = st.file_uploader("📄 Unggah file soal di sini...", type=['pdf', 'jpg', 'jpeg', 'png', 'txt'])
prompt = st.chat_input("Ketik pertanyaanmu di sini...")

# --- Logika Pemrosesan Input ---
if prompt or uploaded_file:
    input_parts = []
    
    with st.chat_message("user"):
        if uploaded_file:
            st.image(uploaded_file if uploaded_file.type != "application/pdf" else "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/PDF_file_icon.svg/1200px-PDF_file_icon.svg.png", 
                     caption=uploaded_file.name, width=100)
        if prompt:
            st.markdown(prompt)

    if uploaded_file:
        file_parts = get_file_parts(uploaded_file)
        if file_parts:
            input_parts.extend(file_parts)
    
    if prompt:
        input_parts.insert(0, prompt)

    if input_parts:
        with st.chat_message("assistant"):
            with st.spinner("Tutor MFK sedang berpikir..."):
                try:
                    response = st.session_state.chat.send_message(input_parts, stream=True)
                    response.resolve()
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Maaf, terjadi kesalahan: {e}")