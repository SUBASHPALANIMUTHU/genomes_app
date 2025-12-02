import streamlit as st
import pandas as pd

st.set_page_config(page_title="Genome Dashboard", layout="wide")

st.markdown("""
<style>

/* FULL PAGE BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #e8eef6, #ffffff);
    padding: 25px;
}

/* CENTERED CONTENT CARD */
.main > div {
    background: #ffffff;
    padding: 40px 50px;
    border-radius: 16px;
    box-shadow: 0px 6px 30px rgba(0,0,0,0.12);
    margin: 20px auto;
}

/* HEADINGS */
h1, h2, h3 {
    font-family: 'Segoe UI', sans-serif;
    font-weight: 650;
    color: #1f2d3d !important;
}

/* TABLE HEADER */
thead tr th {
    background: #2f5597 !important;
    color: #ffffff !important;
    font-size: 15px !important;
    padding: 10px !important;
    border: none !important;
}

/* TABLE ROWS */
tbody tr td {
    background: #f6f8fc !important;
    padding: 9px !important;
    border-bottom: 1px solid #dce2ec !important;
    font-size: 14px !important;
}

/* FILTER DROPDOWNS */
div[data-baseweb="select"], .stMultiSelect, .stSelectbox {
    background: #f4f6fa !important;
    border-radius: 10px !important;
    border: 2px solid #b7c4d7 !important;
    padding: 8px !important;
}

/* FILTER LABEL COLOR BOX */
.filter-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    color: #1a2a3a;
}
.filter-square {
    width: 12px;
    height: 12px;
    background: #2f5597;
    border-radius: 3px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='border-left:6px solid #1E90FF; padding:10px 15px; border-radius:5px;'>
    <h1 style='margin:0;'>Plant Genomes submitted from India</h1>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)

    # Load sheets
    df = pd.read_excel(xls, sheet_name="indian_genomes")
    df2 = pd.read_excel(xls, sheet_name="plants_count")

    st.subheader("Filters for Genome submitted from India")

    # Clean date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    col1, col2, col3 = st.columns(3)

    # Year filter
    years = sorted(df["Date"].dropna().dt.year.unique())
    year_sel = col1.multiselect("Select Year", years)

    # Month filter
    months = sorted(df["Date"].dropna().dt.month.unique())
    month_sel = col2.multiselect("Select Month", months)

    # Institute filter
    institutes = sorted(df["Submitter"].dropna().unique())
    inst_sel = col3.multiselect("Select Institute", institutes)

    # Assembly level filter
    assembly_levels = sorted(df["Assembly level"].dropna().unique())
    assembly_sel = st.multiselect("Assembly Level", assembly_levels)

    # Apply filters
    filtered = df.copy()

    if year_sel:
        filtered = filtered[filtered["Date"].dt.year.isin(year_sel)]

    if month_sel:
        filtered = filtered[filtered["Date"].dt.month.isin(month_sel)]

    if inst_sel:
        filtered = filtered[filtered["Submitter"].isin(inst_sel)]

    if assembly_sel:
        filtered = filtered[filtered["Assembly level"].isin(assembly_sel)]

    st.write("### Filtered Genomes")
    st.dataframe(filtered)

    st.download_button("Download Filtered Data", filtered.to_csv(index=False), "filtered_genomes.csv")

    st.markdown("---")
    st.subheader("Species Count (from second sheet)")

    st.dataframe(df2)

    st.download_button("Download Species Count", df2.to_csv(index=False), "species_count.csv")
