import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

total_rentals_by_weather = day_df.groupby('weathersit')['cnt'].sum()
weather_labels = ['Clear', 'Mist + Cloudy', 'Light Precipitation']

plt.figure(figsize=(8, 6))
plt.pie(total_rentals_by_weather, labels=weather_labels, autopct='%1.1f%%', startangle=140)
plt.title('Distribusi Jumlah Total Penyewaan Sepeda Berdasarkan Cuaca')
st.write(""" ## Dashboard Analisis Bike Sharing """)
st.pyplot()
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

selected_year = st.selectbox('Pilih Tahun:', [2011, 2012])
filtered_data = day_df[day_df['dteday'].dt.year == selected_year]
monthly_rentals = filtered_data.groupby(filtered_data['dteday'].dt.month)['cnt'].sum()
plt.figure(figsize=(10, 6))
plt.plot(monthly_rentals.index, monthly_rentals.values, marker='o', linestyle='-', color='b')
plt.title(f'Tren Penyewaan Sepeda Bulanan pada Tahun {selected_year}')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.grid(True)
plt.xticks(ticks=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

st.pyplot()

# Menghitung total penyewaan sepeda berdasarkan musim
total_rentals_by_season = day_df.groupby('season')['cnt'].sum()

# Menentukan musim dengan jumlah penyewaan tertinggi
musim_terbanyak = total_rentals_by_season.idxmax()

plt.figure(figsize=(8, 6))
plt.bar(total_rentals_by_season.index, total_rentals_by_season.values, color='skyblue')
plt.xlabel('Musim')
plt.ylabel('Total Penyewaan Sepeda')
plt.title(f'Total Penyewaan Sepeda Berdasarkan Musim (Terbanyak: Musim {musim_terbanyak})')
plt.xticks(ticks=[1, 2, 3, 4], labels=['Spring', 'Summer', 'Fall', 'Winter'])

plt.savefig('musim_penyewaan_sepeda.png')

st.subheader(f'Musim dengan Jumlah Penyewaan Sepeda Tertinggi: {musim_terbanyak}')
st.image('musim_penyewaan_sepeda.png')

quiet_hours = hour_df[(hour_df['hr'] >= 1) & (hour_df['hr'] <= 4)]
busy_hours = hour_df[(hour_df['hr'] >= 13) & (hour_df['hr'] <= 16)]
total_rentals_quiet_hours = quiet_hours['cnt'].sum()
total_rentals_busy_hours = busy_hours['cnt'].sum()

# Menampilkan judul dashboard
st.title('Perbandingan Penyewaan Sepeda pada Jam-Jam Sepi dan Ramai')

# Menampilkan deskripsi
st.write('Perbandingan jumlah penyewaan sepeda pada jam-jam sepi (1-4 AM) dan jam ramai (1-4 PM).')

# Menampilkan visualisasi pie chart
labels = ['Jam Sepi (1-4 AM)', 'Jam Ramai (1-4 PM)']
sizes = [total_rentals_quiet_hours, total_rentals_busy_hours]
colors = ['#ff9999', '#66b3ff']
explode = (0.1, 0)  # Menyoroti potongan 'Jam Sepi'
plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Perbandingan Penyewaan Sepeda pada Jam-Jam Sepi dan Ramai')
st.pyplot()