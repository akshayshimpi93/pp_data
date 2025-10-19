import json, random, string
from pathlib import Path

class BankDB:
    DB_FILE = 'data.json'
    data = []

    @classmethod
    def load(cls):
        if Path(cls.DB_FILE).exists():
            cls.data = json.loads(Path(cls.DB_FILE).read_text())
        else:
            cls.data = []

    @classmethod
    def save(cls):
        Path(cls.DB_FILE).write_text(json.dumps(cls.data, indent=2))

    @staticmethod
    def generate_account_no():
        chars = random.choices(string.ascii_letters, k=3) \
              + random.choices(string.digits, k=3) \
              + random.choices("!@#$%^&*", k=1)
        random.shuffle(chars)
        return ''.join(chars)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            raise ValueError("Invalid age or PIN")
        acct = {
            "name": name, "age": age, "email": email,
            "pin": pin, "accountNo": cls.generate_account_no(), "balance": 0
        }
        cls.data.append(acct)
        cls.save()
        return acct

    @classmethod
    def find_user(cls, accountNo, pin):
        for u in cls.data:
            if u["accountNo"] == accountNo and u["pin"] == pin:
                return u
        return None

    @classmethod
    def deposit(cls, user, amt):
        if amt <= 0 or amt > 10000:
            raise ValueError("Amount must be between 1 and 10,000")
        user["balance"] += amt
        cls.save()

    @classmethod
    def withdraw(cls, user, amt):
        if amt <= 0 or amt > user["balance"]:
            raise ValueError("Insufficient or invalid amount")
        user["balance"] -= amt
        cls.save()
