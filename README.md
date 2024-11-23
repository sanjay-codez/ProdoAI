# Productivity Dashboard App

A Python-based productivity application designed for task management, organization, and seamless user interaction. This application features a dynamic dashboard, a to-do list manager, and an AI-powered chatbot for enhanced productivity.

---

## Features

### 1. Dashboard
- Displays task categories: Overdue, Today's, and Future tasks.
- Visualizes task completion status with a bar graph.
- Lists actionable items to prioritize tasks.

### 2. To-Do List
- Add, delete, and manage tasks per subject/class.
- Includes a deadline picker with calendar and time options.
- Displays recently completed tasks for quick reference.

### 3. AI Chatbot
- Interact with ChatGPT for queries or assistance.
- Saves chat history locally for future reference.
- Supports custom API keys for OpenAI integration.

### 4. Data Structures
- `CustomMap` for managing class and task mappings.
- `Stack` for tracking recently completed tasks.
- Priority queue (min-heap) for urgent action items.

### 5. Dark Theme UI
- Sleek and responsive interface using CustomTkinter.
- Sidebar navigation for intuitive switching between features.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Pip**: Ensure the latest version is installed.

### Install Required Libraries
Use the `requirements.txt` file to install dependencies.

```bash
pip install -r requirements.txt
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/productivity-dashboard.git
cd productivity-dashboard
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
python dashboard.py
File Descriptions
dashboard.py: The main application file, combining UI elements and backend logic.
task_manager.py: Manages tasks, deadlines, and data storage using CustomMap and Stack.
custom_map.py: Provides dictionary-like functionality with persistent storage.
stack.py: Implements stack operations for tracking completed tasks.
requirements.txt: List of required libraries for the application.
Usage Instructions
Launch the App:

Run dashboard.py to start the application.
The app launches in full-screen mode with a sidebar navigation menu.
Add Classes:

Navigate to "To Do List".
Use the "Add Subject" button to create a new class.
Add Tasks:

Select a class and click "Add Task".
Provide task details, including deadlines.
Manage Tasks:

Mark tasks as completed using checkboxes.
Delete classes or tasks as needed.
Chat with AI:

Open the "Talk with AI" section.
Enter your OpenAI API key to start chatting.
Requirements
plaintext
Copy code
customtkinter==5.1.3
Pillow==8.2.0
tkcalendar==1.6.1
matplotlib==3.3.4
openai==0.27.0
numpy==1.20.1
