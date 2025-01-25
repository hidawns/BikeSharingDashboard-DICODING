import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv('processed_day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.image("bicycle.png")
    
    st.header("Filter Data")
    
    start_date = st.date_input(
        label="Mulai Tanggal", value=min_date,
        min_value=min_date, max_value=max_date
    )
    
    end_date = st.date_input(
        label="Akhir Tanggal", value=max_date,
        min_value=min_date, max_value=max_date
    )
    
    if start_date > end_date:
        st.error("Tanggal mulai harus lebih kecil atau sama dengan tanggal akhir.")

filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

st.title('Dashboard Permintaan Penyewaan Sepeda')

# Pengaruh Cuaca terhadap Permintaan Penyewaan Sepeda
st.subheader('Pengaruh Cuaca terhadap Permintaan Penyewaan Sepeda')

weather_labels = ['Cerah', 'Berkabut', 'Hujan/Salju Ringan', 'Hujan/Salju Lebat']
weather_avg = filtered_df.groupby('weathersit')['cnt'].mean().reindex(range(1, 5), fill_value=0)
weather_avg_sorted = weather_avg.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bar_colors = sns.color_palette('Blues_d', len(weather_avg_sorted))
ax.bar(weather_labels, weather_avg_sorted, color=bar_colors)
ax.set_xlabel('Cuaca')
ax.set_ylabel('Rata-Rata Jml Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

weather_table = pd.DataFrame({
    'Cuaca': weather_labels,
    'Rata-Rata Jml Penyewaan Sepeda': weather_avg_sorted.values
})
weather_table['Rata-Rata Jml Penyewaan Sepeda'] = weather_table['Rata-Rata Jml Penyewaan Sepeda'].round(0)
st.write(weather_table)

# Pengaruh Musim terhadap Permintaan Penyewaan Sepeda
st.subheader('Pengaruh Musim terhadap Permintaan Penyewaan Sepeda')

season_labels = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
season_avg = filtered_df.groupby('season')['cnt'].mean().reindex(range(1, 5), fill_value=0)
season_avg_sorted = season_avg.sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bar_colors = sns.color_palette('Blues_d', len(season_avg_sorted))
ax.bar(season_labels, season_avg_sorted, color=bar_colors)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-Rata Jml Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

season_table = pd.DataFrame({
    'Musim': season_labels,
    'Rata-Rata Jml Penyewaan Sepeda': season_avg_sorted.values})
season_table['Rata-Rata Jml Penyewaan Sepeda'] = season_table['Rata-Rata Jml Penyewaan Sepeda'].round(0)
st.write(season_table)

# Perbedaan Permintaan Penyewaan Sepeda berdasarkan Working Day
st.subheader('Perbedaan Permintaan Penyewaan Sepeda berdasarkan Working Day')

workingday_labels = ['Akhir Pekan(0)', 'Hari Kerja (1)']
workingday_avg = filtered_df.groupby('workingday')['cnt'].mean().reindex([0, 1], fill_value=0)

fig, ax = plt.subplots(figsize=(8, 6))
bar_colors = sns.color_palette('Blues_d', len(workingday_avg))
ax.bar(workingday_labels, workingday_avg, color=bar_colors)
ax.set_xlabel('Working Day')
ax.set_ylabel('Rata-Rata Jml Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

workingday_table = pd.DataFrame({
    'Working Day': workingday_labels,
    'Rata-Rata Jml Penyewaan Sepeda': workingday_avg.values
})
workingday_table['Rata-Rata Jml Penyewaan Sepeda'] = workingday_table['Rata-Rata Jml Penyewaan Sepeda'].round(0)
st.write(workingday_table)

# Perbedaan Permintaan Penyewaan Sepeda berdasarkan Jenis Keanggotaan
st.subheader('Perbedaan Permintaan Penyewaan Sepeda berdasarkan Jenis Keanggotaan')

user_labels = ['Casual', 'Registered']
user_avg = filtered_df[['casual', 'registered']].mean()

fig, ax = plt.subplots(figsize=(8, 6))
bar_colors = sns.color_palette('Blues_d', len(user_avg))
ax.bar(user_labels, user_avg, color=bar_colors)
ax.set_xlabel('Jenis Keanggotaan')
ax.set_ylabel('Rata-Rata Jml Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

user_table = pd.DataFrame({
    'Jenis Keanggotaan': user_labels,
    'Rata-Rata Jml Penyewaan Sepeda': user_avg.values })
user_table['Rata-Rata Jml Penyewaan Sepeda'] = user_table['Rata-Rata Jml Penyewaan Sepeda'].round(0)
st.write(user_table)

# Rata-rata Penyewaan Sepeda berdasarkan Kategori Windspeed
st.subheader('Rata-Rata Penyewaan Sepeda berdasarkan Kategori Windspeed')

windspeed_bins = [0, 0.1, 0.3, 0.5, 1]  # Rentang kecepatan angin (windspeed)
windspeed_labels = ['Low', 'Medium', 'High', 'Very High']

filtered_df['windspeed_category'] = pd.cut(filtered_df['windspeed'], bins=windspeed_bins, labels=windspeed_labels)
average_cnt_by_windspeed = filtered_df.groupby('windspeed_category', observed=False)['cnt'].mean()

fig, ax = plt.subplots(figsize=(6, 5))
colors = sns.color_palette("Greys", len(average_cnt_by_windspeed))
sns.barplot(x=average_cnt_by_windspeed.index, y=average_cnt_by_windspeed.values, palette=colors, hue=average_cnt_by_windspeed.index, legend=False)
ax.set_xlabel('Kategori Windspeed')
ax.set_ylabel('Rata Rata Jml Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

windspeed_table = pd.DataFrame({
    'Kategori Windspeed': windspeed_labels,
    'Rata-Rata Penyewaan Sepeda': average_cnt_by_windspeed.values
})
windspeed_table['Rata-Rata Penyewaan Sepeda'] = windspeed_table['Rata-Rata Penyewaan Sepeda'].round(0)
st.write(windspeed_table)

# Rata-rata Penyewaan Sepeda berdasarkan Kategori Humidity
st.subheader('Rata-Rata Penyewaan Sepeda berdasarkan Kategori Humidity')

hum_bins = [0, 0.4, 0.7, 1]  # Rentang kelembapan (hum)
hum_labels = ['Low', 'Medium', 'High']

filtered_df['hum_category'] = pd.cut(filtered_df['hum'], bins=hum_bins, labels=hum_labels)
average_cnt_by_hum = filtered_df.groupby('hum_category', observed=False)['cnt'].mean()

fig, ax = plt.subplots(figsize=(6, 5))
colors = sns.color_palette("Greens", len(average_cnt_by_hum))
sns.barplot(x=average_cnt_by_hum.index, y=average_cnt_by_hum.values, palette=colors, hue=average_cnt_by_hum.index, legend=False)
ax.set_xlabel('Kategori Humidity')
ax.set_ylabel('Rata-Rata Jml Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

humidity_table = pd.DataFrame({
    'Kategori Humidity': hum_labels,
    'Rata-Rata Penyewaan Sepeda': average_cnt_by_hum.values
})
humidity_table['Rata-Rata Penyewaan Sepeda'] = humidity_table['Rata-Rata Penyewaan Sepeda'].round(0)
st.write(humidity_table)

# Rata-rata Penyewaan Sepeda berdasarkan Kategori Temperature
st.subheader('Rata-Rata Penyewaan Sepeda berdasarkan Kategori Temperature')

temp_bins = [0, 0.3, 0.6, 0.8, 1]  # Rentang suhu (temp)
temp_labels = ['Low', 'Medium', 'High', 'Very High']

filtered_df['temp_category'] = pd.cut(filtered_df['temp'], bins=temp_bins, labels=temp_labels)
average_cnt_by_temp = filtered_df.groupby('temp_category', observed=False)['cnt'].mean()

fig, ax = plt.subplots(figsize=(6, 5))
colors = sns.color_palette("Oranges", len(average_cnt_by_temp))
sns.barplot(x=average_cnt_by_temp.index, y=average_cnt_by_temp.values, palette=colors, hue=average_cnt_by_temp.index, legend=False)
ax.set_xlabel('Kategori Temperature')
ax.set_ylabel('Rata-Rata Jml Penyewaan Sepeda')
plt.tight_layout()
st.pyplot(fig)

temperature_table = pd.DataFrame({
    'Kategori Temperature': temp_labels,
    'Rata-Rata Penyewaan Sepeda': average_cnt_by_temp.values
})
temperature_table['Rata-Rata Penyewaan Sepeda'] = temperature_table['Rata-Rata Penyewaan Sepeda'].round(0)
st.write(temperature_table)
