# Email Data Scraper

## Overview
This Python script scrapes email interaction data from LeadConnector, retrieving details for opened and clicked emails within a specific date range.

## Features
- Fetch email data with contact information
- Support for different email statuses (opened, clicked)
- Export data to CSV files
- Handles pagination and large datasets

## Requirements
- Python 3.7+
- Libraries: 
  - pandas
  - requests
  - tqdm

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Replace `refresh_token` with a valid authentication token

```python
refresh_token = ""
```
## Usage
Modify the script's date range in `scrape_email_data()` function:

```python
json_data = get_email_page_data(
    status=status,
    start_date="2025-01-16",
    end_date="2025-01-23"
)
```

## Run
```commandline
python main.py
```

## Output
Creates two CSV files:
- `emails_opened.csv`
- `emails_clicked.csv`

## Notes
- Requires valid authentication token
- Uses LeadConnector's backend API
- Chunks large datasets for efficient processing