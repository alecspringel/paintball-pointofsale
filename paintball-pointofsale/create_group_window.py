import tkinter as tk
from group import Group

class CreateGroupWindow:
    """Creates a new window to add a new group. The parent window is recorded in order to refresh/update the UI
    with new information that gets recorded by the user in this window.

     For example, the user will enter the group name, and deposit amount of the group. The parent window will be called
     to update the total value of all groups (+= this group's deposit), and to add this group to the active_players list
     which resides in the parent window.
    """
    def __init__(self, parent):
        self.parent_window = parent
        self.window = tk.Tk()
        self.create_new_group_window()


    def create_new_group_window(self):
        """Loads the input fields/buttons for adding a new group name, its deposit, and type
        """
        tk.Label(self.window, text="Group Name ", font="Helvetica 14 bold").grid(row=0, column=0)  # Group Name
        entry_group_name = tk.Entry(self.window, font='Times 14')  # EntryBox
        entry_group_name.grid(row=0, column=1)

        tk.Label(self.window, text="Deposit ", font="Helvetica 14 bold").grid(row=1, column=0)  # Group Name
        entry_deposit = tk.Entry(self.window, font='Times 14')  # EntryBox
        entry_deposit.grid(row=1, column=1)

        tk.Button(self.window, text='Rental', font="Helvetica 14",
                  command=lambda: self.create_group_data(entry_group_name.get(), float(entry_deposit.get()),
                                                   "Rental")).grid(row=2, column=0)
        tk.Button(self.window, text='Speedball', font="Helvetica 14",
                  command=lambda: self.create_group_data(entry_group_name.get(), float(entry_deposit.get()),
                                                   "Speedball")).grid(row=2, column=1)
        tk.Button(self.window, text='Groupon', font="Helvetica 14",
                  command=lambda: self.create_group_data(entry_group_name.get(), float(entry_deposit.get()),
                                                   "Groupon")).grid(row=2, column=2)

    def create_group_data(self, group_name, group_deposit, group_type):
        """
        Creates "Group" object from user input, adds to active group array, then updates the UI
        """
        # Update total cash value of all active groups
        self.parent_window.add_to_total(group_deposit)
        new_group = (Group(group_name, group_deposit, group_type))
        self.parent_window.add_active_group(new_group)
        self.window.destroy()