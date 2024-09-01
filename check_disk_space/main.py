import check_diskspace


def main():
    options = ["1. Check Diskspace"]

    for option in options:
        print(option)

    choice = int(input("Enter the number of the program you want to run: "))

    if choice == 1:
        tool = check_diskspace.CheckDiskspace()
        print(tool.get_name())
        tool.run()


if __name__ == '__main__':
    main()
