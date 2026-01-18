import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="UIDAI Insights Dashboard 2026",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
    }
    .highlight {
        color: #ff4b4b;
        font-weight: bold;
    }
    div.block-container {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DATA LOADING ENGINE (SMART SEARCH)
# ==========================================
@st.cache_data
def load_data_recursive():
    """
    Scans the ENTIRE current directory and all subfolders to find
    CSV files matching the UIDAI keywords.
    """
    data_store = {
        "enrol": [],
        "bio": [],
        "demo": []
    }

    # 1. SCANNING FILES
    current_dir = os.getcwd()
    file_log = {"enrol": 0, "bio": 0, "demo": 0}

    # Walk through all folders
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if not file.endswith(".csv"):
                continue

            file_path = os.path.join(root, file)

            # Match keywords
            if "api_data_aadhar_enrolment" in file:
                data_store["enrol"].append(file_path)
            elif "api_data_aadhar_biometric" in file:
                data_store["bio"].append(file_path)
            elif "api_data_aadhar_demographic" in file:
                data_store["demo"].append(file_path)

    # 2. LOADING DATA
    final_dfs = {}

    for key, paths in data_store.items():
        if not paths:
            final_dfs[key] = pd.DataFrame()
            continue

        dfs = []
        for p in paths:
            try:
                df = pd.read_csv(p)
                # Quick Date Standardization
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
                dfs.append(df)
            except Exception as e:
                continue

        if dfs:
            final_dfs[key] = pd.concat(dfs, ignore_index=True)
            file_log[key] = len(dfs)
        else:
            final_dfs[key] = pd.DataFrame()

    # 3. CLEANING DATA (State Names & Nulls)
    state_map = {
        'Westbengal': 'West Bengal', 'West  Bengal': 'West Bengal',
        'Uttaranchal': 'Uttarakhand', 'Orissa': 'Odisha',
        'The Dadra And Nagar Haveli And Daman And Diu': 'Dadra and Nagar Haveli'
    }

    for key in final_dfs:
        df = final_dfs[key]
        if not df.empty and 'state' in df.columns:
            df['state'] = df['state'].replace(state_map)
            df['state'] = df['state'].str.strip().str.title()

            # Fill numeric nulls with 0
            num_cols = df.select_dtypes(include=['number']).columns
            df[num_cols] = df[num_cols].fillna(0)
            final_dfs[key] = df

    return final_dfs, file_log


# Execute Load
with st.spinner('🚀 Scanning folders for UIDAI datasets...'):
    data_dict, log_counts = load_data_recursive()

df_enrol = data_dict['enrol']
df_bio = data_dict['bio']
df_demo = data_dict['demo']

# Check if data loaded
total_files = sum(log_counts.values())
if total_files == 0:
    st.error("⚠️ No matching CSV files found!")
    st.warning(f"Searched in: `{os.getcwd()}` and all subfolders.")
    st.info(
        "Expected filenames should contain: `api_data_aadhar_enrolment`, `api_data_aadhar_biometric`, or `api_data_aadhar_demographic`.")
    st.stop()

# ==========================================
# 3. DASHBOARD SIDEBAR
# ==========================================
with st.sidebar:
    st.title("UIDAI Analytics 2026")
    st.image("https://upload.wikimedia.org/wikipedia/en/c/cf/Aadhaar_Logo.svg", width=150)

    st.markdown("### 🎯 Navigation")
    page = st.radio("Go to:",
                    ["Executive Summary", "Border Security", "Ops Efficiency", "Societal Trends", "Raw Data Inspector"])

    st.markdown("---")
    st.markdown("### 📂 Data Source Status")


    # Visual status indicators
    def status_icon(count):
        return "✅" if count > 0 else "❌"


    st.write(f"{status_icon(log_counts['enrol'])} **Enrolment Files:** {log_counts['enrol']}")
    st.write(f"{status_icon(log_counts['bio'])} **Biometric Files:** {log_counts['bio']}")
    st.write(f"{status_icon(log_counts['demo'])} **Demographic Files:** {log_counts['demo']}")

    st.caption("Auto-detected from project folder")

# ==========================================
# 4. PAGE: EXECUTIVE SUMMARY
# ==========================================
if page == "Executive Summary":
    st.title("🇮🇳 Executive Summary: Societal Trends in Aadhaar")
    st.markdown("### Identifying Systemic Anomalies & Operational Risks")

    # KPI Row
    c1, c2, c3, c4 = st.columns(4)

    total_enrol = df_enrol.select_dtypes(include='number').sum().sum() if not df_enrol.empty else 0
    total_updates = (df_bio.select_dtypes(include='number').sum().sum() +
                     df_demo.select_dtypes(include='number').sum().sum()) if not df_bio.empty else 0

    with c1:
        st.metric("Total Transactions", f"{(total_enrol + total_updates) / 1000000:.1f}M", "2025 Data")
    with c2:
        st.metric("New Enrolments", f"{total_enrol / 1000000:.2f}M", "Growth")
    with c3:
        st.metric("Top Anomaly", "North-East", "Adult Spike")
    with c4:
        st.metric("Risk Zone", "Border Districts", "High Velocity")

    st.markdown("---")

    # Main problem Statement
    st.info(
        "💡 **Core Problem:** The system operates on a 'One-Size-Fits-All' model, failing to distinguish between **Urban Maintenance** (Phone updates), **Border Security** (Migration velocity), and **Rural Catch-up** (Adult enrolment).")

    # 4 Key Insights Cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h4>🚨 1. Border Integrity Risk</h4>
            <p>50% of high-growth districts are in sensitive border zones. Enrolment velocity here exceeds natural population growth rates.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class='metric-card'>
            <h4>📉 2. The "Tuesday/Saturday" Crush</h4>
            <p>Static server allocation causes massive load spikes on Saturdays (14M) and Tuesdays (7.5M), wasting capacity on other days.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h4>👴 3. The "Hidden Adult" Cohort</h4>
            <p>Meghalaya & Assam show >30% adult enrolment share (vs <1% National Avg), indicating a massive "Catch-up" phase.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        <div class='metric-card'>
            <h4>📱 4. The Digital Divide</h4>
            <p>Rural citizens update Demographics (Phones) 20x more than Biometrics, risking database obsolescence.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 5. PAGE: BORDER SECURITY
# ==========================================
elif page == "Border Security":
    st.title("🚨 Insight 1: The Border Velocity Anomaly")
    st.markdown("Comparing **New Enrolment Velocity** between Border Districts and Metro Hubs.")

    if not df_enrol.empty:
        # Aggregating Data
        dist_agg = df_enrol.groupby(['state', 'district']).sum(numeric_only=True).sum(axis=1).reset_index(
            name='New_Enrolments')
        top_districts = dist_agg.sort_values('New_Enrolments', ascending=False).head(15)


        # Color coding for plot
        def get_color(row):
            border_districts = ['Sitamarhi', 'Bahraich', 'Murshidabad', 'South 24 Parganas', 'West Champaran',
                                'Purbi Champaran', 'North 24 Parganas']
            return 'red' if row['district'] in border_districts else 'grey'


        top_districts['color'] = top_districts.apply(get_color, axis=1)

        fig = px.bar(
            top_districts,
            x='district',
            y='New_Enrolments',
            color='color',
            color_discrete_map={'red': '#ff4b4b', 'grey': '#bdc3c7'},
            title="Top 15 Districts by Enrolment Volume (Red = Sensitive Border Zone)",
            text_auto='.2s'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.warning(
            "**Observation:** Border districts like **Sitamarhi** and **Bahraich** are enrolling people at the same rate as massive metro hubs like **Thane** or **Pune**, despite having a fraction of the population density. This suggests unnatural growth.")
    else:
        st.error("No Enrolment Data Found.")

# ==========================================
# 6. PAGE: OPS EFFICIENCY
# ==========================================
elif page == "Ops Efficiency":
    st.title("⚙️ Insight 2: Operational Heartbeat")
    st.markdown("Analyzing Server Load to Optimize Infrastructure.")

    if not df_demo.empty:
        # 1. Weekly Trend
        df_demo['weekday'] = df_demo['date'].dt.day_name()
        weekly_load = df_demo.groupby('weekday').sum(numeric_only=True).sum(axis=1)

        # Sort days
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_load = weekly_load.reindex(days)

        fig_week = px.line(
            x=weekly_load.index,
            y=weekly_load.values,
            markers=True,
            title='Weekly Load Distribution: The "Double Spike" Pattern'
        )
        fig_week.update_traces(line_color='#1f77b4', line_width=4)
        fig_week.add_annotation(x='Tuesday', y=weekly_load.get('Tuesday', 0), text="Tuesday Surge", showarrow=True)
        fig_week.add_annotation(x='Saturday', y=weekly_load.get('Saturday', 0), text="Weekend Crush", showarrow=True)

        st.plotly_chart(fig_week, use_container_width=True)

        # 2. Monthly Trend (The August Gap)
        monthly_load = df_demo.set_index('date').resample('M').sum(numeric_only=True).sum(axis=1)

        fig_month = px.area(
            x=monthly_load.index,
            y=monthly_load.values,
            title='Yearly Timeline: The "August Blackout" & "September Surge"'
        )
        fig_month.update_traces(line_color='#ff4b4b')
        st.plotly_chart(fig_month, use_container_width=True)

        st.success(
            "**Recommendation:** Implement automated server auto-scaling on **Tuesday (10 AM)** and **Saturday (9 AM)**. Investigate the August data loss event.")
    else:
        st.error("No Demographic Data found for Operational Analysis.")

# ==========================================
# 7. PAGE: SOCIETAL TRENDS
# ==========================================
elif page == "Societal Trends":
    st.title("👥 Insight 3 & 4: Societal Shifts")

    tab1, tab2 = st.tabs(["The North-East Anomaly", "The Digital Divide"])

    with tab1:
        st.markdown("### The 'Hidden Adult' Cohort")
        if not df_enrol.empty:
            state_stats = df_enrol.groupby('state')[['age_0_5', 'age_18_greater']].sum()
            state_stats['Adult_Share'] = (state_stats['age_18_greater'] / state_stats.sum(axis=1)) * 100
            top_states = state_stats.sort_values('Adult_Share', ascending=False).head(10)

            fig_ne = px.bar(
                top_states,
                x='Adult_Share',
                y=top_states.index,
                orientation='h',
                title="Percentage of Enrolments that are Adults (18+)",
                color='Adult_Share',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_ne, use_container_width=True)
            st.info(
                "While the national average is <1%, **Meghalaya** is at **32%**. The system needs 'Adult-Centric' centers here.")

    with tab2:
        st.markdown("### The Rural Digital Divide")
        st.markdown("Ratio of **Demographic Updates** (Phone/Address) to **Biometric Updates**.")

        if not df_bio.empty and not df_demo.empty:
            # Calculate simple ratio per state/district for Top 10
            demo_count = df_demo.groupby('district').sum(numeric_only=True).sum(axis=1)
            bio_count = df_bio.groupby('district').sum(numeric_only=True).sum(axis=1)

            ratio_df = pd.DataFrame({'Demo': demo_count, 'Bio': bio_count}).fillna(0)
            ratio_df['Ratio'] = ratio_df['Demo'] / (ratio_df['Bio'] + 1)
            ratio_df = ratio_df[ratio_df['Bio'] > 100]  # Filter small noise

            top_ratio = ratio_df.sort_values('Ratio', ascending=False).head(10)

            fig_div = px.bar(
                top_ratio,
                y=top_ratio.index,
                x='Ratio',
                orientation='h',
                title="Top Districts Ignoring Biometric Updates (High Demo:Bio Ratio)",
                color_discrete_sequence=['orange']
            )
            st.plotly_chart(fig_div, use_container_width=True)
            st.warning(
                "Districts like **Manendragarh** have a 20:1 ratio. People update phones for benefits but ignore biometrics.")
        else:
            st.error("Need both Demographic and Biometric data to calculate this ratio.")

# ==========================================
# 8. PAGE: RAW DATA INSPECTOR
# ==========================================
elif page == "Raw Data Inspector":
    st.title("🔍 Data Inspector")
    st.markdown("Filter and explore the raw data used for this analysis.")

    dataset_choice = st.selectbox("Select Dataset", ["Enrolment", "Biometric Updates", "Demographic Updates"])

    target_df = pd.DataFrame()
    if dataset_choice == "Enrolment":
        target_df = df_enrol
    elif dataset_choice == "Biometric Updates":
        target_df = df_bio
    else:
        target_df = df_demo

    if not target_df.empty:
        # Simple Filter
        states = st.multiselect("Filter by State", target_df['state'].unique())
        if states:
            target_df = target_df[target_df['state'].isin(states)]

        st.dataframe(target_df.head(1000), use_container_width=True)

        # Download Button
        csv = target_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Filtered Data",
            csv,
            "filtered_data.csv",
            "text/csv",
            key='download-csv'
        )
    else:
        st.warning(f"{dataset_choice} dataset is empty.")