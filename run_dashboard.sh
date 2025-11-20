#!/bin/bash

# Marketing Dashboard Launch Script for GitHub Codespaces
# This script ensures the dashboard runs properly in Codespaces

echo "🚀 Starting Marketing Performance Dashboard..."
echo ""

# Check if dependencies are installed
if ! python -c "import streamlit" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✅ Dependencies installed!"
    echo ""
fi

# Check if data file exists
if [ ! -f "mntn.csv" ]; then
    echo "⚠️  Warning: mntn.csv not found in current directory"
    echo "Please ensure your data file is present before accessing the dashboard"
    echo ""
fi

# Launch Streamlit with Codespaces-optimized settings
echo "🌐 Dashboard will be available at the forwarded port URL"
echo "📊 Look for the 'Ports' tab in VS Code to access the dashboard"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run marketing_dashboard.py \
    --server.address=0.0.0.0 \
    --server.port=8501 \
    --server.headless=true \
    --browser.serverAddress=0.0.0.0 \
    --browser.gatherUsageStats=false
