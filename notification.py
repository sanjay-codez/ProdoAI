from plyer import notification
import time

class NotificationManager:
    def __init__(self):
        self.notifications = []

    def add_notification(self, title, message, delay_seconds):
        """
        Add a notification to be shown after a delay.
        :param title: Title of the notification
        :param message: Message in the notification
        :param delay_seconds: Time in seconds before the notification is shown
        """
        self.notifications.append((title, message, delay_seconds))

    def show_notifications(self):
        """
        Process and display all notifications in the queue.
        """
        for title, message, delay_seconds in self.notifications:
            time.sleep(delay_seconds)  # Wait for the delay time
            notification.notify(
                title=title,
                message=message,
                app_name="Task Manager",
                timeout=10  # Notification will disappear after 10 seconds
            )

# Example Usage
if __name__ == "__main__":
    manager = NotificationManager()
    manager.add_notification("Task Due", "Complete your math homework!", 5)  # Notify in 5 seconds
    manager.add_notification("gfdsg", "Lgfdsgfds", 10)  # Notify in 10 seconds

    print("Notifications scheduled. Waiting to display...")
    manager.show_notifications()