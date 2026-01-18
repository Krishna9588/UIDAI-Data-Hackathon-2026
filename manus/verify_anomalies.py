import pandas as pd
import glob
import os

def check_monthly_counts(pattern, name):
    files = glob.glob(pattern, recursive=True)
    if not files:
        print(f"No files found for {name}")
        return
    
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        dfs.append(df)
    
    master = pd.concat(dfs)
    master['month'] = master['date'].dt.to_period('M')
    counts = master.groupby('month').size()
    print(f"\nMonthly counts for {name}:")
    print(counts)

print("Verifying data anomalies...")
check_monthly_counts('/home/ubuntu/hackathon_repo/UIDAI_Dataset/api_data_aadhar_enrolment/*.csv', 'Enrolment')
check_monthly_counts('/home/ubuntu/hackathon_repo/UIDAI_Dataset/api_data_aadhar_demographic/*.csv', 'Demographic')
check_monthly_counts('/home/ubuntu/hackathon_repo/UIDAI_Dataset/api_data_aadhar_biometric/*.csv', 'Biometric')
