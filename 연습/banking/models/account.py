from models.transaction import Transaction

class Account:
    def __init__(self) -> None:
        self.__balance = 10000
        self.transactions = []
    
    def deposit(self, amount: int) -> None:
        if amount > 0:
            self.__balance += amount
            self.transactions.append(Transaction("입금", amount, self.__balance))
        else:
            "금액을 제대로 입력해주세요"


    def withdraw(self, amount: int) -> None:
        # 입력 받은 금액이 잔고보다 작아야하고 0보다는 커야해
        if (0 < amount) and (amount <= self.__balance):
            self.__balance -= amount
            self.transactions.append(Transaction("출금", amount, self.__balance))
        else:
            "금액을 제대로 입력해주세요"
