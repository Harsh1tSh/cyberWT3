import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['amount'] = df['amount'].astype(str).str.extract(r'(\d+\.\d+)')[0]
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    # Drop rows with missing or invalid data
    df.dropna(inplace=True)
    return df

def statistical_analysis(df):
    return df.groupby('category')['amount'].agg(['mean', 'median', 'std']).reset_index()

def detect_anomalies_zscore(df, threshold=3):
    anomalies = []
    for category in df['category'].unique():
        category_data = df[df['category'] == category].reset_index(drop=True)  
        mean = category_data['amount'].mean()
        std = category_data['amount'].std()

        # Calculate z-scores
        z_scores = (category_data['amount'] - mean) / std
        anomaly_filter = z_scores.abs() > threshold


        category_anomalies = category_data[anomaly_filter]
        anomalies.append(category_anomalies)

    return pd.concat(anomalies, ignore_index=True)






def detect_anomalies_iqr(df):
    anomalies = []
    for category in df['category'].unique():
        category_data = df[df['category'] == category]
        Q1 = category_data['amount'].quantile(0.25)
        Q3 = category_data['amount'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        category_anomalies = category_data[(category_data['amount'] < lower_bound) | (category_data['amount'] > upper_bound)]
        anomalies.append(category_anomalies)
    return pd.concat(anomalies)

def generate_anomalies_report(df, anomalies_zscore, anomalies_iqr):
    anomalies = pd.concat([anomalies_zscore, anomalies_iqr]).drop_duplicates()
    anomalies['reason_for_anomaly'] = anomalies.apply(
        lambda row: 'High Z-score' if 'zscore' in row and abs(row['zscore']) > 3 else 'Out of IQR bounds',
        axis=1
    )
    report_columns = ['transaction_id', 'date', 'category', 'amount', 'reason_for_anomaly']
    anomalies_report = anomalies[report_columns]
    return anomalies_report



def summarize_results(df, anomalies_report):
    summary_stats = {
        'total_transactions': df.shape[0],
        'total_anomalies': anomalies_report.shape[0],
        'anomaly_percentage': (anomalies_report.shape[0] / df.shape[0]) * 100,
        'anomalies_by_category': anomalies_report['category'].value_counts().to_dict()
    }
    return summary_stats


if __name__ == "__main__":
    data_path = 'transactions.csv'
    data = load_data(data_path)
    print(data.dtypes)  

    stats_df = statistical_analysis(data)
    anomalies_zscore = detect_anomalies_zscore(data)
    anomalies_iqr = detect_anomalies_iqr(data)
    anomalies_report = generate_anomalies_report(data, anomalies_zscore, anomalies_iqr)
    summary_stats = summarize_results(data, anomalies_report)

    print("Anomalies Report:")
    print(anomalies_report)
    print("\nSummary Statistics:")
    print(summary_stats)





