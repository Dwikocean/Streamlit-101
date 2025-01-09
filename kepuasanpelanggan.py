import streamlit as st
import pandas as pd
from io import BytesIO

# Fungsi untuk menghitung total transaksi
def hitung_total(cart):
    total = 0
    for item in cart:
        total += item['harga'] * item['jumlah']
    return total

# Judul Aplikasi
st.title('Aplikasi Kasir UMKM F&B')

# Upload File Produk
uploaded_file = st.file_uploader("Upload file produk Excel", type=["xlsx"])

if uploaded_file is not None:
    # Membaca file yang di-upload
    produk_df = pd.read_excel(uploaded_file)

    # Menampilkan Data Produk
    st.subheader('Daftar Produk')
    st.write(produk_df)

    # Menambah produk ke keranjang
    cart = []
    st.subheader('Tambah Produk ke Keranjang')

    produk_terpilih = st.selectbox('Pilih Produk', produk_df['Nama Produk'])
    jumlah_terpilih = st.number_input('Jumlah', min_value=1, max_value=50, step=1)

    if st.button('Tambah ke Keranjang'):
        produk = produk_df[produk_df['Nama Produk'] == produk_terpilih].iloc[0]
        item = {
            'nama': produk['Nama Produk'],
            'harga': produk['Harga'],
            'jumlah': jumlah_terpilih
        }
        cart.append(item)
        st.success(f'Produk {produk_terpilih} berhasil ditambahkan ke keranjang!')

    # Menampilkan Keranjang Belanja
    st.subheader('Keranjang Belanja')
    if cart:
        cart_df = pd.DataFrame(cart)
        st.write(cart_df)

        # Hitung Total
        total = hitung_total(cart)
        st.write(f'Total Pembayaran: Rp {total}')
    else:
        st.write('Keranjang masih kosong.')

    # Menyelesaikan Transaksi
    if st.button('Selesaikan Transaksi'):
        if cart:
            st.write('Transaksi selesai! Terima kasih telah berbelanja.')
            cart.clear()  # Kosongkan keranjang setelah transaksi selesai
        else:
            st.warning('Keranjang masih kosong. Tambahkan produk terlebih dahulu.')
