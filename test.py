import random
from datetime import datetime


class Customer(object):
    def __init__(self, account_number="", account_name="", account_type="", age="", email="", address=""
                 , account_balance="0"):
        self.account_number = account_number
        self.name = account_name
        self.account_type = account_type
        self.age = age
        self.email = email
        self.address = address
        self.account_balance = account_balance

    def __str__(self):
        return "Account number: " + str(self.account_number) + "\nAccount type: " + str(self.account_type) + \
            "\nAccount name: " + str(self.name) + "\nAge: " + str(self.age) + "\nEmail: " + \
            str(self.email) + "\nAddress: " + str(self.address) + "\nAccount balance: " + str(self.account_balance)

    def create_account(self):
        account_type = int(input("Which account do you want to open?\n"
                                 "Type '1' for Checking; Type '2' to Savings : "))
        if account_type == 1:
            account_type = "Checking Account"
            age = int(input("How old are you? "))
            if age >= 14:
                print("Eligible to open Checking account")
                self.input_account_details(age, account_type)
            else:
                print("Too young to open Checking account")
                print("Exiting Account Creation...")
        elif account_type == 2:
            account_type = "Savings Account"
            age = int(input("How old are you? "))
            if age >= 18:
                print("Eligible to open Checking account")
                self.input_account_details(age, account_type)
            else:
                print("Too young to open Checking account")
                print("Exiting Account Creation...")

    def input_account_details(self, age, account_type):
        account_file = "accounts.txt"
        name = str(input("What is your name? "))
        email = str(input("How can we email you? "))
        address = str(input("Where do you live? (City Country) "))
        account_number = str(random.randint(100, 999))
        account_list = [account_number, account_type, name, str(age), email, address, self.account_balance]
        print("\nOverview Account:\n")
        self.account_number = account_list[0]
        self.account_type = account_list[1]
        self.name = account_list[2]
        self.age = account_list[3]
        self.email = account_list[4]
        self.address = account_list[5]
        self.account_balance = account_list[6]
        print(self.__str__())
        answer = str(input("Type y to confirm account, type n to cancel: "))
        if answer == "y":
            f = open(account_file, "a")
            f.write(",".join(account_list) + "\n")
            f.close()
            print("\nAccount created successfully\n Exiting Account Creation...\n")
        elif answer == "n":
            print("Account creation cancelled\nExiting Account Creation...\n")

    def find_account(self):
        account_number = str(input("What is your account number: "))
        account_file = "accounts.txt"

        # retrieve account info and line number from accounts.txt
        with open(account_file, "r") as filedata:
            retrieved_line = ""
            i = 0
            line_number = 1
            for line in filedata:
                if account_number in line:
                    retrieved_line = line
                    i = i + 1
                    break
                line_number += 1
            if i == 0:
                print("Account \"" + account_number + "\" does not exist in Company BCE records !")
            else:
                # store retrieved information
                account_info = retrieved_line[:-1]
                account_list = list(account_info.split(","))
                self.account_number = account_list[0]
                self.account_type = account_list[1]
                self.name = account_list[2]
                self.age = account_list[3]
                self.email = account_list[4]
                self.address = account_list[5]
                self.account_balance = account_list[6]

                # account management menu
                print("\n*********************\n"
                      "Account Management Menu\n"
                      "*********************\n"
                      "1. View account information \n"
                      "2. View account balance \n"
                      "3. View account transactions \n"
                      "4. Deposit \n"
                      "5. Withdraw \n"
                      "6. Transfer \n"
                      "7. Delete account \n"
                      "x. Exit \n"
                      "*********************\n")
                answer = str(input("Your response: "))
                # variables for methods called in the account management menu
                account_type = self.account_type
                account_name = self.name
                account_age = self.age
                account_email = self.email
                account_address = self.address
                account_balance = self.account_balance

                if answer == "1":
                    # view account information
                    print("\n---Information for account {" + account_number + "}---\n")
                    print("Account type: ", account_type, "\nAccount name : ", account_name, "\nAccount age: ",
                          account_age, "\nAccount email: ", account_email, "\nAccount address: ", account_address, "\n")
                elif answer == "2":
                    # view account balance
                    print("\n---Balance for account \"" + account_number + "\"---\n")
                    print(account_balance, "\n")
                elif answer == "3":
                    # view account transactions
                    self.view_transactions(account_number)
                    self.view_transfers(account_number)
                elif answer == "4":
                    # deposit
                    self.deposit(line_number, account_number)
                elif answer == "5":
                    # withdraw
                    self.withdraw(line_number, account_number, account_type)
                elif answer == "6":
                    # transfer
                    self.transfer(line_number, account_number, account_type)
                elif answer == "7":
                    # delete account
                    self.delete_account(account_number)
                elif answer == "x":
                    print("exit")
                else:
                    print("Invalid menu option\n")

    def deposit(self, line_number, account_number):
        account_file = "accounts.txt"
        transaction_type = "Deposit" # variable for recording the transaction
        amount = int(input("How much do you want to deposit into your account?\n"
                           "Amount: "))

        # check user input is valid
        if amount > 1:
            # retrieve current balance from accounts.txt
            with open(account_file, "r") as filedata:
                lines = filedata.readlines()
            filedata.close()
            line = lines[line_number - 1]
            line_list = line.split(",")
            current_balance = int(line_list[6])

            new_balance = current_balance + amount

            line_list[6] = str(new_balance)
            new_line = ",".join(line_list) + "\n"
            lines[line_number - 1] = new_line

            # write new balance to accounts.txt
            with open(account_file, "w") as f:
                f.writelines(lines)
            filedata.close()
            print("\nNew account balance: ", new_balance)

            # record transaction to accountsTransactions.txt
            self.record_transaction(account_number, transaction_type, amount)
        else:
            print("Invalid amount!")

    def withdraw(self, line_number, account_number, account_type):
        account_file = "accounts.txt"
        transaction_type = "Withdraw" # variable for recording the transaction
        amount = int(input("How much do you want to withdraw from your account?\n"
                           "Amount: "))

        # check that user input is valid integer
        if amount > 1:
            # retrieve current balance from accounts.txt
            with open(account_file, "r") as filedata:
                lines = filedata.readlines()
            filedata.close()
            line = lines[line_number - 1]
            line_list = line.split(",")
            current_balance = int(line_list[6])

            # check user account type to allow/deny withdrawal
            if account_type == "Checking Account":
                new_balance = current_balance - amount
                if new_balance < -200:
                    print("Credit limit of -200€ reached! Cannot withdraw. Try another amount.")
                else:
                    line_list[6] = str(new_balance)
                    new_line = ",".join(line_list) + "\n"
                    lines[line_number - 1] = new_line

                    # write new balance to accounts.txt
                    with open(account_file, "w") as f:
                        f.writelines(lines)
                    filedata.close()
                    print("\nNew account balance: ", new_balance)

                    # record transaction to accountsTransactions.txt
                    self.record_transaction(account_number, transaction_type, amount)

            elif account_type == "Savings Account":
                # check if specific account has already made 1 withdrawal for the month
                # read lines of accountsTransactions.txt
                with open("accountsTransactions.txt", "r") as f:
                    transactions = f.readlines()
                f.close()
                current_month_withdrawals = 0
                # loop through the lines to look for a match in account number, type of transaction & current month
                for transaction in transactions:
                    transaction_info = transaction.split(",")
                    if transaction_info[1] == account_number and transaction_info[2] == "Withdraw"\
                        and self.is_current_month(transaction_info[0]):
                        current_month_withdrawals += 1
                if current_month_withdrawals > 0:
                    print("You have reached your maximum withdrawal of 1 for the month!")
                    return  # end the loop if a withdrawal has been made in current month
                else:
                    new_balance = current_balance - amount
                    if new_balance < 0:
                        print("You cannot withdraw below negative balance!")
                    else:
                        line_list[6] = str(new_balance)
                        new_line = ",".join(line_list) + "\n"
                        lines[line_number - 1] = new_line

                        # write new balance to accounts.txt
                        with open(account_file, "w") as f:
                            f.writelines(lines)
                        filedata.close()
                        print("\nNew account balance: ", new_balance)

                        # record transaction to accountsTransactions.txt
                        self.record_transaction(account_number, transaction_type, amount)
        else:
            print("Invalid amount!")

    def is_current_month(self, timestamp):
        transaction_date = datetime.fromtimestamp(int(timestamp))
        current_date = datetime.now()
        return transaction_date.year == current_date.year and transaction_date.month == current_date.month

    def delete_account(self, account_number):
        print("Do you want to delete your account? Type y for yes, n for no: ")
        answer = str(input("Your response:"))

        if answer == "y":
            file = open("accounts.txt", "r")
            lines = file.readlines()
            new_lines = []
            for line in lines:
                if account_number not in line.strip():
                    new_lines.append(line)
            file.close()
            file = open("accounts.txt", "w")
            file.writelines(new_lines)
            file.close()
            print("Account deleted successfully")
        elif answer == "n":
            print("no account deletion")
        else:
            print("input not recognized")
            answer = str(input("Your response:"))

    def record_transaction(self, account_num, transaction_type, amount):
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        ts_int = int(ts)
        transaction_list = [str(ts_int), account_num, transaction_type, str(amount)]

        f = open("accountsTransactions.txt", "a")
        f.write(",".join(transaction_list) + "\n")
        f.close()
        print("Transaction of type: ", transaction_type, "\nAmount: ", amount,
              "\nAccount number: ", account_num, "\nTransaction successfully recorded\n")

    def view_transactions(self, account_number):
        account_transactions_file = "accountsTransactions.txt"

        # retrieve all transactions for account_number from accountsTransactions.txt
        with open(account_transactions_file, "r") as filedata:
            lines = filedata.readlines()
        filedata.close()
        matching_lines = []

        # loop through retrieved lines to store matching lines in matching_lines list
        for line in lines:
            line_list = list(line.split(","))
            if line_list[1] == account_number:
                matching_lines.append(line.strip())

        if len(matching_lines) == 0:
            print("There are no transactions recorded for account number {", account_number, "}\n")
        else:
            print("Transactions for account number {", account_number, "} :\n")
            for line in matching_lines:
                timestamp, account_number, transaction_type, amount = line.split(",")
                # converting timestamp to date time format
                date_time = datetime.fromtimestamp(int(timestamp))
                print(date_time, transaction_type, amount, "\n")

    def view_transfers(self, account_number):
        account_transfers_file = "accountsTransfers.txt"

        # retrieve all transfers for account_number from accountsTransactions.txt
        with open(account_transfers_file, "r") as filedata:
            lines = filedata.readlines()
        filedata.close()
        matching_lines = []

        # loop through retrieved lines to store matching lines in matching_lines list
        for line in lines:
            line_list = line.split(",")
            if line_list[1] == account_number:
                matching_lines.append(line.strip())

        if len(matching_lines) == 0:
            print("There are no transfers recorded for account number {", account_number, "}\n")
        else:
            print("Transfers for account number {", account_number, "} :\n")
            for line in matching_lines:
                timestamp, account_number, transaction_type, recipient, amount = line.split(",")
                # converting timestamp to date time format
                date_time = datetime.fromtimestamp(int(timestamp))
                print(date_time, transaction_type, recipient, amount, "\n")

    def transfer(self, line_number, account_number, account_type):
        account_file = "accounts.txt"
        transaction_type = "Transfer"  # variable for recording the transaction
        amount = int(input("How much do you want to transfer from your account?\n"
                           "Amount: "))
        # check amount is valid
        if amount > 1:
            # retrieve current balance from accounts.txt
            with open(account_file, "r") as filedata:
                lines = filedata.readlines()
            filedata.close()
            line = lines[line_number - 1]
            line_list = line.split(",")
            current_balance = int(line_list[6])

            # check user account type to confirm/deny transfer
            if account_type == "Checking Account":
                new_balance = current_balance - amount
                print(new_balance)
                if new_balance < -200:
                    print("Credit limit of -200€ reached! Cannot transfer. Try another amount.")
                else:
                    recipient = input("Who do you want to transfer to?\n Account number: ")
                    # check other account number exists
                    with open(account_file, "r") as filedata:
                        i = 0
                        line_number_recipient = 1
                        for line in filedata:
                            if recipient in line:
                                i = i + 1
                                break
                            line_number_recipient += 1
                        if i == 0:
                            print("Account \"" + recipient + "\" does not exist in Company BCE records !")
                        else:
                            # substract amount from account_number
                            line_list[6] = str(new_balance)
                            new_line = ",".join(line_list) + "\n"
                            lines[line_number - 1] = new_line
                            # write new balance to accounts.txt
                            with open(account_file, "w") as f:
                                f.writelines(lines)
                            filedata.close()
                            print("\nNew account balance: ", new_balance)

                            # retrieve current balance recipient
                            with open(account_file, "r") as filedata:
                                lines_recipient = filedata.readlines()
                            filedata.close()
                            line_recipient = lines[line_number_recipient - 1]
                            line_list_recipient = line_recipient.split(",")
                            current_balance_recipient = int(line_list_recipient[6])
                            print(current_balance_recipient)
                            # add amount to recipient
                            new_balance_recipient = current_balance_recipient + amount
                            print(new_balance_recipient)
                            line_list_recipient[6] = str(new_balance_recipient)
                            new_line_recipient = ",".join(line_list_recipient) + "\n"
                            lines_recipient[line_number_recipient - 1] = new_line_recipient
                            # write recipient new balance to accounts.txt
                            with open(account_file, "w") as f:
                                f.writelines(lines_recipient)
                            filedata.close()

                            # record transaction to accountsTransfers.txt
                            self.record_transfers(account_number, recipient, transaction_type, amount)

            elif account_type == "Savings Account":
                # check if specific account has already made 1 withdrawal for the month
                # read lines of accountsTransactions.txt
                with open("accountsTransfers.txt", "r") as f:
                    transactions = f.readlines()
                f.close()
                current_month_withdrawals = 0
                # loop through the lines to look for a match in account number, type of transaction & current month
                for transaction in transactions:
                    transaction_info = transaction.split(",")
                    if transaction_info[1] == account_number and transaction_info[2] == "Transfer" \
                            and self.is_current_month(transaction_info[0]):
                        current_month_withdrawals += 1
                if current_month_withdrawals > 0:
                    print("You have reached your maximum transfer of 1 for the month!")
                    return  # end the loop if a withdrawal has been made in current month
                else:
                    new_balance = current_balance - amount
                    if new_balance < 0:
                        print("You cannot transfer below negative balance!")
                    else:
                        recipient = input("Who do you want to transfer to?\n Account number: ")
                        # check other account number exists
                        with open(account_file, "r") as filedata:
                            i = 0
                            line_number_recipient = 1
                            for line in filedata:
                                if recipient in line:
                                    i = i + 1
                                    break
                                line_number_recipient += 1
                            if i == 0:
                                print("Account \"" + recipient + "\" does not exist in Company BCE records !")
                            else:
                                # substract amount from account_number
                                line_list[6] = str(new_balance)
                                new_line = ",".join(line_list) + "\n"
                                lines[line_number - 1] = new_line
                                # write new balance to accounts.txt
                                with open(account_file, "w") as f:
                                    f.writelines(lines)
                                filedata.close()
                                print("\nNew account balance: ", new_balance)

                                # retrieve current balance recipient
                                with open(account_file, "r") as filedata:
                                    lines_recipient = filedata.readlines()
                                filedata.close()
                                line_recipient = lines[line_number_recipient - 1]
                                line_list_recipient = line_recipient.split(",")
                                current_balance_recipient = int(line_list_recipient[6])
                                print(current_balance_recipient)
                                # add amount to recipient
                                new_balance_recipient = current_balance_recipient + amount
                                print(new_balance_recipient)
                                line_list_recipient[6] = str(new_balance_recipient)
                                new_line_recipient = ",".join(line_list_recipient) + "\n"
                                lines_recipient[line_number_recipient - 1] = new_line_recipient
                                # write recipient new balance to accounts.txt
                                with open(account_file, "w") as f:
                                    f.writelines(lines_recipient)
                                filedata.close()

                                # record transaction to accountsTransfers.txt
                                self.record_transfers(account_number, recipient, transaction_type, amount)
        else:
            print("Invalid amount!")

    def record_transfers(self, account_number, recipient, transaction_type, amount):
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        ts_int = int(ts)
        transaction_list = [str(ts_int), account_number, transaction_type, recipient, str(amount)]

        f = open("accountsTransfers.txt", "a")
        f.write(",".join(transaction_list) + "\n")
        f.close()
        print("Transaction of type: ", transaction_type, "\nAmount: ", amount,
              "\n From account number: ", account_number, "\n To recipient account number: ",
                recipient, "\nTransaction successfully recorded\n")

class Account(object):
    def __init__(self):
        pass


def banking_menu():
    p1 = Customer()
    p2 = Account()
    answer = ""
    while answer != "x":
        print("*********************\n"
              "BANK CDE MENU \n"
              "Welcome to Bank CDE services \n"
              "How can we help you today?\n"
              "*********************\n"
              "Enter the number corresponding to the option you want \n"
              "To exit, enter x\n"
              "*********************\n"
              "1. Create Account \n"
              "2. Manage Account \n"
              "*********************")
        answer = str(input("Your response: "))

        if answer == "1":
            p1.create_account()
        elif answer == "2":
            p1.find_account()
        elif answer == "x":
            print("Thank you for choosing Bank CDE, bye babe!")
        else:
            print("Invalid menu option\n")


banking_menu()
