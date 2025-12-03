# Genome Dashboard – Streamlit Web App

A simple and interactive Streamlit application to visualize genome-related Excel data, explore year-wise submissions, filter by parameters, and generate charts automatically.

# Features

Uploads and reads Excel file(s) containing genome datasets

Automatically detects sheets

Year-wise submission statistics

Interactive charts and tables

Clean and responsive UI

Error handling for missing files

Ready for deployment on Streamlit Cloud / GitHub

# How to Run Locally
1. Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows

3. Install requirements
pip install -r requirements.txt

4. Run the Streamlit app
streamlit run app.py

# Adding Your Excel File

You must create a folder named data in the root of the repo and place:

data/genome_data.xlsx


If the file is missing, the app will show:
"Excel file not found!"

# Deployment (Streamlit Cloud)

# 1. Upload entire project to GitHub

Make sure your repo includes:

app.py

requirements.txt

data/genome_data.xlsx

README.md

# 2. Go to Streamlit Cloud

Create a new app → Select your GitHub repo → Select app.py.

Streamlit will auto-deploy.

 requirements.txt Example

If you need one, here is a minimal version:

streamlit
pandas
altair
openpyxl

# Notes

Ensure your Excel file name and the path in app.py match exactly:

excel_path = "data/genome_data.xlsx"


If you update the Excel file, re-upload it to the data folder and commit the change.

# Contact

If you need help or improvements, feel free to raise an issue or contribute.
