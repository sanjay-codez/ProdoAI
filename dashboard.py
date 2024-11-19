import customtkinter as ctk
from PIL import Image

# Configure CustomTkinter appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Main application window
class ProductivityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Productivity App")

        self.after(0, lambda:self.state('zoomed'))

        # Configure grid layout for the main app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, minsize=300)  # Explicitly set the sidebar width to 400px
        self.grid_columnconfigure(1, weight=1)  # Main content takes up remaining space

        # Load icons from the specified path
        self.icons = [self.load_icon(f"icons/{i}.png") for i in range(1, 7)]

        # Sidebar Frame
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, fg_color="gray20")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)  # Make the column expandable
        self.sidebar.grid_rowconfigure(6, weight=1)  # Add space at the bottom for alignment

        # Sidebar Buttons
        self.sidebar_buttons = [
            ("Dashboard", self.load_dashboard, self.icons[0]),
            ("Task Manager", self.load_task_manager, self.icons[1]),
            ("Planner", self.load_planner, self.icons[2]),
            ("Notifications", self.load_notifications, self.icons[3]),
            ("Progress Tracker", self.load_progress_tracker, self.icons[4]),
            ("Settings", self.load_settings, self.icons[5]),
        ]

        for idx, (name, command, icon) in enumerate(self.sidebar_buttons):
            button = ctk.CTkButton(
                self.sidebar,
                text=name,
                command=command,
                image=icon,
                compound="left",
                hover_color="lightgrey",
                fg_color="gray20",  # Matches sidebar background
                text_color="white",
                font=ctk.CTkFont(size=18, weight="bold"),
                corner_radius=0,  # Square buttons
                anchor="w",  # Align text and icon to the left
                width=300  # Set a fixed width for the buttons
            )
            button.grid(row=idx, column=0, pady=10, padx=10, sticky="ew")  # Added padx for spacing

        # Header Section
        self.header = ctk.CTkLabel(
            self, text="Productivity Dashboard", font=ctk.CTkFont(size=28, weight="bold")
        )
        self.header.grid(row=0, column=1, sticky="n", pady=20)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Placeholder for main content
        self.content_label = ctk.CTkLabel(self.main_frame, text="Welcome to the Dashboard!")
        self.content_label.pack(pady=20)

    def load_icon(self, path):
        # Load and resize icons (increased size to 40x40)
        return ctk.CTkImage(Image.open(path), size=(100, 100))

    # Sidebar Button Commands
    def load_dashboard(self):
        self.update_main_content("Dashboard")

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

    def update_main_content(self, content):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.main_frame, text=f"Welcome to {content}!").pack(pady=20)




if __name__ == "__main__":
    app = ProductivityApp()
    app.mainloop()
