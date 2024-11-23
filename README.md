
# Productivity Dashboard App

A Python-based productivity application designed for task management, organization, and seamless user interaction. This application features a dynamic dashboard, a to-do list manager, and an AI-powered chatbot for enhanced productivity.

## Features

1. **Dashboard**
   - Displays task categories: Overdue, Today's, and Future tasks.
   - Visualizes task completion status with a bar graph.
   - Lists actionable items to prioritize tasks.

2. **To-Do List**
   - Allows users to add, delete, and manage tasks per subject/class.
   - Includes a deadline picker with calendar and time options.
   - Displays recently completed tasks for quick reference.

3. **AI Chatbot**
   - Interact with ChatGPT for queries or assistance.
   - Saves chat history locally for future reference.
   - Supports custom API keys for OpenAI integration.

4. **Data Structures**
   - `CustomMap`: Manages class and task mappings.
   - `Stack`: Tracks recently completed tasks.
   - Priority queue (min-heap): Organizes urgent action items.

5. **Dark Theme UI**
   - A sleek and responsive interface using `CustomTkinter`.
   - Sidebar navigation for intuitive switching between features.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Pip**: Ensure the latest version is installed.

---

## Installation

### Install Required Libraries
Use the `requirements.txt` file to install dependencies:

```bash
pip install -r requirements.txt
```

### Clone the Repository
```bash
git clone https://github.com/your-username/productivity-dashboard.git
cd productivity-dashboard
```

### Run the Application
```bash
python dashboard.py
```

---

## File Descriptions

- **`dashboard.py`**: The main application file, combining UI elements and backend logic.
- **`task_manager.py`**: Manages tasks, deadlines, and data storage using `CustomMap` and `Stack`.
- **`custom_map.py`**: Provides dictionary-like functionality with persistent storage.
- **`stack.py`**: Implements stack operations for tracking completed tasks.
- **`requirements.txt`**: List of required libraries for the application.

---

## Usage Instructions

### Launch the App
1. Run `dashboard.py` to start the application.
2. The app launches in full-screen mode with a sidebar navigation menu.

### Add Classes
1. Navigate to the **To-Do List** section.
2. Use the "Add Subject" button to create a new class.

### Add Tasks
1. Select a class and click **Add Task**.
2. Provide task details, including deadlines.

### Manage Tasks
- Mark tasks as completed using checkboxes.
- Delete classes or tasks as needed.

### Chat with AI
1. Open the **Talk with AI** section.
2. Enter your OpenAI API key to start chatting.

---

## Requirements

```plaintext
customtkinter==5.1.3
Pillow==8.2.0
tkcalendar==1.6.1
matplotlib==3.3.4
openai==0.27.0
numpy==1.20.1
```
