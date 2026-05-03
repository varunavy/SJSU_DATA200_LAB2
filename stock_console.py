from datetime import datetime
from os import path

import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortDailyData, sortStocks


def get_stock_by_symbol(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            return stock
    return None


def print_stock_symbols(stock_list):
    print("Stock List: [", end="")
    for index, stock in enumerate(stock_list):
        end_char = "" if index == len(stock_list) - 1 else " "
        print(stock.symbol, end=end_char)
    print("]")


def pause(message="Press Enter to Continue"):
    input(message)


# Main Menu

def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "3", "4", "5", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")


# Manage Stocks

def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")


# Add new stock to track

def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Add Stock ---")
        symbol = input("Enter Ticker Symbol: ").strip().upper()
        name = input("Enter Company Name: ").strip()
        shares_text = input("Enter Number of Shares: ").strip()

        if symbol == "" or name == "" or shares_text == "":
            print("*** All fields are required. ***")
            pause()
            continue

        if get_stock_by_symbol(stock_list, symbol) is not None:
            print("*** That ticker is already being tracked. ***")
            pause()
            continue

        try:
            shares = float(shares_text)
            if shares < 0:
                raise ValueError
        except ValueError:
            print("*** Shares must be a non-negative number. ***")
            pause()
            continue

        stock_list.append(Stock(symbol, name, shares))
        sortStocks(stock_list)
        option = input("Stock Added - Enter to Add Another Stock or 0 to Stop: ")


# Buy or Sell Shares Menu

def update_shares(stock_list):
    if len(stock_list) == 0:
        clear_screen()
        print("*** No stocks available. Add a stock first. ***")
        pause()
        return

    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)


# Buy Stocks (add to shares)

def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print_stock_symbols(stock_list)
    symbol = input("Which stock do you want to buy?: ").strip().upper()
    stock = get_stock_by_symbol(stock_list, symbol)
    if stock is None:
        print("*** Stock symbol not found. ***")
        pause()
        return

    shares_text = input("How many shares do you want to buy?: ").strip()
    try:
        shares = float(shares_text)
        if shares <= 0:
            raise ValueError
    except ValueError:
        print("*** Shares must be a positive number. ***")
        pause()
        return

    stock.buy(shares)
    print("Shares Purchased")
    pause()


# Sell Stocks (subtract from shares)

def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print_stock_symbols(stock_list)
    symbol = input("Which stock do you want to sell?: ").strip().upper()
    stock = get_stock_by_symbol(stock_list, symbol)
    if stock is None:
        print("*** Stock symbol not found. ***")
        pause()
        return

    shares_text = input("How many shares do you want to sell?: ").strip()
    try:
        shares = float(shares_text)
        if shares <= 0:
            raise ValueError
    except ValueError:
        print("*** Shares must be a positive number. ***")
        pause()
        return

    if shares > stock.shares:
        print("*** Cannot sell more shares than you own. ***")
        pause()
        return

    stock.sell(shares)
    print("Shares Sold")
    pause()


# Remove stock and all daily data

def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    if len(stock_list) == 0:
        print("*** No stocks available to delete. ***")
        pause()
        return

    print_stock_symbols(stock_list)
    symbol = input("Which stock do you want to delete?: ").strip().upper()
    stock = get_stock_by_symbol(stock_list, symbol)
    if stock is None:
        print("*** Stock symbol not found. ***")
        pause()
        return

    stock_list.remove(stock)
    print("Stock Deleted")
    pause()


# List stocks being tracked

def list_stocks(stock_list):
    clear_screen()
    print("Stock List ---")
    if len(stock_list) == 0:
        print("*** No stocks currently tracked. ***")
        pause()
        return

    sortStocks(stock_list)
    print(f"{'SYMBOL':<10}{'NAME':<25}{'SHARES':>10}")
    print("=" * 45)
    for stock in stock_list:
        print(f"{stock.symbol:<10}{stock.name:<25}{stock.shares:>10.1f}")
    print()
    pause("Press Enter to Continue ***")


# Add Daily Stock Data

