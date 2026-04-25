import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="🚲 Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== CUSTOM CSS ========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .main { background-color: #0e1117; }

    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #252b3b 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.15);
    }
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #818cf8, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0 4px 0;
    }
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
    }
    .metric-delta {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #34d399;
        font-weight: 500;
    }
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
    }
    .insight-box {
        background: linear-gradient(135deg, #1e293b 0%, #1a1f2e 100%);
        border-left: 4px solid #6366f1;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
        font-family: 'Inter', sans-serif;
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0f1318 100%);
    }
</style>
""", unsafe_allow_html=True)

# ======================== LOAD DATA ========================
@st.cache_data
def load_data():
    script_dir = Path(__file__).parent
    df = pd.read_csv(script_dir / "main_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# ======================== SIDEBAR FILTERS ========================
with st.sidebar:
    st.markdown("## 🚲 Bike Sharing")
    st.markdown("##### Dashboard Analisis Data")
    st.markdown("---")

    # Date range filter
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    start_date, end_date = st.date_input(
        "📅 Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Season filter
    season_options = df["season"].unique().tolist()
    selected_seasons = st.multiselect(
        "🌤️ Musim", season_options, default=season_options
    )

    # Weather filter
    weather_options = df["weather_condition"].unique().tolist()
    selected_weather = st.multiselect(
        "🌦️ Kondisi Cuaca", weather_options, default=weather_options
    )

    # Working day filter
    workday_filter = st.radio(
        "🗓️ Tipe Hari",
        ["Semua", "Hari Kerja", "Hari Libur"],
        index=0
    )

    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; color:#64748b; font-size:0.75rem;'>"
        "Dashboard by La Rayan<br>Dicoding Submission</p>",
        unsafe_allow_html=True
    )

# ======================== APPLY FILTERS ========================
filtered = df[
    (df["date"].dt.date >= start_date) &
    (df["date"].dt.date <= end_date) &
    (df["season"].isin(selected_seasons)) &
    (df["weather_condition"].isin(selected_weather))
]

if workday_filter == "Hari Kerja":
    filtered = filtered[filtered["workingday"] == 1]
elif workday_filter == "Hari Libur":
    filtered = filtered[filtered["workingday"] == 0]

# ======================== HEADER ========================
st.markdown(
    "<h1 style='text-align:center; font-family:Inter; "
    "background:linear-gradient(135deg,#818cf8,#6366f1,#4f46e5); "
    "-webkit-background-clip:text; -webkit-text-fill-color:transparent; "
    "font-size:2.5rem; margin-bottom:4px;'>"
    "🚲 Bike Sharing Dashboard</h1>"
    "<p style='text-align:center; color:#94a3b8; font-family:Inter; "
    "font-size:1rem; margin-bottom:32px;'>"
    "Analisis Pola Penyewaan Sepeda 2011–2012</p>",
    unsafe_allow_html=True
)

# ======================== KPI METRICS ========================
total_rentals = filtered["total_rentals"].sum()
total_casual = filtered["casual_users"].sum()
total_registered = filtered["registered_users"].sum()
avg_daily = filtered["total_rentals"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Penyewaan</div>
        <div class="metric-value">{total_rentals:,.0f}</div>
        <div class="metric-delta">📊 Seluruh periode</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Rata-rata Harian</div>
        <div class="metric-value">{avg_daily:,.0f}</div>
        <div class="metric-delta">📈 Per hari</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Pengguna Casual</div>
        <div class="metric-value">{total_casual:,.0f}</div>
        <div class="metric-delta">🚶 {total_casual/max(total_rentals,1)*100:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Pengguna Registered</div>
        <div class="metric-value">{total_registered:,.0f}</div>
        <div class="metric-delta">🎫 {total_registered/max(total_rentals,1)*100:.1f}%</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ======================== CHART STYLE ========================
COLORS = {
    "primary": "#6366f1",
    "secondary": "#818cf8",
    "accent": "#a78bfa",
    "success": "#34d399",
    "warning": "#fbbf24",
    "danger": "#f87171",
    "bg": "#0e1117",
    "card": "#1a1f2e",
    "text": "#e2e8f0",
    "muted": "#94a3b8",
}

SEASON_COLORS = {
    "Spring": "#34d399",
    "Summer": "#fbbf24",
    "Fall": "#fb923c",
    "Winter": "#60a5fa",
}

plt.rcParams.update({
    "figure.facecolor": COLORS["bg"],
    "axes.facecolor": COLORS["card"],
    "axes.edgecolor": "#334155",
    "axes.labelcolor": COLORS["text"],
    "text.color": COLORS["text"],
    "xtick.color": COLORS["muted"],
    "ytick.color": COLORS["muted"],
    "grid.color": "#1e293b",
    "grid.alpha": 0.5,
    "font.family": "sans-serif",
})

# ========================================================
# PERTANYAAN 1: Pola penggunaan berdasarkan musim & hari
# ========================================================
st.markdown(
    '<div class="section-header">📊 Pertanyaan 1: Pola Penyewaan Berdasarkan Musim & Hari Kerja</div>',
    unsafe_allow_html=True
)

col_a, col_b = st.columns(2)

with col_a:
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    season_data = (
        filtered.groupby("season")["total_rentals"]
        .mean()
        .reindex(["Spring", "Summer", "Fall", "Winter"])
    )
    bars = ax1.bar(
        season_data.index, season_data.values,
        color=[SEASON_COLORS.get(s, COLORS["primary"]) for s in season_data.index],
        edgecolor="none", width=0.6, zorder=3
    )
    for bar, val in zip(bars, season_data.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                 f'{val:,.0f}', ha='center', va='bottom',
                 fontsize=11, fontweight='bold', color=COLORS["text"])
    ax1.set_title("Rata-rata Penyewaan per Musim", fontsize=14, fontweight="bold", pad=15)
    ax1.set_ylabel("Rata-rata Penyewaan", fontsize=11)
    ax1.set_xlabel("")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.set_axisbelow(True)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig1)
    plt.close(fig1)

with col_b:
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    pivot_data = filtered.pivot_table(
        values="total_rentals", index="season", columns="workingday",
        aggfunc="mean"
    ).reindex(["Spring", "Summer", "Fall", "Winter"])
    x = np.arange(len(pivot_data.index))
    w = 0.35
    if 1 in pivot_data.columns:
        ax2.bar(x - w/2, pivot_data[1], w, label="Hari Kerja",
                color=COLORS["primary"], edgecolor="none", zorder=3)
    if 0 in pivot_data.columns:
        ax2.bar(x + w/2, pivot_data[0], w, label="Hari Libur",
                color=COLORS["success"], edgecolor="none", zorder=3)
    ax2.set_xticks(x)
    ax2.set_xticklabels(pivot_data.index)
    ax2.set_title("Hari Kerja vs Libur per Musim", fontsize=14, fontweight="bold", pad=15)
    ax2.set_ylabel("Rata-rata Penyewaan", fontsize=11)
    ax2.legend(frameon=False, fontsize=10)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    ax2.set_axisbelow(True)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig2)
    plt.close(fig2)

st.markdown(
    '<div class="insight-box">'
    '💡 <b>Insight:</b> Musim <b>Fall (Gugur)</b> memiliki rata-rata penyewaan tertinggi, '
    'disusul Summer dan Winter. Spring memiliki penyewaan terendah. '
    'Pada hari kerja, penyewaan cenderung lebih stabil karena didominasi commuter (registered), '
    'sedangkan di hari libur, pengguna casual meningkat signifikan.'
    '</div>',
    unsafe_allow_html=True
)

# ========================================================
# PERTANYAAN 2: Pengaruh cuaca terhadap penyewaan
# ========================================================
st.markdown(
    '<div class="section-header">🌦️ Pertanyaan 2: Pengaruh Faktor Cuaca terhadap Penyewaan</div>',
    unsafe_allow_html=True
)

col_c, col_d = st.columns(2)

with col_c:
    fig3, axes3 = plt.subplots(1, 3, figsize=(14, 4.5))
    weather_vars = [
        ("temperature", "Suhu (normalized)", COLORS["warning"]),
        ("humidity", "Kelembaban (normalized)", COLORS["secondary"]),
        ("wind_speed", "Kecepatan Angin (normalized)", COLORS["success"]),
    ]
    for ax, (col, label, color) in zip(axes3, weather_vars):
        ax.scatter(filtered[col], filtered["total_rentals"],
                   alpha=0.4, s=15, color=color, edgecolors="none")
        z = np.polyfit(filtered[col], filtered["total_rentals"], 1)
        p = np.poly1d(z)
        x_line = np.linspace(filtered[col].min(), filtered[col].max(), 100)
        ax.plot(x_line, p(x_line), color="#f87171", linewidth=2, linestyle="--")
        corr = filtered[col].corr(filtered["total_rentals"])
        ax.set_title(f"{label}\nr = {corr:.3f}", fontsize=10, fontweight="bold")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid(True, linestyle="--", alpha=0.2)
        sns.despine(left=True, bottom=True)
    fig3.suptitle("Korelasi Faktor Cuaca vs Total Penyewaan",
                  fontsize=13, fontweight="bold", y=1.02)
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

with col_d:
    fig4, ax4 = plt.subplots(figsize=(8, 4.5))
    weather_avg = (
        filtered.groupby("weather_condition")["total_rentals"]
        .mean()
        .sort_values(ascending=True)
    )
    colors_wc = [COLORS["success"], COLORS["warning"], COLORS["danger"]]
    bars4 = ax4.barh(weather_avg.index, weather_avg.values,
                     color=colors_wc[:len(weather_avg)],
                     edgecolor="none", height=0.5, zorder=3)
    for bar, val in zip(bars4, weather_avg.values):
        ax4.text(val + 50, bar.get_y() + bar.get_height()/2,
                 f'{val:,.0f}', va='center', fontsize=11,
                 fontweight='bold', color=COLORS["text"])
    ax4.set_title("Rata-rata Penyewaan per Kondisi Cuaca",
                  fontsize=14, fontweight="bold", pad=15)
    ax4.set_xlabel("Rata-rata Penyewaan", fontsize=11)
    ax4.grid(axis="x", linestyle="--", alpha=0.3)
    ax4.set_axisbelow(True)
    sns.despine(left=True, bottom=True)
    fig4.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

st.markdown(
    '<div class="insight-box">'
    '💡 <b>Insight:</b> <b>Suhu</b> memiliki korelasi positif terkuat terhadap penyewaan. '
    'Semakin hangat cuaca, semakin banyak orang menyewa sepeda. '
    '<b>Kelembaban</b> dan <b>kecepatan angin</b> berkorelasi negatif — cuaca lembap dan berangin '
    'mengurangi minat bersepeda. Cuaca <b>Clear</b> menghasilkan penyewaan tertinggi, '
    'sementara <b>Light Snow/Rain</b> menurunkan penyewaan secara drastis.'
    '</div>',
    unsafe_allow_html=True
)

# ========================================================
# PERTANYAAN 3: Perbandingan Casual vs Registered
# ========================================================
st.markdown(
    '<div class="section-header">👥 Pertanyaan 3: Tren Pengguna Casual vs Registered</div>',
    unsafe_allow_html=True
)

col_e, col_f = st.columns(2)

with col_e:
    fig5, ax5 = plt.subplots(figsize=(10, 5))
    monthly = (
        filtered.groupby(filtered["date"].dt.to_period("M"))
        .agg(casual=("casual_users", "sum"), registered=("registered_users", "sum"))
    )
    monthly.index = monthly.index.astype(str)
    ax5.fill_between(range(len(monthly)), monthly["registered"],
                     alpha=0.3, color=COLORS["primary"], label="Registered")
    ax5.plot(range(len(monthly)), monthly["registered"],
             color=COLORS["primary"], linewidth=2, marker="o", markersize=4)
    ax5.fill_between(range(len(monthly)), monthly["casual"],
                     alpha=0.3, color=COLORS["success"], label="Casual")
    ax5.plot(range(len(monthly)), monthly["casual"],
             color=COLORS["success"], linewidth=2, marker="o", markersize=4)
    step = max(1, len(monthly) // 12)
    ax5.set_xticks(range(0, len(monthly), step))
    ax5.set_xticklabels([monthly.index[i] for i in range(0, len(monthly), step)],
                        rotation=45, ha="right", fontsize=8)
    ax5.set_title("Tren Bulanan: Casual vs Registered", fontsize=14, fontweight="bold", pad=15)
    ax5.set_ylabel("Jumlah Penyewaan", fontsize=11)
    ax5.legend(frameon=False, fontsize=10, loc="upper left")
    ax5.grid(True, linestyle="--", alpha=0.3)
    sns.despine(left=True, bottom=True)
    fig5.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

with col_f:
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_ratio = filtered.groupby("month").agg(
        casual=("casual_users", "sum"),
        registered=("registered_users", "sum")
    )
    month_ratio = month_ratio.reindex(month_order).dropna()
    total_m = month_ratio["casual"] + month_ratio["registered"]
    casual_pct = month_ratio["casual"] / total_m * 100
    registered_pct = month_ratio["registered"] / total_m * 100

    ax6.bar(month_ratio.index, registered_pct, label="Registered",
            color=COLORS["primary"], edgecolor="none", zorder=3)
    ax6.bar(month_ratio.index, casual_pct, bottom=registered_pct,
            label="Casual", color=COLORS["success"], edgecolor="none", zorder=3)
    ax6.set_title("Proporsi Casual vs Registered per Bulan",
                  fontsize=14, fontweight="bold", pad=15)
    ax6.set_ylabel("Persentase (%)", fontsize=11)
    ax6.legend(frameon=False, fontsize=10, loc="upper right")
    ax6.set_ylim(0, 105)
    ax6.grid(axis="y", linestyle="--", alpha=0.3)
    ax6.set_axisbelow(True)
    sns.despine(left=True, bottom=True)
    fig6.tight_layout()
    st.pyplot(fig6)
    plt.close(fig6)

st.markdown(
    '<div class="insight-box">'
    '💡 <b>Insight:</b> Pengguna <b>registered</b> selalu mendominasi (~80%) dibanding casual (~20%). '
    'Proporsi pengguna casual meningkat di bulan-bulan musim panas (Jun–Sep) karena cuaca mendukung '
    'aktivitas rekreasi. Tahun 2012 menunjukkan pertumbuhan signifikan untuk kedua tipe pengguna '
    'dibanding 2011, menandakan adopsi bike-sharing yang meningkat.'
    '</div>',
    unsafe_allow_html=True
)

# ======================== DAILY TREND ========================
st.markdown(
    '<div class="section-header">📈 Tren Penyewaan Harian</div>',
    unsafe_allow_html=True
)

fig7, ax7 = plt.subplots(figsize=(16, 5))
ax7.plot(filtered["date"], filtered["total_rentals"],
         color=COLORS["primary"], linewidth=1, alpha=0.6)
# Moving average
if len(filtered) >= 30:
    ma = filtered.set_index("date")["total_rentals"].rolling(30).mean()
    ax7.plot(ma.index, ma.values, color=COLORS["warning"],
             linewidth=2.5, label="30-day Moving Avg")
ax7.set_title("Tren Penyewaan Sepeda Harian", fontsize=14, fontweight="bold", pad=15)
ax7.set_ylabel("Total Penyewaan", fontsize=11)
ax7.set_xlabel("")
ax7.legend(frameon=False, fontsize=10)
ax7.grid(True, linestyle="--", alpha=0.3)
sns.despine(left=True, bottom=True)
fig7.tight_layout()
st.pyplot(fig7)
plt.close(fig7)

# ======================== FOOTER ========================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b; font-family:Inter; font-size:0.8rem;'>"
    "🚲 Bike Sharing Dashboard — Proyek Analisis Data Dicoding | La Rayan © 2026</p>",
    unsafe_allow_html=True
)