import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob


# ============== LOAD & PREPROCESS ==============
def load_all_data():
    """Loads all datasets and applies standardization."""

    def clean_df(df):
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        state_map = {
            'Westbengal': 'West Bengal', 'Uttaranchal': 'Uttarakhand',
            'Orissa': 'Odisha'
        }
        df['state'] = df['state'].replace(state_map).str.strip().str.title()
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        return df

    df_enrol = pd.concat([clean_df(pd.read_csv(f))
                          for f in glob('UIDAI_Dataset/api_data_aadhar_enrolment/*enrolment*.csv')], ignore_index=True)
    df_bio = pd.concat([clean_df(pd.read_csv(f))
                        for f in glob('UIDAI_Dataset/api_data_aadhar_biometric/*biometric*.csv')], ignore_index=True)
    df_demo = pd.concat([clean_df(pd.read_csv(f))
                         for f in glob('UIDAI_Dataset/api_data_aadhar_demographic/*demographic*.csv')], ignore_index=True)

    return df_enrol, df_bio, df_demo


# ============== FEATURE ENGINEERING ==============
def engineer_features(df_enrol, df_bio, df_demo):
    """Creates derived ratios for analysis."""

    # Aggregate by state
    state_enrol = df_enrol.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
    state_enrol['adult_share_pct'] = (state_enrol['age_18_greater'] /
                                      state_enrol.sum(axis=1) * 100)

    state_bio = df_bio.groupby('state')[['bio_age_18_greater']].sum()
    state_demo = df_demo.groupby('state')[['demo_age_18_greater']].sum()

    merged = state_enrol.join([state_bio, state_demo])
    merged['digital_drive_ratio'] = (merged['demo_age_18_greater'] /
                                     (merged['bio_age_18_greater'] + 1))

    return merged


# ============== ANOMALY DETECTION ==============
def detect_anomalies(df_enrol):
    """Identifies border districts and operational spikes."""

    border_districts = ['Sitamarhi', 'Bahraich', 'Murshidabad',
                        'South 24 Parganas', 'West Champaran']

    district_enrol = df_enrol.groupby('district')[['age_0_5', 'age_5_17',
                                                   'age_18_greater']].sum().sum(axis=1).sort_values(ascending=False)

    top_10 = district_enrol.head(10)
    border_count = sum(1 for d in top_10.index if any(b in d for b in border_districts))

    print(f"Border districts in top 10: {border_count}/10")

    # Weekly pattern
    df_enrol['weekday'] = df_enrol['date'].dt.day_name()
    weekly_load = df_enrol.groupby('weekday').size()

    return top_10, weekly_load


# ============== EXECUTION ==============
if __name__ == "__main__":
    df_enrol, df_bio, df_demo = load_all_data()
    features = engineer_features(df_enrol, df_bio, df_demo)
    anomalies, weekly = detect_anomalies(df_enrol)

    print("\n=== TOP STATES BY ADULT ENROLLMENT % ===")
    print(features['adult_share_pct'].sort_values(ascending=False).head(10))

    print("\n=== WEEKLY LOAD PATTERN ===")
    print(weekly)

    print("\n=== DIGITAL DIVIDE (RURAL) ===")
    print(features['digital_drive_ratio'].sort_values(ascending=False).head(5))