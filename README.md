# PhonePe Pulse Data Analysis and Visualization

This repository contains code for visualizing and exploring PhonePe Pulse data using Streamlit and Plotly.

## Data Extraction

1. Clone the GitHub repository using Git Bash:
git clone https://github.com/your_username/phonepe-pulse.git

2. Retrieve the data from the PhonePe Pulse GitHub repository.

## Data Transformation

1. Use a scripting language such as Python along with libraries such as Pandas to manipulate and preprocess the data.
2. Clean the data, handle missing values, and transform the data into a DataFrame for analysis and visualization.
3. Use libraries such as os, json, pandas, mysql.connector, and csv for data extraction and transformation.

## Database Insertion

1. Connect to a MySQL database using the `mysql.connector` library in Python.
2. Insert the transformed data into the database using SQL commands.

## Dashboard Creation

1. Use Streamlit and Plotly libraries in Python to create an interactive and visually appealing dashboard.
2. Utilize Plotly's built-in geo map functions to display the data on a map.
3. Use Streamlit to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.
4. Import libraries such as pandas, plotly.express, mysql.connector, geopandas, and warnings for dashboard creation.

## Data Retrieval

1. Use the `mysql.connector` library to connect to the MySQL database.
2. Fetch the data into a Pandas DataFrame.
3. Update the dashboard dynamically with the data from the DataFrame.

## Usage

1.Install the required libraries:

   - pandas:
     ```
     pip install pandas
     ```

   - plotly.express:
     ```
     pip install plotly.express
     ```

   - streamlit:
     ```
     pip install streamlit
     ```

   - warnings:
     This library is part of the Python standard library and does not require separate installation.

   - mysql.connector:
     ```
     pip install mysql-connector-python
     ```

   - geopandas:
     ```
     pip install geopandas
     ```

2. Run the Streamlit app:
streamlit run streamlit_dashboard.py


