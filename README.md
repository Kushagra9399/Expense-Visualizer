# 📊 Expense Visualizer

A simple web application using **FastAPI** (backend) and **HTML** (frontend) to:
- Upload CSV or Excel files
- Extract column names
- Select X and Y axes
- Process and visualize data

## 🚀 Features

- Upload `.csv`, `.xlsx`, or `.xls` files
- Auto-detect and list column names
- Select X and Y axis from dropdowns
- Cleans and processes numeric data
- Returns JSON for plotting graphs (frontend can be extended with chart libraries like Chart.js)

## 🛠️ Tech Stack

- **Backend**: FastAPI, Pandas
- **Frontend**: HTML5 (can be extended with JS/Chart.js)
- **Other**: CORS, File uploads
