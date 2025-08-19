# 🛒 E-Commerce Data Exploration

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Libraries](https://img.shields.io/badge/Libraries-pandas%2C%20numpy%2C%20matplotlib%2C%20seaborn%2C%20joblib%2C%20streamlit-orange)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 📌 Overview

This project focuses on exploring and analyzing E-Commerce data to
identify patterns, trends, and customer behavior.
The dataset includes customer information, order details, and
transaction history.

---

## 📂 Project Structure

```
├── Models/
│   ├── kMeans_model.pkl
│   └── rfm_data.pkl
├── Scaler/
│   └── scaler.pk
├── App/
│   └── app.py      
├── Notebook/
│   └── E-Commerce.ipynb
├── README.md
├── Streamlit (1).png
├── Streamlit (2).png
└── requirements.txt
```

---

## 🛠️ Features

-   Data Cleaning (missing values, duplicates, outliers)
-   Exploratory Data Analysis (EDA) with Matplotlib & Seaborn
-   Customer Segmentation using clustering techniques
-   Sales Trend Analysis over time
-   Top Products & Revenue Contribution visualization
-   Interactive Dashboard with Streamlit

---

## 📊 Data Preprocessing

-   Removed duplicates and invalid records
-   Converted dates into proper datetime format
-   Feature extraction (e.g., revenue = quantity × price)
-   Outlier detection and handling

---

## 📈 Insights & Analysis

-   Monthly and daily sales distribution
-   Best-selling products and categories
-   Customer purchase frequency & retention
-   Seasonal demand patterns

---

## 📹 StreamLit (UI)
<img width="3820" height="2128" alt="Streamlit (1)" src="https://github.com/user-attachments/assets/d779ea85-4f17-49ff-ab0c-3b7542d10a84" />
<img width="3820" height="2126" alt="Streamlit (2)" src="https://github.com/user-attachments/assets/d3c2d7d2-058b-4b25-9870-99cc8516f197" />

---
## 🚀 Installation & Usage

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ibrahim-06/E-Commerce-Data-Exploration.git
cd E-Commerce-Data-Exploration
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run Jupyter Notebook
```bash
jupyter notebook Notebook/E-Commerce.ipynb
```

### 4️⃣ Run Streamlit Dashboard
```bash
streamlit run App/app.py
```

---

## 📦 Saved Artifacts

-   Cleaned Dataset
-   Exploration Notebook
-   Streamlit Dashboard

---

## 📚 Requirements

```
pandas
numpy
matplotlib
seaborn
joblib
streamlit
```

---

## 👤 Author
**Ibrahim Mohamed**  
📧 Email: ibrahim.06.dev@gmail.com  
🔗 LinkedIn: [Ibrahim Mohamed](https://www.linkedin.com/in/ibrahim-mohamed-211-)

---

## 📜 License

This project is licensed under the MIT License.
