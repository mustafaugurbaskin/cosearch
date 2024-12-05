import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import customtkinter
import os
import sys
from PIL import Image, ImageTk, ImageSequence
import re
import requests
import time
import xlsxwriter
import threading
import mysql.connector
import pickle
import webbrowser

class CheckUpdates:
    def __init__(self, root):
        self.root = root
        self.version = 'v1.0'
        self.root.title("Checking updates")
        self.root.geometry("400x400")  # Increased window height to accommodate the GIF

        # CoSearch logo
        self.logo = customtkinter.CTkImage(
            light_image=Image.open("logo/CoSearch-logo-small-2.png"),
            dark_image=Image.open("logo/CoSearch-logo-small-4.png"), size=(240, 60))

        # Login text
        self.login_text = "Checking updates..."
        self.login_label = customtkinter.CTkLabel(self.root, text=self.login_text, image=self.logo, compound="top",
                                                  font=("Segoe UI", 16))
        self.login_label.pack(pady=(90, 10))  # Adjusted pady to create some space between the label and GIF

        # Animated GIF
        self.gif_frames = []
        self.load_gif_frames("icons/loading-spinner.gif", self.gif_frames)
        self.current_frame = 0
        self.gif_label = tk.Label(self.root, image=self.gif_frames[0])
        self.gif_label.pack()
        self.animate_gif()

        # Check for updates
        self.check_version()

    def load_gif_frames(self, filename, frames):
        try:
            gif = Image.open(filename)
            for frame in ImageSequence.Iterator(gif):
                frame = frame.convert("RGBA")
                photo = ImageTk.PhotoImage(frame)
                frames.append(photo)
        except Exception as e:
            print("Error loading GIF frames:", e)

    def animate_gif(self):
        if len(self.gif_frames) > 1 and self.gif_label.winfo_exists():
            self.current_frame += 1
            if self.current_frame >= len(self.gif_frames):
                self.current_frame = 0
            self.gif_label.configure(image=self.gif_frames[self.current_frame])
            self.root.after(100, self.animate_gif)

    def destroy_gif(self):
        self.gif_label.destroy()  # Destroy the GIF label widget

    def check_version(self):

        try:
            # Connect to the update server, check version names
            self.update_url = f"https://www.cosearchteam.com/app/update_app"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
            }
            params_for_update = {'version': str(self.version), 'timestamp': str(int(time.time()))}
            response = requests.get(self.update_url, params=params_for_update, headers=headers)  # Send a GET request to the URL
            if response.status_code == 200:
                latest_version = response.text.strip()
                if str(self.version) == str(latest_version):
                    
                    # Destroy loading spinner
                    self.destroy_gif()

                    # Call login form
                    self.login_label.configure(text="You are up-to-date.")

                    # Call the start_login_form method
                    self.start_login_form()

                else:
                    # Destroy loading spinner
                    self.destroy_gif()

                    # Update text
                    self.login_label.configure(text="An update found.\nTo download the update please go to:")
                    
                    # Dashboard link
                    self.dashboard_link = "www.cosearchteam.com/dashboard/download"
                    self.link_label = customtkinter.CTkLabel(self.root, text=self.dashboard_link, cursor="hand2", text_color="blue", font=("Segoe UI", 16))
                    self.link_label.pack(pady=(0, 30))
                    self.link_label.bind("<Button-1>", self.open_dashboard)
            else:
                raise ConnectionError
                
        except AttributeError:
            pass

        except ConnectionError:
            # Show a message due to authentication error
            messagebox.showerror("Connection Error", "There was an error while connecting to the server. Please check your connection.")
            return False
        
    def open_dashboard(self, event):
        webbrowser.open_new("https://www.cosearchteam.com/dashboard/login?redirect=download")

    def start_login_form(self):

        # Close check update and start Login form
        self.root.destroy()

        root = tk.Tk()
        login_form = LoginForm(root)
        login_form.mainloop()

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("500x600")
        self.logged_in = False

        # CoSearch logo
        self.logo = tk.PhotoImage(file="logo/CoSearch-logo-small-2.png")
        self.resized_logo = self.logo.subsample(2)  # Adjust the value as needed
        self.logo_label = customtkinter.CTkLabel(self.root, text="", image=self.resized_logo)
        self.logo_label.pack(pady=60)

        # Login text
        self.login_text = "Login to your CoSearch account.\nFind out your API Key and Secret key at"
        self.dashboard_link = "www.cosearchteam.com/dashboard"
        self.login_label = customtkinter.CTkLabel(self.root, text=self.login_text, font=("Segoe UI", 16))
        self.login_label.pack()

        # Dashboard link
        self.link_label = customtkinter.CTkLabel(self.root, text=self.dashboard_link, cursor="hand2", text_color="blue", font=("Segoe UI", 16))
        self.link_label.pack()
        self.link_label.bind("<Button-1>", self.open_dashboard)

        # Email
        self.email_label = customtkinter.CTkLabel(self.root, text="Email:")
        self.email_label.pack(pady=(20, 0))

        self.email_entry = customtkinter.CTkEntry(self.root)
        self.email_entry.pack()

        # API Key
        self.api_key_label = customtkinter.CTkLabel(self.root, text="API Key:")
        self.api_key_label.pack()

        self.api_key_entry = customtkinter.CTkEntry(self.root, show="*")
        self.api_key_entry.pack()

        # Secret Key
        self.secret_key_label = customtkinter.CTkLabel(self.root, text="Secret Key:")
        self.secret_key_label.pack()

        self.secret_key_entry = customtkinter.CTkEntry(self.root, show="*")
        self.secret_key_entry.pack()

        # Remember Me Checkbox
        self.remember_var = tk.BooleanVar()
        self.remember_checkbox = customtkinter.CTkCheckBox(self.root, text="Remember Me", variable=self.remember_var)
        self.remember_checkbox.pack(pady=(20, 20))

        # Login Button
        self.login_button = customtkinter.CTkButton(self.root, text="Login", command=self.login_button_clicked)
        self.login_button.pack()

        # Error Label
        self.error_label = customtkinter.CTkLabel(self.root, text="")
        self.error_label.pack()

        self.load_saved_credentials()

    def open_dashboard(self, event):
        webbrowser.open_new("http://" + self.dashboard_link)

    def login_button_clicked(self):
        email = self.email_entry.get()
        api_key = self.api_key_entry.get()
        secret_key = self.secret_key_entry.get()

        # API anahtarlarını ve e-posta adresini doğrula
        self.auth_url = f"https://cosearchteam.com/auth?e-mail={email}&API_KEY={api_key}&SECRET_KEY={secret_key}&login_fetch=1"
        
        try:
            response = requests.get(self.auth_url)

            if response.status_code == 200:
                # Yanıtı işle
                user_data = response.json()

                if user_data:
                    first_name = user_data["first_name"]
                    last_name = user_data["last_name"]
                    user_email = user_data["email"]
                    paid_status = int(user_data["paid"])
                    demo_status = int(user_data["demo"])
                    subscription_status = int(user_data["subscription"])

                    if paid_status == 0 or subscription_status == 0:
                        if demo_status == 1:
                            self.error_label.configure(text=f"Welcome, {first_name} {last_name} {user_email}", text_color="green")
                            self.logged_in = True
                            self.check_login_status(user_email)
                        else:
                            self.error_label.configure(text=f"{first_name} {last_name}, you might not have a plan or your current plan might have expired.\nPlease choose a plan at https://cosearchteam.com/dashboard.", text_color="red")
                            self.logged_in = False
                            self.check_login_status(user_email)
                    else:
                        self.error_label.configure(text=f"Welcome, {first_name} {last_name} {user_email}", text_color="green")
                        self.logged_in = True
                        self.check_login_status(user_email)
                else:
                    self.error_label.configure(text="Login successful", text_color="green")

                if self.remember_var.get():
                    self.save_credentials(email, api_key, secret_key)
            else:
                self.error_label.configure(text="Invalid credentials", text_color="red")
        except requests.exceptions.RequestException as e:
            self.error_label.configure(text="An error occurred while connecting to the server. Please check your internet connection.", text_color="red")

    def check_login_status(self, email):
        if self.logged_in == True:

            # Destroy login form
            self.root.destroy()

            # Get credentials
            creds = self.fetch_user_data(email)
            email = creds["email"]
            api_key = creds["api_key"]
            secret_key = creds["secret_key"]

            # Start main app with credentials
            app = App(email, api_key, secret_key)
            app.mainloop()
        else:
            pass

    def fetch_user_data(self, email):
        try:
            response = requests.get(self.auth_url)
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            else:
                return None
        except requests.exceptions.RequestException as e:
            return None

    def save_credentials(self, email, api_key, secret_key):
        directory = os.getcwd()
        credentials = {"email": email, "api_key": api_key, "secret_key": secret_key}
        with open(f"{str(directory)}\\credentials.pkl", "wb") as file:
            pickle.dump(credentials, file)

    def load_saved_credentials(self):
        directory = os.getcwd()
        try:
            with open(f"{str(directory)}\\credentials.pkl", "rb") as file:
                credentials = pickle.load(file)
                self.email_entry.insert(0, credentials["email"])
                self.api_key_entry.insert(0, credentials["api_key"])
                self.secret_key_entry.insert(0, credentials["secret_key"])
                self.remember_var.set(True)
        except FileNotFoundError:
            pass

