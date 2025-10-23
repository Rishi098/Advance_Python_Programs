class BankAccount:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0
    
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive!")
        else:
            self.balance += amount
            print(f"Deposited {amount}. Current balance: {self.balance}")
    
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive!")
        elif amount > self.balance:
            print("Insufficient funds!")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. Current balance: {self.balance}")
    
    def check_balance(self):
        print(f"Current balance: {self.balance}")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username, password

def main():
    print("Welcome to the Bank System")
    
    username, password = login()
    
    user_account = BankAccount(username, password)
    
    while True:
        print("\nChoose an option:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            amount = float(input("Enter amount to deposit: "))
            user_account.deposit(amount)
        elif choice == '2':
            amount = float(input("Enter amount to withdraw: "))
            user_account.withdraw(amount)
        elif choice == '3':
            user_account.check_balance()
        elif choice == '4':
            print("Thank you for using our service!")
            break
        else:
            print("Invalid choice, try again!")

if __name__ == "__main__":
    main()
