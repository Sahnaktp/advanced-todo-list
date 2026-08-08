import json
import os
from datetime import datetime
from typing import List, Dict


class TodoManager:
    """Manage tasks in the To-Do List application."""

    FILE_NAME = "tasks.json"

    def __init__(self):
        self.tasks: List[Dict] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load saved tasks from the JSON file."""
        if not os.path.exists(self.FILE_NAME):
            self.tasks = []
            return

        try:
            with open(self.FILE_NAME, "r", encoding="utf-8") as file:
                self.tasks = json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not load saved tasks.")
            self.tasks = []

    def save_tasks(self) -> None:
        """Save all tasks to the JSON file."""
        try:
            with open(self.FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(self.tasks, file, indent=4)
        except OSError:
            print("Error: Could not save tasks.")

    def add_task(self) -> None:
        """Add a new task."""
        title = input("Enter task: ").strip()

        if not title:
            print("Task cannot be empty.")
            return

        task = {
            "id": self.get_next_id(),
            "title": title,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully!")

    def get_next_id(self) -> int:
        """Generate the next task ID."""
        if not self.tasks:
            return 1

        return max(task["id"] for task in self.tasks) + 1

    def view_tasks(self) -> None:
        """Display all tasks."""
        if not self.tasks:
            print("\nNo tasks available.")
            return

        print("\n========== YOUR TASKS ==========")

        for task in self.tasks:
            status = "Completed" if task["completed"] else "Pending"

            print(
                f"\nID      : {task['id']}\n"
                f"Task    : {task['title']}\n"
                f"Status  : {status}\n"
                f"Created : {task['created_at']}\n"
                "--------------------------------"
            )

    def complete_task(self) -> None:
        """Mark a task as completed."""
        self.view_tasks()

        if not self.tasks:
            return

        task_id = self.get_task_id("Enter task ID to complete: ")

        if task_id is None:
            return

        for task in self.tasks:
            if task["id"] == task_id:
                if task["completed"]:
                    print("Task is already completed.")
                else:
                    task["completed"] = True
                    self.save_tasks()
                    print("Task marked as completed!")
                return

        print("Task ID not found.")

    def delete_task(self) -> None:
        """Delete a task."""
        self.view_tasks()

        if not self.tasks:
            return

        task_id = self.get_task_id("Enter task ID to delete: ")

        if task_id is None:
            return

        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print("Task deleted successfully!")
                return

        print("Task ID not found.")

    def search_tasks(self) -> None:
        """Search tasks using a keyword."""
        keyword = input("Enter keyword to search: ").strip().lower()

        if not keyword:
            print("Search keyword cannot be empty.")
            return

        results = [
            task for task in self.tasks
            if keyword in task["title"].lower()
        ]

        if not results:
            print("No matching tasks found.")
            return

        print("\n========== SEARCH RESULTS ==========")

        for task in results:
            status = "Completed" if task["completed"] else "Pending"
            print(f"{task['id']}. {task['title']} - {status}")

    def show_statistics(self) -> None:
        """Display task statistics."""
        total = len(self.tasks)
        completed = sum(task["completed"] for task in self.tasks)
        pending = total - completed

        print("\n========== STATISTICS ==========")
        print(f"Total Tasks     : {total}")
        print(f"Completed Tasks : {completed}")
        print(f"Pending Tasks   : {pending}")

    @staticmethod
    def get_task_id(message: str):
        """Get a valid task ID from the user."""
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid numeric task ID.")
            return None


def display_menu() -> None:
    """Display the main menu."""
    print("""
========================================
       ADVANCED TO-DO LIST SYSTEM
========================================

1. Add Task
2. View Tasks
3. Mark Task as Completed
4. Delete Task
5. Search Tasks
6. View Statistics
7. Exit

========================================
""")


def main() -> None:
    """Run the To-Do List application."""
    todo = TodoManager()

    print("\nWelcome to the Advanced To-Do List System!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            todo.add_task()

        elif choice == "2":
            todo.view_tasks()

        elif choice == "3":
            todo.complete_task()

        elif choice == "4":
            todo.delete_task()

        elif choice == "5":
            todo.search_tasks()

        elif choice == "6":
            todo.show_statistics()

        elif choice == "7":
            print("\nThank you for using the application!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
