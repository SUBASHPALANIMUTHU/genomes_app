import streamlit as st
import pandas as pd
import altair as alt
import os

# -------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(page_title="Genome Dashboard", layout="wide")

# -------------------------------------------------------------
# PERMANENT EXCEL FILE LOADING
# -------------------------------------------------------------
excel_path = "data/genome_data.xlsx"   # <- keep your Excel here

if not os.path.exists(excel_path):
    st.error("Excel file not found! Place it inside: data/genome_data.xlsx")
    st.stop()

xls = pd.ExcelFile(excel_path)
df = pd.read_excel(xls, sheet_name="indian_genomes")
df2 = pd.read_excel(xls, sheet_name="plants_count")

# -------------------------------------------------------------
# PAGE STYLING
# -------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #e8eef6, #ffffff);
    padding: 25px;
}
.main > div {
    background: #ffffff;
    padding: 40px 50px;
    border-radius: 16px;
    box-shadow: 0px 6px 30px rgba(0,0,0,0.12);
    margin: 20px auto;
}
h1, h2, h3 {
    font-family: 'Segoe UI', sans-serif;
    font-weight: 650;
    color: #1f2d3d !important;
}
thead tr th {
    background: #2f5597 !important;
    color: #ffffff !important;
    font-size: 15px !important;
}
tbody tr td {
    background: #f6f8fc !important;
    padding: 9px !important;
    border-bottom: 1px solid #dce2ec !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TITLE
# -------------------------------------------------------------
st.markdown("""
<div style='border-left:6px solid #1E90FF; padding:10px 15px; border-radius:5px;'>
    <h1 style='margin:0;'>Plant Genomes submitted from India</h1>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# CLEAN DATE COLUMN
# -------------------------------------------------------------
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# -------------------------------------------------------------
# FILTERS SECTION (TOP)
# -------------------------------------------------------------
st.subheader("Filters for Genome submitted from India")

col1, col2, col3 = st.columns(3)

years = sorted(df["Date"].dropna().dt.year.unique())
year_sel = col1.multiselect("Select Year", years)

months = sorted(df["Date"].dropna().dt.month.unique())
month_sel = col2.multiselect("Select Month", months)

institutes = sorted(df["Submitter"].dropna().unique())
inst_sel = col3.multiselect("Select Institute", institutes)

assembly_levels = sorted(df["Assembly level"].dropna().unique())
assembly_sel = st.multiselect("Assembly Level", assembly_levels)

# apply filters
filtered = df.copy()

if year_sel:
    filtered = filtered[filtered["Date"].dt.year.isin(year_sel)]
if month_sel:
    filtered = filtered[filtered["Date"].dt.month.isin(month_sel)]
if inst_sel:
    filtered = filtered[filtered["Submitter"].isin(inst_sel)]
if assembly_sel:
    filtered = filtered[filtered["Assembly level"].isin(assembly_sel)]

# -------------------------------------------------------------
# FILTERED TABLE (MIDDLE)
# -------------------------------------------------------------
st.write("### Filtered Genomes")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Filtered Data",
    filtered.to_csv(index=False),
    "filtered_genomes.csv"
)

st.markdown("---")

# -------------------------------------------------------------
# SECOND SHEET TABLE (MIDDLE)
# -------------------------------------------------------------
st.subheader("Species Count (from second sheet)")
st.dataframe(df2, use_container_width=True)

st.download_button(
    "Download Species Count",
    df2.to_csv(index=False),
    "species_count.csv"
)

st.markdown("---")

# -------------------------------------------------------------
# YEAR-WISE BAR CHART (BOTTOM)
# -------------------------------------------------------------
st.subheader("Year-wise Genome Submissions (Bar Chart)")

df_year = df.dropna(subset=["Date"])
df_year["Year"] = df_year["Date"].dt.year

year_count = df_year.groupby("Year").size().reset_index(name="Count")

chart = (
    alt.Chart(year_count)
    .mark_bar()
    .encode(
        x=alt.X("Year:O", title="Year"),
        y=alt.Y("Count:Q", title="Number of Genome Submissions"),
        tooltip=["Year", "Count"]
    )
    .properties(width=700, height=400)
)

st.altair_chart(chart, use_container_width=True)
