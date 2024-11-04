import customtkinter as ctk
from PIL import Image

# Set up the appearance of the app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ProdoAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ProdoAI")
        self.geometry("1200x700")

        # Load the background image
        self.bg_image = ctk.CTkImage(
            light_image=Image.open("icons/backgrounds/sidebar_bg.jpg"),
            dark_image=Image.open("icons/backgrounds/sidebar_bg.jpg"),
            size=(1200, 700)  # Match your window size
        )

        # Create a label with the background image
        self.bg_label = ctk.CTkLabel(
            self,
            image=self.bg_image,
            text=""  # Empty text
        )
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load icons
        self.icons = {
            "dashboard": ctk.CTkImage(Image.open("icons/1.png"), size=(50, 50)),
            "tasks": ctk.CTkImage(Image.open("icons/2.png"), size=(50, 50)),
            "goals": ctk.CTkImage(Image.open("icons/3.png"), size=(50, 50)),
            "schedule": ctk.CTkImage(Image.open("icons/4.png"), size=(50, 50)),
            "insights": ctk.CTkImage(Image.open("icons/5.png"), size=(50, 50)),
            "chatbot": ctk.CTkImage(Image.open("icons/6.png"), size=(50, 50)),
            "profile": ctk.CTkImage(Image.open("icons/7.png"), size=(50, 50)),
            "journal": ctk.CTkImage(Image.open("icons/8.png"), size=(50, 50))
        }


        self.main_app_logo = ctk.CTkImage(Image.open("icons/app_logo.png"), size=(60, 60))

        # Initialize sidebar and content areas
        self.create_sidebar()
        self.create_content_frames()

        # Start with the dashboard frame visible
        self.show_frame(self.dashboard_frame)

    def create_sidebar(self):
        """Creates a transparent sidebar with custom navigation buttons."""
        self.sidebar = ctk.CTkFrame(
            self,
            width=275,
            height=700,
            fg_color="transparent"
        )

        self.sidebar.pack_propagate(False)  # Keep fixed size even if empty
        self.sidebar.pack(side="left", fill="y", padx=20, pady=10)

        # Spacer label to add vertical space at the top
        spacer = ctk.CTkLabel(self.sidebar, text="")
        spacer.pack(pady=50)  # Adjust the `pady` value to control the spacing

        # Define buttons with text, command, color, and icon
        buttons = [
            ("Dashboard", self.show_dashboard, self.icons["dashboard"]),
            ("Task Management", self.show_task_management, self.icons["tasks"]),
            ("Goal Setting", self.show_goal_setting, self.icons["goals"]),
            ("Schedule", self.show_schedule, self.icons["schedule"]),
            ("Productivity Insights", self.show_productivity_insights, self.icons["insights"]),
            ("Talk to Chatbot", self.show_chatbot, self.icons["chatbot"]),
            ("Profile & Settings", self.show_profile_settings, self.icons["profile"]),
            ("Reflective Journal", self.show_journal, self.icons["journal"])
        ]

        # Add buttons on top of the transparent sidebar
        for text, command, icon in buttons:
            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                image=icon,
                command=command,
                fg_color="purple",
                hover_color="#9932CC",
                corner_radius=15,
                height=50,
                font=("Arial", 16),
                text_color="white",
                compound="left"
            )
            button.pack(pady=5, padx=10, fill="x")


            self.main_app_logo.configure(size=(250, 100))  # Adjust size as needed

            logo_label = ctk.CTkLabel(
                self.sidebar,
                image=self.main_app_logo,
                text="",
                width=250,
                height=100
            )
            logo_label.place(anchor="nw", x=10, y=20)

    def create_content_frames(self):
        """Creates main content frames for each feature section."""
        self.content = ctk.CTkFrame(self, corner_radius=10)
        self.content.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Initialize each section as a separate scrollable frame
        self.dashboard_frame = self.create_scrollable_frame("Dashboard")
        self.task_management_frame = self.create_scrollable_frame("Task Management")
        self.goal_setting_frame = self.create_scrollable_frame("Goal Setting and Tracking")
        self.schedule_frame = self.create_scrollable_frame("Schedule")
        self.productivity_insights_frame = self.create_scrollable_frame("Productivity Insights")
        self.chatbot_frame = self.create_scrollable_frame("Talk to Chatbot")
        self.profile_settings_frame = self.create_scrollable_frame("Profile and Settings")
        self.journal_frame = self.create_scrollable_frame("Reflective Journal")

    def create_scrollable_frame(self, title):
        """Helper method to create a scrollable frame with a title and logo."""
        scrollable_frame = ctk.CTkScrollableFrame(self.content, corner_radius=10, width=800, height=600)
        scrollable_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Add title label
        label = ctk.CTkLabel(scrollable_frame, text=title, font=("Arial", 24))
        label.pack(pady=20, anchor="w")  # Align title to the left

        return scrollable_frame

    def show_frame(self, frame):
        """Displays the selected frame."""
        for f in [self.dashboard_frame, self.task_management_frame, self.goal_setting_frame,
                  self.schedule_frame, self.productivity_insights_frame, self.chatbot_frame,
                  self.profile_settings_frame, self.journal_frame]:
            f.pack_forget()  # Hide all frames
        frame.pack(expand=True, fill="both")  # Show the selected frame

    # Frame-specific display methods
    def show_dashboard(self):
        self.show_frame(self.dashboard_frame)

    def show_task_management(self):
        self.show_frame(self.task_management_frame)

    def show_goal_setting(self):
        self.show_frame(self.goal_setting_frame)

    def show_schedule(self):
        self.show_frame(self.schedule_frame)

    def show_productivity_insights(self):
        self.show_frame(self.productivity_insights_frame)

    def show_chatbot(self):
        self.show_frame(self.chatbot_frame)

    def show_profile_settings(self):
        self.show_frame(self.profile_settings_frame)

    def show_journal(self):
        self.show_frame(self.journal_frame)


# Run the application
if __name__ == "__main__":
    app = ProdoAIApp()
    app.mainloop()
