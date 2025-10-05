# chatbot-streamlit-eureka
final project - LLM-Based Tools and Gemini API Integration for Data Scientists, Maju Bareng AI

# 🤖 Chatbot Tutor Eureka

Chatbot "Tutor Eureka" adalah asisten belajar cerdas berbasis AI yang dirancang untuk membantu siswa SMP & SMA dalam memahami mata pelajaran **Matematika, Fisika,- dan Kimia**. Aplikasi ini dibangun menggunakan Streamlit dan ditenagai langsung oleh model AI canggih dari Google, Gemini, melalui library `google-generativeai`.

## ✨ Fitur Utama

- **Tutor Materi MFK**: Dapatkan penjelasan konsep, rumus, dan rangkuman bab secara interaktif.
- **Solver Soal dari File**: Unggah file soal (`.pdf`, `.jpg`, `.png`, `.txt`) dan dapatkan solusi jawaban langkah-demi-langkah. Chatbot ini mampu membaca teks dan gambar langsung dari file.
- **Visualisasi Cerdas**: Membantu memahami konsep abstrak dengan menampilkan GIF atau gambar diagram (JPG/PNG) secara otomatis.
- **Pilihan Model**: Pilih antara **Gemini 2.5 Flash** atau **Gemini 2.5 Pro** untuk menyeimbangkan antara kecepatan dan kecerdasan.

## 🚀 Tampilan Aplikasi

## 🛠️ Instalasi & Penggunaan

### 1. Prasyarat

- **Python 3.13**
- `conda` atau `venv` untuk manajemen lingkungan virtual.

### 2. Buat Lingkungan Virtual

```bash
conda create -n tutor-mfk python=3.13
conda activate tutor-mfk
```

### 3. Instal Dependensi

Pastikan Anda memiliki file `requirements.txt` di direktori proyek, lalu jalankan:

```bash
pip install -r requirements.txt
```

### 4. Menjalankan Secara Lokal

Jalankan aplikasi dengan perintah berikut di terminal:

```bash
streamlit run streamlit_app.py
```

Aplikasi akan terbuka secara otomatis di browser Anda. Masukkan Gemini API Key Anda di sidebar untuk memulai.

### 5. Deployment

Aplikasi ini dirancang untuk di-*deploy* ke [Streamlit Community Cloud](https://share.streamlit.io/). Cukup hubungkan repositori GitHub Anda dan simpan Gemini API Key di menu **Settings > Secrets**.
