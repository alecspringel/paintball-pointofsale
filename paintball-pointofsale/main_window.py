import tkinter as tk
import pickle
from group import Group, Player, Transaction
from create_group_window import CreateGroupWindow
from group_detail_window import GroupDetailWindow
from checkout import checkout


class MainWindow:
    """Handles the main "Group" Window: monitors active groups objects, keeps track of the total spent
    by all groups, and loads the necessary tkinter UI components with according data.
    """

    def __init__(self, excel_enabled):
        self.window = tk.Tk()
        self.excel_enabled = excel_enabled
        backup = []
        with open("groupBackup.txt", "rb") as f:
            backup = pickle.load(f)
        if(type(backup) is not list):
            backup = []
        self.active_groups = backup
        self.total = 0.0
        self.load_static_UI()
        self.load_groups_into_window()
        self.window.mainloop()

    def add_to_total(self, amount):
        self.total += amount

    def subtract_from_total(self, amount):
        self.total -= amount

    def add_active_group(self, group):
        """Adds group to list of active groups
        """
        self.active_groups.append(group)
        self.refresh()

    def refresh(self):
        """Removes all tkinter components from the window, then reloads the UI along with any added data.
        """
        # Refreshes main window
        _list = self.window.winfo_children()

        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        widget_list = _list
        for item in widget_list:
            item.grid_forget()
        #---
        with open("groupBackup.txt", "wb") as f:
            pickle.dump(self.active_groups, f)
        #---
        self.load_static_UI()
        self.load_groups_into_window()

    def load_static_UI(self):
        """ Builds labels, buttons, and formatting that is always present in the main "Group" window"""

        label_font = ['Helvetica', 20, 'bold', 'underline']

        # Group name header label
        tk.Label(self.window, text="GROUP", font=(label_font), padx=10).grid(row=0, column=0)

        # Group name header space
        tk.Label(self.window, text="").grid(row=19, column=0)

        # Total unpaid/paid players fraction header label
        tk.Label(self.window, text="PAID / PLAYERS", font=(label_font), padx=10).grid(row=0, column=1)

        # Deposit header label
        tk.Label(self.window, text="DEPOSIT", font=(label_font), padx=10).grid(row=0, column=2)

        # Total paid by group header label
        tk.Label(self.window, text="$ PAID", font=(label_font), padx=10).grid(row=0, column=3)

        # Group paint header label
        tk.Label(self.window, text="PAINT", font=(label_font), padx=10).grid(row=0, column=4)

        # Checkout header label
        tk.Label(self.window, text="CHECKOUT", font=(label_font), padx=10).grid(row=0, column=5, columnspan=2)

        # Add group button: Calls create_new_group_window() for user to add a new group
        tk.Button(self.window, text="ADD GROUP", font=('Helvetica', 18, 'bold'),
                  command=lambda: CreateGroupWindow(self)).grid(row=20,
                                                                column=1)  # FIXME ===== change self to self.window

        tk.Label(self.window, text='Total: ', font="Helvetica 14 bold").grid(row=20, column=2)

    def load_groups_into_window(self):
        """Loads each group from self.active_groups into the window with its respective buttons/information
        """
        # Total value of all deposits and money spent by groups
        total_spent_all_groups = 0
        UIfont = "Helvetica 16 bold"

        # Label headers are on row 0 - groups will begin on row 1 of TK window
        row = 1
        for group in self.active_groups:
            # Total number of bags, cases purchased by group
            bags, cases = group.total_bags_and_cases()
            # Color for representing whether or not the group has paid
            group_did_pay_color = "red"

            # Groups names are displayed within a button that can be clicked for additional details about the group
            tk.Button(self.window, text=group.name, command=lambda group=group: GroupDetailWindow(self, group),
                      # FIXME ===
                      font='Times 16').grid(row=row, column=0)

            if group.check_if_players_paid():
                group_did_pay_color = "green"

            # Displays fraction of players paid: is red if < 1, is green if == 1
            tk.Label(self.window, text="{} / {}".format(group.number_players_paid(), group.number_of_players()),
                     fg=group_did_pay_color, font=UIfont).grid(row=row, column=1)
            # Displays group deposit
            tk.Label(self.window, text="${:.2f}".format(group.get_deposit()),
                     fg=group_did_pay_color, font=UIfont).grid(row=row, column=2)
            # Displays total spent by group
            tk.Label(self.window, text="${:.2f}".format(group.total_spent()),
                     fg=group_did_pay_color, font=UIfont).grid(row=row, column=3)

            tk.Label(self.window, text="CASES: {} BAGS: {}".format(cases, bags),
                     fg="blue", font=UIfont).grid(row=row, column=4)

            # Button sends group to excel sheet if excel is enabled, removes the group from window
            tk.Button(self.window, text=u'\u2713', font=UIfont, width=1,
                      command=lambda group=group: self.confirm_checkout(group, "CHECKOUT:\n", True)).grid(row=row,
                                                                                                          column=5)

            # Removes group from window without saving to excel
            tk.Button(self.window, text='X', font=UIfont, width=1, command=lambda group=group: self.confirm_checkout(
                    group, "REMOVE GROUP:\n", False)).grid(row=row, column=6)

            total_spent_all_groups += group.grand_total()
            row += 1

        # Displays all cash from deposits and spending in the window
        tk.Label(self.window, text='$ {:.2f}'.format(total_spent_all_groups), font=UIfont).grid(row=20, column=3)

    def confirm_checkout(self, group, text, save):
        """Creates a confirmation window to ensure the user meant to "checkout" the group"""
        confirmation_window = tk.Tk()
        button_frame = tk.Frame(confirmation_window)
        button_frame.pack(side="bottom")
        tk.Label(confirmation_window, text=text, font="Helvetica 14 bold", fg="red").pack()
        tk.Label(confirmation_window, text="{}\n".format(group.name), font="Helvetica 16 bold", fg="blue").pack()

        tk.Button(button_frame, text="YES", font="Helvetica 14 bold",
                  command=lambda: self.checkout_group(confirmation_window, group, save)).pack(
            side="left")
        tk.Label(button_frame, text="   ").pack(side="left")
        tk.Button(button_frame, text="NO", font="Helvetica 14 bold",
                  command=lambda: confirmation_window.destroy()).pack(side="left")

    def checkout_group(self, window, group, save):
        """Destroys the confirmation window after the user chooses "Yes" or "No", removes the group from the list
        of active groups, and reduces their total value from the window total. If excel saving is enabled, the group
        will be sent to excel
        """
        window.destroy()
        if self.excel_enabled:
            checkout(group, save)
        self.active_groups.remove(group)
        self.total -= group.grand_total()
        self.refresh()
