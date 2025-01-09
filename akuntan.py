import streamlit as st
import pandas as pd
from datetime import date

# Setup title
st.title("Aplikasi Manajemen Keuangan UMKM")

# Sidebar untuk navigasi
menu = st.sidebar.selectbox("Pilih Menu", ["Pencatatan Transaksi", "Laporan Keuangan"])

# File CSV untuk menyimpan data
data_file = "keuangan_umkm.csv"

# Fungsi untuk memuat data
def load_data():
    try:
        return pd.read_csv(data_file)
    except FileNotFoundError:
        # Data dummy jika file tidak ditemukan
        dummy_data = {
            "Tanggal": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", 
                        "2024-01-06", "2024-01-07", "2024-01-08"],
            "Jenis": ["Pemasukan", "Pemasukan", "Pengeluaran", "Pemasukan", "Pengeluaran", 
                      "Pemasukan", "Pengeluaran", "Pemasukan"],
            "Keterangan": ["Penjualan Produk A", "Penjualan Produk B", "Gaji Karyawan", 
                           "Penjualan Produk C", "Sewa Ruang Toko", "Penjualan Produk D", 
                           "Biaya Iklan", "Penjualan Produk E"],
            "Jumlah": [500000, 300000, 150000, 750000, 200000, 600000, 50000, 400000],
            "Status Pembayaran": ["Sudah Dibayar", "Belum Dibayar", "Belum Dibayar", 
                                  "Sudah Dibayar", "Sudah Dibayar", "Sudah Dibayar", 
                                  "Belum Dibayar", "Sudah Dibayar"]
        }
        return pd.DataFrame(dummy_data)

# Fungsi untuk menyimpan data
def save_data(data):
    data.to_csv(data_file, index=False)

# Menu Pencatatan Transaksi
if menu == "Pencatatan Transaksi":
    st.header("Pencatatan Transaksi")

    # Input data transaksi
    with st.form("form_transaksi"):
        tanggal = st.date_input("Tanggal", value=date.today())
        jenis = st.radio("Jenis Transaksi", ["Pemasukan", "Pengeluaran"])
        keterangan = st.text_input("Keterangan")
        jumlah = st.number_input("Jumlah", min_value=0, step=1000)
        status_pembayaran = st.radio("Status Pembayaran", ["Belum Dibayar", "Sudah Dibayar"])
        submit = st.form_submit_button("Simpan")

    if submit:
        # Load existing data
        data = load_data()
        # Tambahkan data baru
        new_data = pd.DataFrame([[tanggal, jenis, keterangan, jumlah, status_pembayaran]], 
                                columns=["Tanggal", "Jenis", "Keterangan", "Jumlah", "Status Pembayaran"])
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success("Transaksi berhasil disimpan!")

# Menu Laporan Keuangan
elif menu == "Laporan Keuangan":
    st.header("Laporan Keuangan")

    # Load data
    data = load_data()

    if not data.empty:
        # Tampilkan tabel data
        st.subheader("Data Transaksi")
        st.dataframe(data)

        # Total pemasukan dan pengeluaran
        total_pemasukan = data[data["Jenis"] == "Pemasukan"]["Jumlah"].sum()
        total_pengeluaran = data[data["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
        saldo = total_pemasukan - total_pengeluaran

        # Tampilkan ringkasan
        st.subheader("Ringkasan Keuangan")
        st.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
        st.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
        st.metric("Saldo Akhir", f"Rp {saldo:,.0f}")

        # Verifikasi Pembayaran
        belum_dibayar = data[data["Status Pembayaran"] == "Belum Dibayar"]
        st.subheader(f"Verifikasi Pembayaran ({len(belum_dibayar)} transaksi belum dibayar)")
        st.dataframe(belum_dibayar)
    else:
        st.warning("Belum ada data transaksi!")

# Informasi tambahan
st.sidebar.info("DWIKI AKA QADA (@dwikocean)")
