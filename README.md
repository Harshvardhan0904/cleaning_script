# 📘 Data Cleaning Script

A Python class `DataCleaner` that takes a DataFrame and cleans it step by step. Remove trash data and get a clean dataset back.

---

## 🚀 Features

- ✅ Removes duplicates
- ✅ Fixes column names (lowercase, underscore-separated)
- ✅ Finds date and ID columns automatically
- ✅ Converts date columns to datetime
- ✅ Fills missing values (mean, mode, ffill, median)
- ✅ Checks null percentage
- ✅ Prints statistics for numeric columns
- ✅ IQR (Interquartile Range) check
- ✅ Plots histograms + scatter plots
- ✅ Logs every step

---

## 📦 Requirements

Install dependencies:

```bash
pip install pandas numpy seaborn matplotlib
```

**Python version:** 3.8+ recommended

---

## 📁 How to Use

### 1️⃣ Import the file

```python
from data_cleaner import DataCleaner
```

### 2️⃣ Load your data

```python
import pandas as pd

df = pd.read_csv("your_file.csv")
```

### 3️⃣ Clean the data

```python
cleaner = DataCleaner(df)
clean_df = cleaner.cleaning_data()
```

### 4️⃣ See graphs

```python
cleaner.graph_plot()
```

---

## 🧠 What the Cleaning Function Does

### ✔ Removes duplicates
Automatically detects and removes duplicate rows.

### ✔ Cleans column names
Everything goes lowercase and spaces turn into `_`.

### ✔ Date detection
If a column has "date" in the name → converts to datetime.

### ✔ Null filling
- **Numbers** → mean
- **Strings** → mode
- **Date/boolean/other** → forward fill
- **Second pass:**
  - Categorical → mode
  - Numeric → median
  - Else → 0

### ✔ IQR
Prints Q1, Q3, and IQR for numeric columns.

### ✔ Plots
- Histogram plots for numeric columns
- Histogram plots for categorical columns
- Scatter plots for numeric columns
- Scatter plots for categorical columns

---

## 📝 Logging

A folder `logs/` gets created. Every step is logged inside:

```
logs/data_cleaning.log
```

---

## 📊 Example Output

- Dataset shape
- Null percentage
- Duplicate count
- Cleaned statistics
- IQR values
- All plots


---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---
