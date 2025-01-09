# app.py

import qrcode
import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Fungsi untuk membuat data dummy transaksi
def create_dummy_database():
    data = {
        "order_id": [123456 + i for i in range(10)],
        "amount": [10000 * (i + 1) for i in range(10)],
        "status": ["unpaid"] * 5 + ["paid"] * 3 + ["not found"] * 2,
        "payment_url": [
            f"https://example.com/pay?amount={10000 * (i + 1)}&order_id={123456 + i}"
            for i in range(8)
        ] + ["invalid_url_1", "invalid_url_2"],
    }
    return pd.DataFrame(data)

# Fungsi untuk membuat QR Code
def generate_qr_code(payment_data, file_name="payment_qr.png"):
    qr = qrcode.make(payment_data)
    qr.save(file_name)
    return file_name

# Fungsi untuk memindai QR Code
def scan_qr_code(file_name):
    img = cv2.imread(file_name)
    decoded_objects = decode(img)
    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        return data
    return None

# Fungsi untuk memverifikasi pembayaran berdasarkan URL
def verify_payment(database, payment_url):
    match = database[database["payment_url"] == payment_url]
    if not match.empty:
        index = match.index[0]
        if database.at[index, "status"] == "unpaid":
            database.at[index, "status"] = "paid"
            return "Verified: Paid"
        elif database.at[index, "status"] == "paid":
            return "Already Paid"
    return "Not Found"

# Fungsi untuk simulasi verifikasi pembayaran
def simulate_verification(database):
    results = []
    for idx, row in database.iterrows():
        qr_file = f"payment_qr_{idx}.png"
        generate_qr_code(row["payment_url"], qr_file)
        scanned_data = scan_qr_code(qr_file)
        verification_status = verify_payment(database, scanned_data or "Invalid QR Code")
        results.append([idx + 1, scanned_data or "Invalid QR Code", verification_status])
    return results, database

# Fungsi utama untuk menampilkan dashboard dengan Streamlit
def main():
    st.title("Payment Verification Dashboard")
    
    # Membuat database transaksi dummy
    database = create_dummy_database()
    st.subheader("Initial Database")
    st.dataframe(database)

    # Menjalankan simulasi verifikasi pembayaran
    st.subheader("Simulating Payment Verification...")
    results, updated_database = simulate_verification(database)
    
    # Menampilkan hasil verifikasi
    st.subheader("Verification Results")
    results_df = pd.DataFrame(results, columns=["QR Code Index", "Payment URL", "Verification Status"])
    st.dataframe(results_df)
    
    # Menampilkan database yang diperbarui
    st.subheader("Updated Database")
    st.dataframe(updated_database)
    
    # Visualisasi data
    st.subheader("Data Visualization")
    status_counts = updated_database["status"].value_counts()
    st.bar_chart(status_counts)
    st.text("Status Distribution:")
    for status, count in status_counts.items():
        st.text(f"{status}: {count}")

if __name__ == "__main__":
    main()
