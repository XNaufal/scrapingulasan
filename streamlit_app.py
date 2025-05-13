import streamlit as st
from google_play_scraper import reviews, Sort
import pandas as pd
import datetime

# ============================
# Judul Aplikasi
# ============================
st.title("📱 Scraper Ulasan Google Play Store + Pelabelan (Tanpa Netral)")

# ============================
# Input Pengguna
# ============================
app_id = st.text_input("Masukkan App ID aplikasi (contoh: id.dana)", value="id.dana")
jumlah = st.slider("Jumlah ulasan yang ingin diambil", 100, 2000, 100)

# ============================
# Fungsi Pelabelan Sentimen
# ============================
def pelabelan(score):
    return 'NEGATIF' if score < 3 else 'POSITIF'

# ============================
# Inisialisasi State
# ============================
if 'scraped' not in st.session_state:
    st.session_state.scraped = False

# ============================
# Proses Scrape dan Pelabelan
# ============================
if st.button("Mulai Scrape"):
    st.info(f"Mengambil {jumlah} ulasan untuk aplikasi: {app_id} ...")
    try:
        st.session_state.scraped = False  # Reset status jika scraping ulang

        # Ambil data ulasan dari Google Play
        hasil, _ = reviews(
            app_id,
            lang='id',
            country='id',
            count=jumlah,
            sort=Sort.MOST_RELEVANT
        )

        # Konversi ke DataFrame dan pelabelan
        df = pd.DataFrame(hasil)[['userName', 'at', 'content', 'score']]
        df['at'] = pd.to_datetime(df['at'])
        df = df[df['score'] != 3]
        df['label'] = df['score'].apply(pelabelan)

        # Tampilkan hasil
        st.success("Sukses! Berikut hasil scraping dan pelabelan (tanpa ulasan netral):")
        st.dataframe(df)

        # Siapkan file untuk diunduh
        tanggal = datetime.datetime.now().strftime('%Y%m%d')
        nama_file = f"ulasan_{app_id.replace('.', '_')}_{len(df)}_{tanggal}.csv"
        csv = df.to_csv(index=False).encode('utf-8')

        # Tampilkan tombol download
        st.download_button("Download sebagai CSV", csv, nama_file, "text/csv")

        # Tandai bahwa scraping berhasil
        st.session_state.scraped = True

    except Exception as e:
        st.error(f"Gagal scraping: {e}")

# ============================
# Tombol Analisis Sentimen (Jika Scraping Selesai)
# ============================
if st.session_state.scraped:
    st.markdown("---")
    st.markdown("Siap untuk Analisis Sentimen lebih lanjut?  \nDownload sebagai CSV terlebih dahulu!")
    st.markdown(
        """
        <a href="http://ahmadnaufal.shinyapps.io/analisissentimen/" target="_blank">
            <button style='background-color:#f63366; color:white; padding:10px 10px; border:none;
                           border-radius:8px; font-size:16px; cursor:pointer;'>
                Analisis Sentimen
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )