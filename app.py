import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Fungsi untuk inisialisasi database
def init_db():
    conn = sqlite3.connect('calculator_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan perhitungan ke database
def save_calculation(expression, result):
    conn = sqlite3.connect('calculator_history.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO calculations (expression, result, timestamp) VALUES (?, ?, ?)",
              (expression, result, timestamp))
    conn.commit()
    conn.close()

# Fungsi untuk mengambil histori dari database
def get_history():
    conn = sqlite3.connect('calculator_history.db')
    df = pd.read_sql_query("SELECT expression, result, timestamp FROM calculations ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# Inisialisasi database saat aplikasi dimulai
init_db()

st.set_page_config(page_title="Kalkulator Sederhana dengan Histori", layout="centered")

st.title("Kalkulator Sederhana")

# Input untuk ekspresi matematika
expression = st.text_input("Masukkan ekspresi matematika (contoh: 2+2*3 atau 10/2-1):", "")

# Tombol hitung
if st.button("Hitung"):
    if expression:
        try:
            # Evaluasi ekspresi matematika
            result = eval(expression)
            st.success(f"Hasil: **{result}**")
            save_calculation(expression, str(result))
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}. Pastikan format ekspresi benar.")
    else:
        st.warning("Mohon masukkan ekspresi terlebih dahulu.")
        
## Histori Perhitungan

if st.button("Refresh Histori"):
    st.experimental_rerun() # Memuat ulang aplikasi untuk menampilkan histori terbaru

history_df = get_history()

if not history_df.empty:
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("Belum ada histori perhitungan.")

st.markdown("""
---
*Kalkulator ini mendukung operasi dasar seperti penjumlahan (+), pengurangan (-), perkalian (*), dan pembagian (/).*
""")