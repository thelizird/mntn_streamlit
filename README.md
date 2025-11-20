# Marketing Performance Dashboard

A professional, interactive marketing analytics dashboard built with Streamlit for analyzing MNTN CTV/video advertising campaign performance.

## 🚀 Quick Start - GitHub Codespaces

This dashboard is **optimized for GitHub Codespaces** and will work out of the box!

### Running in Codespaces (Recommended)

1. Open this repository in GitHub Codespaces
2. Wait for the automatic dependency installation (handled by devcontainer)
3. Run the dashboard using the launch script:
   ```bash
   ./run_dashboard.sh
   ```
   OR manually:
   ```bash
   streamlit run marketing_dashboard.py
   ```
4. When Streamlit starts, VS Code will show a notification about port 8501
5. Click **"Open in Browser"** or go to the **Ports** tab and click the globe icon next to port 8501
6. Your dashboard will open in a new browser tab!

### Codespaces Optimizations Included

- ✅ **Auto-configuration**: `.devcontainer/devcontainer.json` sets up the environment automatically
- ✅ **Port forwarding**: Port 8501 is automatically forwarded and labeled
- ✅ **Dependencies**: All packages are installed on container creation
- ✅ **Streamlit config**: `.streamlit/config.toml` optimized for cloud environments
- ✅ **Launch script**: `run_dashboard.sh` for easy one-command startup

### Running Locally

If you prefer to run locally instead of Codespaces:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run marketing_dashboard.py`
4. Open browser to `http://localhost:8501`

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

## 📁 Repository Structure

```
mntn_streamlit/
├── marketing_dashboard.py    # Main dashboard application
├── mntn.csv                   # Your marketing data (required)
├── requirements.txt           # Python dependencies
├── run_dashboard.sh          # Launch script for Codespaces
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── .devcontainer/
│   └── devcontainer.json     # Codespaces container setup
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

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

## Troubleshooting

### Dashboard Not Loading in Codespaces?
1. Check the **Ports** tab in VS Code (bottom panel)
2. Ensure port 8501 is listed and has visibility set to "Public"
3. Click the globe icon to open in browser
4. If issues persist, try: `Ctrl+C` to stop, then run `./run_dashboard.sh` again

### "File not found" Error?
Make sure `mntn.csv` is in the same directory as `marketing_dashboard.py`

### Dependencies Not Installing?
Codespaces should auto-install on startup. If not, manually run:
```bash
pip install -r requirements.txt
```

## Performance Notes

- **Data Caching**: The dashboard uses `@st.cache_data` for optimal performance
- **Large Files**: For files >100MB, consider filtering data before upload
- **Refresh Rate**: Disabled `runOnSave` in Codespaces to prevent unnecessary reloads

---

**Built with:** Streamlit, Pandas, Plotly
**Data Source:** MNTN Platform
**Optimized for:** GitHub Codespaces ☁️
