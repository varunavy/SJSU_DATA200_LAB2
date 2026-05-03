# DATA 200 - Stock Analysis Lab 2

## Overview
This project is a Python-based stock tracking application developed for DATA 200 at San Jose State University. 

## Lab 2 Objectives
1. **Web scraping** Yahoo Finance historical stock data using **Selenium** and **BeautifulSoup**.
2. **CSV import** of Yahoo Finance historical data using Python’s **csv** library.

## How to Run
- **Console:** `python3 stock_console.py`
- **GUI:** `python3 stock_GUI.py`

## Requirements
`python3 -m pip install -U selenium beautifulsoup4 matplotlib pandas`

## Project Files
- `stock_class.py` - defines Stock and DailyData classes
- `utilities.py` - helper functions for sorting, clearing screen, and charting
- `stock_data.py` - database logic, web scraping, and CSV import
- `stock_console.py` - console interface
- `stock_GUI.py` - Tkinter GUI interface
- `stocks.py` - launcher file

## Features
- Add, update, delete, and list stocks
- Add daily stock data manually
- Show stock history and report
- Generate stock price charts
- Save data to SQLite database
- Load data from SQLite database
- Retrieve stock history from Yahoo Finance
- Import Yahoo Finance historical data from CSV

## Database
This project stores stock and daily history data in a local SQLite database file named `stocks.db`.

## Known Limitations
- Yahoo Finance scraping may break if the website structure changes
- Selenium/Chrome setup may be required depending on the system
- Date input must match the expected format
- Web retrieval is best for shorter date ranges