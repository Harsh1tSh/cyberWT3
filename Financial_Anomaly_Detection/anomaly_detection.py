import pandas as pd

def load_data(filepath):
    """Load data from a CSV file."""
    return pd.read_csv(filepath)

def preprocess_data(df):
    """Preprocess data by handling missing values and converting data types."""
    # Drop rows with missing values
    df = df.dropna()
    # Convert amount to numeric, handling non-numeric values
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  
    return df.dropna()  # Drop rows where conversion to numeric failed

def calculate_statistics(df):
    """Calculate statistical metrics for each category."""
    stats = df.groupby('category')['amount'].agg(['mean', 'median', 'std']).reset_index()
    # Handle cases with no variance
    stats['std'] = stats['std'].fillna(0)
    return stats

def add_outlier_thresholds(stats):
    # Adjust for categories with zero standard deviation
    stats['upper_limit'] = stats.apply(lambda x: x['mean'] + 2.5 * x['std'] if x['std'] > 0 else x['mean'] + 1, axis=1)
    stats['lower_limit'] = stats.apply(lambda x: x['mean'] - 2.5 * x['std'] if x['std'] > 0 else x['mean'] - 1, axis=1)
    return stats

def detect_anomalies(df, stats):
    merged = df.merge(stats, on='category')
    conditions = (
        (merged['amount'] > merged['upper_limit']) |
        (merged['amount'] < merged['lower_limit'])
    )
    anomalies = merged[conditions]
    return anomalies[['transaction_id', 'date', 'category', 'amount']]

def generate_report(anomalies):
    anomalies.to_csv('anomalies_report.csv', index=False)
    print("Report generated: anomalies_report.csv")

def generate_statistics_report(stats):
    stats.to_csv('category_statistics.csv', index=False)
    print("Statistics report generated: category_statistics.csv")

def main():

    df = load_data('sample_transactions.csv')
    df = preprocess_data(df)
    stats = calculate_statistics(df)
    stats = add_outlier_thresholds(stats)
    generate_statistics_report(stats) 
    anomalies = detect_anomalies(df, stats)
    generate_report(anomalies)

if __name__ == "__main__":
    main()
