import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Marketing Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 10px;
        border-bottom: 3px solid #1f77b4;
    }
    h2 {
        color: #2c3e50;
        margin-top: 30px;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    .available-section {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 20px 0;
    }
    .unavailable-section {
        background-color: #ffebee;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        margin: 20px 0;
    }
    .data-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        margin: 5px;
    }
    .badge-available {
        background-color: #4caf50;
        color: white;
    }
    .badge-missing {
        background-color: #f44336;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Load data with caching for performance
@st.cache_data
def load_data():
    df = pd.read_csv('mntn.csv')
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    # Filter out rows where spend and impressions are zero
    df_filtered = df[(df['spend'] > 0) | (df['impressions'] > 0)].copy()
    return df_filtered

# Load the data
try:
    df = load_data()

    # Dashboard Title
    st.title("📊 Marketing Performance Dashboard")
    st.markdown("### CTV & Video Advertising Analytics - Data Availability Report")

    # Data availability badges at the top
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <h4 style='margin-top: 0;'>📋 Quick Data Status</h4>
            <span class='data-badge badge-available'>✅ 10 Metrics Available</span>
            <span class='data-badge badge-missing'>❌ 27 Metrics Missing</span>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Date range filter
    min_date = df['date'].min()
    max_date = df['date'].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['date'] >= pd.Timestamp(start_date)) &
                        (df['date'] <= pd.Timestamp(end_date))]
    else:
        df_filtered = df

    # Campaign filter
    campaigns = df_filtered['campaign'].dropna().unique()
    if len(campaigns) > 0:
        selected_campaigns = st.sidebar.multiselect(
            "Select Campaigns",
            options=sorted(campaigns),
            default=None
        )
        if selected_campaigns:
            df_filtered = df_filtered[df_filtered['campaign'].isin(selected_campaigns)]

    # Calculate available metrics
    total_spend = df_filtered['campaigngroup_spend'].sum()
    total_impressions = df_filtered['impressions'].sum()

    # CPM calculation
    cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0

    # Completed View Rate (weighted by impressions)
    if total_impressions > 0 and len(df_filtered) > 0:
        cvr_data = df_filtered[df_filtered['campaigngroup_completedviewrate'] > 0]
        if len(cvr_data) > 0:
            avg_cvr = np.average(
                cvr_data['campaigngroup_completedviewrate'],
                weights=cvr_data['impressions']
            )
        else:
            avg_cvr = 0
    else:
        avg_cvr = 0

    # Total completed views
    total_completed_views = df_filtered['campaigngroup_completedviews'].sum()

    # Total users reached
    total_users_reached = df_filtered['campaigngroup_usersreached'].sum()

    # Total visits
    total_visits = df_filtered['campaigngroup_visits'].sum()

    # ============================================================================
    # SECTION 1: AVAILABLE METRICS AND DATA
    # ============================================================================

    # ==================== KEY PERFORMANCE INDICATORS ====================
    st.markdown("## 📈 Key Performance Indicators (Available)")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Spend",
            value=f"${total_spend:,.2f}",
            help="Campaign Group Spend: The amount spent in total on all campaign groups"
        )

    with col2:
        st.metric(
            label="Total Impressions",
            value=f"{total_impressions:,.0f}",
            help="Impressions: The number of ad impressions served across all campaigns"
        )

    with col3:
        st.metric(
            label="CPM",
            value=f"${cpm:.2f}",
            help="Cost Per Mille (1,000 impressions): Calculated as (Total Spend / Impressions) × 1,000"
        )

    with col4:
        st.metric(
            label="Completed View Rate",
            value=f"{avg_cvr*100:.2f}%" if avg_cvr > 0 else "N/A",
            help="Campaign Group Completed View Rate: The rate of videos reaching completion (weighted average)"
        )

    # Secondary metrics
    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric(
            label="Total Completed Views",
            value=f"{int(total_completed_views):,}",
            help="Campaign Group Completed Views: The number of videos reaching completion"
        )

    with col6:
        st.metric(
            label="Users Reached",
            value=f"{int(total_users_reached):,}",
            help="Campaign Group Users Reached: The number of people who received ad impressions"
        )

    with col7:
        st.metric(
            label="Total Visits",
            value=f"{int(total_visits):,}",
            help="Campaign Group Visits: The number of verified visits to your site driven by MNTN campaigns"
        )

    # Add insights summary
    st.markdown("---")
    st.markdown("### 💡 Available Data Insights")

    col_insight1, col_insight2 = st.columns(2)

    with col_insight1:
        st.markdown("""
            **What You Can Analyze:**
            - **Campaign Efficiency**: Compare CPM across campaigns to identify cost-effective placements
            - **Engagement Quality**: Track completed view rates to measure creative engagement
            - **Audience Reach**: Monitor unique users reached and visit generation
            - **Spend Trends**: Identify spending patterns and budget pacing over time
            - **Video Performance**: Measure how well videos retain viewer attention through completion rates
        """)

    with col_insight2:
        st.markdown("""
            **Key Questions You Can Answer:**
            - Which campaigns have the best video completion rates?
            - What's the cost per completed view for each campaign?
            - How many verified site visits are campaigns driving?
            - Are certain campaigns more efficient at reaching users?
            - What are the daily spending and impression delivery trends?
        """)

    st.markdown("---")

    # ==================== PERFORMANCE TRENDS ====================
    st.markdown("## 📅 Performance Trends Over Time")

    # Aggregate by date
    daily_performance = df_filtered.groupby('date').agg({
        'campaigngroup_spend': 'sum',
        'impressions': 'sum',
        'campaigngroup_completedviews': 'sum',
        'campaigngroup_usersreached': 'sum'
    }).reset_index()

    daily_performance.columns = ['date', 'spend', 'impressions', 'completed_views', 'users_reached']

    col_trend1, col_trend2 = st.columns(2)

    with col_trend1:
        # Spend trend
        fig_spend = go.Figure()
        fig_spend.add_trace(go.Scatter(
            x=daily_performance['date'],
            y=daily_performance['spend'],
            name='Spend',
            line=dict(color='#1f77b4', width=3),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        fig_spend.update_layout(
            title='Daily Spend Trend',
            xaxis_title='Date',
            yaxis_title='Spend ($)',
            hovermode='x unified',
            template='plotly_white',
            height=350
        )
        st.plotly_chart(fig_spend, use_container_width=True)

    with col_trend2:
        # Impressions trend
        fig_imp = go.Figure()
        fig_imp.add_trace(go.Bar(
            x=daily_performance['date'],
            y=daily_performance['impressions'],
            name='Impressions',
            marker_color='#ff7f0e'
        ))
        fig_imp.update_layout(
            title='Daily Impressions',
            xaxis_title='Date',
            yaxis_title='Impressions',
            hovermode='x unified',
            template='plotly_white',
            height=350
        )
        st.plotly_chart(fig_imp, use_container_width=True)

    # Completed views and users reached
    col_trend3, col_trend4 = st.columns(2)

    with col_trend3:
        fig_views = go.Figure()
        fig_views.add_trace(go.Scatter(
            x=daily_performance['date'],
            y=daily_performance['completed_views'],
            name='Completed Views',
            line=dict(color='#2ca02c', width=3),
            fill='tozeroy',
            fillcolor='rgba(44, 160, 44, 0.2)'
        ))
        fig_views.update_layout(
            title='Daily Completed Views',
            xaxis_title='Date',
            yaxis_title='Completed Views',
            hovermode='x unified',
            template='plotly_white',
            height=350
        )
        st.plotly_chart(fig_views, use_container_width=True)

    with col_trend4:
        fig_users = go.Figure()
        fig_users.add_trace(go.Scatter(
            x=daily_performance['date'],
            y=daily_performance['users_reached'],
            name='Users Reached',
            line=dict(color='#9467bd', width=3),
            mode='lines+markers'
        ))
        fig_users.update_layout(
            title='Daily Users Reached',
            xaxis_title='Date',
            yaxis_title='Users Reached',
            hovermode='x unified',
            template='plotly_white',
            height=350
        )
        st.plotly_chart(fig_users, use_container_width=True)

    st.markdown("---")

    # ==================== CAMPAIGN PERFORMANCE ====================
    st.markdown("## 🎯 Campaign Performance Analysis")

    # Campaign-level aggregation
    campaign_perf = df_filtered[df_filtered['campaign'].notna()].groupby('campaign').agg({
        'campaigngroup_spend': 'sum',
        'impressions': 'sum',
        'campaigngroup_completedviews': 'sum',
        'campaigngroup_usersreached': 'sum',
        'campaigngroup_visits': 'sum'
    }).reset_index()

    campaign_perf.columns = ['campaign', 'spend', 'impressions', 'completed_views', 'users_reached', 'visits']

    campaign_perf['cpm'] = campaign_perf.apply(
        lambda x: (x['spend'] / x['impressions'] * 1000) if x['impressions'] > 0 else 0,
        axis=1
    )

    campaign_perf['completion_rate'] = campaign_perf.apply(
        lambda x: (x['completed_views'] / x['impressions'] * 100) if x['impressions'] > 0 else 0,
        axis=1
    )

    campaign_perf = campaign_perf.sort_values('spend', ascending=False)

    col_camp1, col_camp2 = st.columns(2)

    with col_camp1:
        # Top campaigns by spend
        fig_camp_spend = px.bar(
            campaign_perf.head(10),
            x='spend',
            y='campaign',
            orientation='h',
            title='Top 10 Campaigns by Spend',
            labels={'spend': 'Spend ($)', 'campaign': 'Campaign'},
            color='spend',
            color_continuous_scale='Blues'
        )
        fig_camp_spend.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'},
            template='plotly_white'
        )
        st.plotly_chart(fig_camp_spend, use_container_width=True)

    with col_camp2:
        # Campaign efficiency - best completion rates
        campaign_comp = campaign_perf[campaign_perf['completion_rate'] > 0].sort_values('completion_rate', ascending=False).head(10)
        fig_camp_comp = px.bar(
            campaign_comp,
            x='completion_rate',
            y='campaign',
            orientation='h',
            title='Top 10 Campaigns by Completion Rate',
            labels={'completion_rate': 'Completion Rate (%)', 'campaign': 'Campaign'},
            color='completion_rate',
            color_continuous_scale='Greens'
        )
        fig_camp_comp.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'},
            template='plotly_white'
        )
        st.plotly_chart(fig_camp_comp, use_container_width=True)

    # Campaign metrics table
    st.markdown("### 📊 Detailed Campaign Metrics")
    campaign_display = campaign_perf.copy()
    campaign_display['spend'] = campaign_display['spend'].apply(lambda x: f"${x:,.2f}")
    campaign_display['impressions'] = campaign_display['impressions'].apply(lambda x: f"{int(x):,}")
    campaign_display['completed_views'] = campaign_display['completed_views'].apply(lambda x: f"{int(x):,}")
    campaign_display['users_reached'] = campaign_display['users_reached'].apply(lambda x: f"{int(x):,}")
    campaign_display['visits'] = campaign_display['visits'].apply(lambda x: f"{int(x):,}")
    campaign_display['cpm'] = campaign_display['cpm'].apply(lambda x: f"${x:.2f}")
    campaign_display['completion_rate'] = campaign_display['completion_rate'].apply(lambda x: f"{x:.2f}%")

    campaign_display.columns = ['Campaign', 'Spend', 'Impressions', 'Completed Views', 'Users Reached', 'Visits', 'CPM', 'Completion Rate']
    st.dataframe(campaign_display, use_container_width=True, height=400)

    st.markdown("---")

    # ============================================================================
    # SECTION 2: UNAVAILABLE METRICS (DATA GAPS)
    # ============================================================================

    st.markdown("---")
    st.markdown("## ❌ Missing Data & Metrics")

    # Create tabs for different categories of missing data
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Conversion Metrics",
        "💰 Revenue Metrics",
        "🗺️ Geographic Data",
        "🎨 Creative Data"
    ])

    with tab1:
        st.markdown("""
            **Critical for measuring campaign effectiveness:**

            #### Advertiser-Level Metrics (All Missing)
            - **Conversions** (`advertiser_conversions`) - The number of conversions delivered by MNTN after a Verified Visit
            - **CPA** (`advertiser_cpa`) - The Cost per Verified Conversion
            - **Impression Conversion Rate** (`advertiser_impressionconversionrate`) - The percentage of impressions that resulted in a conversion
            - **Site Visitors** (`advertiser_sitevisitors`) - MNTN Driven Site Visitors
            - **Visits** (`advertiser_visits`) - The number of verified visits
            - **Conversion Assists** (`advertiser_conversionassists`) - The number of conversions that followed an assisted verified visit

            #### Campaign Group Conversions (Missing)
            - **Campaign Group Conversions** (`campaigngroup_conversions`) - The number of conversions delivered by MNTN after a Verified Visit (campaign level)
            - **User Conversion Rate** (`campaigngroup_userconversionrate`) - The number of users that converted
            - **Visit Conversion Rate** (`campaigngroup_visitconversionrate`) - The percentage of visits that resulted in a conversion

            #### Creative-Level Conversions (All Missing)
            - **Creative Conversions** (`creative_conversions`) - The number of conversions delivered by MNTN after a Verified Visit (creative level)
            - **Creative CPA** (`creative_cpa`) - The Cost per Verified Conversion (creative level)
            - **Creative Conversion Rates** - User and visit conversion rates at the creative level
        """)

        st.warning("⚠️ **Impact:** Without conversion data, you cannot calculate ROAS, CPA, or measure campaign ROI accurately.")

    with tab2:
        st.markdown("""

            #### Revenue Metrics
            - **Average Order Value** (`advertiser_averageordervalue`) - The average amount spent on each conversion delivered by MNTN
            - **Order Value** (`advertiser_ordervalue`, `campaigngroup_ordervalue`, `creative_ordervalue`) - The revenue delivered by MNTN
            - **ROAS** (`advertiser_roas`, `campaigngroup_roas`, `creative_roas`) - The Return on Ad Spend (Revenue / Spend)
            - **ROI** (`advertiser_roi`, `creative_roi`) - The Return on Investment

            #### Note on ROI Data
            - `campaigngroup_roi` exists in the data but all values are `-1` (invalid/placeholder)
            - This suggests ROI tracking may be configured but not calculating properly in MNTN
            - Requires proper conversion and revenue tracking to be enabled
        """)

        st.warning("⚠️ **Impact:** Cannot measure revenue generated, calculate true marketing ROI, or optimize for profitability.")

    with tab3:
        st.markdown("""

            #### DMA-Level Metrics (All Missing)
            - **DMA Names** (`dma_name`) - The name of the Designated Market Area (geographic region)
            - **DMA Conversions** (`dma_conversions`) - The number of conversions delivered by MNTN after a Verified Visit (by DMA)
            - **DMA Impressions** (`dma_impressions`) - The number of ad impressions served (by DMA)
            - **DMA Completed Views** (`dma_completedviews`) - The number of videos reaching completion (by DMA)
            - **DMA Completion Rate** (`dma_completedviewrate`) - The rate of videos reaching completion (by DMA)
            - **DMA Spend** (`dma_spend`) - The amount spent in total (by DMA)
            - **DMA Users Reached** (`dma_usersreached`) - The number of people who received ad impressions (by DMA)

            #### Geographic Analysis
            Current Status: **0 unique DMAs** (excluding 'unknown')

            DMA data enables geographic targeting optimization and regional performance analysis.
        """)

        st.warning("⚠️ **Impact:** Cannot analyze performance by geographic market, identify high-performing regions, or optimize regional spend allocation.")

    with tab4:
        st.markdown("""

            #### Creative Identification
            - **Creative Names** (`creative_name`) - The name of the creative ad asset
            - **Creative Size** (`creative_size`) - The size of the creative in pixels (e.g., 1920x1080)
            - Current Status: **0 unique creatives** in the dataset

            #### Creative Performance Metrics (All Missing)
            - **Creative Spend** (`creative_spend`) - The amount spent in total (by creative)
            - **Creative Impressions** (`creative_impressions`) - The number of ad impressions served (by creative)
            - **Creative Completed Views** (`creative_completedviews`) - The number of videos reaching completion (by creative)
            - **Creative Completion Rate** (`creative_completedviewrate`) - The rate of videos reaching completion (by creative)
            - **Creative Conversions** (`creative_conversions`) - The number of conversions delivered by MNTN after a Verified Visit (by creative)
            - **Creative CPA** (`creative_cpa`) - The Cost per Verified Conversion (by creative)
            - **Creative ROAS** (`creative_roas`) - The Verified Return on Ad Spend (by creative)
            - **Creative ROI** (`creative_roi`) - The Return on Investment (by creative)
            - **Creative Users Reached** (`creative_usersreached`) - The number of people who received ad impressions (by creative)
            - **Creative Visits** (`creative_visits`) - The number of verified visits (by creative)

            Creative-level data enables A/B testing, creative optimization, and identifying top-performing ad assets.
        """)

        st.warning("⚠️ **Impact:** Cannot A/B test creatives, compare creative performance, or identify which ad assets drive the best results.")

    # Summary recommendations
    st.markdown("---")
    st.markdown("## 📋 Data Collection Recommendations")

    col_rec1, col_rec2 = st.columns(2)

    with col_rec1:
        st.markdown("""
            ### 🔴 Critical Priorities
            1. **Enable Conversion Tracking**
               - Set up pixel tracking or API integration
               - Track conversions at advertiser, campaign, and creative levels

            2. **Connect Revenue Data**
               - Link sales/revenue data to campaigns
               - Enable ROAS and AOV calculations

            3. **Fix ROI Calculation**
               - Current ROI values are all `-1`
               - Check MNTN platform configuration
        """)

    with col_rec2:
        st.markdown("""
            ### 🟡 Important Enhancements
            4. **Add Geographic Tracking**
               - Enable DMA-level reporting in MNTN
               - Required for regional optimization

            5. **Enable Creative Reporting**
               - Add creative identifiers to data export
               - Track creative-level performance

            6. **Enhanced Visitor Tracking**
               - Site visitor and visit metrics
               - Conversion assist attribution
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
            <p><strong>Marketing Performance Dashboard</strong> | Data Source: MNTN Platform</p>
            <p>Last Updated: {}</p>
            <p style='font-size: 12px;'>📊 Available Metrics: 10 | ❌ Missing Metrics: 27 | 📈 Data Coverage: 27%</p>
        </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Error: mntn.csv file not found. Please ensure the file is in the same directory as this script.")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.write("Please check your data file format and try again.")
