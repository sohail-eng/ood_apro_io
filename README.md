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

create `token.txt` file and paste the content from the below info
2. Credentials
> Go to email page of the website
> right click and click on `inspect`
> click on `network`
> filter by `token` and click on the last api
> click on `Headers`
> Scroll down and copy `token-id`'s value
> paste into `token.txt` file.
> please witch the below video for better understand

[Click here to watch the demo](./get_token.webm)

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