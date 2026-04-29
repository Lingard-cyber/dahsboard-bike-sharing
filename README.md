# 🚲 Bike Sharing Data Analysis Dashboard

## Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment
mkdir proyek_analisis_data
cd proyek_analisis_data
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt

## Menjalankan Dashboard
python -m streamlit run dashboard/dashboard.py

Dashboard akan terbuka di browser pada `http://localhost:8501/`.

## Fitur Dashboard

- **📊 KPI Metrics** — Total penyewaan, rata-rata harian, jumlah pengguna casual & registered.
- **🌤️ Filter Interaktif** — Filter berdasarkan tanggal, musim, kondisi cuaca, dan tipe hari (kerja/libur).
- **📈 Visualisasi** — Bar chart, scatter plot, area chart, stacked bar chart, dan trend line.
- **💡 Insight** — Penjelasan insight untuk setiap pertanyaan bisnis.

