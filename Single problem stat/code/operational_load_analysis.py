import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for plots
os.makedirs('operational_plots', exist_ok=True)

def analyze_operational_load():
    # Data based on the user's previous analysis findings
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Transaction volume in Millions
    volume = [4.5, 7.5, 4.1, 5.7, 4.9, 14.2, 3.3]
    # Static capacity baseline (assuming a fixed resource allocation)
    static_capacity = [7.0] * 7
    
    df = pd.DataFrame({
        'Day': days,
        'Volume': volume,
        'Capacity': static_capacity
    })
    
    # Calculate Efficiency/Stress
    df['Status'] = df.apply(lambda x: 'Overloaded' if x['Volume'] > x['Capacity'] else 'Underutilized', axis=1)
    df['Gap'] = df['Volume'] - df['Capacity']

    # 1. Visualization: Load vs Static Capacity
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    plt.plot(df['Day'], df['Volume'], marker='o', linewidth=4, color='#1f77b4', label='Actual Transaction Volume')
    plt.axhline(y=7.0, color='red', linestyle='--', linewidth=2, label='Static Resource Capacity')
    
    # Fill areas to show waste vs stress
    plt.fill_between(df['Day'], df['Volume'], 7.0, where=(df['Volume'] > 7.0), color='red', alpha=0.2, label='System Stress/Latency')
    plt.fill_between(df['Day'], df['Volume'], 7.0, where=(df['Volume'] <= 7.0), color='green', alpha=0.1, label='Resource Wastage')

    plt.title('Figure 1: The "Static Capacity" Failure - Load vs. Resources', fontsize=15, fontweight='bold')
    plt.ylabel('Volume (Millions of Transactions)', fontsize=12)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('operational_plots/load_vs_capacity.png')
    plt.close()

    # 2. Visualization: Heatmap of the "Tuesday/Saturday" Spikes
    # Simulating hourly data for a "Heatmap" feel
    plt.figure(figsize=(10, 4))
    spike_data = [[4, 5, 7, 5, 5, 14, 3]] # Simplified 1D heatmap
    sns.heatmap(spike_data, annot=True, xticklabels=days, cmap='YlOrRd', cbar=False, fmt='d')
    plt.title('Figure 2: Weekly Operational Heatmap (Intensity of Load)', fontsize=14)
    plt.yticks([])
    plt.tight_layout()
    plt.savefig('operational_plots/load_heatmap.png')
    plt.close()
    
    return df

if __name__ == "__main__":
    results = analyze_operational_load()
    print("Operational Analysis Complete.")
    print(results[['Day', 'Volume', 'Status']].to_string(index=False))
