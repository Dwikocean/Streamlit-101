import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Data dummy untuk pelanggan
data = {
    'Nama': ['Pelanggan A', 'Pelanggan B', 'Pelanggan C', 'Pelanggan D'],
    'Status Pembayaran': ['Belum Bayar', 'Sudah Bayar', 'Belum Bayar', 'Belum Bayar'],
    'Tanggal Pembayaran Terakhir': ['2024-01-01', '2024-01-02', '2024-01-08', '2024-01-07'],
    'Batas Waktu Pembayaran': ['2024-01-10', '2024-01-15', '2024-01-09', '2024-01-10']
}

# Mengubah data ke DataFrame
df = pd.DataFrame(data)

# Mengonversi kolom Tanggal menjadi datetime
df['Tanggal Pembayaran Terakhir'] = pd.to_datetime(df['Tanggal Pembayaran Terakhir'])
df['Batas Waktu Pembayaran'] = pd.to_datetime(df['Batas Waktu Pembayaran'])

# Fungsi untuk cek pelanggan yang belum bayar dan dekat deadline
def check_payment_status(df):
    today = datetime.today()

    # Membuat kolom untuk menentukan apakah sudah dekat deadline (misalnya 2 hari sebelum batas waktu)
    df['Dekat Deadline'] = (df['Batas Waktu Pembayaran'] - today).dt.days <= 2
    
    # Filter pelanggan yang belum bayar dan dekat deadline
    filtered_df = df[(df['Status Pembayaran'] == 'Belum Bayar') & (df['Dekat Deadline'] == True)]
    
    return filtered_df

# Membuat UI dengan Streamlit
st.title('Pemberitahuan Pembayaran')

st.write("Berikut adalah daftar pelanggan yang belum membayar dan sudah mendekati batas waktu:")

# Menampilkan data pelanggan yang belum membayar dan dekat deadline
payment_alerts = check_payment_status(df)
if not payment_alerts.empty:
    st.write(payment_alerts[['Nama', 'Batas Waktu Pembayaran']])
else:
    st.write("Tidak ada pelanggan yang perlu diberi pemberitahuan saat ini.")

# Simulasi pengiriman pesan otomatis
if not payment_alerts.empty:
    for index, row in payment_alerts.iterrows():
        st.write(f"Pesan untuk {row['Nama']}:")
        st.write(f"Hi {row['Nama']}, kami ingin mengingatkan Anda bahwa pembayaran Anda dengan batas waktu {row['Batas Waktu Pembayaran'].strftime('%Y-%m-%d')} sudah dekat. Segera lakukan pembayaran untuk menghindari keterlambatan.")
else:
    st.write("Semua pelanggan sudah membayar atau tidak dekat dengan deadline.")
