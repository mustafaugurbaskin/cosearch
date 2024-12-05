import customtkinter
import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk, ImageSequence
import requests
import time
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
                print(latest_version)
                if str(self.version) == str(latest_version):
                    
                    # Destroy loading spinner
                    self.destroy_gif()

                    # Call login form
                    self.login_label.configure(text="You are up-to-date.")

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
                print("Failed to perform search. Please check your connection.")
                raise ConnectionError
        except Exception:
            # Show a message due to authentication error
            messagebox.showerror("Connection Error", "There was an error while connecting to the server. Please check your connection.")
            return False
        
    def open_dashboard(self, event):
        webbrowser.open_new("https://www.cosearchteam.com/dashboard/login?redirect=download")

if __name__ == "__main__":
    # Login form
    root = tk.Tk()
    login_form = CheckUpdates(root)
    root.mainloop()