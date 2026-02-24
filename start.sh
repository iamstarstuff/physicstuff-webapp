#!/bin/bash

echo "🚀 Starting PhysicStuff Streamlit App..."
echo ""

# Activate codeastro conda environment
echo "🔧 Activating codeastro conda environment..."
conda activate codeastro

echo ""
echo "✅ Environment activated!"
echo "🌐 Starting Streamlit app..."
echo ""

# Run the app
streamlit run app.py
