import customtkinter as ctk
from PIL import Image

# Configure CustomTkinter appearance
ctk.set_appearance_mode("Dark")


# Main application window
class ProductivityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Productivity App")
        self.configure(fg_color="#0b0b38")

        self.after(0, lambda: self.state('zoomed'))  # Start in a maximized window

        # Configure grid layout for the main app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, minsize=300)  # Sidebar width explicitly set
        self.grid_columnconfigure(1, weight=1)     # Main content area

        # Load icons from the specified path
        self.icons = [self.load_icon(f"icons/{i}.png") for i in range(1, 8)]  # Update to include icon for Chatbot

        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, fg_color="#0b0b38")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)  # Buttons fill the sidebar width

        # Sidebar Buttons
        self.sidebar_buttons = [
            ("Dashboard", self.load_dashboard, self.icons[0]),
            ("Task Manager", self.load_task_manager, self.icons[1]),
            ("Planner", self.load_planner, self.icons[2]),
            ("Notifications", self.load_notifications, self.icons[3]),
            ("Progress Tracker", self.load_progress_tracker, self.icons[4]),
            ("Settings", self.load_settings, self.icons[5]),
            ("Chatbot", self.load_chatbot, self.icons[6]),  # New "Chatbot" button
        ]
        # Add App Logo at the top of the sidebar
        app_logo = ctk.CTkImage(Image.open("icons/app_logo.png"), size=(275, 125))  # Resize the logo
        logo_label = ctk.CTkLabel(self.sidebar, image=app_logo, text="")  # Add label with the logo
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")  # Add some padding above the logo

        for idx, (name, command, icon) in enumerate(self.sidebar_buttons):
            button = ctk.CTkButton(
                self.sidebar,
                text=name,
                command=command,
                image=icon,
                compound="left",
                hover_color="#13134a",
                fg_color="#0b0b38",  # Matches sidebar background
                text_color="white",
                font=ctk.CTkFont(size=18, weight="bold"),
                corner_radius=15,  # Square buttons
                anchor="w",  # Align text and icon to the left
                width=300  # Ensures consistent width
            )
            button.grid(row=idx + 2, column=0, pady=10, padx=10, sticky="ew")  # Start buttons from row 2

        # Header Section
        self.header = ctk.CTkLabel(
            self, text="Productivity Dashboard", font=ctk.CTkFont(size=28, weight="bold")
        )
        self.header.grid(row=0, column=1, sticky="n", pady=20)

        # Create a container frame first
        self.main_frame_container = ctk.CTkFrame(
            self,
            fg_color="#0b0b38",  # Match the background color or choose another color
            corner_radius=15
        )
        self.main_frame_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame_container.grid_rowconfigure(0, weight=1)
        self.main_frame_container.grid_columnconfigure(0, weight=1)

        # Create the scrollable frame inside the container
        self.main_frame = ctk.CTkScrollableFrame(
            self.main_frame_container,
            fg_color="#13134a",  # Change this to your desired color
            corner_radius=15,
            scrollbar_button_color="#1a1b4b",  # Customize scrollbar button color
            scrollbar_button_hover_color="#2a2b6b"  # Customize scrollbar hover color
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.update_main_content("Dashboard")
        self.load_dashboard()

    def load_icon(self, path):
        return ctk.CTkImage(Image.open(path), size=(70, 70))  # Adjusted size

    # Sidebar Button Commands
    def load_dashboard(self):
        self.update_main_content("Dashboard")
        # Add sample text below with smaller font
        ctk.CTkLabel(
            self.main_frame,
            text="""
        Rats are the best
        Author: Harsika Krishnan

        In my opinion, I think rats are amazing, but many people don’t believe that. Many people have favorite rodents, and mine is a rat. Rats are the best, because they are adorable, easy to take care of, and are harmless. Rats are amazing. Squeak!

        First of all, rats are adorable. They are really fun to play, and rats are cute when they run on their toes in their cage. To add on, these little rats run in a little wheel, and it is adorable! One time, I saw a rat in a cage. It was in a wheel. It was very cute. Plus you can even dress them up like a different animal you like, or even give it a Halloween costume. It would look like a piece of a yarn ball.

        Second, rats are easy to take care of. You have to give it a cage so it won’t escape. You will also have to clean its cage, because it might make a mess. Then you have to give it lots of food or else it will not survive long. Rats are usually looking for something to do. That's when you have to buy it something it can play with. It’s usually found in pet stores. It can be something squishy or something else. They wouldn’t be bored after all! On the other hand, if you give it something it doesn’t like, it will still be bored.

        Finally, rats are harmless. Rats don’t have very long claws. They're just tiny. They are not spiky. Rats are very soft. When I saw a rat it wasn’t spicky. It was so soft. Plus, pet rats don’t usually have diseases! This is important, because if the harmless little rat has diseases it can spread it to humans. Rats can be very different from each other.

        In conclusion, other people should care about this because rats need love and care. Rats are the best type of rodent and you can do so much with it. Rats are adorable, easy to take care of, and are harmless.






                    """,
            font=ctk.CTkFont(size=14),  # Smaller font size
            text_color="light gray",  # Slightly different color for hierarchy
            wraplength=600  # Wrap text at 600 pixels
        ).pack(pady=10)

    def load_task_manager(self):
        self.update_main_content("Task Manager")

    def load_planner(self):
        self.update_main_content("Planner")

    def load_notifications(self):
        self.update_main_content("Notifications")

    def load_progress_tracker(self):
        self.update_main_content("Progress Tracker")

    def load_settings(self):
        self.update_main_content("Settings")

    def load_chatbot(self):
        self.update_main_content("Chatbot")  # Placeholder for chatbot functionality

    def update_main_content(self, content):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.main_frame,
            text=f"Welcome to {content}!",
            font=ctk.CTkFont(size=42, weight="bold"),  # Larger size and bold
            text_color="white"  # White text color
        ).pack(pady=30)  # Increased padding for better spacing





if __name__ == "__main__":
    app = ProductivityApp()
    app.mainloop()