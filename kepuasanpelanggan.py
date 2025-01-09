import sqlite3
import pandas as pd
import streamlit as st

# Membuat database dan tabel jika belum ada
def create_db():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    # Membuat tabel transaksi jika belum ada
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        amount REAL,
        payment_status TEXT,
        transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

# Fungsi untuk menambah transaksi
def add_transaction(customer_name, amount, payment_status):
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO transactions (customer_name, amount, payment_status)
    VALUES (?, ?, ?)
    ''', (customer_name, amount, payment_status))

    conn.commit()
    conn.close()

# Fungsi untuk mengambil data transaksi
def get_transactions():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    conn.close()

    # Mengubah data menjadi DataFrame untuk tampil lebih rapi
    df = pd.DataFrame(transactions, columns=["ID", "Customer Name", "Amount", "Payment Status", "Transaction Date"])
    return df

# Fungsi untuk menampilkan transaksi
def display_transactions():
    df = get_transactions()
    st.dataframe(df)

# Fungsi untuk menambahkan transaksi baru
def handle_add_transaction():
    st.subheader("Add New Transaction")

    # Input data dari pengguna
    customer_name = st.text_input("Customer Name")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    payment_status = st.selectbox("Payment Status", ["Paid", "Pending"])

    # Tombol submit
    if st.button("Add Transaction"):
        if customer_name and amount > 0:
            add_transaction(customer_name, amount, payment_status)
            st.success("Transaction Added Successfully!")
        else:
            st.error("Please enter all fields correctly.")

# Set up tampilan Streamlit
st.title("UMKM Transaction Management System")
st.sidebar.title("Menu")
menu = st.sidebar.selectbox("Choose an option", ["Home", "Add Transaction", "View Transactions"])

create_db()  # Membuat database dan tabel

if menu == "Home":
    st.header("Welcome to the UMKM Transaction System")
    st.write("""
    This system helps manage transactions for small businesses. You can add new transactions, view transaction history, 
    and track payment statuses. Please use the menu on the sidebar to navigate.
    """)
elif menu == "Add Transaction":
    handle_add_transaction()
elif menu == "View Transactions":
    display_transactions()
