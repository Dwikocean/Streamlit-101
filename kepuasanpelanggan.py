import streamlit as st
import tweepy
from textblob import TextBlob
import pandas as pd

# Twitter API Credentials
api_key = 'YOUR_API_KEY'
api_secret_key = 'YOUR_API_SECRET_KEY'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Auth untuk akses Twitter API
auth = tweepy.OAuth1UserHandler(api_key, api_secret_key, access_token, access_token_secret)
api = tweepy.API(auth)

# Fungsi untuk mengirim tweet
def send_tweet(text):
    api.update_status(text)
    st.success("Tweet telah diposting!")

# Fungsi untuk analisis sentimen dari tweet
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    sentiment = analysis.sentiment.polarity
    if sentiment > 0:
        return "Positif"
    elif sentiment < 0:
        return "Negatif"
    else:
        return "Netral"

# Halaman Streamlit
st.title("Aplikasi Otomatisasi Media Sosial dan Analisis Sentimen")

st.header("1. Kirim Tweet")
tweet_text = st.text_input("Tulis tweet yang ingin dikirim:")
if st.button("Kirim Tweet"):
    if tweet_text:
        send_tweet(tweet_text)
    else:
        st.warning("Tulis sesuatu untuk dikirim!")

st.header("2. Analisis Sentimen dari Tweet")
tweet_input = st.text_area("Masukkan tweet untuk analisis sentimen:")
if st.button("Analisis Sentimen"):
    if tweet_input:
        sentiment = analyze_sentiment(tweet_input)
        st.write(f"Sentimen Tweet: {sentiment}")
    else:
        st.warning("Masukkan tweet untuk dianalisis!")

st.header("3. Lihat Riwayat Tweet")
# Mengambil tweet terakhir pengguna
public_tweets = api.user_timeline(count=10)
tweets_data = [{"Tweet": tweet.text, "Sentimen": analyze_sentiment(tweet.text)} for tweet in public_tweets]
df = pd.DataFrame(tweets_data)

st.write("Riwayat Tweet Terakhir:")
st.dataframe(df)
