import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import numpy as np
from datetime import timedelta


# ==========================================
# 1. DATA INGESTION & CLEANING
# ==========================================

def load_and_process_data():
    print("⏳ Loading Datasets...")

    # Helper to load files
    def load_files(pattern):
        files = glob.glob(pattern)
        dfs = []
        for f in files:
            try:
                df = pd.read_csv(f)
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
                dfs.append(df)
            except:
                continue
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    # Load Data
    df_enrol = load_files('UIDAI_Dataset/api_data_aadhar_enrolment/api_data_aadhar_enrolment_*.csv')
    df_bio = load_files('UIDAI_Dataset/api_data_aadhar_biometric/api_data_aadhar_biometric_*.csv')
    df_demo = load_files('UIDAI_Dataset/api_data_aadhar_demographic/api_data_aadhar_demographic_*.csv')

    # Standardize State Names
    state_map = {
        'Westbengal': 'West Bengal', 'West  Bengal': 'West Bengal',
        'Uttaranchal': 'Uttarakhand', 'Orissa': 'Odisha',
        'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra and Nagar Haveli'
    }

    for df in [df_enrol, df_bio, df_demo]:
        if 'state' in df.columns:
            df['state'] = df['state'].replace(state_map).str.strip().str.title()
            # Fill numeric nulls
            num_cols = df.select_dtypes(include=np.number).columns
            df[num_cols] = df[num_cols].fillna(0)

    print(f"✔ Loaded: {len(df_enrol)} Enrolments, {len(df_bio)} Bio Updates, {len(df_demo)} Demo Updates")
    return df_enrol, df_bio, df_demo


# ==========================================
# 2. ANALYTICAL VISUALIZATIONS (The 5 Questions)
# ==========================================

