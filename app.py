# -*- coding: utf-8 -*-
# Auto-generated from your Jupyter notebook by ChatGPT
# This Streamlit app runs cells top-to-bottom and patches common display functions
import streamlit as st

st.set_page_config(page_title="Notebook App", layout="wide")

# ---- Display helpers to make notebook-style output appear in Streamlit ----
import types

# Patch matplotlib plt.show() -> st.pyplot
try:
    import matplotlib.pyplot as plt
    def _plt_show(*args, **kwargs):
        st.pyplot(plt.gcf(), clear_figure=True)
    plt.show = _plt_show
except Exception:
    pass

# Patch plotly.io.show -> st.plotly_chart
try:
    import plotly.io as pio
    def _pio_show(fig, *args, **kwargs):
        try:
            import plotly.graph_objs as go
            if hasattr(fig, "to_dict") or hasattr(fig, "data"):
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write(fig)
        except Exception:
            st.write(fig)
    pio.show = _pio_show
except Exception:
    pass

# Patch IPython.display.display -> st.write
try:
    import builtins
    def display(obj=None, **kwargs):
        if obj is None:
            return
        # Special-casing pandas DataFrame
        try:
            import pandas as pd
            if isinstance(obj, pd.DataFrame):
                st.dataframe(obj, use_container_width=True)
                return
        except Exception:
            pass
        # Plotly figures (if pio.show wasn't used)
        try:
            import plotly.graph_objs as go
            if hasattr(obj, "to_dict") or hasattr(obj, "data"):
                st.plotly_chart(obj, use_container_width=True)
                return
        except Exception:
            pass
        st.write(obj)
    builtins.display = display
except Exception:
    pass

# Niceties
st.caption("This app was auto-generated. You can tailor the UI (sidebar inputs, tabs, etc.) later.")
st.divider()

# === Cell 1 ===
# 1. Install Streamlit dan pyngrok


# === Cell 2 ===
import pandas as pd
import os
import pickle
import streamlit as st
import pandas as pd
import pickle
import os
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
import calendar
import locale
import plotly.graph_objects as go
from datetime import timedelta

# ----------------------------
# Mapping nama hari ke bahasa Indonesia
# ----------------------------
hari_mapping = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu"
}

bulan_mapping = {
    "January": "Januari",
    "February": "Februari",
    "March": "Maret",
    "April": "April",
    "May": "Mei",
    "June": "Juni",
    "July": "Juli",
    "August": "Agustus",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Desember"
}

def format_tanggal_indonesia(tanggal):
    tgl = pd.to_datetime(tanggal)
    hari = hari_mapping[tgl.strftime("%A")]
    bulan = bulan_mapping[tgl.strftime("%B")]
    return f"{hari}, {tgl.day:02d} {bulan} {tgl.year}"

def format_nohari_indonesia(tanggal):
    tgl = pd.to_datetime(tanggal)
    bulan = bulan_mapping[tgl.strftime("%B")]
    return f"{tgl.day:02d} {bulan} {tgl.year}"

def aggregate_weekly(df, start_date_col, value_col):
    df = df.copy()
    df[start_date_col] = pd.to_datetime(df[start_date_col])
    results = []

    start_date = df[start_date_col].min()
    end_date = df[start_date_col].max()

    current_start = start_date
    while current_start <= end_date:
        current_end = current_start + timedelta(days=6)
        mask = (df[start_date_col] >= current_start) & (df[start_date_col] <= current_end)
        total = df.loc[mask, value_col].sum()
        results.append({
            'periode_awal': current_start,
            'periode_akhir': current_end,
            'total': total
        })
        current_start = current_end + timedelta(days=1)

    return pd.DataFrame(results)

# Load data_dict.pkl
data_dict_path = "data_dict.pkl"
data_dict = {}
if os.path.exists(data_dict_path):
    try:
        with open(data_dict_path, "rb") as f:
            data_dict = pickle.load(f)
    except Exception as e:
        st.error(f"❌ Gagal memuat file pickle: {e}")
