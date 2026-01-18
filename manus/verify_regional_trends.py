import pandas as pd
import glob

def load_data(pattern):
    files = glob.glob(pattern, recursive=True)
    dfs = [pd.read_csv(f) for f in files]
    return pd.concat(dfs)

print("Loading Enrolment Data...")
df_enrol = load_data('UIDAI_Dataset/api_data_aadhar_enrolment/*.csv')

# 1. North-East Anomaly
state_stats = df_enrol.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
state_stats['Adult_Share'] = (state_stats['age_18_greater'] / state_stats.sum(axis=1)) * 100
print("\nTop 10 States by Adult Enrolment Share:")
print(state_stats['Adult_Share'].sort_values(ascending=False).head(10))

# 2. Border District Velocity
dist_agg = df_enrol.groupby(['state', 'district']).size().reset_index(name='Transaction_Count')
# Note: Transaction_Count is number of records, but we should sum the actual enrolment numbers
dist_enrol = df_enrol.groupby(['state', 'district'])[['age_0_5', 'age_5_17', 'age_18_greater']].sum().sum(axis=1).reset_index(name='Total_Enrolments')
print("\nTop 15 Districts by Total Enrolments:")
print(dist_enrol.sort_values('Total_Enrolments', ascending=False).head(15))

# 3. Digital Divide (Demo vs Bio)
print("\nLoading Demographic and Biometric Data...")
df_demo = load_data('/home/ubuntu/hackathon_repo/UIDAI_Dataset/api_data_aadhar_demographic/*.csv')
df_bio = load_data('/home/ubuntu/hackathon_repo/UIDAI_Dataset/api_data_aadhar_biometric/*.csv')

demo_dist = df_demo.groupby('district')[['demo_age_5_17', 'demo_age_17_']].sum().sum(axis=1)
bio_dist = df_bio.groupby('district')[['bio_age_5_17', 'bio_age_17_']].sum().sum(axis=1)

ratio_df = pd.DataFrame({'Demo': demo_dist, 'Bio': bio_dist}).fillna(0)
ratio_df['Ratio'] = ratio_df['Demo'] / (ratio_df['Bio'] + 1)
print("\nTop 10 Districts by Demo:Bio Ratio (Min 1000 Bio updates):")
print(ratio_df[ratio_df['Bio'] > 1000].sort_values('Ratio', ascending=False).head(10))
