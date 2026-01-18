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