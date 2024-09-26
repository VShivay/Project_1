import tkinter as tk
from tkinter import messagebox, simpledialog

class Bank:
    def __init__(self, acc_name, branch, ifsc_code, balance):
        self.acc_name = acc_name
        self.branch = branch
        self.ifsc_code = ifsc_code.upper()
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return f"Deposited {amount}. New balance is {self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient balance"
        else:
            self.balance -= amount
            return f"Withdrawn {amount}. New balance is {self.balance}"

    def transfer(self, amount, recipient):
        if amount > self.balance:
            return "Insufficient balance"
        else:
            self.balance -= amount
            recipient.balance += amount
            return f"Transferred {amount} to {recipient.acc_name}. Your new balance is {self.balance}"

    def display_details(self):
        return f"Account Name: {self.acc_name}, Branch: {self.branch}, IFSC: {self.ifsc_code}, Balance: {self.balance}"

# GUI application using tkinter
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Account Management System")
        self.root.configure(bg="#f0f0f0")
        self.root.attributes('-fullscreen', True)  # Set the window to full-screen mode

        # Close the app when "Escape" key is pressed
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        self.accounts = []

        # Center frame for all the widgets
        self.center_frame = tk.Frame(root, bg="#f0f0f0")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Set colors
        label_bg = "#dde8f2"     # Light blue background for labels
        entry_bg = "#ffffff"     # White background for entry fields
        button_bg = "#4caf50"    # Green background for buttons
        button_fg = "#ffffff"    # White text color for buttons
        frame_bg = "#cfd8dc"     # Light gray background for frames

        # Labels and entries for account creation
        tk.Label(self.center_frame, text="Account Name", bg=label_bg).pack(pady=5)
        self.acc_name_entry = tk.Entry(self.center_frame, bg=entry_bg)
        self.acc_name_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Branch", bg=label_bg).pack(pady=5)
        self.branch_entry = tk.Entry(self.center_frame, bg=entry_bg)
        self.branch_entry.pack(pady=5)

        tk.Label(self.center_frame, text="IFSC Code", bg=label_bg).pack(pady=5)
        self.ifsc_entry = tk.Entry(self.center_frame, bg=entry_bg)
        self.ifsc_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Initial Balance", bg=label_bg).pack(pady=5)
        self.balance_entry = tk.Entry(self.center_frame, bg=entry_bg)
        self.balance_entry.pack(pady=5)

        tk.Button(self.center_frame, text="Create Account", bg=button_bg, fg=button_fg, command=self.create_account).pack(pady=10)

        # Section for operations
        self.operation_frame = tk.LabelFrame(self.center_frame, text="Account Operations", bg=frame_bg)
        self.operation_frame.pack(pady=20, fill="both", expand=True)

        tk.Label(self.operation_frame, text="Select Account", bg=frame_bg).grid(row=0, column=0, padx=5, pady=5)
        self.selected_account = tk.StringVar(self.operation_frame)
        self.selected_account.set("Select Account")
        self.account_menu = tk.OptionMenu(self.operation_frame, self.selected_account, "Select Account")
        self.account_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.operation_frame, text="Deposit", bg=button_bg, fg=button_fg, command=self.deposit).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self.operation_frame, text="Withdraw", bg=button_bg, fg=button_fg, command=self.withdraw).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.operation_frame, text="Transfer", bg=button_bg, fg=button_fg, command=self.transfer).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(self.operation_frame, text="Display Details", bg=button_bg, fg=button_fg, command=self.display_details).grid(row=1, column=3, padx=5, pady=5)
        tk.Button(self.operation_frame, text="Display All Accounts", bg=button_bg, fg=button_fg, command=self.display_all_accounts).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self.operation_frame, text="Delete Account", bg="#f44336", fg=button_fg, command=self.delete_account).grid(row=2, column=2, columnspan=2, padx=5, pady=5)

    def create_account(self):
        acc_name = self.acc_name_entry.get()
        branch = self.branch_entry.get()
        ifsc_code = self.ifsc_entry.get()
        balance = self.balance_entry.get()

        try:
            balance = float(balance)
            account = Bank(acc_name, branch, ifsc_code, balance)
            self.accounts.append(account)
            self.update_account_menu()
            messagebox.showinfo("Success", "Account created successfully!")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Invalid balance amount")

    def update_account_menu(self):
        self.account_menu["menu"].delete(0, "end")
        for index, account in enumerate(self.accounts):
            self.account_menu["menu"].add_command(label=f"{index + 1} - {account.acc_name}",
                                                  command=lambda value=f"{index + 1} - {account.acc_name}": self.selected_account.set(value))

    def get_selected_account(self):
        selected = self.selected_account.get()
        if selected == "Select Account":
            messagebox.showerror("Error", "No account selected")
            return None
        account_index = int(selected.split(" - ")[0]) - 1
        return self.accounts[account_index], account_index

    def deposit(self):
        account, _ = self.get_selected_account()
        if account:
            amount = self.get_amount("Deposit Amount")
            if amount is not None:
                result = account.deposit(amount)
                messagebox.showinfo("Deposit", result)

    def withdraw(self):
        account, _ = self.get_selected_account()
        if account:
            amount = self.get_amount("Withdraw Amount")
            if amount is not None:
                result = account.withdraw(amount)
                messagebox.showinfo("Withdraw", result)

    def transfer(self):
        sender_account, _ = self.get_selected_account()
        if sender_account:
            transfer_to = simpledialog.askinteger("Transfer", f"Enter recipient account number (1 to {len(self.accounts)})", parent=self.root)
            if transfer_to is None or transfer_to < 1 or transfer_to > len(self.accounts) or transfer_to == int(self.selected_account.get().split(" - ")[0]):
                messagebox.showerror("Error", "Invalid recipient account number")
                return
            recipient_account = self.accounts[transfer_to - 1]
            amount = self.get_amount("Transfer Amount")
            if amount is not None:
                result = sender_account.transfer(amount, recipient_account)
                messagebox.showinfo("Transfer", result)

    def display_details(self):
        account, _ = self.get_selected_account()
        if account:
            details = account.display_details()
            messagebox.showinfo("Account Details", details)

    def display_all_accounts(self):
        if not self.accounts:
            messagebox.showinfo("No Accounts", "No accounts have been created yet.")
        else:
            all_accounts_info = "\n\n".join([f"Account {index + 1}:\n{account.display_details()}" for index, account in enumerate(self.accounts)])
            messagebox.showinfo("All Accounts", all_accounts_info)

    def delete_account(self):
        account, account_index = self.get_selected_account()
        if account:
            confirmation = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete account: {account.acc_name}?")
            if confirmation:
                del self.accounts[account_index]
                self.update_account_menu()
                self.selected_account.set("Select Account")
                messagebox.showinfo("Delete Account", "Account deleted successfully!")

    def get_amount(self, prompt):
        amount_str = simpledialog.askstring("Input", prompt, parent=self.root)
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
            return amount
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount")
            return None

    def clear_entries(self):
        self.acc_name_entry.delete(0, tk.END)
        self.branch_entry.delete(0, tk.END)
        self.ifsc_entry.delete(0, tk.END)
        self.balance_entry.delete(0, tk.END)

# Main application execution
if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
