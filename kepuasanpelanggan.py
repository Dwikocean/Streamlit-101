import streamlit as st
import pandas as pd

# Simulasi database produk dan transaksi
products = {'ID': [1, 2, 3],
            'Product': ['Nasi Goreng', 'Mie Goreng', 'Sate Ayam'],
            'Price': [15000, 12000, 18000]}
df_products = pd.DataFrame(products)

# Inisialisasi transaksi jika file belum ada
try:
    df_transactions = pd.read_csv('data/transactions.csv')
except FileNotFoundError:
    df_transactions = pd.DataFrame(columns=['Transaction ID', 'Product', 'Quantity', 'Total'])

# Fungsi untuk menambahkan transaksi
def add_transaction(df_transactions, product, quantity):
    product_data = df_products[df_products['Product'] == product].iloc[0]
    total = product_data['Price'] * quantity
    new_transaction = {
        'Transaction ID': len(df_transactions) + 1,
        'Product': product,
        'Quantity': quantity,
        'Total': total
    }
    df_transactions = pd.concat([df_transactions, pd.DataFrame([new_transaction])], ignore_index=True)
    df_transactions.to_csv('data/transactions.csv', index=False)
    return df_transactions

# Aplikasi Streamlit
st.title('UMKM F&B Management')

# Menampilkan produk
st.header('Daftar Produk')
st.write(df_products)

# Formulir untuk menambahkan transaksi
st.header('Tambah Transaksi')
product_option = st.selectbox('Pilih Produk', df_products['Product'])
quantity = st.number_input('Jumlah', min_value=1, step=1)

if st.button('Tambah Transaksi'):
    df_transactions = add_transaction(df_transactions, product_option, quantity)
    st.success('Transaksi berhasil ditambahkan')

# Menampilkan laporan transaksi
st.header('Laporan Transaksi')
st.write(df_transactions)
