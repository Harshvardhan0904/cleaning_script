📘 Data Cleaning Script – README

This project has a Python class DataCleaner.
It takes a DataFrame and cleans it step by step.
The idea is simple: remove trash data and give a clean dataset back.

🚀 Features

removes duplicates

fixes column names

finds date and id columns

converts date columns

fills missing values (mean, mode, ffill, median)

checks null %

prints stats for numbers

IQR check

plots histograms + scatter plots

logs every step

📦 Requirements

Install these:

pip install pandas numpy seaborn matplotlib


Python version: 3.8+ recommended.

📁 How to Use
1️⃣ import the file
from data_cleaner import DataCleaner

2️⃣ load your data
import pandas as pd

df = pd.read_csv("your_file.csv")

3️⃣ clean the data
cleaner = DataCleaner(df)
clean_df = cleaner.cleaning_data()

4️⃣ see graphs
cleaner.graph_plot()

🧠 What the Cleaning Function Does
✔ removes duplicates
✔ cleans column names

everything goes lowercase and spaces turn into _.

✔ date detection

if a column has “date” in the name → convert to date.

✔ null filling

numbers → mean

strings → mode

date/boolean/other → forward fill

second pass:

cat → mode

num → median

else → 0

✔ IQR

It prints Q1, Q3, and IQR for numeric columns.

✔ plots

hist plots for numeric

hist plots for categorical

scatter for numeric

scatter for categorical

📝 Logging

A folder logs/ gets created.
Every step is logged inside:

logs/data_cleaning.log

📊 Example Output

dataset shape

null percentage

duplicate count

cleaned stats

IQR values

all plots
