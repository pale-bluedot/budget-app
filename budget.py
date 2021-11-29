##################################################################################################
# File name: budget.py
# Author: Johan Andrade
# Date created: 08 / 18 / 2021
# Date last modified  10 / 12 / 2021
# Description: A budget program using class and methods.
# Refer to README.md for full description
##################################################################################################


class Category:
    def __init__(self, category):
        self.ledger = list()
        self.amount = 0
        self.category = category

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.amount += amount

    def check_funds(self, amount):
        if self.amount >= amount:
            return True
        else:
            return False

    def withdraw(self, amount, description=""):
        if self.check_funds(amount) == True:
            self.amount -= amount
            self.ledger.append({
                "amount": amount * -1,
                "description": description
            })
            return True
        else:
            return False

    def get_balance(self):
        return self.amount

    def transfer(self, amount, category):
        if self.check_funds(amount) == True:
            self.withdraw(amount, "Transfer to " + category.category)
            category.deposit(amount, "Transfer from " + self.category)
            return True
        else:
            return False

    def __str__(self):
        result = ""
        result += f"{self.category:*^30}\n"
        for transaction in self.ledger:
            amount = 0
            description = ""
            for key, value in transaction.items():
                if key == "amount":
                    amount = value
                elif key == "description":
                    description = value
            if len(description) > 23:
                description = description[:23]
            amount = str(format(float(amount), '.2f'))
            if len(amount) > 7:
                amount = amount[:7]
            result += description + str(amount).rjust(30 -
                                                      len(description)) + "\n"
        result += "Total: " + str(format(float(self.amount), '.2f'))
        return result

    # Used for spend chart
    def get_withdrawals(self):
        total = 0
        for item in self.ledger:
            if item["amount"] < 0:
                total += item["amount"]
        return total


def create_spend_chart(categories):
    result = "Percentage spent by category\n"
    i = 100
    totals = getTotals(categories)

    while i >= 0:
        cat_spaces = " "
        for total in totals:
            if total * 100 >= i:
                cat_spaces += "o  "
            else:
                cat_spaces += "   "
        result += str(i).rjust(3) + "|" + cat_spaces + "\n"
        i -= 10

    dashes = "-" + "---" * len(categories)
    names = []
    x_axis = ""
    for category in categories:
        names.append(category.category)

    maxi = max(names, key=len)

    for x in range(len(maxi)):
        nameStr = '     '
        for name in names:
            if x >= len(name):
                nameStr += "   "
            else:
                nameStr += name[x] + "  "

        if (x != len(maxi) - 1):
            nameStr += '\n'

        x_axis += nameStr

    result += dashes.rjust(len(dashes) + 4) + "\n" + x_axis
    return result


def getTotals(categories):
    total = 0
    breakdown = []
    for category in categories:
        total += category.get_withdrawals()
        breakdown.append(category.get_withdrawals())
    rounded = list(map(lambda x: truncate(x / total), breakdown))
    return rounded


def truncate(n):
    multiplier = 10
    return int(n * multiplier) / multiplier