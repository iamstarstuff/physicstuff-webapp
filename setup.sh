#!/bin/bash

# Create the .streamlit directory if it doesn't exist
mkdir -p ~/.streamlit/

# Copy config
echo "\
[theme]\n\
primaryColor = \"#3a75c4\"\n\
backgroundColor = \"#0e1117\"\n\
secondaryBackgroundColor = \"#262730\"\n\
textColor = \"#fafafa\"\n\
font = \"sans serif\"\n\
\n\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
enableXsrfProtection = true\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
" > ~/.streamlit/config.toml
