import streamlit as st
from textblob import TextBlob
import pandas as pd

# Fungsi untuk analisis sentimen dari teks
def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        return "Positif"
    elif sentiment < 0:
        return "Negatif"
    else:
        return "Netral"

# Halaman Streamlit
st.title("Aplikasi Analisis Sentimen")

st.header("Masukkan Teks untuk Analisis Sentimen")
text_input = st.text_area("Masukkan teks yang ingin dianalisis:")
if st.button("Analisis Sentimen"):
    if text_input:
        sentiment = analyze_sentiment(text_input)
        st.write(f"Sentimen Teks: {sentiment}")
    else:
        st.warning("Masukkan teks untuk dianalisis!")

st.header("Contoh Teks yang Dapat Dianalisis")

# Contoh data tweet atau review fiktif
example_text = ["Produk ini luar biasa!", "Saya sangat kecewa dengan layanan ini.", "Pengalaman yang sangat biasa saja."]
example_data = [{"Teks": text, "Sentimen": analyze_sentiment(text)} for text in example_text]

df = pd.DataFrame(example_data)
st.write("Contoh Teks dan Analisis Sentimen:")
st.dataframe(df)
