import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk mengolah data kepuasan pelanggan
def analyze_feedback(feedback_data):
    # Menghitung rata-rata skor kepuasan
    average_score = feedback_data['Score'].mean()
    
    # Visualisasi kepuasan pelanggan
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(feedback_data['Score'], bins=10, color='skyblue', edgecolor='black')
    ax.set_title('Distribusi Skor Kepuasan Pelanggan')
    ax.set_xlabel('Skor Kepuasan')
    ax.set_ylabel('Frekuensi')
    
    return average_score, fig

# Streamlit UI
st.title('Aplikasi Analisis Kepuasan Pelanggan')

# Upload file CSV dengan data feedback pelanggan
uploaded_file = st.file_uploader("Unggah File Feedback Pelanggan (CSV)", type="csv")

if uploaded_file is not None:
    # Membaca data feedback pelanggan
    feedback_data = pd.read_csv(uploaded_file)
    
    # Tampilkan data jika ingin
    st.write("Data Feedback Pelanggan:")
    st.write(feedback_data)
    
    # Pastikan ada kolom 'Score'
    if 'Score' in feedback_data.columns:
        average_score, fig = analyze_feedback(feedback_data)
        
        # Menampilkan hasil analisis
        st.write(f"Rata-rata Skor Kepuasan Pelanggan: {average_score:.2f}")
        st.pyplot(fig)
    else:
        st.warning("Kolom 'Score' tidak ditemukan dalam data!")
else:
    st.info("Silakan unggah file CSV yang berisi data feedback pelanggan.")
