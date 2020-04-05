import tkinter as tk
from group import Group, Player, Transaction


class GroupDetailWindow:
    """The group detail window is responsible for displaying the list of player names within a group, transaction
    amounts, quantity of bags/cases of paint that have been purchased, and allows for the addition of new players and
    transactions

    The parent window is recorded in order to refresh/update the UI with new information that gets recorded by the user
    in this window.
    """

    def __init__(self, parent, group):
        self.parent_window = parent
        self.group = group
        self.window = tk.Tk()
        self.create_group_detail_window()

    def refresh(self):
        """Clears all tk window objects from view and calls create_group_detail_window() to reload new data into the
        window.
        """
        # Refreshes main window
        _list = self.window.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        widget_list = _list
        for item in widget_list:
            item.grid_forget()
        self.create_group_detail_window()

    def create_group_detail_window(self):
        """Helper function for building out the detail window."""
        self.load_static_UI()
        self.load_paint()
        self.load_players()
        self.load_transactions()

    def load_paint(self):
        """Loads the paint data and necessary labels to the tk window."""
        bags, cases = self.group.total_bags_and_cases()
        tk.Label(self.window, fg="blue", text="{0:1} CASES".format(cases), font='Helvetica 14 bold').grid(row=0,
                                                                                                          column=12)
        tk.Label(self.window, fg="blue", text="{0:1} BAGS".format(bags), font='Helvetica 14 bold').grid(row=0,
                                                                                                        column=13)

    def load_players(self):
        """Loads the player data and necessary labels to the tk window"""
        player_row = 0
        players_in_group = self.group.get_players()
        for player in players_in_group:
            player_paid_color = "red"
            if player.did_pay():
                player_paid_color = "green"

            # Player is deselected by default when the window loads
            player.deselect()

            # player=player saves the instance of the player object at that iteration of the loop for the function to use
            # Otherwise, each checkbutton would operate on the last player in the list (the last encountered in the loop)
            tk.Checkbutton(self.window, text="{0:1}. ".format(player_row + 1), font='Times 14 bold',
                           command=lambda player=player: player.change_select_status()).grid(row=player_row + 2, column=0)
            tk.Label(self.window, fg=player_paid_color, text="{0:1}".format(player.get_name()),
                     font='Helvetica 14 bold').grid(row=player_row + 2, column=1)
            player_row += 1

    def load_transactions(self):
        """Loads the transaction data and necessary labels to the tk window"""
        transaction_row = 0
        for transaction in self.group.get_transactions():
            transaction.selected = False
            tk.Checkbutton(self.window, text="{}".format(transaction.get_type()), font='Times 14 bold',
                           command=lambda transaction=transaction: transaction.change_select_status(),
                           fg="green").grid(row=transaction_row + 2, column=4)
            tk.Label(self.window, text="$ {:.2f}".format(transaction.get_amount()), font='Times 14 bold',
                     fg="green").grid(row=transaction_row + 2, column=5)
            transaction_row += 1

    def load_static_UI(self):
        """ Builds labels, buttons, and formatting that is always present in the main "Group Detail" window"""
        tk.Label(self.window, font='Helvetica 14 bold', text="PLAYER NAME:").grid(row=0, column=1)  # Group Name
        entry_player_name = tk.Entry(self.window, width=20, font='Times 12')  # EntryBox
        entry_player_name.grid(row=0, column=2)

        tk.Label(self.window, text="    |   ").grid(row=0, column=4)

        tk.Label(self.window, font='Helvetica 14 bold', text="TRANSACTION: ").grid(row=0, column=5)  # Group Name
        transaction_amount = tk.Entry(self.window, width=5, font='Times 12')
        transaction_amount.grid(row=0, column=6)

        tk.Label(self.window, text="    |   ").grid(row=0, column=10)

        tk.Label(self.window, font='Helvetica 14 bold', text="PAINT:").grid(row=0, column=11)

        tk.Button(self.window, text=u'\u21BA', font='Helvetica 12',
                  command=lambda: self.confirm_undo_paint()).grid(row=1, column=11)
        tk.Button(self.window, text='ADD BAG', font='Helvetica 12',
                  command=lambda: self.add_paint(1)).grid(row=1, column=13)
        tk.Button(self.window, text='ADD CASE', font='Helvetica 12',
                  command=lambda: self.add_paint(4)).grid(row=1, column=12)

        tk.Button(self.window, text='ADD PLAYER', font='Helvetica 12',
                  command=lambda: self.add_new_player(entry_player_name.get())).grid(row=0, column=3)
        tk.Label(self.window, text='  ').grid(row=1, column=0)

        tk.Label(self.window, text=' ').grid(row=99, column=2)
        tk.Button(self.window, text='MARK PAID', font='Helvetica 12', command=lambda: self.mark_paid()).grid(row=100, column=2)
        tk.Button(self.window, text="REMOVE", font='Helvetica 12', command=lambda: self.remove()).grid(row=100, column=4)

        tk.Button(self.window, text='CASH', font='Helvetica 12',
                  command=lambda: self.create_transaction(float(transaction_amount.get()), "CASH")).grid(row=0, column=7)
        tk.Button(self.window, text='SQUARE', font='Helvetica 12',
                  command=lambda: self.create_transaction(float(transaction_amount.get()),"SQUARE")).grid(row=0, column=8)
        tk.Button(self.window, text='PAYPAL', font='Helvetica 12',
                  command=lambda: self.create_transaction(float(transaction_amount.get()),"PAYPAL")).grid(row=0, column=9)

    """
    Paint Section
    """

    def confirm_undo_paint(self):
        """Opens a confirmation window to confirm if the player would like to undo the last paint bag/case that
        was added
        """
        confirmation_window = tk.Tk()
        button_frame = tk.Frame(confirmation_window)
        button_frame.pack(side="bottom")
        tk.Label(confirmation_window, text="UNDO previously added paint?\n", font="Helvetica 14 bold", fg="red").pack()

        tk.Button(button_frame, text="YES", font="Helvetica 14 bold",
                  command=lambda: self.undo_paint(confirmation_window)).pack(
            side="left")
        tk.Label(button_frame, text="   ").pack(side="left")
        tk.Button(button_frame, text="NO", font="Helvetica 14 bold", command=lambda: confirmation_window.destroy()).pack(
            side="left")

    def undo_paint(self, close_confirmation_window):
        """Removes the last added paint bag/case and updates the UI"""
        close_confirmation_window.destroy()
        if self.group.paint_length() != 0:
            self.group.delete_last_paint()
            self.refresh()
            self.parent_window.refresh()

    def add_paint(self, num_bags):
        """Adds paint to the group and updates the UI"""
        self.group.paint_bags.append(num_bags)
        self.refresh()
        self.parent_window.refresh()

    """
    Player/Transaction Section
    """

    def add_new_player(self, player_name):
        """Adds a new player to the group and refreshes the UI"""
        new_player = Player(player_name)
        self.group.add_player(new_player)
        self.refresh()
        self.parent_window.refresh()

    def mark_paid(self):
        """Marks players paid/unpaid. If no players are selected, this function will call a confirmation window
        to ask the user if they would like to mark all the players as paid (if none are marked as paid, or if some are
        already marked as paid). If all of the players are marked as paid, the function will ask the user if they want
        to mark all the players as UNPAID.
        """
        no_players_selected = True
        for player in self.group.get_players():
            if player.is_selected():
                no_players_selected = False
                if not player.paid:
                    player.paid = True
                else:
                    player.paid = False
        if no_players_selected:
            if self.group.number_of_players() != 0:
                if self.group.players[0].paid == False:
                    self.confirm_all_paid("Mark all PAID", "green", "allPaid")
                else:
                    self.confirm_all_paid("Mark all UNPAID", "red", "allUnpaid")
        self.refresh()
        self.parent_window.refresh()

    def confirm_all_paid(self, message, color, function):
        """Confirmation window which will ask the user if they would like to mark all players as paid or unpaid.
        """
        confirmation_window = tk.Tk()
        button_frame = tk.Frame(confirmation_window)
        button_frame.pack(side="bottom")
        tk.Label(confirmation_window, text=message + '\n', font="Helvetica 14 bold", fg=color).pack()

        if function == "allPaid":
            tk.Button(button_frame, text="YES", font="Helvetica 14 bold",
                      command=lambda: self.all_paid(confirmation_window)).pack(side="left")
        else:
            tk.Button(button_frame, text="YES", font="Helvetica 14 bold",
                      command=lambda: self.all_unpaid(confirmation_window)).pack(side="left")
        tk.Label(button_frame, text="   ").pack(side="left")
        tk.Button(button_frame, text="NO", font="Helvetica 14 bold", command=lambda: self.window.destroy()).pack(
            side="left")

    def all_paid(self, close_confirmation_window):
        """Mark all players as paid and refreshes UI
        """
        for player in self.group.get_players():
            player.mark_paid()
        self.refresh()
        self.parent_window.refresh()
        close_confirmation_window.destroy()

    def all_unpaid(self, close_confirmation_window):
        """Mark all players as unpaid and refreshes UI
        """
        for player in self.group.get_players():
            player.mark_unpaid()
        self.refresh()
        self.parent_window.refresh()
        close_confirmation_window.destroy()

    def remove(self):
        """Removes any selected transactions or players and refreshes the UI
        """
        updated_player_list = [player for player in self.group.get_players() if not player.is_selected()]
        self.group.players = updated_player_list
        updated_transaction_list = [transaction for transaction in self.group.get_transactions() if not transaction.is_selected()]
        self.group.transactions = updated_transaction_list
        self.refresh()
        self.parent_window.refresh()

    def create_transaction(self, transaction_amount, type):
        """Creates a new transaction and refreshes the UI
        """
        self.parent_window.total += transaction_amount
        new_transaction = Transaction(transaction_amount, type)
        self.group.transactions.append(new_transaction)
        self.refresh()
        self.parent_window.refresh()
