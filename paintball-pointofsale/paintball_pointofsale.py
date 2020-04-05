import tkinter.ttk as ttk
from openpyxl import load_workbook
from main_window import *


def main():
    try:
        load_workbook("GroupRecords.xlsx")
        MainWindow(True)
    except IOError:
        print("GroupRecords.xlsx was not found in this directory.\n")
        print("Module openpyxl is used in this project to create Excel workbooks with multiple sheets")
        print("Please be sure to use the included GroupRecords.xlsx file, or create a new xlsx file with the same name")
        print("The program will run, but checkouts will not be saved to excel")
        MainWindow(False)


if __name__ == '__main__':
    main()
