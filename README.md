# Marketing Performance Dashboard

A professional, interactive marketing analytics dashboard built with Streamlit for analyzing MNTN CTV/video advertising campaign performance.

## Features

### 📈 Key Performance Indicators
- **Total Spend**: Aggregate advertising spend across all campaigns
- **Total Impressions**: Complete view of ad delivery
- **Total Conversions**: Customer acquisition metrics
- **Average ROAS**: Return on Ad Spend - measures revenue efficiency
- **Average CPA**: Cost Per Acquisition - customer acquisition cost
- **CPM**: Cost Per Thousand Impressions
- **Completed View Rate**: Video completion percentage
- **Conversion Rate**: Impression-to-conversion efficiency

### 📅 Performance Trends
- Daily spend tracking with visual trend lines
- Conversion trends over time
- Impression volume analysis
- CPA efficiency tracking by day

### 🎯 Campaign Performance Analysis
- Top 10 campaigns by spend
- Most efficient campaigns (lowest CPA)
- Detailed campaign metrics table with:
  - Spend, impressions, conversions
  - CPA and CPM calculations
  - Completed views tracking

### 🗺️ Geographic Performance (DMA Analysis)
- Spend distribution across top markets
- Top 10 markets by conversions
- Market-level efficiency metrics
- Conversion rates by geographic area

### 🎨 Creative Performance
- Top performing creatives by impressions
- Completion rate analysis
- Creative-level conversion tracking

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard:
```bash
streamlit run marketing_dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Interactive Filters

The dashboard includes sidebar filters for:
- **Date Range**: Analyze specific time periods
- **Campaign Selection**: Focus on specific campaigns
- **Geographic Markets (DMA)**: Filter by designated market areas

## Data Requirements

The dashboard expects a `mntn.csv` file in the same directory with the following key columns:
- date, spend, impressions
- advertiser_conversions, campaign, dma_name
- Various performance metrics (ROAS, CPA, completion rates, etc.)

## Metrics Explained

### ROAS (Return on Ad Spend)
Measures how much revenue is generated for every dollar spent on advertising. Higher is better.
- Formula: Revenue / Ad Spend
- Example: 3.5x ROAS = $3.50 revenue per $1.00 spent

### CPA (Cost Per Acquisition)
The average cost to acquire one customer or conversion. Lower is better.
- Formula: Total Spend / Total Conversions
- Example: $25 CPA = $25 spent per customer acquired

### CPM (Cost Per Mille)
The cost to reach 1,000 impressions. Industry benchmark for ad pricing.
- Formula: (Total Spend / Total Impressions) × 1,000

### Completed View Rate
Percentage of video ads viewed to completion. Indicates creative engagement.
- Formula: (Completed Views / Total Impressions) × 100

### Conversion Rate
Percentage of impressions that result in conversions. Measures campaign effectiveness.
- Formula: (Conversions / Impressions) × 100

## Professional Dashboard Design

The dashboard follows marketing analytics best practices:
1. **KPIs First**: Most important metrics prominently displayed at the top
2. **Trends Analysis**: Time-series visualizations for pattern identification
3. **Campaign Deep-Dive**: Detailed performance breakdowns by campaign
4. **Geographic Insights**: Market-level analysis for optimization opportunities
5. **Creative Performance**: Asset-level metrics for creative optimization

## Color Scheme

- Blue tones: Financial metrics (spend, budget)
- Green tones: Positive performance (conversions, efficiency)
- Orange/Red tones: Attention metrics (CPA, impressions)
- Purple tones: Creative and engagement metrics

## Tips for Use

1. **Compare Time Periods**: Use date filters to compare performance week-over-week or month-over-month
2. **Identify Top Performers**: Sort campaigns by ROAS to find winners worth scaling
3. **Optimize Underperformers**: Review high CPA campaigns for budget reallocation
4. **Geographic Expansion**: Identify high-converting markets for increased investment
5. **Creative Testing**: Compare completion rates to identify winning creative assets

---

**Built with:** Streamlit, Pandas, Plotly
**Data Source:** MNTN Platform
