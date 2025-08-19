import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Model ---
scaler = joblib.load('../Scaler/scaler.pkl')
kmeans = joblib.load('../Models/kMeans_model.pkl')

# --- Page Setup ---
st.set_page_config(page_title="🌊 E-Commerce RFM Clustering", layout="wide")

# --- CSS: SkyBlue / هادئ / hover effects ---
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden !important;}

.stApp {
    background: linear-gradient(45deg,#e6f7ff,#87ceeb) !important;
    font-family:"Segoe UI", sans-serif !important;
    color:#073b4c !important;
    padding:15px !important;
}

/* Inputs */
.stTextInput, .stNumberInput, .stDateInput {
    background: linear-gradient(180deg, #87ceeb, #e6f7ff) !important;
    border-radius:6px !important;
    padding:3px 5px !important;
    font-size:0.85em !important;
    transition: all 0.2s ease-in-out !important;
}
.stTextInput:hover, .stNumberInput:hover, .stDateInput:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg,#90e0ef,#00b4d8) !important;
    color:white !important;
    border-radius:14px !important;
    padding:0.3em 1em !important;
    font-size:0.9em !important;
    font-weight:bold !important;
    transition: all 0.3s ease-in-out !important;
}
div.stButton > button:hover {
    background: linear-gradient(90deg,#00b4d8,#90e0ef) !important;
    transform: scale(1.06) !important;
    box-shadow:0 4px 10px rgba(0,0,0,0.2) !important;
}

/* Result Box */
.result-box {
    padding:12px !important;
    border-radius:14px !important;
    text-align:center !important;
    font-size:1em !important;
    font-weight:bold !important;
    box-shadow:0 3px 8px rgba(0,0,0,0.12) !important;
    background: linear-gradient(135deg,#ade8f4,#90e0ef) !important;
    color:#023e8a !important;
}

/* DataFrame Table */
.stDataFrameWrapper table {
    border:1px solid #0077b6 !important;
    border-radius:8px !important;
}
.stDataFrameWrapper th {
    background-color:#0077b6 !important;
    color:white !important;
    padding:6px !important;
}
.stDataFrameWrapper td {
    padding:4px !important;
}
.stDataFrameWrapper tbody tr:hover {
    background-color:#caf0f8 !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width:8px;
    height:8px;
}
::-webkit-scrollbar-thumb {
    background-color:#00b4d8;
    border-radius:8px;
}

/* تكبير عنوان الاختيار */
.stRadio > label {
    font-size: 22px !important;   /* حجم الخط */
    font-weight: bold !important; /* سمك الخط */
    color: #003366 !important;    /* لون النص */
}
/* تكبير "Choose input method:" */
section[data-testid="stSidebar"] div.stRadio > label > div {
    font-size: 22px !important;
    font-weight: bold !important;
    color: black !imortant;
    margin-bottom: 15px !important;
}
/* تغيير لون الدائرة المختارة */
div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
    background-color: #1E90FF !important; /* SkyBlue */
    border: 2px solid #1E90FF !important;
    box-shadow: 0 0 6px rgba(30,144,255,0.8) !important;
}
</style>
""", unsafe_allow_html=True)

sidebar_bg = """
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #87ceeb, #e6f7ff) !important;
    color: #003366 !important;
    font-weight: bold !important;
}

/* Sidebar labels */
[data-testid="stSidebar"] label {
    color: #003366 !important;
    font-weight: bold !important;
}

/* Radio buttons text */
[data-testid="stSidebar"] .stRadio label {
    color: #004080 !important;
    font-size: 0.9em !important;
}

p
{
font-weight: bold ;
font-size: 0.9em ;
color:white;
}
/* Hover effect */
[data-testid="stSidebar"] .stRadio div:hover {
    # background: rgba(255, 255, 255, 0.4) !important;
    color: black;
    transform: scale(1.03) !important;
    border-radius: 6px !important;
    transition: 0.3s ease-in-out;
}
</style>
"""
st.markdown(sidebar_bg, unsafe_allow_html=True)

# --- Title ---
st.title("🌊 E-Commerce RFM Clustering")
st.write("Upload CSV or enter data manually to perform RFM clustering 🛒")

# --- Sidebar: اختيار طريقة الإدخال ---
input_method = st.sidebar.radio("Choose input method:", ["Upload CSV", "Manual Entry"])

# --- Manual Data Storage ---
if 'manual_data' not in st.session_state:
    st.session_state.manual_data = []

# --- Manual Input ---
manual_df = pd.DataFrame()
if input_method == "Manual Entry":
    with st.form("manual_input"):
        cols = st.columns(3)
        InvoiceNo = cols[0].text_input("InvoiceNo", "10100")
        Description = cols[1].text_input("Description", "Sample Product")
        Quantity = cols[2].number_input("Quantity", 1, 1000, 1)
        UnitPrice = cols[0].number_input("UnitPrice", 0.01, 10000.0, 10.0)
        InvoiceDate = cols[1].date_input("InvoiceDate")
        Country = cols[2].text_input("Country", "United Kingdom")
        submit = st.form_submit_button("Add Entry")
        if submit:
            st.session_state.manual_data.append({
                'InvoiceNo': InvoiceNo,
                'Description': Description,
                'Quantity': Quantity,
                'UnitPrice': UnitPrice,
                'InvoiceDate': pd.to_datetime(InvoiceDate),
                'Country': Country
            })
            st.success("Entry added!")

    if st.session_state.manual_data:
        manual_df = pd.DataFrame(st.session_state.manual_data)
        st.subheader("Manual Entries Added")
        st.dataframe(manual_df)

# --- File Upload ---
uploaded_file = None
if input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        if not manual_df.empty:
            df = pd.concat([df, manual_df], ignore_index=True)
    elif not manual_df.empty:
        df = manual_df
    else:
        st.info("Please upload CSV or enter data manually.")
        st.stop()
else:
    if not manual_df.empty:
        df = manual_df
    else:
        st.info("Please enter manual data to continue.")
        st.stop()

# --- Data Cleaning & RFM Calculation ---
df.drop_duplicates(inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df = df[df['Quantity'] > 0]
df['Description'] = df['Description'].fillna('Unknown')

snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = df.groupby('InvoiceNo').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'Quantity': 'sum',
    'TotalPrice': 'sum'
}).rename(columns={'InvoiceDate':'Recency','Quantity':'Frequency','TotalPrice':'Monetary'})

# --- Scaling + KMeans ---
rfm_scaled = scaler.transform(rfm)
rfm['Cluster'] = kmeans.predict(rfm_scaled)
cluster_order = rfm.groupby('Cluster')['Monetary'].mean().sort_values(ascending=False).index
rfm['Cluster'] = rfm['Cluster'].apply(lambda x: np.where(cluster_order==x)[0][0])

# --- Display Data & Summary ---
st.subheader("RFM with Cluster")
st.dataframe(rfm)

st.subheader("Cluster Summary")
cluster_summary = rfm.groupby('Cluster').agg({
    'Recency':'mean','Frequency':'mean','Monetary':'mean','Cluster':'count'
}).rename(columns={'Cluster':'Count'})
st.dataframe(cluster_summary)

# --- Charts (شفافة) ---
st.subheader("Cluster Visualizations")
sns.set_style("whitegrid")
fig, axes = plt.subplots(1,3,figsize=(18,5))
fig.patch.set_alpha(0.0)   # يخلي خلفية الفيجور كلها شفافة
for ax in axes: ax.set_facecolor("none")
sns.barplot(x=cluster_summary.index, y=cluster_summary['Recency'], ax=axes[0], palette="Blues")
axes[0].set_title("Average Recency per Cluster")
sns.barplot(x=cluster_summary.index, y=cluster_summary['Frequency'], ax=axes[1], palette="Greens")
axes[1].set_title("Average Frequency per Cluster")
sns.barplot(x=cluster_summary.index, y=cluster_summary['Monetary'], ax=axes[2], palette="Oranges")
axes[2].set_title("Average Monetary per Cluster")
st.pyplot(fig)

# --- Download ---
csv = rfm.reset_index().to_csv(index=False).encode('utf-8')
st.download_button("Download CSV with Clusters", csv, "rfm_clusters_results.csv","text/csv")
