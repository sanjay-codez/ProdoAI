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
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import openai
import json
from datetime import datetime
import customtkinter as ctk
import tkinter as tk

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"


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

        self.api_key = None  # API key for ChatGPT

        self.after(0, lambda: self.state('zoomed'))  # Start in a maximized window

        # Configure grid layout for the main app
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, minsize=300)  # Sidebar width explicitly set
        self.grid_columnconfigure(1, weight=1)     # Main content area

        #self.load_chatbot()

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
            ("Talk with AI", self.load_chatbot, self.icons[5]),
        ]
        # Add App Logo at the top of the sidebar
        app_logo = ctk.CTkImage(Image.open("icons/app_logo.png"), size=(210, 210))  # Resize the logo
        logo_label = ctk.CTkLabel(self.sidebar, image=app_logo, text="")  # Add label with the logo
        logo_label.grid(row=0, column=0, pady=(20, 10), sticky="n")  # Add some padding above the logo

        # Add a white title text label under the logo
        logo_title = ctk.CTkLabel(
            self.sidebar,
            text="Productivity App",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="white"  # Set text color to white
        )
        logo_title.grid(row=1, column=0, pady=(0, 20), sticky="n")  # Add spacing below the title

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

        # Fetch task counts
        task_counts = self.task_manager.get_task_counts()
        open_tasks, closed_tasks = task_counts[0][1], task_counts[1][1]  # Extract open and closed tasks

        # Fetch categorized tasks
        categorized_tasks = self.task_manager.categorize_tasks()

        # Fetch action items
        action_items = self.task_manager.get_action_items()

        # Create a container frame for the layout
        layout_frame = ctk.CTkFrame(self.main_frame, fg_color="#13134a")
        layout_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # First row: Task categories (Overdue, Today's, Future)
        task_row_frame = ctk.CTkFrame(layout_frame, fg_color="#13134a")
        task_row_frame.pack(fill="x", pady=10)

        self.create_task_category_box("Overdue Tasks", categorized_tasks["overdue"], "#ff6666", task_row_frame)
        self.create_task_category_box("Today's Tasks", categorized_tasks["today"], "#ffff66", task_row_frame)
        self.create_task_category_box("Future Tasks", categorized_tasks["future"], "#66ff66", task_row_frame)

        # Second row: Action Items and Graph
        second_row_frame = ctk.CTkFrame(layout_frame, fg_color="#13134a")
        second_row_frame.pack(fill="both", expand=True, pady=10)

        action_items_frame = ctk.CTkFrame(second_row_frame, fg_color="#262667", corner_radius=15)
        action_items_frame.pack(side="left", fill="both", expand=True, padx=10)

        graph_frame = ctk.CTkFrame(second_row_frame, fg_color="#262667", corner_radius=15)
        graph_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Populate the action items box and graph
        self.populate_action_items_box(action_items, action_items_frame)
        self.create_task_completion_graph(open_tasks, closed_tasks, graph_frame)

    def create_task_category_box(self, title, tasks, color, parent_frame):
        # Adjust color for a translucent effect (darker shade)
        color = self.get_translucent_color(color, opacity=0.6)

        # Create the category frame
        category_frame = ctk.CTkFrame(parent_frame, fg_color=color, corner_radius=15)
        category_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # Add category title
        title_label = ctk.CTkLabel(
            category_frame,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)

        # Add tasks with checkboxes
        if tasks:
            for task_name, class_name, deadline in tasks:
                task_frame = ctk.CTkFrame(category_frame, fg_color=color, corner_radius=10)
                task_frame.pack(fill="x", pady=2, padx=10)

                # Add a checkbox for the task
                checkbox = ctk.CTkCheckBox(
                    task_frame,
                    text=f"{task_name} ({class_name}) - Due: {deadline}",
                    font=ctk.CTkFont(size=14),
                    text_color="white",
                    command=lambda t=task_name, c=class_name: self.tick_off_task(c, t)
                )
                checkbox.pack(side="left", padx=5)
        else:
            no_task_label = ctk.CTkLabel(
                category_frame,
                text="No tasks",
                font=ctk.CTkFont(size=14),
                text_color="black"
            )
            no_task_label.pack(pady=10)

    def create_action_items_box(self, action_items, row, column):
        action_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="#262667",
            corner_radius=15,
        )
        action_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Add title
        title_label = ctk.CTkLabel(
            action_frame,
            text="Action Items",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)

        # Add action items
        if action_items:
            for task_name, class_name, deadline in action_items:
                action_label = ctk.CTkLabel(
                    action_frame,
                    text=f"{task_name} ({class_name}) - Due: {deadline}",
                    font=ctk.CTkFont(size=14),
                    text_color="light gray"
                )
                action_label.pack(pady=5)
        else:
            no_action_label = ctk.CTkLabel(
                action_frame,
                text="No urgent tasks",
                font=ctk.CTkFont(size=14),
                text_color="light gray"
            )
            no_action_label.pack(pady=10)

    def create_task_completion_graph(self, open_tasks, closed_tasks, parent_frame):
        # Create bar graph
        fig = plt.Figure(figsize=(4, 2), dpi=100, facecolor="#262667")  # Set background color to match GUI
        ax = fig.add_subplot(111)

        # Data
        categories = ['Pending', 'Completed']
        values = [open_tasks, closed_tasks]
        colors = ['#262667', '#262667']

        # Plot bar graph
        ax.bar(categories, values, color=colors)
        ax.set_title('Task Completion Status', fontsize=14, color="white")  # White text for title
        ax.set_ylabel('Number of Tasks', fontsize=12, color="white")  # White text for axis label
        ax.set_facecolor("#13134a")  # Match the background of the GUI
        ax.tick_params(axis='x', colors="white")  # White text for x-axis ticks
        ax.tick_params(axis='y', colors="white")  # White text for y-axis ticks

        # Remove top and right borders for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color("white")  # White border for left axis
        ax.spines['bottom'].set_color("white")  # White border for bottom axis

        # Embed graph into frame
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)











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
        for class_name, tasks in self.task_manager.tasks.items():
            self.display_class(class_name)

        # Display Recently Completed Tasks
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





    def load_chatbot(self):
        """Load the chatbot interface."""
        self.update_main_content("Chat")

        # API Key Entry
        api_key_frame = ctk.CTkFrame(self.main_frame, fg_color="#13134a", corner_radius=15)
        api_key_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(api_key_frame, text="API Key:", text_color="white").pack(side="left", padx=10)
        self.api_key_entry = ctk.CTkEntry(api_key_frame, show="*", placeholder_text="Enter API Key")
        self.api_key_entry.pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkButton(api_key_frame, text="Set Key", command=self.set_api_key).pack(side="left", padx=10)

        # Create a parent frame for chat history (ensures control over layout)
        chat_frame_container = ctk.CTkFrame(self.main_frame, fg_color="#1a1b4b", corner_radius=15)
        chat_frame_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Disable propagation to control height manually
        chat_frame_container.pack_propagate(False)

        # Chat History (Text Widget for Selectable Content)
        self.chat_text = tk.Text(
            chat_frame_container,
            wrap="word",
            state="disabled",
            bg="#1a1b4b",
            fg="white",
            font=("Arial", 12),
            height=300
        )
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=10)  # Fills the container

        # Scrollbar for Chat History
        scrollbar = tk.Scrollbar(self.chat_text, command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Message Input Frame
        message_frame = ctk.CTkFrame(self.main_frame, fg_color="#13134a", corner_radius=15)
        message_frame.pack(fill="x", padx=10, pady=10)  # Use pack instead of grid

        # Message Entry
        self.message_entry = ctk.CTkEntry(message_frame, placeholder_text="Type your message here...")
        self.message_entry.pack(side="left", fill="x", expand=True, padx=10)

        # Send Button
        ctk.CTkButton(message_frame, text="Send", command=self.send_message).pack(side="left", padx=10)

        # Load existing chat history
        self.load_chat_history()

    def set_api_key(self):
        """Set the API key from the input field."""
        self.api_key = self.api_key_entry.get()
        if not self.api_key:
            self.display_message("System", "API key is required to use the chatbot.")

    def send_message(self):
        """Send a message to the ChatGPT API and display the response."""
        if not self.api_key:
            self.display_message("System", "Please enter an API key first.")
            return

        user_message = self.message_entry.get()
        if not user_message.strip():
            return  # Ignore empty messages

        # Display user's message
        self.display_message("You", user_message)
        self.message_entry.delete(0, "end")

        # Send the message to ChatGPT
        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
            )
            bot_message = response.choices[0].message.content.strip()
            self.display_message("ChatGPT", bot_message)

            # Save chat to history
            self.save_chat_to_history("You", user_message)
            self.save_chat_to_history("ChatGPT", bot_message)
        except Exception as e:
            self.display_message("System", f"Error: {str(e)}")

    def display_message(self, sender, message):
        """Display a message in the chat frame."""
        self.chat_text.configure(state="normal")  # Enable text widget for editing
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_text.insert("end", f"{sender} [{timestamp}]: {message}\n\n")
        self.chat_text.configure(state="disabled")  # Set back to read-only
        self.chat_text.see("end")  # Scroll to the latest message

    def save_chat_to_history(self, sender, message):
        """Save a message to the chat history file."""
        chat_entry = {"sender": sender, "message": message, "timestamp": str(datetime.now())}
        try:
            if os.path.exists(CHAT_HISTORY_FILE):
                with open(CHAT_HISTORY_FILE, "r") as file:
                    history = json.load(file)
            else:
                history = []

            history.append(chat_entry)
            with open(CHAT_HISTORY_FILE, "w") as file:
                json.dump(history, file, indent=4)
        except Exception as e:
            print(f"Error saving chat history: {str(e)}")

    def load_chat_history(self):
        """Load chat history from the file."""
        if os.path.exists(CHAT_HISTORY_FILE):
            try:
                with open(CHAT_HISTORY_FILE, "r") as file:
                    history = json.load(file)
                    for entry in history:
                        self.display_message(entry["sender"], entry["message"])
            except Exception as e:
                print(f"Error loading chat history: {str(e)}")

    def update_main_content(self, content):
        """Clear the main frame and set the header."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(
            self.main_frame,
            text=f"Welcome to {content}!",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color="white",
        ).pack(pady=30)

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

    def populate_action_items_box(self, action_items, parent_frame):
        # Add title
        title_label = ctk.CTkLabel(
            parent_frame,
            text="Action Items",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=10)

        # Add action items
        if action_items:
            for task_name, class_name, deadline in action_items:
                action_label = ctk.CTkLabel(
                    parent_frame,
                    text=f"{task_name} ({class_name}) - Due: {deadline}",
                    font=ctk.CTkFont(size=14),
                    text_color="light gray"
                )
                action_label.pack(pady=5)
        else:
            no_action_label = ctk.CTkLabel(
                parent_frame,
                text="No urgent tasks",
                font=ctk.CTkFont(size=14),
                text_color="light gray"
            )
            no_action_label.pack(pady=10)

    def get_translucent_color(self, hex_color, opacity=0.7):
        """
        Adjust the given hex color to simulate transparency by blending with a dark background.
        :param hex_color: The hex color code (e.g., '#ff6666').
        :param opacity: Opacity level (0.0 to 1.0).
        :return: Adjusted hex color.
        """
        # Ensure valid opacity range
        opacity = max(0.0, min(1.0, opacity))

        # Parse the hex color
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        # Background color (dark)
        bg_r, bg_g, bg_b = 19, 19, 74  # #13134a in RGB

        # Blend with the background
        r = int((1 - opacity) * bg_r + opacity * r)
        g = int((1 - opacity) * bg_g + opacity * g)
        b = int((1 - opacity) * bg_b + opacity * b)

        # Return the blended color as hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def tick_off_task(self, class_name, task_name):
        """Mark a task as completed when ticked and refresh the dashboard."""
        if self.task_manager.complete_task(class_name, task_name):
            # Refresh the dashboard to remove completed task from category
            self.load_dashboard()
if __name__ == "__main__":
    app = ProductivityApp()
    app.mainloop()