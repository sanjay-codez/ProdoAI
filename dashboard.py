import os
from pprint import pprint

import customtkinter as ctk
from PIL import Image
from task_manager import TaskManager
import tkinter as tk
from tkinter import Toplevel
from tkcalendar import Calendar
import time
import array


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
        #print("\nTask List:")
        #pprint(dict(self.task_manager.tasks), indent=4)

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
            ("Settings", self.load_settings, self.icons[5]),
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
        """Load the To-Do List screen."""
        self.update_main_content("To Do List")

        # Add a button to create new classes
        add_class_button = ctk.CTkButton(
            self.main_frame,
            text="Add Subject",
            command=self.add_class_ui,
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=15,
            fg_color="#1a1b4b",
            hover_color="#2a2b6b"
        )
        add_class_button.pack(pady=10)

        # Display all classes and tasks
        for class_name in self.task_manager.tasks.keys():
            self.display_class(class_name)
            print("Classes loaded from tasks.pkl:", list(self.task_manager.tasks.keys()))

        # Display recently completed tasks
        self.display_recently_completed_tasks()

    def display_recently_completed_tasks(self):
        """Display the 'Recently Completed Tasks' section."""
        recently_completed_tasks = self.task_manager.get_recently_completed_tasks()
        if recently_completed_tasks:  # Check if there are completed tasks
            # Create a frame for recently completed tasks
            completed_frame = ctk.CTkFrame(
                self.main_frame, fg_color="#262667", corner_radius=15
            )
            completed_frame.pack(fill="x", pady=100, padx=20)

            # Add a header label for the section
            completed_label = ctk.CTkLabel(
                completed_frame,
                text="Recently Completed Tasks",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color="white",
            )
            completed_label.pack(pady=10)

            # Add each completed task to the frame
            for task in recently_completed_tasks:
                task_label = ctk.CTkLabel(
                    completed_frame,
                    text=f"{task['class_name']}: {task['task_name']}",
                    font=ctk.CTkFont(size=16),
                    text_color="white",
                )
                task_label.pack(pady=2)
        else:
            # Add a placeholder message if no completed tasks
            no_tasks_label = ctk.CTkLabel(
                self.main_frame,
                text="No recently completed tasks.",
                font=ctk.CTkFont(size=16),
                text_color="light gray",
            )
            no_tasks_label.pack(pady=10, padx=20)

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

    # def complete_task(self, class_name, task_name):
    #     if self.task_manager.remove_task(class_name, task_name):  # Remove the task from the backend
    #         self.load_to_do_list()  # Refresh the UI to reflect the change
    def complete_task(self, class_name, task_name):
        """Mark a task as completed and refresh the UI."""
        if self.task_manager.complete_task(class_name, task_name):  # Use the correct method
            self.load_to_do_list()  # Refresh the To-Do List UI dynamically

    def add_class_ui(self):
        # Popup or dropdown UI for adding a new class
        popup = ctk.CTkInputDialog(text="Enter Class Name:", title="Add Class")
        class_name = popup.get_input()
        if class_name:
            self.task_manager.add_class(class_name)
            self.load_to_do_list()  # Refresh the To-Do List





    def load_settings(self):
        self.update_main_content("Settings")



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