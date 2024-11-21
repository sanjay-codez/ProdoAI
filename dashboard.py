import os

import customtkinter as ctk
from PIL import Image
from task_manager import TaskManager
import tkinter as tk
from tkinter import Toplevel
from tkcalendar import Calendar
import time
from habit_tracker import HabitTracker
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure CustomTkinter appearance
ctk.set_appearance_mode("Dark")


# Main application window
class ProductivityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Productivity App")
        self.configure(fg_color="#0b0b38")
        self.task_manager = TaskManager()
        self.habit_tracker = HabitTracker()
        self.points = 0  # Initialize points

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
            ("To Do List", self.load_to_do_list, self.icons[1]),
            ("Habit Tracker", self.load_habit_tracker, self.icons[2]),
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
            text="This is sample text",
            font=ctk.CTkFont(size=14),  # Smaller font size
            text_color="light gray",  # Slightly different color for hierarchy
            wraplength=600  # Wrap text at 600 pixels
        ).pack(pady=10)

    def display_class(self, class_name):
        # Create a frame for the class
        class_frame = ctk.CTkFrame(self.main_frame, fg_color="#262667", corner_radius=15)
        class_frame.pack(fill="x", pady=10, padx=20)

        # Class label
        class_label = ctk.CTkLabel(
            class_frame,
            text=class_name,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        class_label.pack(side="left", padx=10)

        # Toggle tasks button
        toggle_button = ctk.CTkButton(
            class_frame,
            text="▼",
            width=30,
            command=lambda: self.toggle_tasks(class_frame, class_name),
            fg_color="#1a1b4b",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        toggle_button.pack(side="left", padx=10)

        # Add task button
        add_task_button = ctk.CTkButton(
            class_frame,
            text="Add Task",
            command=lambda: self.add_task_popup(class_name),
            fg_color="#1a1b4b",
            hover_color="#2a2b6b",
            font=ctk.CTkFont(size=16)
        )
        add_task_button.pack(side="right", padx=5)

        # Delete class button
        delete_button = ctk.CTkButton(
            class_frame,
            text="Delete",
            command=lambda: self.delete_class_ui(class_name),
            fg_color="#992222",
            hover_color="#aa3333",
            font=ctk.CTkFont(size=16)
        )
        delete_button.pack(side="right", padx=5)

    def load_to_do_list(self):
        self.update_main_content("To Do List")

        # Add a button to create new classes
        add_class_button = ctk.CTkButton(
            self.main_frame,
            text="Add Class",
            command=self.add_class_ui,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=15,
            fg_color="#1a1b4b",
            hover_color="#2a2b6b"
        )
        add_class_button.pack(pady=10)

        # Display all classes
        for class_name in self.task_manager.tasks.keys():  # Use .keys() to iterate over class names
            self.display_class(class_name)

    def toggle_tasks(self, class_frame, class_name):
        # Remove existing task frames if already displayed
        for widget in class_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.destroy()
                return

        # Fetch tasks using the get method
        tasks = self.task_manager.tasks.get(class_name, [])
        if not isinstance(tasks, list):  # Ensure tasks is a list
            tasks = []

        for task in tasks:
            if not isinstance(task, dict):  # Skip invalid task entries
                continue
            task_frame = ctk.CTkFrame(class_frame, fg_color="#333399", corner_radius=10)
            task_frame.pack(fill="x", pady=5, padx=10)

            # Ensure deadline is displayed properly
            deadline_text = f" - Due: {task['deadline']}" if task.get("deadline") else ""
            task_label = ctk.CTkLabel(
                task_frame,
                text=f"{task['name']}{deadline_text}",
                font=ctk.CTkFont(size=16),
                text_color="white"
            )
            task_label.pack(side="left", padx=10)

            complete_button = ctk.CTkButton(
                task_frame,
                text="✔",
                width=30,
                command=lambda t=task["name"]: self.complete_task(class_name, t),
                fg_color="#1a1b4b"
            )
            complete_button.pack(side="right", padx=10)

    def open_date_time_picker(self, task_name_entry, class_name):
        # Open a date/time picker dialog
        picker_window = Toplevel(self)
        picker_window.title("Pick Deadline")
        picker_window.geometry("300x400")

        calendar = Calendar(picker_window, selectmode="day")
        calendar.pack(pady=20)

        def set_time_and_add_task():
            selected_date = calendar.get_date()
            current_time = time.strftime("%H:%M:%S")  # Current time in HH:MM:SS format
            full_datetime = f"{selected_date} {current_time}"
            self.add_task_ui(class_name, task_name_entry.get(), full_datetime)
            picker_window.destroy()

        confirm_button = ctk.CTkButton(
            picker_window,
            text="Confirm",
            command=set_time_and_add_task,
            fg_color="#1a1b4b"
        )
        confirm_button.pack(pady=20)

    def complete_task(self, class_name, task_name):
        if self.task_manager.remove_task(class_name, task_name):  # Remove the task from the backend
            self.load_to_do_list()  # Refresh the UI to reflect the change

    def add_class_ui(self):
        # Popup or dropdown UI for adding a new class
        popup = ctk.CTkInputDialog(text="Enter Class Name:", title="Add Class")
        class_name = popup.get_input()
        if class_name:
            self.task_manager.add_class(class_name)
            self.load_to_do_list()  # Refresh the To-Do List

    def load_habit_tracker(self):
        self.update_main_content("Habit Tracker")

        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Header with title and total points
        header = ctk.CTkFrame(self.main_frame, fg_color="#1a1b4b", corner_radius=10)
        header.pack(fill="x", pady=10, padx=10)

        title_label = ctk.CTkLabel(
            header,
            text="                                      Welcome to Habit Tracker!",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=10)

        self.points_label = ctk.CTkLabel(
            header,
            text=f"Total Points: {self.points}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        self.points_label.pack(side="right", padx=10)

        # Add Habit button
        add_habit_button = ctk.CTkButton(
            self.main_frame,
            text="Add Habit",
            command=self.add_habit_popup,
            fg_color="#2a2b6b",
            hover_color="#333399",
            font=ctk.CTkFont(size=16)
        )
        add_habit_button.pack(pady=10)

        # Display habits
        self.display_habits()

    def add_habit_popup(self):
        # Create a popup for adding a habit
        popup = ctk.CTkToplevel(self)
        popup.title("Add Habit")
        popup.geometry("400x500")
        popup.configure(fg_color="#1a1b4b")  # Blue background theme

        # Make the popup modal and grab focus
        popup.transient(self)  # Associate with the parent window
        popup.grab_set()  # Prevent interaction with parent window
        popup.focus_force()  # Bring the popup to the foreground

        # Habit name entry
        habit_name_label = ctk.CTkLabel(popup, text="Habit Name:", text_color="white", font=ctk.CTkFont(size=18))
        habit_name_label.pack(pady=10)
        habit_name_entry = ctk.CTkEntry(popup, placeholder_text="Enter habit name", corner_radius=10,
                                        fg_color="#262667")
        habit_name_entry.pack(pady=10, padx=20)

        # Frequency selection
        frequency_label = ctk.CTkLabel(popup, text="Frequency:", text_color="white", font=ctk.CTkFont(size=18))
        frequency_label.pack(pady=10)
        frequency_options = ["Daily", "Weekly", "Monthly"]
        frequency_dropdown = ctk.CTkOptionMenu(popup, values=frequency_options, fg_color="#1a1b4b",
                                               button_color="#2a2b6b")
        frequency_dropdown.set("Daily")
        frequency_dropdown.pack(pady=10)

        # Target streak
        streak_label = ctk.CTkLabel(popup, text="Target Streak:", text_color="white", font=ctk.CTkFont(size=18))
        streak_label.pack(pady=10)
        streak_entry = ctk.CTkEntry(popup, placeholder_text="Enter target streak (e.g., 7)", corner_radius=10,
                                    fg_color="#262667")
        streak_entry.pack(pady=10, padx=20)

        # Confirm button to add the habit
        def confirm_habit():
            habit_name = habit_name_entry.get()
            frequency = frequency_dropdown.get()
            target_streak = streak_entry.get()

            if not habit_name or not target_streak.isdigit():
                warning_label = ctk.CTkLabel(popup, text="Invalid input!", text_color="red", font=ctk.CTkFont(size=14))
                warning_label.pack(pady=5)
                return

            # Add the habit using HabitTracker
            self.habit_tracker.add_habit(habit_name, frequency, int(target_streak))
            popup.destroy()
            self.display_habits()  # Refresh the habit tracker display

        confirm_button = ctk.CTkButton(
            popup, text="Add Habit", command=confirm_habit, fg_color="#2a2b6b", hover_color="#333399",
            font=ctk.CTkFont(size=16)
        )
        confirm_button.pack(pady=20, padx=20)

    def display_habits(self):
        # Create a frame for habit cards
        habits_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        habits_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # Configure grid layout for habit cards
        habits_frame.grid_columnconfigure((0, 1, 2), weight=1)  # Three columns

        # Fetch and display habits
        habits = self.habit_tracker.inorder_traversal()
        row, col = 0, 0
        for habit in habits:
            # Create flashcard for each habit
            habit_frame = ctk.CTkFrame(habits_frame, fg_color=habit.color, corner_radius=15, height=200, width=300)
            habit_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            # Habit name and streak
            habit_label = ctk.CTkLabel(
                habit_frame,
                text=f"{habit.name}\nStreak: {habit.streak}/{habit.target_streak}",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="white",
                anchor="center"
            )
            habit_label.pack(pady=10)

            # Progress bar
            progress_bar = ctk.CTkProgressBar(habit_frame, width=250, height=20)
            progress_bar.set(habit.progress / 100)
            progress_bar.pack(pady=10)

            # Buttons: Complete and Delete
            button_frame = ctk.CTkFrame(habit_frame, fg_color="transparent")
            button_frame.pack(pady=10)

            complete_button = ctk.CTkButton(
                button_frame,
                text="✔ Complete",
                command=lambda h=habit.name: self.complete_habit(h),
                fg_color="#1a1b4b",
                font=ctk.CTkFont(size=14)
            )
            complete_button.pack(side="left", padx=5)

            delete_button = ctk.CTkButton(
                button_frame,
                text="Delete",
                command=lambda h=habit.name: self.delete_habit(h),
                fg_color="#992222",
                font=ctk.CTkFont(size=14)
            )
            delete_button.pack(side="left", padx=5)

            # Update row and column for grid layout
            col += 1
            if col >= 3:  # Limit to 3 cards per row
                col = 0
                row += 1
    def display_infographics(self):
        fig, ax = plt.subplots()
        labels = ['Completed', 'Remaining']
        values = [self.completed_habits, self.remaining_habits]
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=["#2a2b6b", "#333399"])

        canvas = FigureCanvasTkAgg(fig, self.main_content)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def complete_habit(self, habit_name):
        if self.habit_tracker.update_progress(habit_name):
            self.points += 10  # Add points for completing a habit
            self.save_points()
            self.points_label.configure(text=f"Total Points: {self.points}")  # Update the points label
            self.display_habits()  # Refresh habit cards

    def save_points(self):
        with open("points.enc", "w") as file:
            file.write(str(self.points))  # Save points as plain text for now

    def load_points(self):
        if os.path.exists("points.enc"):
            with open("points.enc", "r") as file:
                self.points = int(file.read())
        else:
            self.points = 0

    def delete_habit(self, habit_name):
        """Delete a habit from the Habit Tracker."""
        if self.habit_tracker.remove_habit(habit_name):  # Remove habit from the binary tree
            self.display_habits()  # Refresh the display after deletion
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

    def delete_class_ui(self, class_name):
        self.task_manager.delete_class(class_name)  # Delete the class from the data structure
        self.load_to_do_list()  # Refresh the To-Do List UI

    def add_task_ui(self, class_name, task_name, deadline=None):
        if task_name:  # Ensure task name is not empty
            self.task_manager.add_task(class_name, task_name, deadline)
            self.load_to_do_list()  # Refresh the UI


    def add_task_popup(self, class_name):
        # Create a popup for adding a task
        popup = ctk.CTkToplevel(self)
        popup.title("Add Task")
        popup.geometry("400x500")
        popup.configure(fg_color="#1a1b4b")  # Blue background theme

        # Make the popup modal and grab focus
        popup.transient(self)  # Associate with the parent window
        popup.grab_set()  # Prevent interaction with parent window
        popup.focus_force()  # Bring the popup to the foreground

        # Task name entry
        task_name_label = ctk.CTkLabel(popup, text="Task Name:", text_color="white", font=ctk.CTkFont(size=18))
        task_name_label.pack(pady=10)
        task_name_entry = ctk.CTkEntry(popup, placeholder_text="Enter task name", corner_radius=10, fg_color="#262667")
        task_name_entry.pack(pady=10, padx=20)

        # Calendar for date selection
        calendar_label = ctk.CTkLabel(popup, text="Select Deadline Date:", text_color="white",
                                      font=ctk.CTkFont(size=18))
        calendar_label.pack(pady=10)
        calendar = Calendar(popup, selectmode="day", background="#262667", foreground="white",
                            headersbackground="#1a1b4b", headersforeground="white",
                            selectbackground="#2a2b6b", selectforeground="white")
        calendar.pack(pady=10)

        # Time picker
        time_label = ctk.CTkLabel(popup, text="Select Deadline Time:", text_color="white", font=ctk.CTkFont(size=18))
        time_label.pack(pady=10)
        time_frame = ctk.CTkFrame(popup, fg_color="#262667", corner_radius=10)
        time_frame.pack(pady=10)

        hour_values = [f"{i:02d}" for i in range(1, 13)]  # 1 to 12
        minute_values = [f"{i:02d}" for i in range(60)]  # 00 to 59
        am_pm_values = ["AM", "PM"]

        hour_dropdown = ctk.CTkOptionMenu(time_frame, values=hour_values, width=70, fg_color="#1a1b4b",
                                          button_color="#2a2b6b")
        hour_dropdown.set("12")
        hour_dropdown.pack(side="left", padx=5)

        minute_dropdown = ctk.CTkOptionMenu(time_frame, values=minute_values, width=70, fg_color="#1a1b4b",
                                            button_color="#2a2b6b")
        minute_dropdown.set("00")
        minute_dropdown.pack(side="left", padx=5)

        am_pm_dropdown = ctk.CTkOptionMenu(time_frame, values=am_pm_values, width=70, fg_color="#1a1b4b",
                                           button_color="#2a2b6b")
        am_pm_dropdown.set("AM")
        am_pm_dropdown.pack(side="left", padx=5)

        # Confirm button to add the task
        def confirm_task():
            task_name = task_name_entry.get()
            if not task_name:
                warning_label = ctk.CTkLabel(popup, text="Task name cannot be empty!", text_color="red",
                                             font=ctk.CTkFont(size=14))
                warning_label.pack(pady=5)
                return

            selected_date = calendar.get_date()
            hour = hour_dropdown.get()
            minute = minute_dropdown.get()
            am_pm = am_pm_dropdown.get()

            # Convert time to 24-hour format
            hour = int(hour)
            if am_pm == "PM" and hour != 12:
                hour += 12
            elif am_pm == "AM" and hour == 12:
                hour = 0

            full_datetime = f"{selected_date} {hour:02d}:{minute}:00"

            # Add the task
            self.add_task_ui(class_name, task_name, full_datetime)
            popup.destroy()  # Close the popup after adding the task

        confirm_button = ctk.CTkButton(popup, text="Add Task", command=confirm_task,
                                       fg_color="#2a2b6b", hover_color="#333399", font=ctk.CTkFont(size=16))
        confirm_button.pack(pady=20, padx=20)

if __name__ == "__main__":
    app = ProductivityApp()
    app.mainloop()