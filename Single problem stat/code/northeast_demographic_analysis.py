import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for plots
os.makedirs('northeast_plots', exist_ok=True)

def analyze_northeast_gaps():
    # Data based on the user's previous analysis findings
    states = ['Meghalaya', 'Assam', 'Mizoram', 'Nagaland', 'Arunachal Pradesh', 'Gujarat', 'Maharashtra', 'National Avg']
    # Percentage of new enrolments that are adults (18+)
    adult_share = [32.1, 9.9, 8.3, 7.5, 6.8, 1.2, 0.8, 0.9]
    # Total new enrolments (simulated for visualization)
    total_enrolments = [109000, 450000, 42000, 38000, 35000, 850000, 1200000, 5000000]
    
    df = pd.DataFrame({
        'State': states,
        'Adult_Share_Pct': adult_share,
        'Total_Enrolments': total_enrolments
    })
    
    # 1. Visualization: Adult Share vs National Average
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    
    # Sort for better visualization
    df_sorted = df.sort_values('Adult_Share_Pct', ascending=False)
    colors = ['#800000' if x > 5 else '#2F4F4F' for x in df_sorted['Adult_Share_Pct']]
    
    bars = plt.barh(df_sorted['State'], df_sorted['Adult_Share_Pct'], color=colors, alpha=0.8)
    plt.axvline(x=0.9, color='red', linestyle='--', label='National Average (0.9%)')
    
    # Add labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{width}%', va='center', fontweight='bold')

    plt.title('Figure 1: The "Hidden Cohort" - Adult Enrolment Share by State', fontsize=15, fontweight='bold')
    plt.xlabel('Percentage of New Enrolments that are Adults (18+)', fontsize=12)
    plt.legend()
    plt.tight_layout()
    plt.savefig('northeast_plots/adult_share_comparison.png')
    plt.close()

    # 2. Visualization: Composition of Enrolments (Children vs Adults)
    # Focus on Meghalaya vs National Avg
    comp_data = {
        'Category': ['Children (0-17)', 'Adults (18+)'],
        'Meghalaya': [67.9, 32.1],
        'National': [99.1, 0.9]
    }
    df_comp = pd.DataFrame(comp_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.pie(df_comp['Meghalaya'], labels=df_comp['Category'], autopct='%1.1f%%', colors=['#66b3ff','#ff9999'], startangle=90)
    ax1.set_title('Meghalaya Enrolment Mix')
    
    ax2.pie(df_comp['National'], labels=df_comp['Category'], autopct='%1.1f%%', colors=['#66b3ff','#ff9999'], startangle=90)
    ax2.set_title('National Enrolment Mix')
    
    plt.suptitle('Figure 2: Regional Demographic Divergence', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('northeast_plots/demographic_mix.png')
    plt.close()
    
    return df

if __name__ == "__main__":
    results = analyze_northeast_gaps()
    print("North-East Demographic Analysis Complete.")
    print(results[['State', 'Adult_Share_Pct']].to_string(index=False))
