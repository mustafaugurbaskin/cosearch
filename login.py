import customtkinter as ctk
import tkinter as tk
import mysql.connector
import pickle

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x250")

        self.email_label = ctk.CTkLabel(self.root, text="Email:")
        self.email_label.pack()

        self.email_entry = ctk.CTkEntry(self.root)
        self.email_entry.pack()

        self.api_key_label = ctk.CTkLabel(self.root, text="API Key:")
        self.api_key_label.pack()

        self.api_key_entry = ctk.CTkEntry(self.root, show="*")
        self.api_key_entry.pack()

        self.secret_key_label = ctk.CTkLabel(self.root, text="Secret Key:")
        self.secret_key_label.pack()

        self.secret_key_entry = ctk.CTkEntry(self.root, show="*")
        self.secret_key_entry.pack()

        self.remember_var = tk.BooleanVar()
        self.remember_checkbox = ctk.CTkCheckBox(self.root, text="Remember Me", variable=self.remember_var)
        self.remember_checkbox.pack()

        self.login_button = ctk.CTkButton(self.root, text="Login", command=self.login_button_clicked)
        self.login_button.pack()

        self.error_label = ctk.CTkLabel(self.root, text="")
        self.error_label.pack()

        self.load_saved_credentials()

    def login_button_clicked(self):
        email = self.email_entry.get()
        api_key = self.api_key_entry.get()
        secret_key = self.secret_key_entry.get()

        if self.authenticate(email, api_key, secret_key):
            user_data = self.fetch_user_data(email)
            if user_data:
                first_name = user_data["first_name"]
                last_name = user_data["last_name"]
                user_email = user_data["email"]
                self.error_label.configure(text=f"Welcome, {first_name} {last_name} {user_email}", text_color="green")
            else:
                self.error_label.configure(text="Login successful", text_color="green")

            if self.remember_var.get():
                self.save_credentials(email, api_key, secret_key)
        else:
            self.error_label.configure(text="Invalid credentials", text_color="red")

    def fetch_user_data(self, email):
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "cosearch_users"
        }

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT first_name, last_name, email FROM cosearch_users WHERE email = %s"
            values = (email,)
            cursor.execute(query, values)
            user_data = cursor.fetchone()

            cursor.close()
            connection.close()

            return user_data

        except mysql.connector.Error as err:
            print("Error:", err)
            return None

    def authenticate(self, email, api_key, secret_key):
        # Replace these credentials with your MySQL database credentials
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "cosearch_users"
        }

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            query = "SELECT * FROM cosearch_users WHERE email = %s AND api_key = %s AND secret_key = %s"
            values = (email, api_key, secret_key)
            cursor.execute(query, values)
            user_data = cursor.fetchone()

            cursor.close()
            connection.close()

            return user_data is not None

        except mysql.connector.Error as err:
            print("Error:", err)
            return False

    def save_credentials(self, email, api_key, secret_key):
        credentials = {"email": email, "api_key": api_key, "secret_key": secret_key}
        with open("credentials.pkl", "wb") as file:
            pickle.dump(credentials, file)

    def load_saved_credentials(self):
        try:
            with open("credentials.pkl", "rb") as file:
                credentials = pickle.load(file)
                self.email_entry.insert(0, credentials["email"])
                self.api_key_entry.insert(0, credentials["api_key"])
                self.secret_key_entry.insert(0, credentials["secret_key"])
                self.remember_var.set(True)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    login_form = LoginForm(root)
    root.mainloop()
