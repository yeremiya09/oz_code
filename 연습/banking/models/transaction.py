"""
transaction_type: 입금 또는 출금이라는 값이 입력이 됩니다
"""


class Transaction:
    def __init__(self, transaction_type: str, amount: int, balance: int) -> None:
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance = balance
    def __str__(self) -> str:
        return f"{self,transaction_type}: {self.amount}원, 잔고: {self.balance}원"
    def to_tuple(self) -> tuple:
        return self.transaction_type, self.amount, self.balance

