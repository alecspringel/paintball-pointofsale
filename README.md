# Point of Sale System for Paintball Fields
A simple point of sale system for paintball fields that manages groups, players, and transactions with exports to Microsoft Excel.  
  
## Why?
During my Sophomore year of college, I worked at a small paintball field near my school. The owner of the field would write hundreds of names down each day, tally inventory that had been moved, and record transactions with pen and paper. This program is for other small field owners who need a way to keep track of their customers and sales.  
  
## Usage
### Getting Started
1. Clone the project  
2. Run requirements.txt (```$ pip install -r requirements.txt```)
  * tkinter is also required but comes standard with most installations of Python  
3. Run (```$ python paintball_pointofsale.py```)

### Using the Program
![alt text](https://raw.githubusercontent.com/alecspringel/paintball-pointofsale/master/readme-assets/readmeDemo.PNG)
**The lower window is the main window, represented by `class MainWindow` in main_window.py**  
  * The main window is responsible for displaying an overview of all "active" groups
  * Clicking the "ADD GROUP" button will open a small window to add a new active group by inputting a group name, deposit amount, and "type"
  * The checkmark button: Removes the group from the window and exports data to GroupRecords.xlsx
    * If GroupRecords.xlsx is not present in the directory, the group will be removed without saving the data
  * The X button: Deletes the group, removing it without attempting to save
  * Clicking on the group name (in this case, "Bob's Group") will launch the upper window, the group detail window represented by `class GroupDetailWindow` in group_detail_window.py
---
**The upper window is the group detail window, represented by `class GroupDetailWindow` in group_detail_window.py**  
  * The group detail window is responsible for displaying all of the players/transactions associated with a group
    * "Ticking" a player and clicking "MARK PAID" will turn the name green, or will turn the name red if the player was already marked as paid (mark/unmark as paid)
    * The "REMOVE" button will remove any selected players/transactions from the window
  * The window also allows the user to add quantities of paintballs purchased by the group, for the sake of tracking inventory
    * The counter-clockwise arrow button allows the user to remove the last case/bag of paint that was added
