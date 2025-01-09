import streamlit as st
import pandas as pd

# Fungsi untuk mengolah data kepuasan pelanggan
def analyze_feedback(feedback_data):
    # Menghitung rata-rata skor kepuasan
    average_score = feedback_data['Score'].mean()
    
    # Menghitung distribusi nilai skor
    score_distribution = feedback_data['Score'].value_counts().sort_index()
    
    return average_score, score_distribution

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
        average_score, score_distribution = analyze_feedback(feedback_data)
        
        # Menampilkan hasil analisis
        st.write(f"Rata-rata Skor Kepuasan Pelanggan: {average_score:.2f}")
        
        # Menampilkan distribusi nilai skor
        st.write("Distribusi Skor Kepuasan Pelanggan:")
        st.bar_chart(score_distribution)
    else:
        st.warning("Kolom 'Score' tidak ditemukan dalam data!")
else:
    st.info("Silakan unggah file CSV yang berisi data feedback pelanggan.")