def q1_maintenance_gap(df_enrol, df_bio, df_demo):
    """
    Q1: Identify states where enrolment is high but updates are low.
    Metric: Maintenance Index
    """
    # Aggregation
    enrol_agg = df_enrol.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum(axis=1)
    bio_agg = df_bio.groupby('state')[['bio_age_5_17', 'bio_age_17_']].sum().sum(axis=1)
    demo_agg = df_demo.groupby('state')[['demo_age_5_17', 'demo_age_17_']].sum().sum(axis=1)

    df_combined = pd.DataFrame({'Enrolment': enrol_agg, 'Updates': bio_agg + demo_agg}).dropna()

    # Filter for significant states only (>1000 enrolments) to reduce noise
    df_combined = df_combined[df_combined['Enrolment'] > 1000]

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_combined, x='Enrolment', y='Updates', s=100, color='blue', alpha=0.6)

    # Highlight "Danger Zone" (High Enrolment, Low Updates)
    for state, row in df_combined.iterrows():
        # Label Outliers
        if row['Enrolment'] > df_combined['Enrolment'].quantile(0.8) or row['Updates'] > df_combined[
            'Updates'].quantile(0.8):
            plt.text(row['Enrolment'] + 50, row['Updates'], state, fontsize=9)

    plt.title('Q1: The "Maintenance Gap" (High Growth vs. Low Hygiene)', fontsize=14)
    plt.xlabel('Total New Enrolments (Growth)', fontsize=12)
    plt.ylabel('Total Updates (Maintenance)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


def q2_compliance_ratio(df_enrol, df_bio):
    """
    Q2: Age-wise enrolment growth vs demographic correction frequency.
    Focus: Age 5-17 (School Age)
    """
    enrol_5_17 = df_enrol.groupby('state')['age_5_17'].sum()
    bio_5_17 = df_bio.groupby('state')['bio_age_5_17'].sum()

    df_comp = pd.DataFrame({'New_Kids': enrol_5_17, 'Mandatory_Updates': bio_5_17})
    df_comp = df_comp.sort_values('New_Kids', ascending=False).head(10)  # Top 10 States

    df_comp.plot(kind='bar', figsize=(12, 6), color=['#3498db', '#e74c3c'])
    plt.title('Q2: Compliance Gap in Age 5-17 (New Enrolments vs Mandatory Updates)', fontsize=14)
    plt.ylabel('Volume', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


def q3_urban_rural_divide(df_bio, df_demo):
    """
    Q3: Urban vs Rural behavior.
    Metric: Digital Ratio (Demo/Bio)
    """
    # Group by Pincode
    demo_pin = df_demo.groupby('pincode')[['demo_age_17_']].sum()
    bio_pin = df_bio.groupby('pincode')[['bio_age_17_']].sum()

    df_pin = demo_pin.join(bio_pin, lsuffix='_d', rsuffix='_b').fillna(0)
    df_pin['Total_Vol'] = df_pin['demo_age_17_'] + df_pin['bio_age_17_']

    # Filter valid data
    df_pin = df_pin[df_pin['Total_Vol'] > 100]
    df_pin['Digital_Ratio'] = df_pin['demo_age_17_'] / (df_pin['bio_age_17_'] + 1)

    # Define "Rural" vs "Urban" proxy by Volume (Top 10% volume = Urban)
    vol_90 = df_pin['Total_Vol'].quantile(0.9)
    df_pin['Category'] = np.where(df_pin['Total_Vol'] > vol_90, 'Urban (High Vol)', 'Rural (Low Vol)')

    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Category', y='Digital_Ratio', data=df_pin, palette="Set2")
    plt.title('Q3: The Digital Divide (Ratio of Phone Updates to Biometric Updates)', fontsize=14)
    plt.ylabel('Digital Ratio (Phone Updates per 1 Bio Update)', fontsize=12)
    plt.ylim(0, 20)  # Limit y-axis to remove extreme outliers for readability
    plt.show()


def q4_load_volatility(df_demo):
    """
    Q4: Detect anomalies where updates spike unusually.
    Metric: Daily Volume
    """
    daily_load = df_demo.groupby('date')[['demo_age_5_17', 'demo_age_17_']].sum().sum(axis=1)

    # Identify Spikes (Mean + 2 Std Dev)
    limit = daily_load.mean() + (2 * daily_load.std())
    spikes = daily_load[daily_load > limit]

    plt.figure(figsize=(12, 6))
    plt.plot(daily_load.index, daily_load.values, label='Daily Transactions', color='grey', alpha=0.7)
    plt.scatter(spikes.index, spikes.values, color='red', label='Anomalies (>2σ)', s=50, zorder=5)

    plt.title('Q4: Operational Anomalies & Load Volatility (2025)', fontsize=14)
    plt.ylabel('Transactions per Day', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def q5_load_forecast(df_demo):
    """
    Q5: Forecast future enrolment/update load.
    Method: Weekly Aggregation + Linear Trend Projection
    """
    # Resample to Weekly
    weekly = df_demo.set_index('date').resample('W')[['demo_age_17_']].sum().sum(axis=1)

    # Create simple forecast (Avg of last 4 weeks projected forward)
    last_4_avg = weekly.tail(4).mean()
    growth_rate = (weekly.iloc[-1] - weekly.iloc[-4]) / weekly.iloc[-4]  # Simple momentum

    # Generate next 12 weeks
    last_date = weekly.index[-1]
    future_dates = [last_date + timedelta(weeks=x) for x in range(1, 13)]
    future_vals = [last_4_avg * (1 + (growth_rate * 0.1 * i)) for i in range(1, 13)]  # Conservative growth

    plt.figure(figsize=(12, 6))
    plt.plot(weekly.index, weekly.values, label='Actual Data (2025)', linewidth=2)
    plt.plot(future_dates, future_vals, label='Q1 2026 Forecast', linestyle='--', color='green', linewidth=2)

    plt.title('Q5: Q1 2026 Load Forecast (Projecting Current Momentum)', fontsize=14)
    plt.ylabel('Weekly Volume', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()


# ==========================================
# 3. EXECUTION
# ==========================================
if __name__ == "__main__":
    df_e, df_b, df_d = load_and_process_data()

    if not df_e.empty:
        q1_maintenance_gap(df_e, df_b, df_d)
        q2_compliance_ratio(df_e, df_b)
        q3_urban_rural_divide(df_b, df_d)
        q4_load_volatility(df_d)
        q5_load_forecast(df_d)
    else:
        print("❌ Data not found. Please check file paths.")