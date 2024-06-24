import pandas as pd

def load_data(filepath):
    """Load and preprocess data from a CSV file."""
    df = pd.read_csv(filepath)
    df['amount'] = df['amount'].astype(str)
    df['amount'] = df['amount'].str.extract('(\d+\.\d+)', expand=False)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df.dropna(inplace=True)  # Drop rows with missing or malformed data
    return df

def calculate_statistics(df):
    stats = df.groupby('category')['amount'].agg(['mean', 'median', 'std']).reset_index()
    return stats

def detect_anomalies(df, stats):
    anomalies = []
    for index, row in stats.iterrows():
        category_data = df[df['category'] == row['category']]
        threshold = 2
        mean = row['mean']
        std = row['std']
        anomaly_filter = (category_data['amount'] > mean + threshold * std) | (category_data['amount'] < mean - threshold * std)
        anomalies.append(category_data[anomaly_filter])
    anomalies = pd.concat(anomalies).drop_duplicates().reset_index(drop=True)
    return anomalies

def generate_report(anomalies):
    print("Anomalies Report:")
    print(anomalies)

if __name__ == "__main__":
    filepath = 'transactions.csv'
    data = load_data(filepath)
    statistics = calculate_statistics(data)
    anomalies = detect_anomalies(data, statistics)
    generate_report(anomalies)


import matplotlib.pyplot as plt

def plot_data(df):
    for category in df['category'].unique():
        plt.figure()
        category_data = df[df['category'] == category]
        category_data['amount'].plot(kind='hist', bins=30, title=f"Amount Distribution - {category}")
        plt.show()

if __name__ == "__main__":
    filepath = 'transactions.csv'
    data = load_data(filepath)
    plot_data(data) 
    statistics = calculate_statistics(data)
    anomalies = detect_anomalies(data, statistics)
    generate_report(anomalies)

