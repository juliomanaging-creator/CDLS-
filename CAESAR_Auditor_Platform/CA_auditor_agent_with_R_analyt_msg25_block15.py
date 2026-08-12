# Ubuntu 24.04 LTS
sudo apt update
sudo apt install -y r-base r-base-dev

# Install R packages (one command)
sudo R -e "install.packages(c('tidyverse', 'forecast', 'prophet', 
    'ggplot2', 'anomalize', 'caret', 'DBI', 'RPostgres'), 
    repos='https://cloud.r-project.org')"

# Install Python-R bridge
pip3 install rpy2 --break-system-packages

# Test integration
python3 -c "from integration.python_r_bridge import RAnalytics; r = RAnalytics()"
# Should print: ✓ R environment initialized