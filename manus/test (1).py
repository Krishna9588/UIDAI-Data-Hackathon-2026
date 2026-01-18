import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
import os

# Set a consistent style for better presentation
plt.style.use('seaborn-v0_8-whitegrid')

# ==========================================
# 1. DATA LOADING & PREPROCESSING UTILS
# ==========================================

# NOTE: The original script used hardcoded data for plots. 
# For the final submission, the user should use the actual loaded data.
# Since the goal is to generate the visualizations based on the user's existing logic, 
# we will use the hardcoded data from the user's script for reproducibility of their intended figures.

# ==========================================
# 2. VISUALIZATION FUNCTIONS
# ==========================================

def plot_border_anomaly():
    """
    Generates Figure 1: Border District Velocity.
    Highlights the disproportionate enrolment in border zones.
    """
    districts = ['Thane (Urban)', 'Sitamarhi (Border)', 'Bahraich (Border)',
                 'Murshidabad (Border)', 'South 24 Parganas (Coastal)',
                 'Pune (Urban)', 'Jaipur (Urban)', 'Bangalore (Urban)']
    values = [43688, 42232, 39338, 35911, 33540, 31763, 31146, 30980]
    colors = ['#4c72b0', '#c44e52', '#c44e52', '#c44e52', '#f58518', '#4c72b0', '#4c72b0', '#4c72b0'] # Custom colors for clarity

    plt.figure(figsize=(12, 6))
    bars = plt.bar(districts, values, color=colors)
    
    # Add labels to bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 500, f'{yval:,}', ha='center', va='bottom', fontsize=9)

    plt.title('Figure 1: High Enrolment Velocity in Border Districts (Red)', fontsize=16, pad=20)
    plt.ylabel('New Enrolments (Count)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('figure_1_border_anomaly.png')
    plt.close()


def plot_operational_load():
    """
    Generates Figure 2: The Tuesday/Saturday Spike.
    Shows the weekly load distribution derived from full dataset.
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Aggregated volume in Millions
    load = [4.5, 7.5, 4.1, 5.7, 4.9, 14.2, 3.3]

    plt.figure(figsize=(10, 5))
    plt.plot(days, load, marker='o', linewidth=3, color='#1f77b4', zorder=2)
    plt.fill_between(days, load, color='#1f77b4', alpha=0.1, zorder=1)

    # Highlight Spikes
    plt.scatter(['Tuesday'], [7.5], marker='o', color='orange', s=150, zorder=3)
    plt.scatter(['Saturday'], [14.2], marker='o', color='red', s=150, zorder=3)
    
    # Add text labels
    for i, (day, val) in enumerate(zip(days, load)):
        plt.text(i, val + 0.5, f'{val}M', ha='center', va='bottom', fontsize=10)

    plt.title('Figure 2: Weekly Operational Load - The "Double Spike" Pattern', fontsize=16, pad=20)
    plt.ylabel('Transaction Volume (Millions)', fontsize=12)
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.savefig('figure_2_operational_load.png')
    plt.close()


def plot_northeast_anomaly():
    """
    Generates Figure 3: Adult Enrolment Share.
    Contrasts National Average with North-East states.
    """
    states = ['Meghalaya', 'Assam', 'Mizoram', 'Gujarat', 'National Avg']
    pct = [32.1, 9.9, 8.3, 5.8, 0.9]
    colors = ['#c44e52', '#c44e52', '#c44e52', '#4c72b0', '#55a868'] # Highlight anomalies in red

    plt.figure(figsize=(10, 5))
    bars = plt.barh(states, pct, color=colors)
    
    # Add labels to bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center', fontsize=10)

    plt.title('Figure 3: % of New Enrolments that are Adults (18+)', fontsize=16, pad=20)
    plt.xlabel('Percentage (%)', fontsize=12)
    plt.gca().invert_yaxis() # Highest percentage at the top
    plt.tight_layout()
    plt.savefig('figure_3_northeast_anomaly.png')
    plt.close()


def plot_digital_divide():
    """
    Generates Figure 4: The Digital Divide.
    Compares Demographic vs Biometric update ratios.
    """
    regions = ['Manendragarh (Rural)', 'Sribhumi (Rural)', 'Pune (Urban)', 'Bangalore (Urban)']
    ratios = [19.9, 15.5, 1.2, 1.1]  # Derived from "Digital_Drive_Ratio"
    colors = ['#c44e52', '#c44e52', '#4c72b0', '#4c72b0']

    plt.figure(figsize=(10, 5))
    bars = plt.bar(regions, ratios, color=colors)
    
    # Add labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.1f}:1', ha='center', va='bottom', fontsize=10)

    plt.title('Figure 4: The Digital Divide (Demographic vs Biometric Ratio)', fontsize=16, pad=20)
    plt.ylabel('Ratio (Demo Updates per 1 Bio Update)', fontsize=12)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('figure_4_digital_divide.png')
    plt.close()


def plot_temporal_anomaly():
    """
    Generates Figure 5: August Blackout & September Surge.
    """
    months = ['June', 'July', 'August', 'September', 'October']
    volume = [0.21, 0.61, 0.0, 1.47, 0.81]  # Millions

    plt.figure(figsize=(10, 5))
    plt.plot(months, volume, color='black', linestyle='--', marker='o', zorder=2)
    bars = plt.bar(months, volume, color=['#4c72b0', '#4c72b0', '#c44e52', '#f58518', '#4c72b0'], alpha=0.7, zorder=1)
    
    # Add labels
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f'{yval:.2f}M', ha='center', va='bottom', fontsize=10)

    plt.title('Figure 5: The "August Blackout" and Recovery Surge', fontsize=16, pad=20)
    plt.ylabel('Enrolments (Millions)', fontsize=12)
    plt.tight_layout()
    plt.savefig('figure_5_temporal_anomaly.png')
    plt.close()


def plot_correlation_matrix():
    """
    Generates correlation matrix heatmap.
    Confirming link between Adult Demo Updates and Child Enrolment.
    """
    # Sample Correlation Data derived from analysis
    data = {
        'Adult_Demo_Updates': [1.0, 0.95, 0.2, 0.1],
        'Child_Enrolments': [0.95, 1.0, 0.25, 0.15],
        'Biometric_Updates': [0.2, 0.25, 1.0, 0.8],
        'Adult_Enrolments': [0.1, 0.15, 0.8, 1.0]
    }
    corr_df = pd.DataFrame(data, index=['Adult_Demo_Updates', 'Child_Enrolments',
                                        'Biometric_Updates', 'Adult_Enrolments'])

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f", linewidths=.5, linecolor='black')
    plt.title('Figure 6: Correlation Matrix - Predictive Indicators', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig('figure_6_correlation_matrix.png')
    plt.close()


def plot_maintenance_mode():
    """
    Generates trend line for Age 0-5 vs Age 5-17.
    """
    months = ['Sep', 'Oct', 'Nov', 'Dec']
    age_0_5 = [0.99, 0.56, 0.76, 0.56]  # Millions
    age_5_17 = [0.46, 0.23, 0.29, 0.18]  # Millions

    plt.figure(figsize=(10, 5))
    plt.plot(months, age_0_5, label='Age 0-5 (Newborns)', marker='o', linewidth=3, color='#55a868')
    plt.plot(months, age_5_17, label='Age 5-17 (School)', marker='x', linestyle='--', linewidth=3, color='#c44e52')
    
    plt.title('Figure 7: The Shift to "Maintenance Mode" (Newborn Dominance)', fontsize=16, pad=20)
    plt.ylabel('Enrolments (Millions)', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('figure_7_maintenance_mode.png')
    plt.close()


# ==========================================
# 3. EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    # We are not loading data here as the plots use hardcoded, derived values for the report.
    # The actual data loading logic is in the Streamlit app.
    print("Generating Analysis Plots...")

    # Run all visualizations
    plot_border_anomaly()
    plot_operational_load()
    plot_northeast_anomaly()
    plot_digital_divide()
    plot_temporal_anomaly()
    plot_correlation_matrix()
    plot_maintenance_mode()

    print("Analysis Complete. All charts saved as PNG files.")
