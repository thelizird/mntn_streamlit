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
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
    st.markdown("### CTV & Video Advertising Analytics")

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

    # DMA filter
    dmas = df_filtered['dma_name'].dropna().unique()
    dmas = [d for d in dmas if d != 'unknown']
    if len(dmas) > 0:
        selected_dmas = st.sidebar.multiselect(
            "Select Geographic Markets (DMA)",
            options=sorted(dmas),
            default=None
        )
        if selected_dmas:
            df_filtered = df_filtered[df_filtered['dma_name'].isin(selected_dmas)]

    # Calculate key metrics
    total_spend = df_filtered['spend'].sum()
    total_impressions = df_filtered['impressions'].sum()
    total_conversions = df_filtered['advertiser_conversions'].sum()

    # Calculate weighted averages for rates
    df_calc = df_filtered[df_filtered['spend'] > 0].copy()

    # ROAS calculation (weighted by spend)
    if total_spend > 0 and len(df_calc) > 0:
        roas_values = df_calc[df_calc['advertiser_roas'] >= 0]['advertiser_roas']
        roas_weights = df_calc[df_calc['advertiser_roas'] >= 0]['spend']
        if len(roas_values) > 0 and roas_weights.sum() > 0:
            avg_roas = np.average(roas_values, weights=roas_weights)
        else:
            avg_roas = 0
    else:
        avg_roas = 0

    # CPA calculation
    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0

    # CPM calculation
    cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0

    # Completed View Rate (weighted by impressions)
    if total_impressions > 0 and len(df_calc) > 0:
        cvr_values = df_calc[df_calc['advertiser_completedviewrate'] > 0]['advertiser_completedviewrate']
        cvr_weights = df_calc[df_calc['advertiser_completedviewrate'] > 0]['impressions']
        if len(cvr_values) > 0 and cvr_weights.sum() > 0:
            avg_cvr = np.average(cvr_values, weights=cvr_weights)
        else:
            avg_cvr = 0
    else:
        avg_cvr = 0

    # Conversion Rate
    conversion_rate = (total_conversions / total_impressions * 100) if total_impressions > 0 else 0

    # ==================== KEY PERFORMANCE INDICATORS ====================
    st.markdown("## 📈 Key Performance Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Spend",
            value=f"${total_spend:,.2f}",
            help="Total advertising spend across all campaigns"
        )

    with col2:
        st.metric(
            label="Total Impressions",
            value=f"{total_impressions:,.0f}",
            help="Total number of ad impressions served"
        )

    with col3:
        st.metric(
            label="Total Conversions",
            value=f"{int(total_conversions):,}",
            help="Total number of conversions generated"
        )

    with col4:
        st.metric(
            label="Average ROAS",
            value=f"{avg_roas:.2f}x" if avg_roas > 0 else "N/A",
            help="Return on Ad Spend - Revenue generated per dollar spent"
        )

    with col5:
        st.metric(
            label="Average CPA",
            value=f"${avg_cpa:.2f}" if avg_cpa > 0 else "N/A",
            help="Cost Per Acquisition - Average cost to acquire a customer"
        )

    # Secondary KPIs
    col6, col7, col8 = st.columns(3)

    with col6:
        st.metric(
            label="CPM",
            value=f"${cpm:.2f}",
            help="Cost Per Thousand Impressions"
        )

    with col7:
        st.metric(
            label="Completed View Rate",
            value=f"{avg_cvr*100:.2f}%" if avg_cvr > 0 else "N/A",
            help="Percentage of video ads viewed to completion"
        )

    with col8:
        st.metric(
            label="Conversion Rate",
            value=f"{conversion_rate:.3f}%",
            help="Percentage of impressions that resulted in conversions"
        )

    st.markdown("---")

    # ==================== PERFORMANCE TRENDS ====================
    st.markdown("## 📅 Performance Trends Over Time")

    # Aggregate by date
    daily_performance = df_filtered.groupby('date').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'advertiser_conversions': 'sum'
    }).reset_index()

    daily_performance['cpa'] = daily_performance.apply(
        lambda x: x['spend'] / x['advertiser_conversions'] if x['advertiser_conversions'] > 0 else 0,
        axis=1
    )

    col_trend1, col_trend2 = st.columns(2)

    with col_trend1:
        # Spend & Conversions trend
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
        # Conversions trend
        fig_conv = go.Figure()
        fig_conv.add_trace(go.Scatter(
            x=daily_performance['date'],
            y=daily_performance['advertiser_conversions'],
            name='Conversions',
            line=dict(color='#2ca02c', width=3),
            fill='tozeroy',
            fillcolor='rgba(44, 160, 44, 0.2)'
        ))
        fig_conv.update_layout(
            title='Daily Conversions Trend',
            xaxis_title='Date',
            yaxis_title='Conversions',
            hovermode='x unified',
            template='plotly_white',
            height=350
        )
        st.plotly_chart(fig_conv, use_container_width=True)

    # Impressions and CPA trend
    col_trend3, col_trend4 = st.columns(2)

    with col_trend3:
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

    with col_trend4:
        fig_cpa = go.Figure()
        daily_cpa = daily_performance[daily_performance['cpa'] > 0]
        fig_cpa.add_trace(go.Scatter(
            x=daily_cpa['date'],
            y=daily_cpa['cpa'],
            name='CPA',
            line=dict(color='#d62728', width=3),
            mode='lines+markers'
        ))
        fig_cpa.update_layout(
            title='Daily CPA Trend',
            xaxis_title='Date',
            yaxis_title='CPA ($)',
            hovermode='x unified',
            template='plotly_white',
            height=350
        )
        st.plotly_chart(fig_cpa, use_container_width=True)

    st.markdown("---")

    # ==================== CAMPAIGN PERFORMANCE ====================
    st.markdown("## 🎯 Campaign Performance Analysis")

    # Campaign-level aggregation
    campaign_perf = df_filtered[df_filtered['campaign'].notna()].groupby('campaign').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'advertiser_conversions': 'sum',
        'campaigngroup_completedviews': 'sum'
    }).reset_index()

    campaign_perf['cpa'] = campaign_perf.apply(
        lambda x: x['spend'] / x['advertiser_conversions'] if x['advertiser_conversions'] > 0 else 0,
        axis=1
    )

    campaign_perf['cpm'] = campaign_perf.apply(
        lambda x: (x['spend'] / x['impressions'] * 1000) if x['impressions'] > 0 else 0,
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
        # Campaign efficiency - CPA
        campaign_cpa = campaign_perf[campaign_perf['cpa'] > 0].sort_values('cpa').head(10)
        fig_camp_cpa = px.bar(
            campaign_cpa,
            x='cpa',
            y='campaign',
            orientation='h',
            title='Top 10 Most Efficient Campaigns (Lowest CPA)',
            labels={'cpa': 'CPA ($)', 'campaign': 'Campaign'},
            color='cpa',
            color_continuous_scale='Greens_r'
        )
        fig_camp_cpa.update_layout(
            height=500,
            showlegend=False,
            yaxis={'categoryorder': 'total descending'},
            template='plotly_white'
        )
        st.plotly_chart(fig_camp_cpa, use_container_width=True)

    # Campaign metrics table
    st.markdown("### 📊 Detailed Campaign Metrics")
    campaign_display = campaign_perf.copy()
    campaign_display['spend'] = campaign_display['spend'].apply(lambda x: f"${x:,.2f}")
    campaign_display['impressions'] = campaign_display['impressions'].apply(lambda x: f"{int(x):,}")
    campaign_display['advertiser_conversions'] = campaign_display['advertiser_conversions'].apply(lambda x: f"{int(x):,}")
    campaign_display['cpa'] = campaign_display['cpa'].apply(lambda x: f"${x:.2f}" if x > 0 else "N/A")
    campaign_display['cpm'] = campaign_display['cpm'].apply(lambda x: f"${x:.2f}")

    campaign_display.columns = ['Campaign', 'Spend', 'Impressions', 'Conversions', 'Completed Views', 'CPA', 'CPM']
    st.dataframe(campaign_display, use_container_width=True, height=400)

    st.markdown("---")

    # ==================== GEOGRAPHIC PERFORMANCE ====================
    st.markdown("## 🗺️ Geographic Performance (DMA Analysis)")

    dma_perf = df_filtered[
        (df_filtered['dma_name'].notna()) &
        (df_filtered['dma_name'] != 'unknown')
    ].groupby('dma_name').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'dma_conversions': 'sum'
    }).reset_index()

    dma_perf['cpa'] = dma_perf.apply(
        lambda x: x['spend'] / x['dma_conversions'] if x['dma_conversions'] > 0 else 0,
        axis=1
    )

    dma_perf['conversion_rate'] = dma_perf.apply(
        lambda x: (x['dma_conversions'] / x['impressions'] * 100) if x['impressions'] > 0 else 0,
        axis=1
    )

    dma_perf = dma_perf.sort_values('spend', ascending=False)

    if len(dma_perf) > 0:
        col_geo1, col_geo2 = st.columns(2)

        with col_geo1:
            # Geographic spend distribution
            fig_geo_spend = px.pie(
                dma_perf.head(8),
                values='spend',
                names='dma_name',
                title='Spend Distribution by Top Markets',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_geo_spend.update_traces(textposition='inside', textinfo='percent+label')
            fig_geo_spend.update_layout(height=450, template='plotly_white')
            st.plotly_chart(fig_geo_spend, use_container_width=True)

        with col_geo2:
            # Top markets by conversions
            dma_conv = dma_perf.sort_values('dma_conversions', ascending=False).head(10)
            fig_geo_conv = px.bar(
                dma_conv,
                x='dma_conversions',
                y='dma_name',
                orientation='h',
                title='Top 10 Markets by Conversions',
                labels={'dma_conversions': 'Conversions', 'dma_name': 'Market'},
                color='dma_conversions',
                color_continuous_scale='Viridis'
            )
            fig_geo_conv.update_layout(
                height=450,
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'},
                template='plotly_white'
            )
            st.plotly_chart(fig_geo_conv, use_container_width=True)

        # Geographic metrics table
        st.markdown("### 📊 Detailed Geographic Metrics")
        dma_display = dma_perf.copy()
        dma_display['spend'] = dma_display['spend'].apply(lambda x: f"${x:,.2f}")
        dma_display['impressions'] = dma_display['impressions'].apply(lambda x: f"{int(x):,}")
        dma_display['dma_conversions'] = dma_display['dma_conversions'].apply(lambda x: f"{int(x):,}")
        dma_display['cpa'] = dma_display['cpa'].apply(lambda x: f"${x:.2f}" if x > 0 else "N/A")
        dma_display['conversion_rate'] = dma_display['conversion_rate'].apply(lambda x: f"{x:.3f}%")

        dma_display.columns = ['Market (DMA)', 'Spend', 'Impressions', 'Conversions', 'CPA', 'Conversion Rate']
        st.dataframe(dma_display, use_container_width=True, height=350)
    else:
        st.info("No geographic data available for the selected filters.")

    st.markdown("---")

    # ==================== CREATIVE PERFORMANCE ====================
    st.markdown("## 🎨 Creative Performance")

    creative_perf = df_filtered[df_filtered['creative_name'].notna()].groupby('creative_name').agg({
        'spend': 'sum',
        'impressions': 'sum',
        'creative_conversions': 'sum',
        'creative_completedviews': 'sum'
    }).reset_index()

    creative_perf['ctr'] = creative_perf.apply(
        lambda x: (x['creative_completedviews'] / x['impressions'] * 100) if x['impressions'] > 0 else 0,
        axis=1
    )

    creative_perf['conversion_rate'] = creative_perf.apply(
        lambda x: (x['creative_conversions'] / x['impressions'] * 100) if x['impressions'] > 0 else 0,
        axis=1
    )

    creative_perf = creative_perf.sort_values('impressions', ascending=False)

    if len(creative_perf) > 0:
        col_cre1, col_cre2 = st.columns(2)

        with col_cre1:
            # Top creatives by impressions
            fig_cre_imp = px.bar(
                creative_perf.head(10),
                x='impressions',
                y='creative_name',
                orientation='h',
                title='Top 10 Creatives by Impressions',
                labels={'impressions': 'Impressions', 'creative_name': 'Creative'},
                color='impressions',
                color_continuous_scale='Purples'
            )
            fig_cre_imp.update_layout(
                height=450,
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'},
                template='plotly_white'
            )
            st.plotly_chart(fig_cre_imp, use_container_width=True)

        with col_cre2:
            # Top creatives by completion rate
            creative_ctr = creative_perf[creative_perf['ctr'] > 0].sort_values('ctr', ascending=False).head(10)
            fig_cre_ctr = px.bar(
                creative_ctr,
                x='ctr',
                y='creative_name',
                orientation='h',
                title='Top 10 Creatives by Completion Rate',
                labels={'ctr': 'Completion Rate (%)', 'creative_name': 'Creative'},
                color='ctr',
                color_continuous_scale='Oranges'
            )
            fig_cre_ctr.update_layout(
                height=450,
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'},
                template='plotly_white'
            )
            st.plotly_chart(fig_cre_ctr, use_container_width=True)
    else:
        st.info("No creative data available for the selected filters.")

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
            <p>Marketing Performance Dashboard | Data Source: MNTN Platform</p>
            <p>Last Updated: {}</p>
        </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Error: mntn.csv file not found. Please ensure the file is in the same directory as this script.")
except Exception as e:
    st.error(f"❌ An error occurred: {str(e)}")
    st.write("Please check your data file format and try again.")
