import csv
import sqlite3
import time
from datetime import datetime

from utilities import clear_screen, sortDailyData
from stock_class import Stock, DailyData


DB_NAME = "stocks.db"


def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                                symbol TEXT NOT NULL PRIMARY KEY,
                                name TEXT,
                                shares REAL
                            );"""
        createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                    symbol TEXT NOT NULL,
                                    date TEXT NOT NULL,
                                    price REAL NOT NULL,
                                    volume REAL NOT NULL,
                                    PRIMARY KEY (symbol, date)
                            );"""
        cur.execute(createStockTableCmd)
        cur.execute(createDailyDataTableCmd)
        conn.commit()


def save_stock_data(stock_list):
    create_database()
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM dailyData;")
        cur.execute("DELETE FROM stocks;")

        insertStockCmd = """INSERT INTO stocks
                                (symbol, name, shares)
                                VALUES
                                (?, ?, ?);"""
        insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""

        for stock in stock_list:
            cur.execute(insertStockCmd, (stock.symbol, stock.name, stock.shares))
            for daily_data in stock.DataList:
                cur.execute(
                    insertDailyDataCmd,
                    (
                        stock.symbol,
                        daily_data.date.strftime("%m/%d/%y"),
                        daily_data.close,
                        daily_data.volume,
                    ),
                )
        conn.commit()


def load_stock_data(stock_list):
    create_database()
    stock_list.clear()
    with sqlite3.connect(DB_NAME) as conn:
        stockCur = conn.cursor()
        stockSelectCmd = """SELECT symbol, name, shares
                            FROM stocks
                            ORDER BY symbol;"""
        stockCur.execute(stockSelectCmd)
        stockRows = stockCur.fetchall()

        for row in stockRows:
            new_stock = Stock(row[0], row[1], row[2])
            dailyDataCur = conn.cursor()
            dailyDataCmd = """SELECT date, price, volume
                              FROM dailyData
                              WHERE symbol=?
                              ORDER BY date;"""
            dailyDataCur.execute(dailyDataCmd, (new_stock.symbol,))
            dailyDataRows = dailyDataCur.fetchall()
            for dailyRow in dailyDataRows:
                daily_data = DailyData(
                    datetime.strptime(dailyRow[0], "%m/%d/%y"),
                    float(dailyRow[1]),
                    float(dailyRow[2]),
                )
                new_stock.add_data(daily_data)
            stock_list.append(new_stock)
    sortDailyData(stock_list)


def retrieve_stock_web(dateStart, dateEnd, stock_list):
    from bs4 import BeautifulSoup
    from selenium import webdriver

    dateFrom = str(int(time.mktime(time.strptime(dateStart, "%m/%d/%y"))))
    dateTo = str(int(time.mktime(time.strptime(dateEnd, "%m/%d/%y"))))
    recordCount = 0

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option(
        "prefs",
        {'profile.managed_default_content_settings.javascript': 2},
    )

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(60)
    except Exception as exc:
        raise RuntimeWarning("Chrome Driver Not Found") from exc

    try:
        for stock in stock_list:
            stockSymbol = stock.symbol
            url = (
                "https://finance.yahoo.com/quote/"
                + stockSymbol
                + "/history?period1="
                + dateFrom
                + "&period2="
                + dateTo
                + "&interval=1d&filter=history&frequency=1d"
            )
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find('table', class_="W(100%) M(0)") or soup.find('table')
            if table is None:
                continue
            dataRows = table.find_all('tr')
            for row in dataRows:
                td = row.find_all('td')
                rowList = [cell.get_text(strip=True) for cell in td]
                if len(rowList) == 7:
                    try:
                        daily_data = DailyData(
                            datetime.strptime(rowList[0], "%b %d, %Y"),
                            float(rowList[5].replace(',', '')),
                            float(rowList[6].replace(',', '')),
                        )
                    except ValueError:
                        continue
                    stock.add_data(daily_data)
                    recordCount += 1
    finally:
        if driver is not None:
            driver.quit()

    sortDailyData(stock_list)
    return recordCount


def import_stock_web_csv(stock_list, symbol, filename):
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            with open(filename, newline='') as stockdata:
                datareader = csv.reader(stockdata, delimiter=',')
                next(datareader, None)
                for row in datareader:
                    if len(row) < 7:
                        continue
                    if row[4] in ["null", ""] or row[6] in ["null", ""]:
                        continue
                    daily_data = DailyData(
                        datetime.strptime(row[0], "%Y-%m-%d"),
                        float(row[4]),
                        float(row[6]),
                    )
                    stock.add_data(daily_data)
            sortDailyData(stock_list)
            return
    raise ValueError(f"Stock '{symbol}' was not found in the portfolio.")


def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")


if __name__ == "__main__":
    main()
