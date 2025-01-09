import streamlit as st
import qrcode
import cv2
from pyzbar.pyzbar import decode
import numpy as np

# Fungsi untuk generate QR code
def generate_qr(data, filename="qr_code.png"):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)
    return filename

# Fungsi untuk scan QR code
def scan_qr(image_path):
    img = cv2.imread(image_path)
    qr_codes = decode(img)
    if qr_codes:
        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            return qr_data
    return None

# Streamlit interface
st.title("Verifikasi QR Code UMKM")

menu = st.sidebar.selectbox("Pilih Menu", ["Generate QR Code", "Verifikasi QR Code"])

if menu == "Generate QR Code":
    st.subheader("Generate QR Code")
    data = st.text_input("Masukkan Data untuk QR Code")
    if st.button("Generate QR Code"):
        if data:
            filename = generate_qr(data)
            st.image(filename)
            st.success("QR Code berhasil dibuat!")

elif menu == "Verifikasi QR Code":
    st.subheader("Verifikasi QR Code")
    uploaded_file = st.file_uploader("Upload QR Code", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Simpan file yang diupload
        with open("uploaded_qr.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        qr_data = scan_qr("uploaded_qr.png")
        if qr_data:
            st.write(f"Data dalam QR Code: {qr_data}")
        else:
            st.error("QR Code tidak dapat dibaca!")
