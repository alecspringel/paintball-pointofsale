class Group:
    """
    name: Name of group (String)
    deposit: $ Amount required to book the group (Float)
    type: Speedball, Recball, Rental (String)
    players: ([Object])
    paint_bags: list of paint the group has purchased ([Int])
    transactions: ([Object])
    """

    def __init__(self, name, deposit, type):
        self.name = name
        self.deposit = deposit
        self.type = type
        self.players = []
        self.paint_bags = []
        self.transactions = []

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def number_of_players(self):
        return len(self.players)

    def total_spent(self):
        total_spent_by_group = 0.0
        for transaction in self.transactions:
            total_spent_by_group += transaction.amount
        return total_spent_by_group

    def get_deposit(self):
        return self.deposit

    def grand_total(self):
        return self.total_spent() + self.deposit

    def check_if_players_paid(self):
        if len(self.players) == 0:
            return False
        for player in self.players:
            if not player.paid:
                return False
        return True

    def number_players_paid(self):
        players_who_paid = 0
        for player in self.players:
            if player.paid:
                players_who_paid += 1
        return players_who_paid

    def total_bags_and_cases(self):
        cases = sum(self.paint_bags) // 4
        bags = sum(self.paint_bags) % 4

        return bags, cases

    def get_players(self):
        return self.players

    def add_player(self, player):
        self.players.append(player)

    def get_transactions(self):
        return self.transactions

    def paint_length(self):
        return len(self.paint_bags)

    def delete_last_paint(self):
        del self.paint_bags[-1]

class Player:
    def __init__(self, name):
        self.name = name
        self.paid = False  # 2
        self.selected = False  # 6

    def change_select_status(self):
        if not self.selected:
            self.selected = True
        else:
            self.selected = False

    def get_name(self):
        return self.name

    def mark_paid(self):
        self.paid = True

    def mark_unpaid(self):
        self.paid = False

    def did_pay(self):
        return self.paid

    def change_pay_status(self):
        if self.paid:
            self.paid = False
        else:
            self.paid = True

    def is_selected(self):
        return self.selected

    def deselect(self):
        self.selected = False

class Transaction:
    def __init__(self, amount, type):
        self.amount = amount
        self.type = type
        self.selected = False

    def change_select_status(self):
        if not self.selected:
            self.selected = True
        else:
            self.selected = False

    def get_type(self):
        return self.type

    def get_amount(self):
        return self.amount

    def is_selected(self):
        return self.selected