import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for plots
os.makedirs('border_plots', exist_ok=True)

def analyze_border_velocity():
    # Simulated data based on the user's previous analysis findings
    # Districts identified as sensitive border zones vs typical urban/inland districts
    data = {
        'District': [
            'Sitamarhi (Bihar-Nepal)', 'Bahraich (UP-Nepal)', 'Murshidabad (WB-Bangladesh)', 
            'West Champaran (Bihar-Nepal)', 'Araria (Bihar-Nepal)', 
            'Pune (Urban)', 'Jaipur (Urban)', 'Indore (Inland)', 'Nagpur (Inland)'
        ],
        'New_Enrolments': [45200, 38500, 41200, 39800, 37600, 15200, 14100, 13500, 12800],
        'Update_Frequency': [5200, 4800, 6100, 5500, 4900, 28500, 26400, 24200, 23100],
        'Category': ['Border', 'Border', 'Border', 'Border', 'Border', 'Urban', 'Urban', 'Inland', 'Inland']
    }
    
    df = pd.DataFrame(data)
    df['Velocity_Ratio'] = df['New_Enrolments'] / df['Update_Frequency']
    
    # 1. Visualization: Enrolment vs Updates
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    
    # Create a scatter plot to show the divergence
    scatter = sns.scatterplot(data=df, x='Update_Frequency', y='New_Enrolments', 
                              hue='Category', style='Category', s=200, palette='Set1')
    
    # Annotate points
    for i in range(df.shape[0]):
        plt.text(df.Update_Frequency[i]+500, df.New_Enrolments[i], df.District[i], 
                 fontsize=9, verticalalignment='center')

    plt.title('Figure 1: Divergence of Enrolment Velocity in Border Districts', fontsize=15, fontweight='bold')
    plt.xlabel('Update Frequency (Maintenance Activity)', fontsize=12)
    plt.ylabel('New Enrolments (Growth Activity)', fontsize=12)
    plt.tight_layout()
    plt.savefig('border_plots/enrolment_divergence.png')
    plt.close()

    # 2. Visualization: Velocity Ratio Bar Chart
    plt.figure(figsize=(12, 6))
    df_sorted = df.sort_values('Velocity_Ratio', ascending=False)
    colors = ['red' if cat == 'Border' else 'blue' for cat in df_sorted['Category']]
    
    plt.bar(df_sorted['District'], df_sorted['Velocity_Ratio'], color=colors, alpha=0.7)
    plt.axhline(y=df[df['Category'] != 'Border']['Velocity_Ratio'].mean(), color='green', linestyle='--', label='National/Urban Avg')
    
    plt.title('Figure 2: Enrolment Velocity Ratio (New Enrolments per 1 Update)', fontsize=15, fontweight='bold')
    plt.ylabel('Velocity Ratio', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig('border_plots/velocity_ratio.png')
    plt.close()
    
    return df

if __name__ == "__main__":
    results = analyze_border_velocity()
    print("Analysis Complete. Results summary:")
    print(results[['District', 'Velocity_Ratio']].to_string(index=False))
