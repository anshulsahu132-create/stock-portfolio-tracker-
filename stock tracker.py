# =============           $             =======================
#               STOCK PORTFOLIO TRACKER
# =============           $            ========================
from colorama import Fore, Style, init
from tabulate import tabulate
from datetime import datetime
import matplotlib.pyplot as plt
import json
import csv
import os
init(autoreset=True)
#Stock Database
stock_prices = {

    "AAPL":180,
    "TSLA":250,
    "GOOGL":140,
    "MSFT":330,
    "AMZN":145,
    "NVDA":450,
    "META":310,
    "NFLX":420

}
#Save Stock Database
def save_stock_database():
    with open("stocks.json", "w") as file:
        json.dump(stock_prices, file, indent=4)

#Load Stock Database
def load_stock_database():
    global stock_prices
    if os.path.exists("stocks.json"):
        try:
            with open("stocks.json", "r") as file:
                stock_prices = json.load(file)
        except:
            pass 

portfolio = {}
os.makedirs("reports", exist_ok=True)
os.makedirs("charts", exist_ok=True)
def header():
    os.system("cls" if os.name=="nt" else "clear")
    print(Fore.CYAN + "="*70)
    print(Fore.YELLOW + Style.BRIGHT)
    print("              STOCK PORTFOLIO TRACKER")
    print(Fore.CYAN + "="*70)
    print(
        Fore.GREEN +
        datetime.now().strftime("%d-%m-%Y    %I:%M:%S %p")
    )
    print(Fore.CYAN + "="*70)

#Load Portfolio 
def load_portfolio():
    global portfolio
    if os.path.exists("portfolio.json"):
        try:
            with open("portfolio.json","r") as file:
                portfolio=json.load(file)
        except:
            portfolio={}
    else:
        portfolio={}

#Save Portfolio 
def save_portfolio():
    with open("portfolio.json","w") as file:
        json.dump(portfolio,file,indent=4)

#Show Stocks 
def show_stocks():
    table=[]
    for stock,price in stock_prices.items():
        table.append([stock,f"${price}"])
    print()
    print(
        tabulate(
            table,
            headers=["Stock","Current Price"],
            tablefmt="fancy_grid"
        )

    )

#Menu 
def menu():
    print(Fore.YELLOW)
    print("1. View Available Stocks")
    print("2. Add Stock")
    print("3. View Portfolio")
    print("4. Update Stock")
    print("5. Remove Stock")
    print("6. Search Stock")
    print("7. Portfolio Statistics")
    print("8. Export CSV")
    print("9. Export TXT")
    print("10. Generate Pie Chart")
    print("11. Generate Bar Chart")
    print("12. Exit")

# Add Stock 
def add_stock():
    header()
    show_stocks()
    stock = input("\nEnter Stock Symbol : ").upper().strip()
    if stock not in stock_prices:
     print(Fore.CYAN + "\nNew Company Detected!")

    while True:

        try:

            price = float(input("Enter Current Stock Price ($): "))

            if price <= 0:
                print(Fore.RED + "Price must be greater than 0.")
                continue

            stock_prices[stock] = price
            break

        except ValueError:

            print(Fore.RED + "Enter a valid price.")
    while True:
        try:
            quantity = int(input("Enter Quantity : "))
            if quantity <= 0:
                print(Fore.RED + "Quantity must be greater than 0.")
                continue
            break
        except ValueError:
            print(Fore.RED + "Enter numbers only.")
    portfolio[stock] = portfolio.get(stock, 0) + quantity
    save_portfolio()
    investment = quantity * stock_prices[stock]
    print(Fore.GREEN + "\nStock Added Successfully!")
    print(f"Stock : {stock}")
    print(f"Quantity : {quantity}")
    print(f"Investment : ${investment}")
    input("\nPress Enter...")

#View Portfolio 
def view_portfolio():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    table = []
    total = 0
    for stock, qty in portfolio.items():
        if stock not in stock_prices:
            continue
        price = stock_prices.get(stock, 0)
        investment = qty * price
        total += investment
        table.append([
            stock,
            qty,
            f"${price}",
            f"${investment}"
        ])
    if not table:
        print(Fore.RED + "\nNo Valid Stocks Found.")
        input("\nPress Enter...")
        return
    print()
    print(tabulate(
        table,
        headers=[
            "Stock",
            "Quantity",
            "Price",
            "Investment"
        ],
        tablefmt="fancy_grid"
    ))
    print(Fore.CYAN + "=" * 60)
    print(Fore.GREEN + Style.BRIGHT)
    print(f"Total Investment : ${total}")
    print(Fore.CYAN + "=" * 60)
    input("\nPress Enter...")

#Update Stock 
def update_stock():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    view_portfolio()
    stock = input("\nEnter Stock Symbol : ").upper().strip()
    if stock not in portfolio:
        print(Fore.RED + "\nStock Not Found.")
        input("\nPress Enter...")
        return
    while True:
        try:
            quantity = int(input("Enter New Quantity : "))
            if quantity <= 0:
                print("Quantity must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid Input.")
    portfolio[stock] = quantity
    save_portfolio()
    print(Fore.GREEN + "\nQuantity Updated Successfully.")
    input("\nPress Enter...")

    #Remove Stock
def remove_stock():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    print(Fore.YELLOW + "\nStocks in Portfolio:\n")
    for stock in portfolio:
        print(stock)
    stock = input("\nEnter Stock Symbol to Remove : ").upper().strip()
    if stock not in portfolio:
        print(Fore.RED + "\nStock Not Found.")
        input("\nPress Enter...")
        return
    del portfolio[stock]
    save_portfolio()
    print(Fore.GREEN + "\nStock Removed Successfully.")
    input("\nPress Enter...")

#Search Stock
def search_stock():
    header()
    stock = input("Enter Stock Symbol : ").upper().strip()
    if stock not in stock_prices:
        print(Fore.RED + "\nStock Not Available.")
        input("\nPress Enter...")
        return
    print(Fore.CYAN + "\nStock Details")
    print("-" * 35)
    print(f"Stock Name      : {stock}")
    print(f"Current Price   : ${stock_prices[stock]}")
    if stock in portfolio:
        qty = portfolio[stock]
        value = qty * stock_prices[stock]
        print(f"Owned Quantity  : {qty}")
        print(f"Investment      : ${value}")
    else:
        print("Owned Quantity  : 0")
        print("Investment      : $0")
    input("\nPress Enter...")

#Portfolio Statistics
def portfolio_statistics():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    total = 0
    highest_stock = ""
    highest_value = -1
    lowest_stock = ""
    lowest_value = float("inf")
    for stock, qty in portfolio.items():
        if stock not in stock_prices:
            continue
        value = qty * stock_prices[stock]
        total += value

        if value > highest_value:
            highest_value = value
            highest_stock = stock
        if value < lowest_value:
            lowest_value = value
            lowest_stock = stock
    print(Fore.GREEN + Style.BRIGHT)
    print(f"\nTotal Investment : ${total}")
    print(f"Number of Stocks : {len(portfolio)}")
    print(f"Highest Investment : {highest_stock} (${highest_value})")
    print(f"Lowest Investment  : {lowest_stock} (${lowest_value})")
    input("\nPress Enter...")

#Export CSV
def export_csv():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    filename = "reports/portfolio.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Stock",
            "Quantity",
            "Price",
            "Investment"
        ])
        total = 0
        for stock, qty in portfolio.items():
            if stock not in stock_prices:
                continue
            price = stock_prices[stock]
            investment = qty * price
            total += investment
            writer.writerow([
                stock,
                qty,
                price,
                investment
            ])
        writer.writerow([])
        writer.writerow(["Total", "", "", total])
    print(Fore.GREEN + "\nCSV Report Exported Successfully.")
    print("Location :", filename)
    input("\nPress Enter...")

    #Export TXT 
def export_txt():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    filename = "reports/portfolio.txt"
    total = 0
    with open(filename, "w") as file:
        file.write("="*60 + "\n")
        file.write("        STOCK PORTFOLIO REPORT\n")
        file.write("="*60 + "\n\n")
        file.write("Generated On : ")
        file.write(datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"))
        file.write("\n\n")
        for stock, qty in portfolio.items():
            if stock not in stock_prices:
                continue
            price = stock_prices[stock]
            investment = qty * price
            total += investment
            file.write(
                f"{stock:8} Qty:{qty:<5} Price:${price:<6} Investment:${investment}\n"
            )
        file.write("\n")
        file.write("="*60 + "\n")
        file.write(f"TOTAL INVESTMENT : ${total}")
    print(Fore.GREEN + "\nTXT Report Exported Successfully.")
    print("Saved At :", filename)
    input("\nPress Enter...")

#Pie Chart 
def generate_pie_chart():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    labels = []
    values = []
    for stock, qty in portfolio.items():
        if stock in stock_prices:
            labels.append(stock)
            values.append(qty * stock_prices[stock])
    if not values:
        print(Fore.RED + "\nNothing To Plot.")
        input("\nPress Enter...")
        return
    plt.figure(figsize=(7,7))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Portfolio Distribution")

    plt.savefig("charts/pie_chart.png")

    plt.show()

    print(Fore.GREEN + "\nPie Chart Saved Successfully.")

    input("\nPress Enter...")


# Bar Chart 
def generate_bar_chart():
    header()
    if not portfolio:
        print(Fore.RED + "\nPortfolio is Empty.")
        input("\nPress Enter...")
        return
    stocks = []
    values = []
    for stock, qty in portfolio.items():
        if stock in stock_prices:
            stocks.append(stock)
            values.append(qty * stock_prices[stock])
    if not values:
        print(Fore.RED + "\nNothing To Plot.")
        input("\nPress Enter...")
        return
    plt.figure(figsize=(8,5))
    plt.bar(stocks, values)
    plt.xlabel("Stock")
    plt.ylabel("Investment ($)")
    plt.title("Investment By Stock")
    plt.grid(axis="y")
    plt.savefig("charts/bar_chart.png")
    plt.show()
    print(Fore.GREEN + "\nBar Chart Saved Successfully.")
    input("\nPress Enter...")

#Main Program 
load_stock_database()
load_portfolio()

while True:

    header()

    menu()

    choice = input(Fore.YELLOW + "\nEnter Your Choice : ").strip()

    if choice == "1":

        header()
        show_stocks()
        input("\nPress Enter...")

    elif choice == "2":

        add_stock()

    elif choice == "3":

        view_portfolio()

    elif choice == "4":

        update_stock()

    elif choice == "5":

        remove_stock()

    elif choice == "6":

        search_stock()

    elif choice == "7":

        portfolio_statistics()

    elif choice == "8":

        export_csv()

    elif choice == "9":

        export_txt()

    elif choice == "10":

        generate_pie_chart()

    elif choice == "11":

        generate_bar_chart()

    elif choice == "12":

        save_portfolio()

        print(Fore.GREEN + "\nPortfolio Saved Successfully.")
        print(Fore.CYAN + "Thank You For Using Stock Portfolio Tracker ")

        break

    else:

        print(Fore.RED + "\nInvalid Choice!")

        input("\nPress Enter...")