class ConsoleRedirector:
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, message):
        self.textbox.insert("end", message)
        self.textbox.see("end")  # Scroll to the end of the textbox

class App(tk.Tk):
    def __init__(self, e_mail, api_key, secret_key):
        super().__init__()
        self.e_mail = e_mail
        self.api_key = api_key
        self.secret_key = secret_key
        
        self.edit_user_data()

        self.title("CoSearch")
        self.geometry("1280x720")

        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        if customtkinter.set_appearance_mode("System") == None:
            if customtkinter.get_appearance_mode() == "Light":
                self.configure(bg="#dbdbdb")
            else:
                self.configure(bg="#2b2b2b")
        if customtkinter.set_appearance_mode == "Light":
            self.configure(bg="#dbdbdb")
        if customtkinter.set_appearance_mode == "Dark":
            self.configure(bg="#2b2b2b")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.logo_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/search-icon-light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "icons/search-icon-dark.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "a.png")), size=(500, 150))
        self.upload_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/upload-icon-light.png")), 
                                                        dark_image=Image.open(os.path.join(image_path, "icons/upload-icon-dark.png")), size=(30, 30))
        self.how_to_use_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/question-mark-light.png")),
                                                       dark_image=Image.open(os.path.join(image_path, "icons/question-mark-dark.png")), size=(30, 30))
        self.trash_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/trash-icon-light.png")), 
                                                       dark_image=Image.open(os.path.join(image_path, "icons/trash-icon-dark.png")), size=(30, 30))
        self.x_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/x-icon-light.png")), 
                                                       dark_image=Image.open(os.path.join(image_path, "icons/x-icon-dark.png")), size=(30, 30))
        self.search_icon_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/search-icon-light.png")), 
                                                        dark_image=Image.open(os.path.join(image_path, "icons/search-icon-dark.png")), size=(30, 30))
        self.my_account_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/my-account-light.png")), 
                                                        dark_image=Image.open(os.path.join(image_path, "icons/my-account-dark.png")), size=(30, 30))
        self.contact_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "icons/contact-light.png")), 
                                                        dark_image=Image.open(os.path.join(image_path, "icons/contact-dark.png")), size=(30, 30))
        self.search_button_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "icons/search-icon-light.png")), size=(30, 30))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "a.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "a.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "a.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "a.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "a.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "a.png")), size=(20, 20))
        self.use_image_1 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "imgs/use-1-light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "imgs/use-1-dark.png")), size=(550, 140))
        self.use_image_2 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "imgs/use-2-light.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "imgs/use-2-dark.png")), size=(550, 140))
        self.use_image_3 = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "imgs/use-3-light.png")),
                                                            dark_image=Image.open(os.path.join(image_path, "imgs/use-3-dark.png")), size=(550, 140))

        # Navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(8, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, height=80, text=" | CoSearch", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(family="Segoe UI", size=24, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, sticky="ew")

        self.how_to_use_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="How To Use",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.how_to_use_image, anchor="w", command=self.frame_3_button_event)
        self.how_to_use_button.grid(row=1, column=0, sticky="ew")

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Bulk Business Information Finder",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.search_icon_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=2, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Single Business Information Finder",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.search_icon_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=3, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="My Account",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.my_account_image, anchor="w", command=self.frame_4_button_event)
        self.frame_3_button.grid(row=4, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Contact",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.contact_image, anchor="w", command=self.frame_5_button_event)
        self.frame_4_button.grid(row=5, column=0, sticky="ew")

        self.appearence_mode_label = customtkinter.CTkLabel(self.navigation_frame, height=50, text="Appearance Mode:",
                                                     anchor="w", font=customtkinter.CTkFont(family="Segoe UI", size=15))
        self.appearence_mode_label.grid(row=9, column=0)
        
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, width=150, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, pady=(0, 25))

        # create how to use frame
        self.how_to_use_frame = customtkinter.CTkFrame(self, corner_radius=0)

        self.how_to_use_label = customtkinter.CTkLabel(self.how_to_use_frame, text="How to use CoSearch?", font=customtkinter.CTkFont(family="Segoe UI", size=36, weight="bold"))
        self.how_to_use_label.place(x=20, y=20)

        self.use_info_label = customtkinter.CTkLabel(self.how_to_use_frame, text="Learn how to use CoSearch more accurately.", font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.use_info_label.place(x=20, y=70)

        self.info1_headers = customtkinter.CTkLabel(self.how_to_use_frame, text="Use the full names\nof businesses.", font=customtkinter.CTkFont(family="Segoe UI", size=22, weight="bold"), justify="left")
        self.info1_headers.place(x=20, y=140)

        self.info1_text = customtkinter.CTkLabel(self.how_to_use_frame, text="Instead of using XXXXX Co.,\nuse the full name of the business.\nSuch as XXXXX Technologies Corporation.",
                                                 font=customtkinter.CTkFont(family="Segoe UI", size=16), justify="left")
        self.info1_text.place(x=20, y=210)

        self.info2_headers = customtkinter.CTkLabel(self.how_to_use_frame, text="Specify the location of\nthe businesses.", font=customtkinter.CTkFont(family="Segoe UI", size=22, weight="bold"), justify="left")
        self.info2_headers.place(x=20, y=300)

        self.info2_text = customtkinter.CTkLabel(self.how_to_use_frame, text="If a business has a location more than\none place, specifying the location of the business\nwill be helpful for you to get accurate results.",
                                                 font=customtkinter.CTkFont(family="Segoe UI", size=16), justify="left")
        self.info2_text.place(x=20, y=370)

        self.info3_headers = customtkinter.CTkLabel(self.how_to_use_frame, text="Avoid typos and\nmisspellings.", font=customtkinter.CTkFont(family="Segoe UI", size=22, weight="bold"), justify="left")
        self.info3_headers.place(x=20, y=460)

        self.info3_text = customtkinter.CTkLabel(self.how_to_use_frame, text="By double-checking and verify the spelling\nof business names before initiating a\nsearch, users can enhance the precision\nand reliability of the results\ngenerated by CoSearch.",
                                                 font=customtkinter.CTkFont(family="Segoe UI", size=16), justify="left")
        self.info3_text.place(x=20, y=530)

        self.use_img_1 = customtkinter.CTkLabel(self.how_to_use_frame, text="", image=self.use_image_1)
        self.use_img_1.place(x=410, y=140)

        self.use_img_2 = customtkinter.CTkLabel(self.how_to_use_frame, text="", image=self.use_image_2)
        self.use_img_2.place(x=410, y=300)

        self.use_img_3 = customtkinter.CTkLabel(self.how_to_use_frame, text="", image=self.use_image_3)
        self.use_img_3.place(x=410, y=460)

        # create bulk search frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.home_frame.grid_columnconfigure(0, weight=1)

        #self.dashboard_frame = customtkinter.CTkFrame(self.home_frame)
        #self.dashboard_frame.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_label = customtkinter.CTkLabel(self.home_frame, text="Find Bulk Business Information", font=customtkinter.CTkFont(family="Segoe UI", size=36, weight="bold"))
        self.dashboard_label.place(x=20, y=20)

        self.dashboard_info_label = customtkinter.CTkLabel(self.home_frame, text="With this application, you can find the information of businesses in the uploaded .txt document in a bulk manner.\nThe information will be saved to an Excel file.", font=customtkinter.CTkFont(family="Segoe UI", size=16), justify="left")
        self.dashboard_info_label.place(x=20, y=70)

        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Upload File", font=customtkinter.CTkFont(family="Segoe UI", size=16), fg_color="orange", text_color="black", hover_color="#CC5500", image=self.upload_icon_image, command=self.upload_files_clicked, compound="right")
        self.home_frame_button_2.place(x=20, y=120)

        self.home_frame_button_5 = customtkinter.CTkButton(self.home_frame, text="Clear The Screen", font=customtkinter.CTkFont(family="Segoe UI", size=16), image=self.trash_icon_image, command=self.clearTextBox, compound="right")
        self.home_frame_button_5.place(x=20, y=170)

        self.home_frame_button_6 = customtkinter.CTkButton(self.home_frame, text="Stop Searching", font=customtkinter.CTkFont(family="Segoe UI", size=16), image=self.x_icon_image, command=self.bulkStopSearching, compound="right")
        self.home_frame_button_6.place(x=200, y=170)

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self.home_frame, width=700, height=470, font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.textbox.place(x=20, y=220)

        # create single search frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0)

        self.second_frame_label = customtkinter.CTkLabel(self.second_frame, text="Find Single Business Information", font=customtkinter.CTkFont(family="Segoe UI", size=36, weight="bold"))
        self.second_frame_label.place(x=20, y=20)

        self.dashboard_info_label = customtkinter.CTkLabel(self.second_frame, text="With this application, you can find the information of a single business.", font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.dashboard_info_label.place(x=20, y=70)

        # create business textbox
        self.business_textbox = customtkinter.CTkTextbox(self.second_frame, width=400, height=50, font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.business_textbox.place(x=20, y=110)
        
        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="Search", font=customtkinter.CTkFont(family="Segoe UI", size=16), fg_color="orange", text_color="black", hover_color="#CC5500", image=self.search_button_icon_image, command=lambda: self.do_search_clicked(self.business_textbox.get('1.0', 'end')), compound="right")
        self.second_frame_button_1.place(x=430, y=115)

        self.second_frame_button_2 = customtkinter.CTkButton(self.second_frame, text="Clear The Screen", font=customtkinter.CTkFont(family="Segoe UI", size=16), image=self.trash_icon_image, command=self.clearTextBox2, compound="right")
        self.second_frame_button_2.place(x=20, y=170)

        self.second_frame_button_3 = customtkinter.CTkButton(self.second_frame, text="Stop Searching", font=customtkinter.CTkFont(family="Segoe UI", size=16), image=self.x_icon_image, command=self.stopSearching, compound="right")
        self.second_frame_button_3.place(x=200, y=170)

        # create textbox
        self.textbox_2 = customtkinter.CTkTextbox(self.second_frame, width=700, height=470, font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.textbox_2.place(x=20, y=220)

        # create my account frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0)

        self.third_frame_label = customtkinter.CTkLabel(self.third_frame, text="My CoSearch Account", font=customtkinter.CTkFont(family="Segoe UI", size=36, weight="bold"))
        self.third_frame_label.place(x=20, y=20)

        self.third_frame_description = customtkinter.CTkLabel(self.third_frame, text="Explore your acount details, usages, view your current plan details, and find out your upcoming billing date.", font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.third_frame_description.place(x=20, y=70)

        self.third_frame_user_fullname_email_welcome = customtkinter.CTkLabel(self.third_frame, text=f"Welcome, ", font=customtkinter.CTkFont(family="Segoe UI", size=24))
        self.third_frame_user_fullname_email_welcome.place(x=20, y=120)

        self.third_frame_user_fullname_email = customtkinter.CTkLabel(self.third_frame, text=f"{self.first_name} {self.last_name} ({self.user_email})", font=customtkinter.CTkFont(family="Segoe UI", size=24, weight="bold"))
        self.third_frame_user_fullname_email.place(x=130, y=120)

        self.third_frame_user_company_name = customtkinter.CTkLabel(self.third_frame, text=f"{self.user_company_name}", font=customtkinter.CTkFont(family="Segoe UI", size=22))
        self.third_frame_user_company_name.place(x=20, y=150)

        self.logout_button = customtkinter.CTkButton(self.third_frame, width=100, height=30, text=f"Logout", font=customtkinter.CTkFont(family="Segoe UI", size=22), command=self.logout, fg_color="#5d87ff", text_color="white")
        self.logout_button.place(x=20, y=190)

        self.account_details_label = customtkinter.CTkLabel(self.third_frame, text="Your Account Details:", font=customtkinter.CTkFont(family="Segoe UI", size=28, weight="bold"))
        self.account_details_label.place(x=20, y=270)

        self.third_frame_current_plan = customtkinter.CTkButton(self.third_frame, width=250, height=100, text=f"Your current plan:\n{self.user_plan_name}", font=customtkinter.CTkFont(family="Segoe UI", size=24), fg_color="#5d87ff", text_color="white", hover_color="#5d87ff")
        self.third_frame_current_plan.place(x=20, y=320)

        self.third_frame_next_billing_date = customtkinter.CTkButton(self.third_frame, width=250, height=100, text=f"Next billing date:\n{self.user_next_billing_date}", font=customtkinter.CTkFont(family="Segoe UI", size=24), fg_color="#5d87ff", text_color="white", hover_color="#5d87ff")
        self.third_frame_next_billing_date.place(x=280, y=320)

        self.third_frame_credits_usage = customtkinter.CTkButton(self.third_frame, width=250, height=100, text=f"Search credit usage:\n{self.user_usages}/{self.user_credits}", font=customtkinter.CTkFont(family="Segoe UI", size=24), fg_color="#5d87ff", text_color="white", hover_color="#5d87ff")
        self.third_frame_credits_usage.place(x=540, y=320)

        self.more_information_label = customtkinter.CTkLabel(self.third_frame, text="For more information and settings about your CoSearch account, visit:", font=customtkinter.CTkFont(family="Segoe UI", size=28, weight="bold"))
        self.more_information_label.place(x=20, y=470)

        def callback(url):
           webbrowser.open_new_tab(url)

        self.more_information_website_label = tk.Label(self.third_frame, text="Visit CoSearch Dashboard",font="SegoeUI 18 underline", fg="blue", bg="#dbdbdb", cursor="hand2")
        self.more_information_website_label.place(x=20, y=510)
        if self.user_demo == "1":
            self.more_information_website_label.bind("<Button-1>", lambda e: callback("https://cosearchteam.com/pricing"))
        else:
            self.more_information_website_label.bind("<Button-1>", lambda e: callback("https://cosearchteam.com/dashboard"))

        # create contact frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0)

        self.fourth_frame_label = customtkinter.CTkLabel(self.fourth_frame, text="Contact Us", font=customtkinter.CTkFont(family="Segoe UI", size=36, weight="bold"))
        self.fourth_frame_label.place(x=20, y=20)

        self.fourth_frame_description = customtkinter.CTkLabel(self.fourth_frame, text="Get in touch with our team for any questions or assistance you may need.", font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.fourth_frame_description.place(x=20, y=70)

        self.contact_us_label_1 = customtkinter.CTkLabel(self.fourth_frame, text="Our support team is here to help with any inquiries you might have. Don't hesitate to", font=customtkinter.CTkFont(family="Segoe UI", size=24))
        self.contact_us_label_1.place(x=20, y=120)

        self.contact_us_label_2 = customtkinter.CTkLabel(self.fourth_frame, text="get in touch. You can reach us at our dedicated email address for customer inquiries:", font=customtkinter.CTkFont(family="Segoe UI", size=24))
        self.contact_us_label_2.place(x=20, y=160)

        self.contact_us_label_3 = tk.Label(self.fourth_frame, text="technical-support@cosearchteam.com",font="SegoeUI 18 underline", fg="blue", bg="#dbdbdb", cursor="hand2")
        self.contact_us_label_3.place(x=20, y=210)
        self.contact_us_label_3.bind("<Button-1>", lambda e:
        callback(f"mailto:technical-support@cosearchteam.com?subject=Technical Support Request from CoSearch App&body=Please write your inquiry for Inquiry section:%0D%0A%0D%0AInquiry:%0D%0A%0D%0ACustomer Information (Please do not change the information below):%0D%0AEmail: {self.user_email}%0D%0APhone Number: {self.user_phone_number}%0D%0ACompany Name: {self.user_company_name}%0D%0APlan: {self.user_plan_name}%0D%0AUsages: {self.user_usages}%0D%0ACredits: {self.user_credits}"))

        self.contact_us_label_4 = customtkinter.CTkLabel(self.fourth_frame, text="Are there any other questions you have? You can ask us these questions at the email", font=customtkinter.CTkFont(family="Segoe UI", size=24))
        self.contact_us_label_4.place(x=20, y=300)

        self.contact_us_label_5 = customtkinter.CTkLabel(self.fourth_frame, text="address below:", font=customtkinter.CTkFont(family="Segoe UI", size=24))
        self.contact_us_label_5.place(x=20, y=340)

        self.contact_us_label_6 = tk.Label(self.fourth_frame, text="other-inquiries@cosearchteam.com",font="SegoeUI 18 underline", fg="blue", bg="#dbdbdb", cursor="hand2")
        self.contact_us_label_6.place(x=20, y=390)
        self.contact_us_label_6.bind("<Button-1>", lambda e:
        callback(f"mailto:other-inquiries@cosearchteam.com?subject=Other Inquiries from CoSearch App&body=Please write your inquiry for Inquiry section:%0D%0A%0D%0AInquiry:%0D%0A%0D%0ACustomer Information (Please do not change the informatione below):%0D%0AEmail: {self.user_email}%0D%0APhone Number: {self.user_phone_number}%0D%0ACompany Name: {self.user_company_name}%0D%0APlan: {self.user_plan_name}%0D%0AUsages: {self.user_usages}%0D%0ACredits: {self.user_credits}"))

        self.contact_us_label_7 = customtkinter.CTkLabel(self.fourth_frame, text="CoSearch has no association with Microsoft Corporation, Bing, Bing Search, or Bing Search API.", font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.contact_us_label_7.place(x=20, y=650)

        self.contact_us_label_7 = customtkinter.CTkLabel(self.fourth_frame, text="Copyright © 2023 - CoSearch. All rights reserved.", font=customtkinter.CTkFont(family="Segoe UI", size=16))
        self.contact_us_label_7.place(x=20, y=675)

        # select default frame
        self.select_frame_by_name("home")

    def authenticate(self, email, api_key, secret_key):
        try:

            # API anahtarlarını ve e-posta adresini doğrula
            self.auth_url = f"https://cosearchteam.com/auth?e-mail={email}&API_KEY={api_key}&SECRET_KEY={secret_key}&app_fetch=1"

            # Get user's data          
            response = requests.get(self.auth_url)

            if response.status_code == 200:
                # Yanıtı işle
                user_data = response.json()

                return user_data
            else:
                raise ConnectionError
        except Exception:
            # Show a message due to authentication error
            messagebox.showerror("Connection Error", "There was an error while connecting to the server. Please check your connection.")
            return False
            
        
    """def fetch_user_data(self, email):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT first_name, last_name, company_name, phone_number, email, plan, paid, demo, subscription, usages, credits, signup_date, next_billing_date, bing_search_api_key FROM cosearch_users WHERE email = %s"
            values = (email,)
            cursor.execute(query, values)
            user_data = cursor.fetchone()

            cursor.close()
            connection.close()

            return user_data

        except mysql.connector.Error as err:
            print("Error:", err)
            return None"""
        
    def edit_user_data(self):

        # Edit user data
        if self.authenticate(self.e_mail, self.api_key, self.secret_key):

            # User credentials
            self.user_plan_name = "None"

            # Fetch user data
            user_data = self.authenticate(self.e_mail, self.api_key, self.secret_key)
            if user_data:
                self.first_name = user_data["first_name"]
                self.last_name = user_data["last_name"]
                self.user_email = user_data["email"]
                self.user_company_name = user_data["company_name"]
                self.user_phone_number = user_data["phone_number"]
                user_paid = user_data["paid"]
                self.user_demo = user_data["demo"]
                user_plan = user_data["plan"]
                user_subscription = user_data["subscription"]
                self.user_usages = user_data["usages"]
                self.user_credits = user_data["credits"]
                self.user_next_billing_date = user_data["next_billing_date"]
                self.bing_search_api_key = user_data["bing_search_api_key"]

                # Edit plan names, check paid, demo and subscription type then generate plan name
                # No subscription
                if user_paid == "0" or user_subscription == "0":
                    if self.user_demo == 0:
                        self.user_plan_name = "None"
                        self.destroy()
                    else:

                        # Demo version
                        if user_subscription == "3" and self.user_demo == "1" and user_paid == "0":
                            if user_plan == "0":
                                self.user_plan_name = "None"
                            elif user_plan == "5":
                                self.user_plan_name = "Demo"
                            else:
                                pass

                        else:
                            pass
                
                # Paid subscription
                else:
                    # Paid monthly subscription
                    if user_paid == "1" and user_subscription == "1":
                        user_plan_billing_type = "Monthly"
                        
                        if user_plan == "0":
                            self.user_plan_name = "None"
                        elif user_plan == "1":
                            self.user_plan_name = f"Basic ({user_plan_billing_type})"
                        elif user_plan == "2":
                            self.user_plan_name = f"Standard ({user_plan_billing_type})"
                        elif user_plan == "3":
                            self.user_plan_name = f"Professional ({user_plan_billing_type})"
                        elif user_plan == "4":
                            self.user_plan_name = f"Premium ({user_plan_billing_type})"
                        else:
                            pass

                    # Paid annually subscription
                    elif user_paid == "1" and user_subscription == "2":
                        user_plan_billing_type = "Annually"

                        if user_plan == "0":
                            self.user_plan_name = "None"
                        elif user_plan == "1":
                            self.user_plan_name = f"Basic ({user_plan_billing_type})"
                        elif user_plan == "2":
                            self.user_plan_name = f"Standard ({user_plan_billing_type})"
                        elif user_plan == "3":
                            self.user_plan_name = f"Professional ({user_plan_billing_type})"
                        elif user_plan == "4":
                            self.user_plan_name = f"Premium ({user_plan_billing_type})"
                        else:
                            pass


    def update_user_info_labels(self):
        self.third_frame_user_fullname_email.configure(
            text=f"{self.first_name} {self.last_name} ({self.user_email})"
        )
        self.third_frame_user_company_name.configure(text=self.user_company_name)
        self.third_frame_current_plan.configure(
            text=f"Your current plan:\n{self.user_plan_name}"
        )
        if self.user_demo == "1":
            self.third_frame_next_billing_date.configure(
                text=f"Demo ending date:\n{self.user_next_billing_date}"
            )
            self.more_information_label.configure(text="You are currently using the demo version of CoSearch.")
            self.more_information_label_2 = customtkinter.CTkLabel(self.third_frame, text="Would you like to upgrade your plan to further enhance your benefits with CoSearch?", font=customtkinter.CTkFont(family="Segoe UI", size=24, weight="bold"))
            self.more_information_label_2.place(x=20, y=520)
            
            self.more_information_website_label.configure(text="Show me the plans")
            self.more_information_website_label.place(x=20, y=570)
        else:
            self.third_frame_next_billing_date.configure(
                text=f"Next billing date:\n{self.user_next_billing_date}"
            )
        self.third_frame_credits_usage.configure(
            text=f"Search credit usage:\n{self.user_usages}/{self.user_credits}"
        )

    def update_user_usages(self):
        try:
            # Add a cache-busting parameter (timestamp) to the URL
            self.update_url = f"https://www.cosearchteam.com/auth"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            params_for_update = {'e-mail': str(self.user_email), 'API_KEY': self.api_key, 'SECRET_KEY': self.secret_key, 'app_update': 1, 'app_usages': self.user_usages, 'timestamp': str(int(time.time()))}
            response = requests.get(self.update_url, params=params_for_update, headers=headers)  # Send a GET request to the URL
            if response.status_code == 200:
                pass
            else:
                print("Failed to perform search. Please check your connection.")
                raise ConnectionError
        except Exception:
            # Show a message due to authentication error
            messagebox.showerror("Connection Error", "There was an error while connecting to the server. Please check your connection.")
            return False

    def logout(self):
        # Destroy the window
        self.destroy()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.how_to_use_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.how_to_use_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.how_to_use_frame.grid_forget()
        if name == "frame_4":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_5":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def home_button_event(self):
        self.edit_user_data()
        self.update_user_info_labels()
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.edit_user_data()
        self.update_user_info_labels()
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.edit_user_data()
        self.update_user_info_labels()
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.edit_user_data()
        self.update_user_info_labels()
        self.select_frame_by_name("frame_4")

    def frame_5_button_event(self):
        self.edit_user_data()
        self.update_user_info_labels()
        self.select_frame_by_name("frame_5")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        if new_appearance_mode == "System":
            if customtkinter.get_appearance_mode() == "Light":
                self.configure(bg="#dbdbdb")
            else:
                self.configure(bg="#2b2b2b")
        elif new_appearance_mode == "Light":
            self.configure(bg="#dbdbdb")
        elif new_appearance_mode == "Dark":
            self.configure(bg="#2b2b2b")

    # Define the button click event handlers
    def upload_files_clicked(self):
        self.edit_user_data()
        self.update_user_info_labels()
        user_usages = int(self.user_usages)
        user_credits = int(self.user_credits)
        if user_usages >= user_credits:
            messagebox.showerror("Limit Exceeded", "You have exceeded your monthly search limit.")
        else:
            self.home_frame_button_2.configure(state="disabled")
            self.second_frame_button_1.configure(state="disabled")
            self.UploadAction()

    def UploadAction(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", ".txt")])
        if not filename:
            self.home_frame_button_2.configure(state="normal")
            self.second_frame_button_1.configure(state="normal")
            self.home_frame_button_2.place_configure(width=140, height=40)  # Reset button size
            self.second_frame_button_1.place_configure(width=140, height=40)  # Reset button size
            return
        else:
            # Redirect sys.stdout to the custom ConsoleRedirector
            sys.stdout = ConsoleRedirector(self.textbox)
            print('Selected:', filename)
            thread = threading.Thread(target=self.searchForBulkBusinessInformation, args=(filename,))
            thread.start()

    def searchForBulkBusinessInformation(self, filename):
        self.filename = filename
        self.bulkstopsearch = 0
        self.counter1 = 1

        # Redirect sys.stdout to the custom ConsoleRedirector
        sys.stdout = ConsoleRedirector(self.textbox)

        # Create an new Excel file and add a worksheet.
        current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        workbook = xlsxwriter.Workbook(os.path.join(current_path, "List_Of_Businesses_Information.xlsx"))
        worksheet = workbook.add_worksheet()

        def do_search(businessname):
            deletephonenumbers = ['01234567890', '12345678910']
            deletepatterns = ['john.doe', 'johndoe', 'jane.doe', 'janedoe', 'j.doe', 'jdoe', 'info@rehberfx.com']
            # Separate the specific email address
            excluded_emails = ['info@rehberfx.com']

            query_data = response_query.json()

            website_url = query_data['webPages']['value'][0]['url']
            address = f"https://www.google.com/maps/search/{businessname}"

            # Get phone numbers
            try:
                phonenumbers = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', str(response_query.text))
            
                # Filter out the dates in YYYY-MM-DD format
                phonenumbers = [number for number in phonenumbers if not re.findall(r'20\d{2}-\d{2}-\d{2}', number)]

                # Remove duplicates by converting to a set and back to a list
                phonenumbers = list(set(phonenumbers))

                if len(phonenumbers) == 1:
                    for a in phonenumbers:
                        if a in deletephonenumbers:
                            phonenumbers = "Phone number not found."
            except:
                phonenumbers = "Phone number not found."
            
            # Check e-mail addresses
            email_addresses = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', str(response_query.text).lower())

            # Filter out email addresses based on patterns
            filtered_emails = [email for email in email_addresses if email.lower() not in excluded_emails and not any(pattern in email.split('@')[0] for pattern in deletepatterns)]
            
            # Remove duplicates by converting to a set and back to a list
            filtered_emails = list(set(filtered_emails))

            # Get LinkedIn profiles
            pattern = r'"name": "(.*?)",\s+"url": "(.*?)"'
            matches = re.findall(pattern, str(response_query_linkedin.text), re.DOTALL)

            # Filter out only LinkedIn profiles
            linkedin_profiles = []
            max_profiles = 5  # Set the maximum number of LinkedIn profiles you want

            for match in matches:
                title = match[0]
                link = match[1].replace('\\/', '/')
                if "linkedin.com/in/" in link:
                    linkedin_profiles.append(f"\t» LinkedIn Contacts: {title}\n\t» Link: {link}\n")
                    if len(linkedin_profiles) >= max_profiles:
                        break  # Stop collecting more profiles once the limit is reached

            print("\n------------------------------------------",
                f"\n{self.counter1}. Business name:", businessname,
                "\n⬤ Website:", website_url,
                "\n⬤ Phone numbers:", phonenumbers,
                "\n⬤ Address:", address,
                "\n⬤ E-mail accounts:", filtered_emails,
                f"\n⬤ LinkedIn accounts ({str(len(linkedin_profiles))} were found):")

            # Print LinkedIn profiles
            new_linkedin_profiles = []
            for profile in linkedin_profiles:
                new_linkedin_profiles.append(profile.replace('\n', '').replace('\t', ''))
                print(profile)

            print("\n------------------------------------------\n")

            # Write these results to a excel file
            worksheet.write(f'A{str(self.counter1)}', f'{str(businessname)}')
            worksheet.write(f'B{str(self.counter1)}', f'{str(website_url)}')
            worksheet.write(f'C{str(self.counter1)}', f'{str(phonenumbers)}')
            worksheet.write(f'D{str(self.counter1)}', f'{str(address)}')
            worksheet.write(f'E{str(self.counter1)}', f'{str(filtered_emails)}')
            worksheet.write(f'F{str(self.counter2)}', f'{str(new_linkedin_profiles)}')

        with open(self.filename, 'r', encoding="utf8") as businesses:
            # Check user usages, if exceeded, raise error
            self.length_of_list = 0
            self.length_of_list = sum(1 for line in businesses)
            new_usages = int(self.user_usages) + int(self.length_of_list)
            usages_left = int(self.user_credits) - int(self.user_usages)
            user_credits = int(self.user_credits)
            if new_usages > user_credits:
                # Show an error message and activate the buttons
                messagebox.showerror("Limit Exceeded", f"There are {self.length_of_list} business(es) in your list. You have {usages_left} search credit(s) left. Search cannot be performed.")
                self.home_frame_button_2.configure(state="normal")
                self.second_frame_button_1.configure(state="normal")
                self.home_frame_button_2.configure(width=140, height=40)
                self.second_frame_button_1.configure(width=140, height=40)
                workbook.close()
            else:
                # Update user usages
                self.user_usages = str(new_usages)
                self.update_user_usages()
                
                # Reset the loop
                businesses.seek(0)

                # Perform search
                for a in businesses:
                    # Construct a request
                    mkt = 'en-US'
                    params_for_query = { 'q': f'{str(a)} email phone number linkedin', 'mkt': mkt }
                    params_for_linkedin_query = { 'q': f'{str(a)} linkedin', 'mkt': mkt }
                    endpoint = 'https://api.bing.microsoft.com/v7.0/search'
                    headers = { 'Ocp-Apim-Subscription-Key': self.bing_search_api_key }

                    # Get business phone number and e-mail
                    response_query = requests.get(endpoint, headers=headers, params=params_for_query)
                    response_query.raise_for_status()

                    # Get business LinkedIn contacts
                    response_query_linkedin = requests.get(endpoint, headers=headers, params=params_for_linkedin_query)
                    response_query_linkedin.raise_for_status()

                    #response_query_address = requests.get(endpoint, headers=headers, params=params_for_query_address)
                    #response_query_address.raise_for_status()

                    if self.bulkstopsearch == 1:
                        # Redirect sys.stdout to the custom ConsoleRedirector
                        sys.stdout = ConsoleRedirector(self.textbox)
                        print("Search stopped.")
                        break
                    else:
                        a = a.replace('Â', '')
                        do_search(a)
                        self.counter1 += 1

                self.home_frame_button_2.configure(state="normal")
                self.second_frame_button_1.configure(state="normal")
                self.home_frame_button_2.configure(width=140, height=40)
                self.second_frame_button_1.configure(width=140, height=40)
                workbook.close()

    def do_search_clicked(self, businessname):
        self.edit_user_data()
        self.update_user_info_labels()
        user_usages = int(self.user_usages)
        user_credits = int(self.user_credits)
        if user_usages >= user_credits:
            messagebox.showerror("Limit Exceeded", "You have exceeded your monthly search limit.")
        else:
            self.home_frame_button_2.configure(state="disabled")
            self.second_frame_button_1.configure(state="disabled")
            user_usages += 1
            self.user_usages = str(user_usages)
            # Update the database with the new usage count
            self.update_user_usages()
            self.SearchAction(businessname)

    def SearchAction(self, businessname):
        if not businessname:
            self.home_frame_button_2.configure(state="normal")
            self.second_frame_button_1.configure(state="normal")
            self.second_frame_button_1.configure(width=140, height=40)
            self.home_frame_button_2.configure(width=140, height=40)
        else:
            # Redirect sys.stdout to the custom ConsoleRedirector
            sys.stdout = ConsoleRedirector(self.textbox_2)
            print('Searching:', businessname)
            thread = threading.Thread(target=self.searchForBusinessInformation, args=(businessname,))
            thread.start()

    def searchForBusinessInformation(self, filename):
            self.filename = filename.replace("\n", "")
            self.stopsearch = 0
            self.fullfilename = f"{self.filename}_Business_Information.xlsx"
            self.counter2 = 1

            # Create an new Excel file and add a worksheet.
            current_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
            workbook = xlsxwriter.Workbook(os.path.join(current_path, self.fullfilename))
            worksheet = workbook.add_worksheet()

            def do_search(businessname):

                # Construct a request
                mkt = 'en-US'
                params_for_query = { 'q': businessname, 'mkt': mkt }
                params_for_linkedin_query = { 'q': f"{str(businessname)} linkedin", 'mkt': mkt }
                endpoint = 'https://api.bing.microsoft.com/v7.0/search'
                headers = { 'Ocp-Apim-Subscription-Key': self.bing_search_api_key }

                # Get business phone number and e-mail
                response_query = requests.get(endpoint, headers=headers, params=params_for_query)
                response_query.raise_for_status()

                # Get business LinkedIn contacts
                response_query_linkedin = requests.get(endpoint, headers=headers, params=params_for_linkedin_query)
                response_query_linkedin.raise_for_status()

                deletephonenumbers = ['01234567890', '12345678910']
                deletepatterns = ['john.doe', 'johndoe', 'jane.doe', 'janedoe', 'j.doe', 'jdoe', 'info@rehberfx.com']
                # Separate the specific email address
                excluded_emails = ['info@rehberfx.com']

                query_data = response_query.json()

                website_url = query_data['webPages']['value'][0]['url']
                address = f"https://www.google.com/maps/search/{businessname}"

                # Get phone numbers
                try:
                    phonenumbers = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', str(response_query.text))
                
                    # Filter out the dates in YYYY-MM-DD format
                    phonenumbers = [number for number in phonenumbers if not re.findall(r'20\d{2}-\d{2}-\d{2}', number)]

                    # Remove duplicates by converting to a set and back to a list
                    phonenumbers = list(set(phonenumbers))

                    if len(phonenumbers) == 1:
                        for a in phonenumbers:
                            if a in deletephonenumbers:
                                phonenumbers = "Phone number not found."
                except:
                    phonenumbers = "Phone number not found."
                
                # Check e-mail addresses
                email_addresses = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', str(response_query.text).lower())

                # Filter out email addresses based on patterns
                filtered_emails = [email for email in email_addresses if email.lower() not in excluded_emails and not any(pattern in email.split('@')[0] for pattern in deletepatterns)]
                
                # Remove duplicates by converting to a set and back to a list
                filtered_emails = list(set(filtered_emails))

                # Get LinkedIn profiles
                pattern = r'"name": "(.*?)",\s+"url": "(.*?)"'
                matches = re.findall(pattern, str(response_query_linkedin.text), re.DOTALL)

                # Filter out only LinkedIn profiles
                linkedin_profiles = []
                max_profiles = 5  # Set the maximum number of LinkedIn profiles you want

                for match in matches:
                    title = match[0]
                    link = match[1].replace('\\/', '/')
                    if "linkedin.com/in/" in link:
                        linkedin_profiles.append(f"\t» LinkedIn Contacts: {title}\n\t» Link: {link}\n")
                        if len(linkedin_profiles) >= max_profiles:
                            break  # Stop collecting more profiles once the limit is reached

                print("------------------------------------------",
                      "\n⬤ Business name:", businessname,
                      "\n⬤ Website:", website_url,
                      "\n⬤ Phone numbers:",  phonenumbers,
                      "\n⬤ Address:", address,
                      "\n⬤ E-mail accounts:", filtered_emails,
                      f"\n⬤ LinkedIn accounts ({str(len(linkedin_profiles))} were found):")
                
                # Print LinkedIn profiles
                new_linkedin_profiles = [] 
                for profile in linkedin_profiles:
                    new_linkedin_profiles.append(profile.replace('\n', '').replace('\t', ''))
                    print(profile)

                print("\n------------------------------------------\n")

                # Write these results to a excel file
                worksheet.write(f'A{str(self.counter2)}', f'{str(businessname)}')
                worksheet.write(f'B{str(self.counter2)}', f'{str(website_url)}')
                worksheet.write(f'C{str(self.counter2)}', f'{str(phonenumbers)}')
                worksheet.write(f'D{str(self.counter2)}', f'{str(address)}')
                worksheet.write(f'E{str(self.counter2)}', f'{str(filtered_emails)}')
                worksheet.write(f'F{str(self.counter2)}', f'{str(new_linkedin_profiles)}')

            do_search(self.filename)
            self.counter2 += 1

            self.home_frame_button_2.configure(state="normal")
            self.second_frame_button_1.configure(state="normal")
            self.home_frame_button_2.configure(width=140, height=40)
            self.second_frame_button_1.configure(width=140, height=40)
            workbook.close()

    def clearTextBox(self):
        self.textbox.delete(1.0, "end")

    def clearTextBox2(self):
        self.textbox_2.delete(1.0, "end")

    def bulkStopSearching(self):
        self.bulkstopsearch = 1

    def stopSearching(self):
        self.stopsearch = 1

if __name__ == "__main__":

    # Check updates
    root = tk.Tk()
    check_updates = CheckUpdates(root)
    root.mainloop()