# CMPT353DataScience

This repository contains data science scripts developed for CMPT 353.  
The project involves cleaning, processing, and analyzing NHL statistics.  
To reproduce the workflow, run the provided Python scripts (`00` through `05`) **in order**.

## Requirements

- **Python**
- The following Python libraries:
  - `pandas`
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `seaborn`
  - 'requests'

## How To Run
Download the files and run the following in order using Python:
- 00-api_data.py (Extracts NHL API data from NHL.com)
- 01-extract_data.py (Extracts Data from moneypuck.com)
- 02-data_clean.py (Cleans the data and organizes it)
- 03-stat_analysis.py (produces .png of statistical results)
- 04-data_reshape.py (Reshapes the data for ML)
- 05-ML.py (Performs GradientBoosting and RandomForest)
## Expected Output
When running '05-ML.py' the output will generate:
- Depth of the Tree
- RandomForestClassifier Result
- GradientBoosting Result
## Extra
You can modify ML.py to also produce results for other seasons.
If any error occurs, please contact me at nwa47@sfu.ca
