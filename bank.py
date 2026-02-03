import json
import random
import string
from pathlib import Path

class Bank:
    database = Path(__file__).parent / "data.json"

    def __init__(self):
        if self.database.exists():
            self.data = json.loads(self.database.read_text())
        else:
            self.data = []

    def __save(self):
        self.database.write_text(json.dumps(self.data, indent=4))

    def __generate_account(self):
        while True:
            acc = "".join(
                random.sample(string.ascii_letters + string.digits, 8)
            )
            if not any(u["account_no"] == acc for u in self.data):
                return acc

    def create_account(self, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return False, "Invalid age or PIN"

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_no": self.__generate_account(),
            "balance": 0
        }

        self.data.append(account)
        self.__save()
        return True, account

    def authenticate(self, acc_no, pin):
        for user in self.data:
            if user["account_no"] == acc_no and user["pin"] == pin:
                return user
        return None
    
    def show_details(self, acc_no, pin):
        user = self.authenticate(acc_no, pin)
        if not user:
            return False, "Invalid credentials"

        return True, {
            "Name": user["name"],
            "Age": user["age"],
            "Email": user["email"],
            "Account Number": user["account_no"],
            "Balance": user["balance"]
        }


    def deposit(self, acc_no, pin, amount):
        user = self.authenticate(acc_no, pin)
        if not user:
            return False, "Invalid credentials"
        if amount <= 0 or amount > 100000:
            return False, "Invalid deposit amount"

        user["balance"] += amount
        self.__save()
        return True, user["balance"]

    def withdraw(self, acc_no, pin, amount):
        user = self.authenticate(acc_no, pin)
        if not user:
            return False, "Invalid credentials"
        if amount <= 0 or amount > 50000:
            return False, "Invalid withdrawal amount"
        if user["balance"] < amount:
            return False, "Insufficient balance"

        user["balance"] -= amount
        self.__save()
        return True, user["balance"]

    def update_details(self, acc_no, pin, name=None, email=None, new_pin=None):
        user = self.authenticate(acc_no, pin)
        if not user:
            return False, "Invalid credentials"

        if name:
            user["name"] = name
        if email:
            user["email"] = email
        if new_pin and len(str(new_pin)) == 4:
            user["pin"] = new_pin

        self.__save()
        return True, "Details updated"

    def delete_account(self, acc_no, pin):
        user = self.authenticate(acc_no, pin)
        if not user:
            return False, "Invalid credentials"

        self.data.remove(user)
        self.__save()
        return True, "Account deleted"
