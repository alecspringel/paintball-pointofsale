import datetime
from openpyxl import load_workbook
from group import Group, Player, Transaction

def checkout(group, save):
    square = 0
    paypal = 0
    cash = 0

    for transaction in group.get_transactions():
        if transaction.type == "CASH":
            cash += transaction.get_amount()
        elif transaction.type == "SQUARE":
            square += transaction.get_amount()
        else:
            paypal += transaction.get_amount()

    total_spent = paypal + square + cash + group.get_deposit()

    if not save:
        return total_spent

    wb = load_workbook("GroupRecords.xlsx")

    # FIND EMPTY ROW IN SHEETS
    group_row = empty_row(wb, 'Groups')
    player_row = empty_row(wb, 'Players')
    # PUT DATA IN ROW
    wb['Groups']['A' + str(group_row)] = datetime.datetime.now()  # date/time
    wb['Groups']['B' + str(group_row)] = group.get_name()  # group name
    wb['Groups']['C' + str(group_row)] = group.number_of_players()  # number players
    wb['Groups']['E' + str(group_row)] = group.get_deposit()  # Deposit
    wb['Groups']['F' + str(group_row)] = cash  # transactions
    wb['Groups']['G' + str(group_row)] = square  # transactions
    wb['Groups']['H' + str(group_row)] = paypal  # transactions
    wb['Groups']['D' + str(group_row)] = sum(group.paint_bags)  # paint
    wb['Groups']['I' + str(group_row)] = total_spent  # transactions
    wb['Groups']['J' + str(group_row)] = group.get_type()  # Speedball, Recball, or Rental

    for player in group.get_players():
        wb['Players']['A' + str(player_row)] = datetime.datetime.now()
        wb['Players']['B' + str(player_row)] = group.get_name()
        wb['Players']['C' + str(player_row)] = player.get_name()
        player_row += 1
    wb.save("GroupRecords.xlsx")

    return total_spent

def empty_row(wb, sheet):
    """Finds first empty row in excel sheet"""
    row = 1
    cell = 'A' + str(row)
    while wb[sheet][cell].value != None:
        row += 1
        cell = 'A' + str(row)
    return row