else:
    st.error(f"❌ File '{data_dict_path}' tidak ditemukan. Silakan pastikan file tersedia di direktori kerja.")

# ===== MENU SELECTION DI SIDEBAR =====
if "menu" not in st.session_state:
    st.session_state.menu = "Data"

# Label manual pakai markdown + styling
st.sidebar.markdown(
    """
    <div style="
        font-weight: 500;
        font-size: 22px;
        color: #1f2937;
        margin-bottom: 8px;
    ">
        🗂️ Menu Pilihan
    </div>
    """,
    unsafe_allow_html=True,
)

# Selectbox tanpa label bawaan
menu = st.sidebar.selectbox(
    label="",
    options=["Data", "Prediksi"],
    index=0 if st.session_state.get("menu", "Data") == "Data" else 1,
    key="menu",
)



if menu == "Data":
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        body { background-color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header: Judul + selectbox file di kanan atas satu baris
    col_title, col_file = st.columns([3, 1])
    with col_title:
        st.write("## Dashboard Data Keseluruhan Prediksi")
    with col_file:
        selected_file = st.selectbox(
            "Pilih file data",
            options=list(data_dict.keys()) if data_dict else [],
            key="data_file"
        )

    if selected_file and selected_file in data_dict:
      df = data_dict[selected_file].copy()
      df["Tanggal"] = pd.to_datetime(df["Tanggal"])

      # Pastikan kolom prediksi ada
      if "Prediksi" not in df.columns:
          st.error("Kolom 'Prediksi' tidak ditemukan di data.")
      else:
          df["Prediksi"] = pd.to_numeric(df["Prediksi"], errors="coerce")
          prediksi_series = df["Prediksi"]
          max_val = round(df["Prediksi"].max())
          min_val = round(df["Prediksi"].min())
          mean_val = round(df["Prediksi"].mean())
          std_val = round(df["Prediksi"].std())

          # Ambil tanggal saat nilai max/min terjadi
          max_idx = df["Prediksi"].idxmax()
          min_idx = df["Prediksi"].idxmin()

          max_date = pd.to_datetime(df.loc[max_idx, "Tanggal"])
          min_date = pd.to_datetime(df.loc[min_idx, "Tanggal"])
          max_date_str = format_tanggal_indonesia(max_date)
          min_date_str = format_tanggal_indonesia(min_date)

          col1, col2, col3, col4 = st.columns(4)
          def render_stat(col, title, value, tanggal_str=None):
            tanggal_html = f"<div style='font-size:12px; margin-top:4px; color:gray;'>{tanggal_str}</div>" if tanggal_str else ""
            col.markdown(
                f"""
                <div style='
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                '>
                    <div style='font-weight: bold; font-size: 20px;'>{title}</div>
                    <div style='font-size: 28px; font-weight: bold;'>{value}</div>
                    {tanggal_html}
                </div>
                """,
                unsafe_allow_html=True,
            )

          render_stat(col1, "Maksimum", round(df["Prediksi"].max()), format_tanggal_indonesia(max_date))
          render_stat(col2, "Minimum", round(df["Prediksi"].min()), format_tanggal_indonesia(min_date))
          render_stat(col3, "Rata-rata", round(df["Prediksi"].mean()))
          render_stat(col4, "Standar Deviasi", round(df["Prediksi"].std()))

          st.markdown("---")

          col_left, col_right = st.columns([4, 2])

          with col_left:
            st.markdown("#### Grafik Data Prediksi")
            fig = px.line(
                df,
                x="Tanggal",
                y="Prediksi",
                title="Grafik Prediksi",
                labels={"Tanggal": "Tanggal", "Prediksi": "Nilai Prediksi"},
                template="plotly_white",
            )
            fig.update_traces(
                mode="lines",
                line=dict(color='#ABA9A9'),
                hovertemplate='<b>Prediksi:</b> %{y:.0f}<extra></extra>'
            )
            fig.update_layout(
                xaxis_tickangle=45,
                hoverlabel=dict(
                    bgcolor="rgba(70, 73, 91, 0.8)",  # warna latar belakang tooltip semi transparan ungu
                    font_size=14,
                    # borderwidth=2,
                    font_family="Arial",
                    font_color="white",
                ),
                dragmode="zoom",  # default drag mode untuk zoom
                margin=dict(l=40, r=40, t=40, b=40),
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True)

          with col_right:
              # Format tanggal + hari
                df["Tanggal_Format"] = df["Tanggal"].apply(format_tanggal_indonesia)

                # 5 nilai tertinggi
                top5 = df.nlargest(5, "Prediksi")[["Tanggal_Format", "Prediksi"]].copy()
                top5["Prediksi"] = top5["Prediksi"].round().astype(int)
                top5 = top5.reset_index(drop=True)
                top5.index = top5.index + 1

                # 5 nilai terendah
                bottom5 = df.nsmallest(5, "Prediksi")[["Tanggal_Format", "Prediksi"]].copy()
                bottom5["Prediksi"] = bottom5["Prediksi"].round().astype(int)
                bottom5 = bottom5.reset_index(drop=True)
                bottom5.index = bottom5.index + 1
                st.write("#### 5 Jumlah Penumpang Tertinggi")
                # st.table(top5.rename(columns={"Tanggal_Format": "Tanggal", "Prediksi": "Prediksi"}).reset_index(drop=True))
                st.dataframe(
                    top5.rename(columns={"Tanggal_Format": "Tanggal", "Prediksi": "Prediksi"}),
                    use_container_width=True
                )
                st.write("#### 5 Jumlah Penumpang Terendah")
                st.dataframe(
                    bottom5.rename(columns={"Tanggal_Format": "Tanggal", "Prediksi": "Prediksi"}),
                    use_container_width=True
                )



    else:
        st.info("Silakan pilih file data untuk melihat konten.")

elif menu == "Prediksi":
    st.title("📈 Dashboard Prediksi")



    col1, col2, col3 = st.columns([1, 2, 2])

    with col3:
        file_for_forecast = st.selectbox(
            "Pilih Koridor",
            options=list(data_dict.keys()) if data_dict else [],
        )

    with col1:
        if file_for_forecast and file_for_forecast in data_dict:
          df = data_dict[file_for_forecast].copy()
        # Ambil range tanggal dari data (pastikan kolom Tanggal sudah datetime)
        tanggal_min = df["Tanggal"].min()
        tanggal_max = df["Tanggal"].max()
        forecast_type = st.selectbox(
            "Jenis Prediksi",
            options=["Harian", "Mingguan", "Bulanan"],
            index=0,
        )

    with col2:
        if forecast_type == "Harian":
            # Pilih tanggal tunggal dengan batasan min dan max
            forecast_date = st.date_input(
                "Pilih Tanggal yang Diprediksi",
                min_value=tanggal_min,
                max_value=tanggal_max,
                value=tanggal_min,
            )

        elif forecast_type == "Mingguan":
            # Pilih 1 tanggal awal
            tanggal_awal = st.date_input(
                "Pilih Periode Awal Mingguan",
                value=tanggal_min,
                min_value=tanggal_min,
                max_value=tanggal_max - pd.Timedelta(days=6),
                help="Pilih tanggal awal periode mingguan"
            )

            # Tanggal akhir otomatis 6 hari setelahnya
            tanggal_akhir = tanggal_awal + pd.Timedelta(days=6)

            forecast_date = (tanggal_awal, tanggal_akhir)

        else:  # Bulanan
            # Buat list bulan unik dari df dalam format YYYY-MM
            bulan_unique = df["Tanggal"].dt.to_period("M").unique()

            # Mapping manual nama bulan Indonesia
            nama_bulan_id = {
                1: "Januari",
                2: "Februari",
                3: "Maret",
                4: "April",
                5: "Mei",
                6: "Juni",
                7: "Juli",
                8: "Agustus",
                9: "September",
                10: "Oktober",
                11: "November",
                12: "Desember"
            }

            # Buat dict mapping dari format YYYY-MM ke format Nama Bulan Tahun Indonesia
            bulan_mapping = {
                str(b): f"{nama_bulan_id[b.month]} {b.year}"
                for b in bulan_unique
            }

            # Gunakan nama bulan tahun sebagai opsi tampilan
            bulan_pilih_display = st.selectbox(
                "Pilih Bulan yang Diprediksi",
                options=list(bulan_mapping.values())
            )

            # Ambil kembali nilai asli (YYYY-MM) berdasarkan pilihan user
            bulan_pilih = [k for k, v in bulan_mapping.items() if v == bulan_pilih_display][0]

            forecast_date = bulan_pilih

    df = data_dict[file_for_forecast].copy()
    st.markdown("---")  # Pembatas

    row1_col1, row1_col2 = st.columns([4, 2])

    with row1_col1:
        # --- Ganti blok with row1_col1: dengan kode berikut ---
        st.subheader("📅 Hasil Prediksi Periode Terpilih")

        # pastikan kolom Tanggal bertipe datetime64[ns]
        df["Tanggal"] = pd.to_datetime(df["Tanggal"])
        df["Prediksi"] = [int(round(x)) for x in df["Prediksi"]]

        # mapping nama bulan id (dipakai untuk label)
        nama_bulan_id = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
            5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
            9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }

        def fmt_date_id(ts):
            ts = pd.Timestamp(ts)
            return f"{ts.day} {nama_bulan_id[ts.month]} {ts.year}"

        if forecast_type == "Harian":
            # pastikan tipe
            fd = pd.Timestamp(forecast_date)
            nilai_terpilih = df.loc[df["Tanggal"] == fd, "Prediksi"].values
            nilai_terpilih = int(nilai_terpilih[0]) if len(nilai_terpilih) > 0 else None

            # metric (atas)
            st.metric(
                label=format_tanggal_indonesia(fd),
                value=f"{nilai_terpilih:,}" if nilai_terpilih is not None else "Data tidak ditemukan"
            )

            # grafik ±5 hari
            start_date = fd - pd.Timedelta(days=5)
            end_date = fd + pd.Timedelta(days=5)
            df_range = df[(df["Tanggal"] >= start_date) & (df["Tanggal"] <= end_date)].sort_values("Tanggal")

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_range["Tanggal"], y=df_range["Prediksi"],
                mode="lines+markers", name="Prediksi",
                hovertemplate="%{x|%d %b %Y} : %{y:,}<extra></extra>"
            ))
            if nilai_terpilih is not None:
                fig.add_trace(go.Scatter(
                    x=[fd], y=[nilai_terpilih],
                    mode="markers", marker=dict(color="red", size=10),
                    name="Target",
                    hovertemplate="%{x|%d %b %Y} : %{y:,}<extra></extra>"
                ))

            # Buat label tanggal Indonesia, contoh format '12 Agu 2025'
            bulan_id = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

            ticktext = [
                f"{dt.day} {bulan_id[dt.month - 1]} {dt.year}"
                for dt in df_range["Tanggal"]
            ]

            tickvals = df_range["Tanggal"]  # posisi tick sesuai tanggal asli

            fig.update_layout(title="Pergerakan 5 Hari Sebelum & Sesudah",
                              xaxis_title="Tanggal", yaxis_title="Prediksi",
                              xaxis=dict(
                                        tickmode='array',
                                        tickvals=tickvals,
                                        ticktext=ticktext
                                    ))
            st.plotly_chart(fig, use_container_width=True)

        elif forecast_type == "Mingguan":
            start_date = pd.Timestamp(forecast_date[0])
            end_date = pd.Timestamp(forecast_date[1])

            nilai_terpilih = df[(df["Tanggal"] >= start_date) & (df["Tanggal"] <= end_date)]["Prediksi"].sum()

            st.metric(
                label=f"Periode {format_tanggal_indonesia(start_date)} - {format_tanggal_indonesia(end_date)}",
                value=f"{nilai_terpilih:,}"
            )


            week_starts = [start_date + pd.Timedelta(days=7 * i) for i in range(-5, 6)]
            week_sums = []
            for ws in week_starts:
                we = ws + pd.Timedelta(days=6)
                s = df[(df["Tanggal"] >= ws) & (df["Tanggal"] <= we)]["Prediksi"].sum()
                week_sums.append(int(s))

            colors_main = "rgba(100,150,200,0.8)"  # warna semua titik default
            color_focus = "crimson"  # warna fokus

            # Tentukan index fokus
            focus_index = 5  # posisi minggu fokus di week_starts
            # Buat label periode untuk hover
            hover_labels = [
                f"{start.strftime('%d %B %Y')} - {(start + pd.Timedelta(days=6)).strftime('%d %B %Y')}"
                for start in week_starts
            ]

            # Cari indeks minggu pertama yang nilai week_sums != 0
            first_nonzero_idx = next((i for i, val in enumerate(week_sums) if val != 0), 0)

            # Potong list mulai dari first_nonzero_idx
            week_starts_trim = week_starts[first_nonzero_idx:]
            week_sums_trim = week_sums[first_nonzero_idx:]
            hover_labels_trim = hover_labels[first_nonzero_idx:]

            focus_index_orig = 5
            focus_index_trim = max(0, focus_index_orig - first_nonzero_idx)
            if focus_index_trim >= len(week_starts_trim):
                focus_index_trim = len(week_starts_trim) - 1  # jika lebih dari panjang list, set ke akhir


            fig = go.Figure()

            # Trace garis + semua titik (warna default)
            fig.add_trace(go.Scatter(
                x=week_starts_trim,
                y=week_sums_trim,
                mode="lines+markers",
                line=dict(color=colors_main),
                marker=dict(color=colors_main, size=8),
                name="Jumlah per Minggu",
                hovertemplate="%{customdata}<br>%{y:,.0f}<extra></extra>",
                customdata=hover_labels_trim
            ))

            # Trace titik fokus (warna merah)
            fig.add_trace(go.Scatter(
                x=[week_starts_trim[focus_index_trim]],
                y=[week_sums_trim[focus_index_trim]],
                mode="markers",
                marker=dict(color=color_focus, size=10),
                name="Target",
                hovertemplate="%{customdata}<br>%{y:,.0f}<extra></extra>",
                customdata=hover_labels_trim
            ))

            # Buat label tanggal Indonesia, contoh format '12 Agu 2025'
            bulan_id = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

            ticktext = [
                f"{dt.day} {bulan_id[dt.month - 1]} {dt.year}"
                for dt in week_starts_trim
            ]

            tickvals = week_starts_trim  # posisi tick sesuai tanggal asli


            fig.update_layout(
                title="Grafik Prediksi Mingguan",
                xaxis_title="Minggu",
                yaxis_title="Total Prediksi",
                xaxis_tickangle=-45,
                xaxis=dict(
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=ticktext
                ),

                showlegend=False  # hilangkan legenda
            )
            st.plotly_chart(fig, use_container_width=True)


        else:  # Bulanan
            # Ambil total nilai untuk seluruh bulan yang ada di data
            df['Periode_Bulan'] = df['Tanggal'].dt.to_period("M")
            df_bulanan = df.groupby('Periode_Bulan', as_index=False)['Prediksi'].sum()
            df_bulanan['Bulan_Teks'] = df_bulanan['Periode_Bulan'].apply(lambda p: f"{nama_bulan_id[p.month]} {p.year}")

            period_obj = pd.Period(forecast_date, freq="M")
            nilai_terpilih = int(df_bulanan.loc[df_bulanan['Periode_Bulan'] == period_obj, 'Prediksi'].values[0])

            st.metric(
                label=f"{nama_bulan_id[period_obj.month]} {period_obj.year}",
                value=f"{nilai_terpilih:,}"
            )

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_bulanan['Bulan_Teks'], y=df_bulanan['Prediksi'],
                mode="lines+markers",
                marker=dict(color=[
                    "rgba(100,150,200,0.8)" if p != period_obj else "crimson"
                    for p in df_bulanan['Periode_Bulan']
                ]),
                hovertemplate="%{x} : %{y:,}<extra></extra>",
                name="Prediksi Bulanan"
            ))
            fig.update_layout(title="Grafik Prediksi Bulanan (Total per Bulan)",
                              xaxis_title="Bulan", yaxis_title="Total Prediksi",
                              xaxis_tickangle=-45, autosize=True)
            st.plotly_chart(fig, use_container_width=True)


    with row1_col2:

      st.write("###### Jumlah Penumpang 5 Periode Ke Depan")

      # Siapkan df dasar
      df_sorted = df.sort_values("Tanggal").reset_index(drop=True).copy()
      df_sorted["Tanggal"] = pd.to_datetime(df_sorted["Tanggal"])

      if forecast_type == "Harian":
          fd = pd.Timestamp(forecast_date)
          agg_df = df_sorted[["Tanggal", "Prediksi"]].copy()

      elif forecast_type == "Mingguan":
          fd = pd.Timestamp(forecast_date[0])  # awal minggu fokus

          # Hanya ambil data dari fd ke depan
          df_future = df_sorted[df_sorted["Tanggal"] >= fd].copy()

          # Tentukan periode mingguan (0 untuk minggu fokus, 1 untuk minggu berikutnya, dst)
          df_future["minggu_ke"] = ((df_future["Tanggal"] - fd).dt.days // 7)

          # Agregasi per minggu
          agg_df = (
              df_future.groupby("minggu_ke", as_index=False)
              .agg({
                  "Tanggal": "min",  # ambil awal minggu
                  "Prediksi": "sum"
              })
              .sort_values("minggu_ke")
              .reset_index(drop=True)
          )
          agg_df = agg_df.drop(columns=["minggu_ke"])

      else:  # Bulanan
          period_obj = pd.Period(forecast_date, freq="M")
          fd = pd.Timestamp(period_obj.start_time)
          agg_df = (
              df_sorted.resample("M", on="Tanggal", label="right", closed="right")["Prediksi"]
              .sum()
              .reset_index()
              .sort_values("Tanggal")
              .reset_index(drop=True)
          )

      # Cari index fokus
      if forecast_type == "Mingguan":
          fokus_idx = agg_df.index[agg_df["Tanggal"] == fd].tolist()
          fokus_idx = fokus_idx[0] if fokus_idx else 0
      else:
          matches = agg_df.index[agg_df["Tanggal"] == fd].tolist()
          if matches:
              fokus_idx = matches[0]
          else:
              pos = agg_df["Tanggal"].searchsorted(fd)
              fokus_idx = max(0, min(pos, len(agg_df) - 1))

      # Ambil 5 periode berikutnya (tidak termasuk fokus)
      df_tampil = agg_df.iloc[fokus_idx + 1 : fokus_idx + 6].copy()

      if df_tampil.empty:
          st.info("Data tidak cukup untuk menampilkan 5 periode ke depan.")
      else:
          if forecast_type == "Harian":
              df_tampil["Tanggal"] = df_tampil["Tanggal"].apply(format_tanggal_indonesia)
          elif forecast_type == "Mingguan":
              nama_bulan_id = {
                  1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
                  5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
                  9: "September", 10: "Oktober", 11: "November", 12: "Desember"
              }
              df_tampil["Tanggal"] = (
                  df_tampil["Tanggal"].dt.strftime("%d/%m/%Y") + " - " +
                  (df_tampil["Tanggal"] + pd.Timedelta(days=6)).dt.strftime("%d/%m/%Y")
              )
          else:  # Bulanan
              nama_bulan_id = {
                  1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
                  5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
                  9: "September", 10: "Oktober", 11: "November", 12: "Desember"
              }
              df_tampil["Tanggal"] = (
                  df_tampil["Tanggal"].dt.month.map(nama_bulan_id) + " " +
                  df_tampil["Tanggal"].dt.year.astype(str)
              )

          df_tampil = df_tampil.reset_index(drop=True)
          df_tampil.index = df_tampil.index + 1

          # Inject CSS untuk mengatur kolom fit content
          st.markdown("""
              <style>
              .stDataFrame td {
                  white-space: nowrap;
              }
              </style>
          """, unsafe_allow_html=True)

          st.dataframe(df_tampil, use_container_width=True)

      # Bagian 2: Daftar Halte (3/6 tinggi)
      st.write("##### 🚏 Daftar Halte")

      if file_for_forecast == "Total Keseluruhan":
          halte_list = [f"Koridor {i}" for i in range(1, 14)]
      elif file_for_forecast == "Koridor 1":
          halte_list = ["Blok M", "Masjid Agung", "Bundaran Senayan", "Gelora Bung Karno", "Polda", "Bendungan Hilir", "Karet", "Dukuh Atas 1", "Tosari", "Bundaran HI", "Sarinah", "BI", "BI Arah Blok M", "BI Arah Kota", "Monas", "Harmoni", "Sawah Besar", "Mangga Besar", "Olimo", "Glodok", "Kota", "Kejaksaan Agung", "Asean"]
      elif file_for_forecast == "Koridor 2":
          halte_list = ["Pulo Gadung", "Bermis", "Pulo Mas", "Perintis Kemerdekaan", "Pedongkelan", "Cempaka Mas", "Sumur Batu", "Cempaka Baru", "Pasar Cempaka Putih", "Rawa Selatan", "Galur", "Senen Raya", "Rspad", "Pejambon", "Gambir", "Istiqlal", "Juanda", "Pecenongan", "Balai Kota", "Gambir 2", "Kwitang", "Pasar Senen"]
      elif file_for_forecast == "Koridor 3":
          halte_list = ["Kalideres", "Pesakih", "Sumur Bor", "Rawa Buaya", "Jembatan Baru", "Dispenda", "Jembatan Gantung", "Taman Kota", "Indosiar", "Jelambar", "Grogol 1", "RS Sumber Waras", "Pasar Baru"]
      elif file_for_forecast == "Koridor 4":
          halte_list = ["Terminal Pulogadung", "Pasar Pulo Gadung", "Pemuda Merdeka", "Layur", "Pemuda RW.Mangun", "Velodrome", "Kayu Jati", "Rawamangun", "Pramuka BPKP", "Pramuka Sari", "Utan Kayu", "Pasar Genjing", "Flyover Pramuka", "Manggarai", "Pasar Rumput", "Halimun", "Galunggung"]
      elif file_for_forecast == "Koridor 5":
          halte_list = ["Kampung Melayu", "Ps.Jatinegara", "Matraman Baru", "Slamet Riyadi", "Tegalan", "Matraman I", "Salemba Carolus", "Salemba UI", "Kramat Sentiong", "Pal Putih", "Senen Sentral", "Budi Utomo", "Ps.Baru Timur", "Jembatan Merah", "Gn.Sahari Mg.Dua", "Pademangan", "Ancol"]
      elif file_for_forecast == "Koridor 6":
          halte_list = ["Ragunan", "Departemen Pertanian", "SMK 57", "Jati Padang", "Pejaten", "Buncit Indah", "Warung Jati", "Imigrasi Jakarta Selatan", "Duren Tiga", "Mampang Prapatan", "Kuningan Timur", "Patra Kuningan", "Departemen Kesehatan", "Gor Sumantri", "Karet Kuningan", "Kuningan Madya", "Setiabudi Utara Aini", "Latuharhari"]
      elif file_for_forecast == "Koridor 7":
          halte_list = ["Kampung Rambutan", "Tanah Merdeka", "Flyover Raya Bogor", "RS.Harapan Bunda", "Ps. Induk Kramat Jati", "Ps. Kramat Jati", "PGC1", "BKN", "Cawang UKI", "BNN", "Cawang Otista", "Gelanggang Remaja", "Bidara Cina", "Tanah Merdeka 2"]
      elif file_for_forecast == "Koridor 8":
          halte_list = ["Lebak Bulus", "Pondok Pinang", "Pondok Indah I", "Pondok Indah II", "Tanah Kusir Kodim", "Kebayoran Lama Bungur", "Ps.Kebayoran lama", "Simprug", "Permata Hijau", "Permata Hijau RS Medika", "Pos Pengumben", "Kelapa Dua Sasak", "Kebon Jeruk", "Duri Kepa", "Kedoya Assidiqiyah", "Kedoya Green Garden", "Grogol II", "S. PARMAN PODOMORO CITY", "Tomang Mandala", "RS Tarakan", "Petojo"]
      elif file_for_forecast == "Koridor 9":
          halte_list = ["Pinang Ranti", "Garuda Taman Mini", "Cawang Ciliwung", "Cikoko St.Cawang", "Tebet BKPM", "Pancoran Tugu", "Pancoran Barat", "Tegal Parang", "Kuningan Barat", "Jamsostek GT.Subroto", "Lipi GT.Subroto", "Semanggi", "JCC Senayan", "Slipi Pertamburan", "Slipi Kemanggisan", "RS.Harapan Kita", "Latumenten ST. K.A ", "Jembatan Besi", "Jembatan Dua", "Jembatan Tiga", "Penjaringan", "Pluit"]
      elif file_for_forecast == "Koridor 10":
          halte_list = ["PGC2", "Cawang Soetoyo", "Penas Kalimalang", "Cipinang Kebon Nanas", "Pedati Prumpung", "Bea Cukai A.yani", "Utan Kayu Rawamangun", "Kayu Putih Rawasari", "Pulomas ByPass", "Cempaka Putih", "Yos Sudarso Kodamar", "Sunter kelapa Gading", "RS. Puri Medika Plumpang", "Walikota Jakarta Utara Arah Cililitan", "Walikota Jakarta Utara Arah TJ.Priuk", "Permai Koja", "Enggano", "Terminal Tj.Priuk"]
      elif file_for_forecast == "Koridor 11":
          halte_list = ["Pulo Gebang", "Walikota Jakarta Timur", "Penggilingan", "Perumnas Klender", "Flyover Raden Inten", "Buaran", "Kampung Sumur", "Flyover Klender", "Stasiun Klender", "Cipinang", "Imigrasi Jakarta Timur", "Pasar Enjo", "Flyover Jatinegara", "Stasiun Jatinegara Timur", "Jatinegara RS Premier"]
      elif file_for_forecast == "Koridor 12":
          halte_list = ["Sunter Boulevard Barat", "Sunter Karya", "SMP 140", "Danau Agung", "Landas Pacu", "Mangga Dua", "Pangeran Jayakarta", "Kali Besar Barat", "Bandengan Selatan", "Museum Fatahilah", "Gedung Panjang", "Pakin", "Landmark Auto Plaza", "PRJ"]
      elif file_for_forecast == "Koridor 13":
          halte_list = ["Tendean", "Rawa Barat", "Pangeran Tirtayasa", "CSW", "Mayestik", "Velbak", "Kebayoran Lama", "Seskoal", "Cipulir", "Swadharma", "JORR", "Adam Malik", "Puri Beta 1", "Puri Beta 2", "CBD"]
      cols = st.columns(3)  # 3 kolom

      for i, halte in enumerate(halte_list):
        with cols[i % 3]:
            st.markdown(
                f"<div style='background:#d1e7dd; padding:5px; border-radius:5px; margin-bottom:5px; text-align:center; color:#0f5132; font-weight:600; font-size:12px; line-height: 1.1;'>{halte}</div>",
                unsafe_allow_html=True
            )





# Footer / identitas pembuat
st.markdown("""
<hr>
<div style='text-align: right; font-size: 14px; color: gray;'>
    Dibuat oleh <b>Hasan Bahtiar Habibi</b> © 2025
</div>
""", unsafe_allow_html=True)

