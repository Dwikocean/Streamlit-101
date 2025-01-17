import streamlit as st
import pandas as pd
from datetime import datetime

# Inisialisasi file CSV untuk menyimpan data transaksi dan pengeluaran
TRANSAKSI_FILE = 'transaksi.csv'
PENGELUARAN_FILE = 'pengeluaran.csv'

# Daftar produk ayam beserta harga
produk_ayam = {
    "Ayam Goreng 1 Porsi": 15000,
    "Ayam Bakar 1 Porsi": 17000,
    "Ayam Penyet 1 Porsi": 16000,
    "Nasi Ayam Goreng": 20000,
    "Nasi Ayam Bakar": 22000
}

# Fungsi untuk memuat data transaksi dan pengeluaran
def load_data(file_name):
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Tanggal", "Produk", "Jumlah", "Harga Total"])

# Fungsi untuk menambahkan transaksi
def add_transaction(tanggal, produk, jumlah, harga_total, file_name):
    new_data = pd.DataFrame({"Tanggal": [tanggal], "Produk": [produk], "Jumlah": [jumlah], "Harga Total": [harga_total]})
    data = load_data(file_name)
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv(file_name, index=False)

# Fungsi untuk menambahkan pengeluaran
def add_expense(tanggal, deskripsi, jumlah, harga_total, file_name):
    new_data = pd.DataFrame({"Tanggal": [tanggal], "Deskripsi": [deskripsi], "Jumlah": [jumlah], "Harga Total": [harga_total]})
    data = load_data(file_name)
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_csv(file_name, index=False)

# Fungsi untuk menghitung total keuntungan kotor
def calculate_gross_profit():
    data_transaksi = load_data(TRANSAKSI_FILE)
    return data_transaksi["Harga Total"].sum()

# Fungsi untuk menghitung total pengeluaran
def calculate_total_expenses():
    data_pengeluaran = load_data(PENGELUARAN_FILE)
    return data_pengeluaran["Harga Total"].sum()

# Fungsi untuk menghitung keuntungan bersih
def calculate_net_profit():
    gross_profit = calculate_gross_profit()
    total_expenses = calculate_total_expenses()
    return gross_profit - total_expenses

# Streamlit UI
st.title("Aplikasi UMKM F&B - Pencatatan Transaksi & Pengeluaran")

menu = ["Input Transaksi", "Input Pengeluaran", "Lihat Transaksi", "Lihat Pengeluaran", "Lihat Keuntungan"]
choice = st.sidebar.selectbox("Pilih Menu", menu)

# Input Transaksi
if choice == "Input Transaksi":
    st.header("Tambah Transaksi (Kasir)")

    # Pilih produk ayam dari dropdown
    produk = st.selectbox("Pilih Produk", list(produk_ayam.keys()))
    
    # Input jumlah
    jumlah = st.number_input("Jumlah", min_value=1, step=1)

    # Kalkulasi total harga
    harga_per_unit = produk_ayam[produk]
    harga_total = harga_per_unit * jumlah

    # Tampilkan harga per unit dan total harga
    st.write(f"Harga per Unit: Rp {harga_per_unit:,}")
    st.write(f"Total Harga: Rp {harga_total:,}")

    # Simpan transaksi jika tombol ditekan
    if st.button("Simpan Transaksi"):
        tanggal = datetime.today().strftime('%Y-%m-%d')
        add_transaction(tanggal, produk, jumlah, harga_total, TRANSAKSI_FILE)
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

# Lihat Keuntungan
elif choice == "Lihat Keuntungan":
    st.header("Keuntungan")
    
    # Hitung Keuntungan Kotor dan Bersih
    gross_profit = calculate_gross_profit()
    net_profit = calculate_net_profit()
    
    # Tampilkan Keuntungan
    st.write(f"Total Keuntungan Kotor: Rp {gross_profit:,}")
    st.write(f"Total Pengeluaran: Rp {calculate_total_expenses():,}")
    st.write(f"Total Keuntungan Bersih: Rp {net_profit:,}")
