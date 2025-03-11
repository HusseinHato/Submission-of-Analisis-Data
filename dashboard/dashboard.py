import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

st.title("Analisis Bike Sharing Dataset")
st.write("Analisis data bike sharing untuk mengetahui pola permintaan sewa sepeda")

col1, col2 = st.columns(2)
with col1:
    st.write("Jumlah Data harian :")
    st.write(len(day_df))
with col2:
    st.write("Jumlah Data per jam :")
    st.write(len(hour_df))

st.subheader("Pengaruh Variabel Cuaca terhadap tingkat permintaan sewa")

# List variabel cuaca dan warnanya
weather_vars = [
    ("temp", "Temperatur (Normalized)", "#FFB74D"),
    ("hum", "Kelembaban (Normalized)", "#64B5F6"),
    ("windspeed", "Kecepatan Angin (Normalized)", "#81C784")
]

# Loop untuk membuat scatter plot per variabel cuaca
for var, label, color in weather_vars:
    st.subheader(f"{label} vs. Jumlah Sewa")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(ax=ax, x=hour_df[var], y=hour_df['cnt'], color=color, alpha=0.6)
    ax.set_xlabel(label)
    ax.set_ylabel("Jumlah Sewa")
    st.pyplot(fig)

# Membandingkan jumlah sewa antara hari kerja dan akhir pekan
st.subheader("Rata-rata Jumlah Sewa Sepeda: Hari Kerja vs. Akhir Pekan")
df_grouped = hour_df.groupby('workingday')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(ax=ax, x=df_grouped['workingday'], y=df_grouped['cnt'], palette=["#64B5F6", "#FFB74D"], legend=False)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Akhir Pekan', 'Hari Kerja'])
ax.set_title('Rata-rata Jumlah Sewa Sepeda: Hari Kerja vs. Akhir Pekan')
ax.set_xlabel('Kategori')
ax.set_ylabel('Rata-rata Jumlah Sewa')
ax.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig)

# Rata-rata jumlah sewa per jam
st.subheader("Rata-rata Jumlah Sewa Sepanjang Hari")
hourly_avg = hour_df.groupby('hr')['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(ax=ax, x=hourly_avg['hr'], y=hourly_avg['cnt'], marker='o', linestyle='-', color="#FF7043")
ax.set_xticks(range(0, 24))
ax.set_title('Rata-rata Jumlah Sewa Sepanjang Hari')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Sewa')
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# Perbandingan jumlah sewa per jam antara hari kerja dan akhir pekan
st.subheader("Perbandingan Jumlah Sewa: Hari Kerja vs. Akhir Pekan/Liburan")
hourly_workingday = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_workingday, x='hr', y='cnt', hue='workingday', marker='o', palette=["#FFB74D", "#64B5F6"], legend="auto", ax=ax)
ax.set_xticks(range(0, 24))
ax.set_title('Perbandingan Jumlah Sewa: Hari Kerja vs. Akhir Pekan/Liburan')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Sewa')
ax.grid(True, linestyle='--', alpha=0.5)
st.pyplot(fig)

# Menandai jam sibuk dalam bar chart
st.subheader("Rata-rata Jumlah Sewa Sepanjang Hari dengan Jam Sibuk")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(ax=ax, x=hourly_avg['hr'], y=hourly_avg['cnt'], palette=["#90CAF9" if (7 <= hr <= 9 or 17 <= hr <= 19) else "#B0BEC5" for hr in hourly_avg['hr']])
ax.set_xticks(range(0, 24))
ax.set_title('Rata-rata Jumlah Sewa Sepanjang Hari')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Sewa')
ax.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig)

# Segmentasi jam berdasarkan pola permintaan
st.subheader("Segmentasi Jam Berdasarkan Pola Permintaan")
hourly_avg['demand_category'] = hourly_avg['cnt'].apply(lambda x: 'Low Demand' if x < hourly_avg['cnt'].quantile(0.33) else ('Medium Demand' if x < hourly_avg['cnt'].quantile(0.66) else 'High Demand'))

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(ax=ax, x=hourly_avg['hr'], y=hourly_avg['cnt'], hue=hourly_avg['demand_category'], palette={'Low Demand': '#64B5F6', 'Medium Demand': '#FFB74D', 'High Demand': '#E57373'})
ax.set_xticks(range(0, 24))
ax.set_title('Segmentasi Jam Berdasarkan Pola Permintaan')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Rata-rata Jumlah Sewa')
ax.legend(title="Kategori Permintaan")
ax.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig)