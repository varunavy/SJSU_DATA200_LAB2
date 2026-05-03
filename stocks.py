import stock_console
import stock_GUI


def main():
    print("1 - Console Version")
    print("2 - GUI Version")
    choice = input("Select version to run: ").strip()
    if choice == "1":
        stock_console.main()
    else:
        stock_GUI.main()


if __name__ == "__main__":
    main()
