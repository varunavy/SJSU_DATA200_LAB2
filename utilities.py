import matplotlib.pyplot as plt
from os import system, name


def clear_screen():
    if name == "nt":
        _ = system('cls')
    else:
        _ = system('clear')


def sortStocks(stock_list):
    stock_list.sort(key=lambda stock: stock.symbol.upper())


def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda daily_data: daily_data.date)


def display_stock_chart(stock_list, symbol):
    selected_stock = None
    for stock in stock_list:
        if stock.symbol.upper() == symbol.upper():
            selected_stock = stock
            break

    if selected_stock is None:
        raise ValueError(f"Stock '{symbol}' was not found.")

    if len(selected_stock.DataList) == 0:
        raise ValueError(f"Stock '{symbol}' has no daily data to chart.")

    selected_stock.DataList.sort(key=lambda daily_data: daily_data.date)
    dates = [daily_data.date for daily_data in selected_stock.DataList]
    prices = [daily_data.close for daily_data in selected_stock.DataList]

    plt.figure()
    plt.plot(dates, prices, marker='o')
    plt.title(selected_stock.name.upper())
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
