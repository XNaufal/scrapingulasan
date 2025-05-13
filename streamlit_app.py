import streamlit as st
from google_play_scraper import reviews
import pandas as pd

st.title("📱 Scraper Ulasan Google Play Store")

# Input app ID
app_id = st.text_input("Masukkan App ID aplikasi (contoh: com.whatsapp)", value="com.whatsapp")

# Slider jumlah ulasan
jumlah = st.slider("Jumlah ulasan yang ingin diambil", 10, 200, 50)

# Tombol scrape
if st.button("Mulai Scrape"):
    st.info(f"Mengambil {jumlah} ulasan untuk aplikasi: {app_id} ...")

    try:
        hasil, _ = reviews(
            app_id,
            lang='id',
            country='id',
            count=jumlah
        )

        # Simpan ke DataFrame
        df = pd.DataFrame(hasil)[['userName', 'score', 'content', 'at']]
        df['at'] = pd.to_datetime(df['at'])

        # Tampilkan tabel
        st.success("Sukses! Berikut hasil scraping:")
        st.dataframe(df)

        # Unduh sebagai CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download sebagai CSV", csv, "ulasan.csv", "text/csv")

    except Exception as e:
        st.error(f"Gagal scraping: {e}")