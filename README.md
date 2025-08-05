# 🚚 Transport Vendor Dashboard

An interactive web dashboard built with **Dash** and **Plotly** that allows logistics and fleet managers to upload Excel-based vendor data, visualize fleet statistics, and verify vendor compliance — all in real-time.

## 🔧 Features

- 📤 Upload `.xlsx` Excel files directly through the web UI
- 📊 Auto-generated visualizations:
  - Fleet size by **Company**
  - Fleet size by **Vendor**
  - Vendor distribution by **Location** (Pie Chart)
- ✅ **Compliance Checker** for:
  - A/c Number
  - IFSC Code
  - PAN Number
- 📋 Dynamic master table of all uploaded vendor data

## 📁 Excel File Requirements

Your Excel file must contain the following columns (case-insensitive, trimmed automatically):

- `Company name`
- `Vehicle No`
- `Name` (Vendor Name)
- `Location`
- `A/c`
- `IFSC Code`
- `Pan No`

Empty or missing values will be marked as `"Missing"` and reflected in the compliance checker.

## 🚀 Getting Started

##Install Dependencies
pip install -r requirements.txt
pip install dash pandas plotly openpyxl


##Run the App
python app.py





### 1. Clone the Repository

```bash
git clone https://github.com/your-username/transport-vendor-dashboard.git
cd transport-vendor-dashboard
