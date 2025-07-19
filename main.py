from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def homepage():
    """Home Page displays"""
    return FileResponse("index.html")

@app.post("/read-columns")
async def read_columns(file: UploadFile = File(...)):
    """Reads the uploaded file and returns its column names."""
    extension = file.filename.split('.')[-1].lower()
    try:
        if extension == 'csv':
            df = pd.read_csv(file.file, keep_default_na=False, na_values=[''])
        elif extension in ['xlsx', 'xls']:
            df = pd.read_excel(file.file, keep_default_na=False, na_values=[''])
        else:
            return {"error": "Only CSV and Excel files are supported."}
    except Exception as e:
        return {"error": f"Failed to read file: {e}"}

    return {"columns": df.columns.tolist()}


@app.post("/process-data")
async def process_data(
    file: UploadFile = File(...),
    x_column: str = Form(...),
    y_column: str = Form(...)
):
    """
    Processes the file for plotting.
    - X-axis column is treated as a category (string).
    - Y-axis column is converted to a number.
    """
    extension = file.filename.split('.')[-1].lower()

    try:
        if extension == "csv":
            df = pd.read_csv(file.file, keep_default_na=False, na_values=[''])
        elif extension in ["xlsx", "xls"]:
            df = pd.read_excel(file.file, keep_default_na=False, na_values=[''])
        else:
            return {"error": "Only CSV and Excel files are supported."}

        if x_column not in df.columns or y_column not in df.columns:
            return {"error": "Selected columns not found in the file."}

        # Select only the necessary columns
        df_plot = df[[x_column, y_column]].copy()

        # Treat the X-axis column as a string.
        df_plot[x_column] = df_plot[x_column].astype(str)

        # Only convert the Y-axis column to numeric.
        df_plot[y_column] = pd.to_numeric(
            df_plot[y_column].astype(str).str.replace(',', '').str.strip(),
            errors='coerce'
        )

        # Drop rows only if the Y-axis value is invalid (NaN).
        df_plot.dropna(subset=[y_column], inplace=True)

        if df_plot.empty:
            return {"error": "No valid numeric data found for the Y-axis."}

        # Return the clean data as lists.
        return {
            "x_data": df_plot[x_column].tolist()[:50],
            "y_data": df_plot[y_column].tolist()[:50]
        }
    except Exception as e:
        return {"error": f"An error occurred during data processing: {e}"}