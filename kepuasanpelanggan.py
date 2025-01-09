import streamlit as st
import pandas as pd
from datetime import datetime

# Inisialisasi file CSV untuk menyimpan data transaksi dan pengeluaran
TRANSAKSI_FILE = 'transaksi.csv'
PENGELUARAN_FILE = 'pengeluaran.csv'

# Fungsi untuk memuat data transaksi dan pengeluaran
def load_data(file_name):
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Tanggal", "Deskripsi", "Jumlah", "Harga Total"])

# Fungsi untuk menambahkan transaksi
def add_transaction(tanggal, deskripsi, jumlah, harga_total, file_name):
    new_data = pd.DataFrame({"Tanggal": [tanggal], "Deskripsi": [deskripsi], "Jumlah": [jumlah], "Harga Total": [harga_total]})
    data = load_data(file_name)
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv(file_name, index=False)

# Fungsi untuk menambahkan pengeluaran
def add_expense(tanggal, deskripsi, jumlah, harga_total, file_name):
    new_data = pd.DataFrame({"Tanggal": [tanggal], "Deskripsi": [deskripsi], "Jumlah": [jumlah], "Harga Total": [harga_total]})
    data = load_data(file_name)
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv(file_name, index=False)

# Streamlit UI
st.title("Aplikasi UMKM F&B - Pencatatan Transaksi & Pengeluaran")

menu = ["Input Transaksi", "Input Pengeluaran", "Lihat Transaksi", "Lihat Pengeluaran"]
choice = st.sidebar.selectbox("Pilih Menu", menu)

# Input Transaksi
if choice == "Input Transaksi":
    st.header("Tambah Transaksi")
    tanggal = st.date_input("Tanggal Transaksi", datetime.today())
    deskripsi = st.text_input("Deskripsi Barang")
    jumlah = st.number_input("Jumlah", min_value=1)
    harga_total = st.number_input("Harga Total", min_value=1)
    
    if st.button("Simpan Transaksi"):
        add_transaction(tanggal, deskripsi, jumlah, harga_total, TRANSAKSI_FILE)
        st.success("Transaksi berhasil disimpan!")

# Input Pengeluaran
elif choice == "Input Pengeluaran":
    st.header("Tambah Pengeluaran Bahan Baku")
    tanggal = st.date_input("Tanggal Pengeluaran", datetime.today())
    deskripsi = st.text_input("Deskripsi Pengeluaran")
    jumlah = st.number_input("Jumlah", min_value=1)
    harga_total = st.number_input("Harga Total", min_value=1)
    
    if st.button("Simpan Pengeluaran"):
        add_expense(tanggal, deskripsi, jumlah, harga_total, PENGELUARAN_FILE)
        st.success("Pengeluaran berhasil disimpan!")

# Lihat Transaksi
elif choice == "Lihat Transaksi":
    st.header("Data Transaksi")
    data_transaksi = load_data(TRANSAKSI_FILE)
    st.write(data_transaksi)

# Lihat Pengeluaran
elif choice == "Lihat Pengeluaran":
    st.header("Data Pengeluaran")
    data_pengeluaran = load_data(PENGELUARAN_FILE)
    st.write(data_pengeluaran)
