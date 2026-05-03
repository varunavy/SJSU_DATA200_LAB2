from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog

import stock_data
from stock_class import Stock, DailyData
from utilities import display_stock_chart, sortStocks, sortDailyData


class StockApp:
    def __init__(self):
        self.stock_list = []
        if path.exists("stocks.db") is False:
            stock_data.create_database()

        self.root = Tk()
        self.root.title("Stock Manager")
        self.root.geometry("900x600")

        self.menubar = Menu(self.root)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Data from Database", command=self.load)
        self.filemenu.add_command(label="Save Data to Database", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.destroy)

        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV From Yahoo! Finance...", command=self.importCSV_web_data)

        self.chartmenu = Menu(self.menubar, tearoff=0)
        self.chartmenu.add_command(label="Display Selected Stock Chart", command=self.display_chart)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)
        self.root.config(menu=self.menubar)

        top_frame = Frame(self.root)
        top_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        left_frame = Frame(top_frame)
        left_frame.pack(side=LEFT, fill=Y, padx=(0, 10))

        right_frame = Frame(top_frame)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True)

        self.headingLabel = Label(right_frame, text="Select a stock", font=("Arial", 16, "bold"))
        self.headingLabel.pack(anchor="w", pady=(0, 10))

        Label(left_frame, text="Tracked Stocks").pack(anchor="w")
        self.stockList = Listbox(left_frame, exportselection=False, width=20, height=20)
        self.stockList.pack(fill=Y, expand=False)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=BOTH, expand=True)

        self.mainTab = Frame(self.notebook)
        self.historyTab = Frame(self.notebook)
        self.reportTab = Frame(self.notebook)
        self.notebook.add(self.mainTab, text="Main")
        self.notebook.add(self.historyTab, text="History")
        self.notebook.add(self.reportTab, text="Report")

        add_frame = LabelFrame(self.mainTab, text="Add Stock")
        add_frame.pack(fill=X, padx=10, pady=10)
        Label(add_frame, text="Symbol").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        Label(add_frame, text="Name").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        Label(add_frame, text="Shares").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.addSymbolEntry = Entry(add_frame)
        self.addNameEntry = Entry(add_frame)
        self.addSharesEntry = Entry(add_frame)
        self.addSymbolEntry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.addNameEntry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.addSharesEntry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        Button(add_frame, text="Add Stock", command=self.add_stock).grid(row=3, column=0, columnspan=2, pady=5)
        add_frame.grid_columnconfigure(1, weight=1)

        update_frame = LabelFrame(self.mainTab, text="Update Shares")
        update_frame.pack(fill=X, padx=10, pady=10)
        Label(update_frame, text="Share Amount").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.updateSharesEntry = Entry(update_frame)
        self.updateSharesEntry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        Button(update_frame, text="Buy", command=self.buy_shares).grid(row=1, column=0, padx=5, pady=5)
        Button(update_frame, text="Sell", command=self.sell_shares).grid(row=1, column=1, padx=5, pady=5)
        Button(update_frame, text="Delete Selected Stock", command=self.delete_stock).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        update_frame.grid_columnconfigure(1, weight=1)

        manual_frame = LabelFrame(self.mainTab, text="Add Daily Data")
        manual_frame.pack(fill=X, padx=10, pady=10)
        Label(manual_frame, text="Date (m/d/yy)").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        Label(manual_frame, text="Price").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        Label(manual_frame, text="Volume").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.dateEntry = Entry(manual_frame)
        self.priceEntry = Entry(manual_frame)
        self.volumeEntry = Entry(manual_frame)
        self.dateEntry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.priceEntry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.volumeEntry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        Button(manual_frame, text="Add Daily Data", command=self.add_daily_data).grid(row=3, column=0, columnspan=2, pady=5)
        manual_frame.grid_columnconfigure(1, weight=1)

        self.dailyDataList = Text(self.historyTab, wrap=NONE)
        self.dailyDataList.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.stockReport = Text(self.reportTab, wrap=WORD)
        self.stockReport.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.root.mainloop()

    def get_selected_stock(self):
        selection = self.stockList.curselection()
        if not selection:
            return None
        symbol = self.stockList.get(selection[0])
        for stock in self.stock_list:
            if stock.symbol == symbol:
                return stock
        return None

    def refresh_stock_list(self, select_symbol=None):
        self.stockList.delete(0, END)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)
        if self.stock_list:
            index_to_select = 0
            if select_symbol is not None:
                for index, stock in enumerate(self.stock_list):
                    if stock.symbol == select_symbol:
                        index_to_select = index
                        break
            self.stockList.selection_clear(0, END)
            self.stockList.selection_set(index_to_select)
            self.stockList.activate(index_to_select)
            self.display_stock_data()
        else:
            self.headingLabel['text'] = "Select a stock"
            self.dailyDataList.delete("1.0", END)
            self.stockReport.delete("1.0", END)

    def build_report_text(self, stock):
        lines = [f"Report for: {stock.symbol} {stock.name}", f"Shares: {stock.shares}"]
        if len(stock.DataList) == 0:
            lines.append("*** No daily history.")
            return "\n".join(lines)

        sortDailyData(self.stock_list)
        first_day = stock.DataList[0]
        last_day = stock.DataList[-1]
        lines.append(f"History Records: {len(stock.DataList)}")
        lines.append(f"Starting Close ({first_day.date.strftime('%m/%d/%y')}): ${first_day.close:,.2f}")
        lines.append(f"Latest Close   ({last_day.date.strftime('%m/%d/%y')}): ${last_day.close:,.2f}")
        lines.append(f"Position Value: ${stock.shares * last_day.close:,.2f}")
        lines.append(f"Price Change:   ${last_day.close - first_day.close:,.2f}")
        lines.append(f"Total Change:   ${(last_day.close - first_day.close) * stock.shares:,.2f}")
        return "\n".join(lines)

    def load(self):
        stock_data.load_stock_data(self.stock_list)
        self.refresh_stock_list()
        messagebox.showinfo("Load Data", "Data Loaded")

    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    def update_data(self, evt=None):
        self.display_stock_data()

    def display_stock_data(self):
        stock = self.get_selected_stock()
        if stock is None:
            return

        sortDailyData(self.stock_list)
        self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        self.dailyDataList.delete("1.0", END)
        self.stockReport.delete("1.0", END)
        self.dailyDataList.insert(END, "- Date -   - Price -   - Volume -\n")
        self.dailyDataList.insert(END, "=================================\n")
        for daily_data in stock.DataList:
            row = (
                daily_data.date.strftime("%m/%d/%y")
                + "   "
                + '${:0,.2f}'.format(daily_data.close)
                + "   "
                + str(daily_data.volume)
                + "\n"
            )
            self.dailyDataList.insert(END, row)

        self.stockReport.insert(END, self.build_report_text(stock))

    def add_stock(self):
        symbol = self.addSymbolEntry.get().strip().upper()
        name = self.addNameEntry.get().strip()
        shares_text = self.addSharesEntry.get().strip()

        if symbol == "" or name == "" or shares_text == "":
            messagebox.showerror("Add Stock", "All fields are required.")
            return
        if any(stock.symbol == symbol for stock in self.stock_list):
            messagebox.showerror("Add Stock", "That ticker is already being tracked.")
            return
        try:
            shares = float(shares_text)
            if shares < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Add Stock", "Shares must be a non-negative number.")
            return

        new_stock = Stock(symbol, name, shares)
        self.stock_list.append(new_stock)
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)
        self.refresh_stock_list(select_symbol=symbol)

    def buy_shares(self):
        stock = self.get_selected_stock()
        if stock is None:
            messagebox.showerror("Buy Shares", "Please select a stock first.")
            return
        try:
            shares = float(self.updateSharesEntry.get())
            if shares <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Buy Shares", "Enter a positive number of shares.")
            return
        stock.buy(shares)
        self.updateSharesEntry.delete(0, END)
        self.display_stock_data()
        messagebox.showinfo("Buy Shares", "Shares Purchased")

    def sell_shares(self):
        stock = self.get_selected_stock()
        if stock is None:
            messagebox.showerror("Sell Shares", "Please select a stock first.")
            return
        try:
            shares = float(self.updateSharesEntry.get())
            if shares <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Sell Shares", "Enter a positive number of shares.")
            return
        if shares > stock.shares:
            messagebox.showerror("Sell Shares", "Cannot sell more shares than you own.")
            return
        stock.sell(shares)
        self.updateSharesEntry.delete(0, END)
        self.display_stock_data()
        messagebox.showinfo("Sell Shares", "Shares Sold")

    def delete_stock(self):
        stock = self.get_selected_stock()
        if stock is None:
            messagebox.showerror("Delete Stock", "Please select a stock first.")
            return
        self.stock_list.remove(stock)
        self.refresh_stock_list()
        messagebox.showinfo("Delete Stock", "Stock Deleted")

    def add_daily_data(self):
        stock = self.get_selected_stock()
        if stock is None:
            messagebox.showerror("Add Daily Data", "Please select a stock first.")
            return
        try:
            daily_data = DailyData(
                datetime.strptime(self.dateEntry.get().strip(), "%m/%d/%y"),
                float(self.priceEntry.get().strip()),
                float(self.volumeEntry.get().strip()),
            )
        except ValueError:
            messagebox.showerror("Add Daily Data", "Use date m/d/yy and numeric price/volume.")
            return
        stock.add_data(daily_data)
        sortDailyData(self.stock_list)
        self.dateEntry.delete(0, END)
        self.priceEntry.delete(0, END)
        self.volumeEntry.delete(0, END)
        self.display_stock_data()
        messagebox.showinfo("Add Daily Data", "Daily data added")

    def scrape_web_data(self):
        if not self.stock_list:
            messagebox.showerror("Cannot Get Data from Web", "Add or load at least one stock first.")
            return
        dateFrom = simpledialog.askstring("Starting Date", "Enter Starting Date (m/d/yy)")
        if dateFrom is None:
            return
        dateTo = simpledialog.askstring("Ending Date", "Enter Ending Date (m/d/yy)")
        if dateTo is None:
            return
        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
        except Exception:
            messagebox.showerror("Cannot Get Data from Web", "Check Chrome / ChromeDriver / Selenium setup and date format.")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web", "Data Retrieved")

    def importCSV_web_data(self):
        stock = self.get_selected_stock()
        if stock is None:
            messagebox.showerror("Import CSV", "Please select a stock first.")
            return
        filename = filedialog.askopenfilename(
            title="Select " + stock.symbol + " File to Import",
            filetypes=[('Yahoo Finance! CSV', '*.csv')],
        )
        if filename != "":
            try:
                stock_data.import_stock_web_csv(self.stock_list, stock.symbol, filename)
            except Exception as exc:
                messagebox.showerror("Import CSV", str(exc))
                return
            self.display_stock_data()
            messagebox.showinfo("Import Complete", stock.symbol + " Import Complete")

    def display_chart(self):
        stock = self.get_selected_stock()
        if stock is None:
            messagebox.showerror("Display Chart", "Please select a stock first.")
            return
        try:
            display_stock_chart(self.stock_list, stock.symbol)
        except Exception as exc:
            messagebox.showerror("Display Chart", str(exc))


def main():
    StockApp()


if __name__ == "__main__":
    main()
