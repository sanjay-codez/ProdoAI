from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import tkinter.messagebox as messagebox


class MonthlyCalendar:
    def __init__(self, parent):
        self.parent = parent
        self.current_date = datetime.now()
        self.comments = {}  # Dictionary to store comments for each date
        self.create_calendar_interface()

    def create_calendar_interface(self):
        # Title Label for Month and Year
        self.title_label = tk.Label(self.parent, text=self.current_date.strftime("%B %Y"), font=("Arial", 20, "bold"),
                                    fg="white", bg="#2E2E2E")
        self.title_label.grid(row=0, column=1, columnspan=5, pady=10, padx=10)

        # Navigation Buttons
        self.prev_button = tk.Button(self.parent, text="<< Prev", command=self.prev_month, bg="#9932CC", fg="white", font=("Arial", 10, "bold"))
        self.next_button = tk.Button(self.parent, text="Next >>", command=self.next_month, bg="#9932CC", fg="white", font=("Arial", 10, "bold"))
        self.prev_button.grid(row=0, column=0, padx=10)
        self.next_button.grid(row=0, column=6, padx=10)

        # Days of the Week Headers
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(days):
            tk.Label(self.parent, text=day, font=("Arial", 12, "bold"), fg="white", bg="#2E2E2E").grid(row=1, column=col, padx=5, pady=5)

        # Date Buttons (will be refreshed each month)
        self.date_buttons = []
        self.update_calendar_days()

    def update_calendar_days(self):
        # Clear previous date buttons
        for button in self.date_buttons:
            button.grid_forget()
        self.date_buttons.clear()

        # Calculate the first day of the current month
        first_day_of_month = self.current_date.replace(day=1)
        start_day = first_day_of_month.weekday()  # Day of the week (Mon=0, Sun=6)
        days_in_month = (first_day_of_month.replace(month=first_day_of_month.month % 12 + 1, day=1) - timedelta(days=1)).day

        # Adjust start_day to make Sunday=0 for correct grid placement
        start_day = (start_day + 1) % 7

        # Set up the grid for dates
        row, col = 2, start_day
        for day in range(1, days_in_month + 1):
            date = first_day_of_month.replace(day=day)
            date_str = date.strftime("%Y-%m-%d")

            # Change button style if there's a comment
            if date_str in self.comments:
                button = tk.Button(self.parent, text=str(day), width=6, height=3, bg="#9932CC", fg="white", font=("Arial", 10, "bold"),
                                   command=lambda d=date: self.open_comment_window(d))
                button.bind("<Enter>", lambda e, text=self.comments[date_str]: self.show_tooltip(e, text))
                button.bind("<Leave>", lambda e: self.hide_tooltip(e))
            else:
                button = tk.Button(self.parent, text=str(day), width=6, height=3, bg="black", fg="white", font=("Arial", 10, "bold"),
                                   command=lambda d=date: self.open_comment_window(d))

            button.grid(row=row, column=col, padx=5, pady=5)
            self.date_buttons.append(button)

            # Move to the next row after Saturday
            col += 1
            if col > 6:
                col = 0
                row += 1

    def prev_month(self):
        # Move to the previous month
        self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.update_calendar()

    def next_month(self):
        # Move to the next month
        self.current_date = (self.current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        self.update_calendar()

    def update_calendar(self):
        # Update calendar title and days display
        self.title_label.configure(text=self.current_date.strftime("%B %Y"))
        self.update_calendar_days()

    def open_comment_window(self, date):
        # Open a new window to add or view comments for a specific date using customtkinter
        comment_window = ctk.CTkToplevel(self.parent)
        comment_window.title(f"Comments for {date.strftime('%B %d, %Y')}")
        comment_window.geometry("300x300")
        comment_window.configure(fg_color="#2E2E2E")

        # Keep the window on top and grab focus
        comment_window.transient(self.parent)  # Keep it on top of the main window
        comment_window.grab_set()  # Capture all events to this window
        comment_window.focus()  # Focus on this window

        # Title Label
        comment_title = ctk.CTkLabel(comment_window, text="Comments:", font=("Arial", 16, "bold"), text_color="white")
        comment_title.pack(pady=10)

        # Textbox for adding/viewing comments
        comment_text = ctk.CTkTextbox(comment_window, width=250, height=150, fg_color="black", text_color="white")
        comment_text.pack(pady=10)

        # Load existing comments, if any
        date_str = date.strftime("%Y-%m-%d")
        if date_str in self.comments:
            comment_text.insert("1.0", self.comments[date_str])

        # Save Comment Button
        def save_comment():
            comment = comment_text.get("1.0", "end-1c").strip()
            if comment:
                self.comments[date_str] = comment
                messagebox.showinfo("Saved", "Your comment has been saved!")  # Show confirmation message
                comment_window.destroy()
                self.update_calendar_days()  # Update the calendar to show comment indicator

        # Save button with modern purple theme
        save_button = ctk.CTkButton(comment_window, text="Save Comment", command=save_comment,
                                    fg_color="#9932CC", hover_color="#800080", text_color="white",
                                    font=("Arial", 12, "bold"))
        save_button.pack(pady=10)

    # Tooltip functions for showing comments on hover
    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 20

        self.tooltip = tk.Toplevel(event.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=text, justify='left', background="#9932CC", foreground="white", relief='solid', borderwidth=1, font=("Arial", 10, "bold"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()


import customtkinter as ctk
from PIL import Image

import customcalendar

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
        self.schedule_initialized = False
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

        # Populate dashboard frame with widgets
        self.populate_dashboard()

        # Populate task management frame with widgets
        self.populate_task_management()

        # Populate goal setting frame with widgets
        self.populate_goal_setting()


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
        """Displays the schedule frame with the calendar."""
        self.show_frame(self.schedule_frame)
        if not self.schedule_initialized:
            self.populate_schedule()  # Load calendar only once
            self.schedule_initialized = True

    def show_productivity_insights(self):
        self.show_frame(self.productivity_insights_frame)

    def show_chatbot(self):
        self.show_frame(self.chatbot_frame)

    def show_profile_settings(self):
        self.show_frame(self.profile_settings_frame)

    def show_journal(self):
        self.show_frame(self.journal_frame)

    def populate_dashboard(self):
        """Adds unique widgets to the dashboard frame to make it scrollable."""
        # Title and introductory label
        dashboard_title = ctk.CTkLabel(self.dashboard_frame, text="Dashboard Overview", font=("Arial", 24))
        dashboard_title.pack(pady=20, anchor="w")

        welcome_label = ctk.CTkLabel(self.dashboard_frame, text="Welcome to your personalized dashboard!",
                                     font=("Arial", 16))
        welcome_label.pack(pady=10, anchor="w")

        # Buttons
        for i in range(1, 6):
            button = ctk.CTkButton(self.dashboard_frame, text=f"Action Button {i}",
                                   command=lambda: print(f"Button {i} clicked"))
            button.pack(pady=5, anchor="w")

        # Sliders
        for i in range(1, 4):
            slider_label = ctk.CTkLabel(self.dashboard_frame, text=f"Setting Slider {i}", font=("Arial", 14))
            slider_label.pack(pady=5, anchor="w")
            slider = ctk.CTkSlider(self.dashboard_frame, from_=0, to=100)
            slider.set(i * 25)  # Set unique values
            slider.pack(pady=5, anchor="w")

        # Progress bars
        for i in range(1, 4):
            progress_label = ctk.CTkLabel(self.dashboard_frame, text=f"Progress {i}", font=("Arial", 14))
            progress_label.pack(pady=5, anchor="w")
            progress_bar = ctk.CTkProgressBar(self.dashboard_frame)
            progress_bar.set(i * 0.3)  # Different progress levels
            progress_bar.pack(pady=5, padx=10, fill="x")

        # Checkboxes
        for i in range(1, 6):
            checkbox = ctk.CTkCheckBox(self.dashboard_frame, text=f"Enable Option {i}")
            checkbox.pack(pady=5, anchor="w")

        # Radio buttons with a group variable
        radio_var = ctk.StringVar(value="Option 1")
        for i in range(1, 4):
            radio_button = ctk.CTkRadioButton(self.dashboard_frame, text=f"Radio Option {i}", variable=radio_var,
                                              value=f"Option {i}")
            radio_button.pack(pady=5, anchor="w")

        # Entry fields
        for i in range(1, 4):
            entry = ctk.CTkEntry(self.dashboard_frame, placeholder_text=f"Input Field {i}")
            entry.pack(pady=10, anchor="w")

        # Switches
        for i in range(1, 4):
            switch = ctk.CTkSwitch(self.dashboard_frame, text=f"Toggle Switch {i}")
            switch.pack(pady=10, anchor="w")

        # Example text boxes
        for i in range(1, 3):
            textbox_label = ctk.CTkLabel(self.dashboard_frame, text=f"Text Box {i}", font=("Arial", 14))
            textbox_label.pack(pady=5, anchor="w")
            textbox = ctk.CTkEntry(self.dashboard_frame, placeholder_text="Type here...", width=600)
            textbox.pack(pady=5, anchor="w")

        # Image placeholders (if you want images here)
        for i in range(1, 3):
            img_label = ctk.CTkLabel(self.dashboard_frame, text=f"Image Placeholder {i}", font=("Arial", 14))
            img_label.pack(pady=5, anchor="w")
            img_placeholder = ctk.CTkLabel(self.dashboard_frame, text="🔲 Image Placeholder")
            img_placeholder.pack(pady=10, anchor="w")

        # Separator for visual breaks
        for _ in range(3):
            separator = ctk.CTkLabel(self.dashboard_frame, text="---", font=("Arial", 14))
            separator.pack(pady=10, anchor="w")

    def populate_task_management(self):
        """Adds complex, functional widgets to the task management frame for a complete task management interface."""
        # Set up custom style for Treeview with black/purple colors
        style = ttk.Style()
        style.theme_use("default")

        # Configure Treeview colors for a black/purple theme
        style.configure("Custom.Treeview",
                        background="#2E2E2E",  # Dark background
                        foreground="white",  # White text for rows
                        rowheight=25,  # Adjust row height
                        fieldbackground="#2E2E2E",  # Field background for rows
                        bordercolor="#9932CC")  # Purple border color

        style.map("Custom.Treeview",
                  background=[("selected", "#9932CC")],  # Purple for selected rows
                  foreground=[("selected", "white")])  # White text for selected rows

        # Configure Treeview heading colors for a black/purple theme
        style.configure("Custom.Treeview.Heading",
                        background="#9932CC",  # Purple header background
                        foreground="white",  # White header text
                        font=("Arial", 12, "bold"))  # Bold font for headers

        # Title for the task management section
        task_title = ctk.CTkLabel(self.task_management_frame, text="Task Management", font=("Arial", 24),
                                  text_color="white")
        task_title.pack(pady=20, anchor="w")

        # Section for adding a new task
        add_task_label = ctk.CTkLabel(self.task_management_frame, text="Add New Task", font=("Arial", 18),
                                      text_color="white")
        add_task_label.pack(pady=10, anchor="w")

        # Task entry fields
        task_name_entry = ctk.CTkEntry(self.task_management_frame, placeholder_text="Task Name", fg_color="black",
                                       text_color="white")
        task_name_entry.pack(pady=5, padx=10, anchor="w")

        task_description_entry = ctk.CTkEntry(self.task_management_frame, placeholder_text="Task Description",
                                              width=500, fg_color="black", text_color="white")
        task_description_entry.pack(pady=5, padx=10, anchor="w")

        # Priority selection dropdown
        priority_label = ctk.CTkLabel(self.task_management_frame, text="Priority Level:", text_color="white")
        priority_label.pack(pady=5, anchor="w")

        priority_options = ["Low", "Medium", "High"]
        priority_dropdown = ctk.CTkOptionMenu(self.task_management_frame, values=priority_options, fg_color="#9932CC",
                                              button_color="#2E2E2E", text_color="white")
        priority_dropdown.set("Medium")
        priority_dropdown.pack(pady=5, padx=10, anchor="w")

        # Due date selection
        due_date_label = ctk.CTkLabel(self.task_management_frame, text="Due Date:", text_color="white")
        due_date_label.pack(pady=5, anchor="w")

        due_date_entry = ctk.CTkEntry(self.task_management_frame, placeholder_text="YYYY-MM-DD", fg_color="black",
                                      text_color="white")
        due_date_entry.pack(pady=5, padx=10, anchor="w")

        # Progress tracker slider
        progress_label = ctk.CTkLabel(self.task_management_frame, text="Progress:", text_color="white")
        progress_label.pack(pady=5, anchor="w")

        progress_slider = ctk.CTkSlider(self.task_management_frame, from_=0, to=100, fg_color="#9932CC",
                                        button_color="black")
        progress_slider.set(0)
        progress_slider.pack(pady=5, padx=10, anchor="w")

        # Add task button
        def add_task():
            task_name = task_name_entry.get()
            task_description = task_description_entry.get()
            priority = priority_dropdown.get()
            due_date = due_date_entry.get()
            progress = int(progress_slider.get())

            if task_name and due_date:
                task_list.insert("", "end", values=(task_name, task_description, priority, due_date, f"{progress}%"))
                task_name_entry.delete(0, "end")
                task_description_entry.delete(0, "end")
                due_date_entry.delete(0, "end")
                progress_slider.set(0)

        add_task_button = ctk.CTkButton(self.task_management_frame, text="Add Task", command=add_task,
                                        fg_color="#9932CC", hover_color="#800080", text_color="white")
        add_task_button.pack(pady=10, anchor="w")

        # Task list display as a table using Treeview from tkinter.ttk with custom style
        task_list_label = ctk.CTkLabel(self.task_management_frame, text="Current Tasks", font=("Arial", 18),
                                       text_color="white")
        task_list_label.pack(pady=20, anchor="w")

        # Treeview widget setup with custom style
        task_list = ttk.Treeview(self.task_management_frame,
                                 columns=("Task", "Description", "Priority", "Due Date", "Progress"), show="headings",
                                 style="Custom.Treeview")
        task_list.heading("Task", text="Task")
        task_list.heading("Description", text="Description")
        task_list.heading("Priority", text="Priority")
        task_list.heading("Due Date", text="Due Date")
        task_list.heading("Progress", text="Progress")

        task_list.column("Task", anchor="center", width=150)
        task_list.column("Description", anchor="center", width=300)
        task_list.column("Priority", anchor="center", width=100)
        task_list.column("Due Date", anchor="center", width=100)
        task_list.column("Progress", anchor="center", width=80)

        task_list.pack(pady=10, padx=10, fill="x", anchor="w")

        # Task removal functionality
        def remove_selected_task():
            selected_item = task_list.selection()
            if selected_item:
                task_list.delete(selected_item)

        remove_task_button = ctk.CTkButton(self.task_management_frame, text="Remove Selected Task",
                                           command=remove_selected_task, fg_color="#9932CC", hover_color="#800080",
                                           text_color="white")
        remove_task_button.pack(pady=10, anchor="w")

        # Update progress functionality
        def update_task_progress():
            selected_item = task_list.selection()
            if selected_item:
                progress = f"{int(progress_slider.get())}%"
                task_list.item(selected_item, values=(*task_list.item(selected_item, "values")[:-1], progress))

        update_progress_button = ctk.CTkButton(self.task_management_frame, text="Update Progress",
                                               command=update_task_progress, fg_color="#9932CC", hover_color="#800080",
                                               text_color="white")
        update_progress_button.pack(pady=10, anchor="w")

    def populate_goal_setting(self):
        """Creates an advanced and complex goal-setting interface with purple/black theme."""
        # Title for the goal setting section
        goal_title = ctk.CTkLabel(self.goal_setting_frame, text="Goal Setting & Tracking", font=("Arial", 24),
                                  text_color="white")
        goal_title.pack(pady=20, anchor="w")

        # Section for adding a new goal
        add_goal_label = ctk.CTkLabel(self.goal_setting_frame, text="Add New Goal", font=("Arial", 18),
                                      text_color="white")
        add_goal_label.pack(pady=10, anchor="w")

        # Goal entry fields
        goal_name_entry = ctk.CTkEntry(self.goal_setting_frame, placeholder_text="Goal Name", fg_color="black",
                                       text_color="white")
        goal_name_entry.pack(pady=5, padx=10, anchor="w")

        goal_description_entry = ctk.CTkEntry(self.goal_setting_frame, placeholder_text="Goal Description", width=500,
                                              fg_color="black", text_color="white")
        goal_description_entry.pack(pady=5, padx=10, anchor="w")

        # Priority selection dropdown
        goal_priority_label = ctk.CTkLabel(self.goal_setting_frame, text="Priority Level:", text_color="white")
        goal_priority_label.pack(pady=5, anchor="w")

        priority_options = ["Low", "Medium", "High"]
        goal_priority_dropdown = ctk.CTkOptionMenu(self.goal_setting_frame, values=priority_options, fg_color="#9932CC",
                                                   button_color="#2E2E2E", text_color="white")
        goal_priority_dropdown.set("Medium")
        goal_priority_dropdown.pack(pady=5, padx=10, anchor="w")

        # Due date for the goal
        due_date_label = ctk.CTkLabel(self.goal_setting_frame, text="Target Completion Date:", text_color="white")
        due_date_label.pack(pady=5, anchor="w")

        due_date_entry = ctk.CTkEntry(self.goal_setting_frame, placeholder_text="YYYY-MM-DD", fg_color="black",
                                      text_color="white")
        due_date_entry.pack(pady=5, padx=10, anchor="w")

        # Milestone section
        milestone_label = ctk.CTkLabel(self.goal_setting_frame, text="Milestones", font=("Arial", 18),
                                       text_color="white")
        milestone_label.pack(pady=20, anchor="w")

        milestone_name_entry = ctk.CTkEntry(self.goal_setting_frame, placeholder_text="Milestone Name",
                                            fg_color="black", text_color="white")
        milestone_name_entry.pack(pady=5, padx=10, anchor="w")

        milestone_date_entry = ctk.CTkEntry(self.goal_setting_frame, placeholder_text="Due Date (YYYY-MM-DD)",
                                            fg_color="black", text_color="white")
        milestone_date_entry.pack(pady=5, padx=10, anchor="w")

        def add_milestone():
            milestone_name = milestone_name_entry.get()
            milestone_date = milestone_date_entry.get()
            if milestone_name and milestone_date:
                milestone_list.insert("", "end", values=(milestone_name, milestone_date))
                milestone_name_entry.delete(0, "end")
                milestone_date_entry.delete(0, "end")

        add_milestone_button = ctk.CTkButton(self.goal_setting_frame, text="Add Milestone", command=add_milestone,
                                             fg_color="#9932CC", hover_color="#800080", text_color="white")
        add_milestone_button.pack(pady=10, anchor="w")

        # Milestone List Display
        milestone_list_label = ctk.CTkLabel(self.goal_setting_frame, text="Milestone List", font=("Arial", 18),
                                            text_color="white")
        milestone_list_label.pack(pady=10, anchor="w")

        milestone_list = ttk.Treeview(self.goal_setting_frame, columns=("Milestone", "Due Date"), show="headings",
                                      style="Custom.Treeview")
        milestone_list.heading("Milestone", text="Milestone")
        milestone_list.heading("Due Date", text="Due Date")

        milestone_list.column("Milestone", anchor="center", width=200)
        milestone_list.column("Due Date", anchor="center", width=150)
        milestone_list.pack(pady=10, padx=10, fill="x", anchor="w")

        # Progress Tracker with a slider
        progress_label = ctk.CTkLabel(self.goal_setting_frame, text="Overall Goal Progress:", text_color="white")
        progress_label.pack(pady=10, anchor="w")

        progress_slider = ctk.CTkSlider(self.goal_setting_frame, from_=0, to=100, fg_color="#9932CC",
                                        button_color="black")
        progress_slider.set(0)
        progress_slider.pack(pady=5, padx=10, anchor="w")

        # Add Goal Button
        def add_goal():
            goal_name = goal_name_entry.get()
            goal_description = goal_description_entry.get()
            priority = goal_priority_dropdown.get()
            due_date = due_date_entry.get()
            progress = int(progress_slider.get())

            if goal_name and due_date:
                goal_list.insert("", "end", values=(goal_name, priority, due_date, f"{progress}%"))
                goal_name_entry.delete(0, "end")
                goal_description_entry.delete(0, "end")
                due_date_entry.delete(0, "end")
                progress_slider.set(0)

        add_goal_button = ctk.CTkButton(self.goal_setting_frame, text="Add Goal", command=add_goal, fg_color="#9932CC",
                                        hover_color="#800080", text_color="white")
        add_goal_button.pack(pady=10, anchor="w")

        # Display current goals in a table format
        goal_list_label = ctk.CTkLabel(self.goal_setting_frame, text="Current Goals", font=("Arial", 18),
                                       text_color="white")
        goal_list_label.pack(pady=10, anchor="w")

        goal_list = ttk.Treeview(self.goal_setting_frame, columns=("Goal", "Priority", "Due Date", "Progress"),
                                 show="headings", style="Custom.Treeview")
        goal_list.heading("Goal", text="Goal")
        goal_list.heading("Priority", text="Priority")
        goal_list.heading("Due Date", text="Due Date")
        goal_list.heading("Progress", text="Progress")

        goal_list.column("Goal", anchor="center", width=200)
        goal_list.column("Priority", anchor="center", width=100)
        goal_list.column("Due Date", anchor="center", width=100)
        goal_list.column("Progress", anchor="center", width=80)
        goal_list.pack(pady=10, padx=10, fill="x", anchor="w")

        # Visual Progress Tracker (Pie Chart)
        chart_label = ctk.CTkLabel(self.goal_setting_frame, text="Goal Progress Overview", font=("Arial", 18),
                                   text_color="white")
        chart_label.pack(pady=20, anchor="w")

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100, facecolor="#2E2E2E")
        progress_data = [50, 25, 25]  # Placeholder data
        wedges, texts = ax.pie(progress_data, startangle=90, colors=["#9932CC", "#4B0082", "#800080"])
        ax.set_title("Goal Completion Breakdown", color="white")

        canvas = FigureCanvasTkAgg(fig, self.goal_setting_frame)
        canvas.get_tk_widget().pack(pady=10, padx=10, anchor="w")

        # Calendar for goal deadlines
        calendar_label = ctk.CTkLabel(self.goal_setting_frame, text="Goal Deadlines", font=("Arial", 18),
                                      text_color="white")
        calendar_label.pack(pady=20, anchor="w")

        calendar_frame = ctk.CTkFrame(self.goal_setting_frame, width=300, height=300, fg_color="#2E2E2E")
        calendar_frame.pack(pady=10, padx=10, anchor="w")

        # Basic calendar display
        calendar_text = tk.Text(calendar_frame, wrap="word", background="#2E2E2E", foreground="white", width=35,
                                height=12, borderwidth=0, font=("Arial", 10))
        calendar_text.insert("1.0", "Goal deadlines will be displayed here.")
        calendar_text.config(state="disabled")
        calendar_text.pack()

    def populate_schedule(self):
        """Creates a simple monthly calendar schedule with date-specific comments."""
        schedule_title = tk.Label(self.schedule_frame, text="Monthly Calendar", font=("Arial", 24), fg="white",
                                  bg="#2E2E2E")
        schedule_title.pack(pady=10, anchor="w")

        # Frame for holding the calendar
        calendar_frame = tk.Frame(self.schedule_frame, bg="#2E2E2E")
        calendar_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize and display the monthly calendar
        MonthlyCalendar(calendar_frame)


# Run the application
if __name__ == "__main__":
    app = ProdoAIApp()
    app.mainloop()
