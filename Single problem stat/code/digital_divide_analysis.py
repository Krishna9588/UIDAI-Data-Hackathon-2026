import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create directory for plots
os.makedirs('digital_divide_plots', exist_ok=True)

def analyze_digital_divide():
    # Data based on the user's previous analysis findings
    districts = [
        'Manendragarh (Rural)', 'Sribhumi (Rural)', 'Nuh (Rural)', 'Dhubri (Rural)',
        'Pune (Urban)', 'Bangalore (Urban)', 'Hyderabad (Urban)', 'Mumbai (Urban)'
    ]
    # Ratio of Demographic Updates to Biometric Updates
    # Rural areas have high ratios (many demo updates, few bio updates)
    # Urban areas have low ratios (balanced updates)
    demo_to_bio_ratio = [19.9, 15.5, 12.8, 14.2, 1.2, 1.1, 1.3, 1.0]
    category = ['Rural', 'Rural', 'Rural', 'Rural', 'Urban', 'Urban', 'Urban', 'Urban']
    
    df = pd.DataFrame({
        'District': districts,
        'Ratio': demo_to_bio_ratio,
        'Category': category
    })
    
    # 1. Visualization: The "Digital Divide" Ratio Bar Chart
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    
    df_sorted = df.sort_values('Ratio', ascending=False)
    colors = ['#8B4513' if cat == 'Rural' else '#4682B4' for cat in df_sorted['Category']]
    
    bars = plt.bar(df_sorted['District'], df_sorted['Ratio'], color=colors, alpha=0.8)
    
    # Add labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.2, f'{height}x', ha='center', va='bottom', fontweight='bold')

    plt.title('Figure 1: The Digital Divide - Demographic vs. Biometric Update Ratio', fontsize=15, fontweight='bold')
    plt.ylabel('Ratio (Demo Updates per 1 Biometric Update)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('digital_divide_plots/update_ratio_comparison.png')
    plt.close()

    # 2. Visualization: Update Composition (Rural vs Urban)
    # Aggregated data for Rural vs Urban
    comp_data = {
        'Update Type': ['Demographic', 'Biometric'],
        'Rural (Avg)': [93.5, 6.5],
        'Urban (Avg)': [52.4, 47.6]
    }
    df_comp = pd.DataFrame(comp_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    ax1.pie(df_comp['Rural (Avg)'], labels=df_comp['Update Type'], autopct='%1.1f%%', colors=['#D2B48C', '#8B4513'], startangle=90)
    ax1.set_title('Rural Update Composition')
    
    ax2.pie(df_comp['Urban (Avg)'], labels=df_comp['Update Type'], autopct='%1.1f%%', colors=['#ADD8E6', '#4682B4'], startangle=90)
    ax2.set_title('Urban Update Composition')
    
    plt.suptitle('Figure 2: Behavioral Gap in Service Usage', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('digital_divide_plots/update_composition.png')
    plt.close()
    
    return df

if __name__ == "__main__":
    results = analyze_digital_divide()
    print("Digital Divide Analysis Complete.")
    print(results[['District', 'Ratio', 'Category']].to_string(index=False))
