import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Create directory for plots
os.makedirs('plots', exist_ok=True)

def plot_border_anomaly():
    districts = ['Thane (Urban)', 'Sitamarhi (Border)', 'Bahraich (Border)',
                 'Murshidabad (Border)', 'South 24 Parganas (Coastal)',
                 'Pune (Urban)', 'Jaipur (Urban)', 'Bangalore (Urban)']
    values = [12000, 45000, 38000, 41000, 35000, 15000, 14000, 13000]
    colors = ['grey', 'red', 'red', 'red', 'orange', 'grey', 'grey', 'grey']

    plt.figure(figsize=(10, 6))
    plt.bar(districts, values, color=colors)
    plt.title('Figure 1: High Enrolment Velocity in Border Districts (Red)', fontsize=14)
    plt.ylabel('New Enrolments (Count)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('plots/figure1_border_anomaly.png')
    plt.close()

def plot_operational_load():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    load = [4.5, 7.5, 4.1, 5.7, 4.9, 14.2, 3.3]

    plt.figure(figsize=(10, 5))
    plt.plot(days, load, marker='o', linewidth=3, color='#1f77b4')
    plt.fill_between(days, load, color='#1f77b4', alpha=0.1)
    plt.plot(['Tuesday'], [7.5], marker='o', color='orange', markersize=10)
    plt.plot(['Saturday'], [14.2], marker='o', color='red', markersize=10)
    plt.title('Figure 2: Weekly Operational Load - The "Double Spike" Pattern', fontsize=14)
    plt.ylabel('Transaction Volume (Millions)', fontsize=12)
    plt.grid(True)
    plt.savefig('plots/figure2_operational_load.png')
    plt.close()

def plot_northeast_anomaly():
    states = ['Meghalaya', 'Assam', 'Mizoram', 'Gujarat', 'National Avg']
    pct = [32.1, 9.9, 8.3, 5.8, 0.9]

    plt.figure(figsize=(10, 5))
    plt.barh(states, pct, color=['maroon', 'red', 'red', 'grey', 'green'])
    plt.title('Figure 3: % of New Enrolments that are Adults (18+)', fontsize=14)
    plt.xlabel('Percentage (%)', fontsize=12)
    plt.tight_layout()
    plt.savefig('plots/figure3_northeast_anomaly.png')
    plt.close()

def plot_digital_divide():
    regions = ['Manendragarh (Rural)', 'Sribhumi (Rural)', 'Pune (Urban)', 'Bangalore (Urban)']
    ratios = [19.9, 15.5, 1.2, 1.1]

    plt.figure(figsize=(8, 5))
    plt.bar(regions, ratios, color=['brown', 'brown', 'blue', 'blue'])
    plt.title('Figure 4: The Digital Divide (Demographic vs Biometric Ratio)', fontsize=14)
    plt.ylabel('Ratio (Demo Updates per 1 Bio Update)', fontsize=12)
    plt.tight_layout()
    plt.savefig('plots/figure4_digital_divide.png')
    plt.close()

def plot_temporal_anomaly():
    months = ['June', 'July', 'August', 'September', 'October']
    volume = [0.21, 0.61, 0.0, 1.47, 0.81]

    plt.figure(figsize=(10, 5))
    plt.plot(months, volume, color='black', linestyle='--')
    plt.bar(months, volume, color=['grey', 'grey', 'red', 'orange', 'grey'], alpha=0.7)
    plt.title('Figure 5: The "August Blackout" and Recovery Surge', fontsize=14)
    plt.ylabel('Enrolments (Millions)', fontsize=12)
    plt.savefig('plots/figure5_temporal_anomaly.png')
    plt.close()

def plot_correlation_matrix():
    data = {
        'Adult_Demo_Updates': [1, 0.95, 0.2, 0.1],
        'Child_Enrolments': [0.95, 1, 0.25, 0.15],
        'Biometric_Updates': [0.2, 0.25, 1, 0.8],
        'Adult_Enrolments': [0.1, 0.15, 0.8, 1]
    }
    corr_df = pd.DataFrame(data, index=['Adult_Demo_Updates', 'Child_Enrolments',
                                      'Biometric_Updates', 'Adult_Enrolments'])

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix: Predicting Child Enrolment')
    plt.tight_layout()
    plt.savefig('plots/figure6_correlation_matrix.png')
    plt.close()

def plot_maintenance_mode():
    months = ['Sep', 'Oct', 'Nov', 'Dec']
    age_0_5 = [0.99, 0.56, 0.76, 0.56]
    age_5_17 = [0.46, 0.23, 0.29, 0.18]

    plt.figure(figsize=(10, 5))
    plt.plot(months, age_0_5, label='Age 0-5 (Newborns)', marker='o', linewidth=2)
    plt.plot(months, age_5_17, label='Age 5-17 (School)', marker='x', linestyle='--')
    plt.title('The Shift to "Maintenance Mode" (Newborn Dominance)')
    plt.ylabel('Enrolments (Millions)')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/figure7_maintenance_mode.png')
    plt.close()

if __name__ == "__main__":
    print("Generating Analysis Plots...")
    plot_border_anomaly()
    plot_operational_load()
    plot_northeast_anomaly()
    plot_digital_divide()
    plot_temporal_anomaly()
    plot_correlation_matrix()
    plot_maintenance_mode()
    print("Analysis Complete. Plots saved in 'plots' directory.")