def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    if len(stock_list) == 0:
        print("*** No stocks available. Add a stock first. ***")
        pause()
        return

    print_stock_symbols(stock_list)
    symbol = input("Which stock do you want to use?: ").strip().upper()
    stock = get_stock_by_symbol(stock_list, symbol)
    if stock is None:
        print("*** Stock symbol not found. ***")
        pause()
        return

    print(f"Ready to add data for: {stock.symbol}")
    print("Enter Data Separated by Commas - Do Not use Spaces")
    print("Enter a Blank Line to Quit")
    print("Enter Date,Price,Volume")
    print("Example: 8/28/20,47.85,10550")

    while True:
        row = input("Enter Date,Price,Volume: ").strip()
        if row == "":
            break
        try:
            date_text, price_text, volume_text = row.split(",")
            daily_data = DailyData(
                datetime.strptime(date_text, "%m/%d/%y"),
                float(price_text),
                float(volume_text),
            )
            stock.add_data(daily_data)
            sortDailyData(stock_list)
            print("Daily data added.")
        except ValueError:
            print("*** Invalid format. Use m/d/yy,price,volume ***")
    pause()


# Display Report for All Stocks

def display_report(stock_data_list):
    clear_screen()
    print("Stock Report ---")
    if len(stock_data_list) == 0:
        print("*** No stocks currently tracked. ***")
        pause()
        return

    sortStocks(stock_data_list)
    sortDailyData(stock_data_list)
    for stock in stock_data_list:
        print(f"Report for: {stock.symbol} {stock.name}")
        print(f"Shares: {stock.shares}")
        if len(stock.DataList) == 0:
            print("*** No daily history.")
        else:
            first_day = stock.DataList[0]
            last_day = stock.DataList[-1]
            print(f"History Records: {len(stock.DataList)}")
            print(f"Starting Close ({first_day.date.strftime('%m/%d/%y')}): ${first_day.close:,.2f}")
            print(f"Latest Close   ({last_day.date.strftime('%m/%d/%y')}): ${last_day.close:,.2f}")
            print(f"Position Value: ${stock.shares * last_day.close:,.2f}")
            print(f"Price Change:   ${last_day.close - first_day.close:,.2f}")
            print(f"Total Change:   ${(last_day.close - first_day.close) * stock.shares:,.2f}")
            print("- Date -   - Price -   - Volume -")
            print("=================================")
            for daily_data in stock.DataList:
                print(
                    f"{daily_data.date.strftime('%m/%d/%y')}   "
                    f"${daily_data.close:,.2f}   {daily_data.volume}"
                )
        print()
    print("--- Report Complete ---")
    pause()


# Display Chart

def display_chart(stock_list):
    clear_screen()
    if len(stock_list) == 0:
        print("*** No stocks available to chart. ***")
        pause()
        return

    print_stock_symbols(stock_list)
    symbol = input("Which stock do you want to use?: ").strip().upper()
    try:
        display_stock_chart(stock_list, symbol)
    except Exception as exc:
        print(f"*** {exc} ***")
        pause()


# Manage Data Menu

def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")

        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("--- Data Saved to Database ---")
            pause()
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("--- Data Loaded from Database ---")
            pause()
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)


# Get stock price and volume history from Yahoo! Finance using Web Scraping

def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    if len(stock_list) == 0:
        print("*** No stocks available. Add or load stocks first. ***")
        pause()
        return

    print("This will retrieve data from all stocks in your stock list.")
    dateFrom = input("Enter starting date: (MM/DD/YY): ").strip()
    dateTo = input("Enter ending date: (MM/DD/YY): ").strip()
    try:
        records = stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
        print(f"Records Retrieved: {records}")
    except Exception as exc:
        print(f"*** Unable to retrieve data from web: {exc} ***")
    pause()


# Import stock price and volume history from Yahoo! Finance using CSV Import

def import_csv(stock_list):
    clear_screen()
    print("Import CSV Data ---")
    if len(stock_list) == 0:
        print("*** No stocks available. Add or load stocks first. ***")
        pause()
        return

    print_stock_symbols(stock_list)
    symbol = input("Enter stock symbol to import for: ").strip().upper()
    filename = input("Enter full CSV file path: ").strip()
    if filename == "":
        print("*** File path cannot be blank. ***")
        pause()
        return

    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print("CSV Import Complete")
    except FileNotFoundError:
        print("*** CSV file not found. ***")
    except Exception as exc:
        print(f"*** Unable to import CSV: {exc} ***")
    pause()


# Begin program

def main():
    if path.exists("stocks.db") is False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)


# Program Starts Here
if __name__ == "__main__":
    main()
