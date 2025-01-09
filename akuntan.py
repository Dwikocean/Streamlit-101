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
        return pd.DataFrame(columns=["Tanggal", "Jenis", "Keterangan", "Jumlah"])

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
        submit = st.form_submit_button("Simpan")

    if submit:
        # Load existing data
        data = load_data()
        # Tambahkan data baru
        new_data = pd.DataFrame([[tanggal, jenis, keterangan, jumlah]], columns=["Tanggal", "Jenis", "Keterangan", "Jumlah"])
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
    else:
        st.warning("Belum ada data transaksi!")

# Informasi tambahan
st.sidebar.info("Dibuat dengan Streamlit untuk membantu UMKM mencatat keuangan.")
