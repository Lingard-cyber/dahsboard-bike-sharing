# 🚲 Bike Sharing Data Analysis Dashboard

## Deskripsi Proyek

Proyek ini merupakan analisis data penyewaan sepeda (*bike sharing*) menggunakan dataset dari Capital Bikeshare System (Washington D.C.) periode **2011–2012**. Dashboard interaktif dibangun menggunakan **Streamlit** untuk memvisualisasikan insight dari data.

## Setup Environment
pip install -r requirements.txt

## Menjalankan Dashboard
python -m streamlit run dashboard/dashboard.py

Dashboard akan terbuka di browser pada `http://localhost:8501/`.

## Fitur Dashboard

- **📊 KPI Metrics** — Total penyewaan, rata-rata harian, jumlah pengguna casual & registered.
- **🌤️ Filter Interaktif** — Filter berdasarkan tanggal, musim, kondisi cuaca, dan tipe hari (kerja/libur).
- **📈 Visualisasi** — Bar chart, scatter plot, area chart, stacked bar chart, dan trend line.
- **💡 Insight** — Penjelasan insight untuk setiap pertanyaan bisnis.

## Kesimpulan

1. **Musim Fall (Gugur)** memiliki rata-rata penyewaan tertinggi. Pada hari kerja, penyewaan lebih stabil karena didominasi commuter, sedangkan di hari libur pengguna casual meningkat signifikan.
2. **Suhu** memiliki korelasi positif terkuat terhadap penyewaan sepeda. Kelembaban dan kecepatan angin berkorelasi negatif. Cuaca cerah (*Clear*) menghasilkan penyewaan paling tinggi.
3. **Pengguna registered** selalu mendominasi (~80%). Proporsi casual meningkat di musim panas (Jun–Sep). Tahun 2012 menunjukkan pertumbuhan signifikan dibanding 2011.
