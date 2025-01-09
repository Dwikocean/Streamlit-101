import streamlit as st
import pandas as pd
import random
import faker

# Fungsi untuk mengolah data kepuasan pelanggan
def analyze_feedback(feedback_data):
    # Menghitung rata-rata skor kepuasan
    average_score = feedback_data['Skor Kepuasan'].mean()
    
    # Menghitung distribusi nilai skor
    score_distribution = feedback_data['Skor Kepuasan'].value_counts().sort_index()
    
    return average_score, score_distribution

# Membuat data fiktif dengan menggunakan Faker
fake = faker.Faker('id_ID')

# Menentukan jumlah data yang akan dibuat (20 data)
num_data = 20

# Membuat kolom-kolom yang diperlukan
data = {
    "ID": [i+1 for i in range(num_data)],
    "Nama Pelanggan": [fake.name() for _ in range(num_data)],
    "Skor Kepuasan": [random.randint(1, 5) for _ in range(num_data)],  # Skor dari 1 hingga 5
    "Ulasan": [fake.sentence(nb_words=random.randint(6, 12)) for _ in range(num_data)]
}

# Membuat DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.title('Aplikasi Analisis Kepuasan Pelanggan UMKM F&B')

# Menampilkan data feedback pelanggan
st.write("Data Feedback Pelanggan:")
st.write(df)

# Analisis data kepuasan pelanggan
average_score, score_distribution = analyze_feedback(df)

# Menampilkan hasil analisis
st.write(f"Rata-rata Skor Kepuasan Pelanggan: {average_score:.2f}")

# Menampilkan distribusi nilai skor
st.write("Distribusi Skor Kepuasan Pelanggan:")
st.bar_chart(score_distribution)

# Menyimpan data ke file CSV
csv_file = "feedback_pelanggan_umkm_fnb.csv"
df.to_csv(csv_file, index=False, encoding="utf-8")
st.download_button(label="Unduh Data Feedback Pelanggan (CSV)", data=open(csv_file, "rb"), file_name=csv_file)
