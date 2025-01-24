import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv('processed_day.csv')

# Set up Streamlit page
st.title('Dashboard Analisis Penyewaan Sepeda')

# Pengaruh Cuaca terhadap Permintaan Penyewaan Sepeda
st.subheader('Pengaruh Cuaca terhadap Permintaan Penyewaan Sepeda')

weather_labels = ['Cerah', 'Berkabut', 'Hujan/Salju Ringan', 'Hujan/Salju Lebat']
weather_avg = day_df.groupby('weathersit')['cnt'].mean().reindex(range(1, 5), fill_value=0)
weather_avg_sorted = weather_avg.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bar_colors = sns.color_palette('Blues_d', len(weather_avg_sorted))
ax.bar(weather_labels, weather_avg_sorted, color=bar_colors)
ax.set_title('Pengaruh Cuaca terhadap Permintaan Penyewaan Sepeda')
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-Rata Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

weather_table = pd.DataFrame({
    'Kondisi Cuaca': weather_labels,
    'Rata-Rata Penyewaan Sepeda': weather_avg_sorted.values
})
st.write(weather_table)

# Pengaruh Musim terhadap Permintaan Penyewaan Sepeda
st.subheader('Pengaruh Musim terhadap Permintaan Penyewaan Sepeda')

season_labels = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
season_avg = day_df.groupby('season')['cnt'].mean().reindex(range(1, 5), fill_value=0)
season_avg_sorted = season_avg.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bar_colors = sns.color_palette('Blues_d', len(season_avg_sorted))
ax.bar(season_labels, season_avg_sorted, color=bar_colors)
ax.set_title('Pengaruh Musim terhadap Permintaan Penyewaan Sepeda')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-Rata Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

season_table = pd.DataFrame({
    'Musim': season_labels,
    'Rata-Rata Penyewaan Sepeda': season_avg_sorted.values})
st.write(season_table)

# Perbedaan Pola Penyewaan antara Hari Kerja dan Akhir Pekan
st.subheader('Perbedaan Pola Penyewaan: Hari Kerja vs Akhir Pekan')

workingday_labels = ['Akhir Pekan(0)', 'Hari Kerja (1)']
workingday_avg = day_df.groupby('workingday')['cnt'].mean().reindex([0, 1], fill_value=0)

fig, ax = plt.subplots(figsize=(8, 6))
bar_colors = sns.color_palette('Blues_d', len(workingday_avg))
ax.bar(workingday_labels, workingday_avg, color=bar_colors)
ax.set_title('Rata-rata Peminjaman Sepeda: Hari Kerja vs Akhir Pekan')
ax.set_xlabel('Kategori Hari')
ax.set_ylabel('Rata-Rata Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

workingday_table = pd.DataFrame({
    'Kategori Hari': workingday_labels,
    'Rata-Rata Penyewaan Sepeda': workingday_avg.values
})
st.write(workingday_table)

# Perbedaan Permintaan antara Pengguna Kasual dan Terdaftar
st.subheader('Perbedaan Permintaan Penyewaan: Kasual vs Terdaftar')

user_labels = ['Casual', 'Registered']
user_avg = day_df[['casual', 'registered']].mean()

fig, ax = plt.subplots(figsize=(8, 6))
bar_colors = sns.color_palette('Blues_d', len(user_avg))
ax.bar(user_labels, user_avg, color=bar_colors)
ax.set_title('Rata-rata Peminjaman Sepeda: Casual vs Registered')
ax.set_xlabel('Kategori Pengguna')
ax.set_ylabel('Rata-Rata Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

user_table = pd.DataFrame({
    'Kategori Pengguna': user_labels,
    'Rata-Rata Penyewaan Sepeda': user_avg.values })
st.write(user_table)
