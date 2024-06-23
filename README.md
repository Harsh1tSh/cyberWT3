# Financial Anomaly Detection

## Project Overview
This project includes a Python script designed to detect anomalies in financial transaction data. The script processes transaction records, calculates statistical thresholds, and identifies transactions that deviate significantly from established patterns.

## Features
- Load and preprocess data from CSV files.
- Calculate basic statistical metrics (mean, median, and standard deviation).
- Detect anomalies based on dynamically calculated thresholds.
- Generate a detailed report listing all detected anomalies.


### Prerequisites
- Python 3
- pandas library

## Methodology and Rationale

### Data Preprocessing
The script starts by loading the transaction data from a CSV file, ensuring that all data is present and correctly formatted. It removes any rows with missing data and converts transaction amounts to numeric values, ensuring robustness in subsequent calculations.

### Statistical Analysis
Statistical metrics such as mean, median, and standard deviation are computed for each category of transactions. These metrics form the basis for identifying what constitutes a "normal" transaction within each category.

### Anomaly Detection
Anomalies are detected using a Z-score approach, modified to handle small datasets effectively:
- Transactions are flagged as anomalies if they deviate from the mean by more than 2.5 standard deviations, a standard threshold in statistical outlier detection.
- For categories with a single transaction or no variance, a fixed threshold of ±1 from the mean is used to flag anomalies. This accounts for situations where the standard deviation is zero or undefined, ensuring the system remains sensitive to extreme values even in small datasets.

### Rationale Behind Statistical Methods
The chosen methods allow for a balance between sensitivity and specificity, minimizing the risk of false positives (normal transactions wrongly flagged as anomalies) while ensuring significant deviations are caught. The thresholds can be adjusted based on feedback and the specific requirements of the financial monitoring system in use.


