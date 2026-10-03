import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Data Cleaning Automation Engine", layout="wide")

st.title("🧼 Data Cleaning & Reporting Automation Pipeline")
st.markdown("Instantly process messy operational logs, fix structural anomalies, and download standardized data products.")

# Load internal file baseline framework
@st.cache_data
def load_raw_data():
    try:
        return pd.read_csv("messy_sales_data.csv")
    except FileNotFoundError:
        st.error("Error: 'messy_sales_data.csv' missing from workspace environment.")
        return None

df_raw = load_raw_data()

if df_raw is not None:
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("⚠️ Unprocessed Raw Input Data")
        st.dataframe(df_raw, use_container_width=True)
        
    # Pipeline execution operations
    total_rows = len(df_raw)
    
    # 1. Identify and drop exact duplicate rows
    duplicate_count = df_raw.duplicated().sum()
    df_cleaned = df_raw.drop_duplicates()
    
    # 2. Text standardization formatting fixes
    df_cleaned['Product'] = df_cleaned['Product'].astype(str).str.strip().str.title()
    
    # 3. Handle missing values
    missing_dates = df_cleaned['Date'].isna().sum()
    df_cleaned['Date'] = df_cleaned['Date'].fillna("2024-01-01")
    df_cleaned['Region'] = df_cleaned['Region'].fillna("Unknown")
    
    # Impute missing values with column medians
    missing_sales = df_cleaned['Sales_Amount'].isna().sum()
    df_cleaned['Sales_Amount'] = df_cleaned['Sales_Amount'].fillna(df_cleaned['Sales_Amount'].median())
    
    missing_qty = df_cleaned['Quantity'].isna().sum()
    df_cleaned['Quantity'] = df_cleaned['Quantity'].fillna(1)
    
    with col_right:
        st.subheader("✨ Automated Pipeline Clean Output")
        st.dataframe(df_cleaned, use_container_width=True)
        
    st.markdown("---")
    
    # Metric Summary Tracking Blocks
    st.subheader("📋 Pipeline Metrics Execution Logs")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Duplicate Rows Dropped", f"{duplicate_count}")
    with m2:
        st.metric("Missing Sales Amounts Fixed", f"{missing_sales}")
    with m3:
        st.metric("Missing Quantities Fixed", f"{missing_qty}")
    with m4:
        st.metric("Final Post-Audit Records", f"{len(df_cleaned)} / {total_rows}")
        
    st.markdown("---")
    
    # Aggregated Summary Report Section
    st.subheader("📊 Automated Aggregated Regional Performance Report")
    report_df = df_cleaned.groupby('Region')[['Sales_Amount', 'Quantity']].sum().reset_index()
    report_df.columns = ['Operational Region', 'Aggregated Sales Revenue ($)', 'Total Volume Dispatched']
    st.dataframe(report_df.style.format({'Aggregated Sales Revenue ($)': "{:,.2f}"}), use_container_width=True)
    
    # Export clean data buffers
    csv_buffer = io.StringIO()
    df_cleaned.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.sidebar.header("📥 Export Cleared Deliverables")
    st.sidebar.download_button(
        label="Download Cleaned CSV Dataset",
        data=csv_data,
        file_name="automated_clean_sales_report.csv",
        mime="text/csv"
    )
