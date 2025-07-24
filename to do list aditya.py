import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List Application")

        self.tasks = [] # To store our tasks

        # --- GUI Elements ---
        self.task_label = tk.Label(master, text="New Task / Edit Task:")
        self.task_label.pack(pady=5) # Add some padding

        self.task_entry = tk.Entry(master, width=50)
        self.task_entry.pack(pady=5)

        # Frame for buttons to organize them
        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        self.add_button = tk.Button(button_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5) # Use grid for buttons in the frame

        self.update_button = tk.Button(button_frame, text="Update Task", command=self.update_task)
        self.update_button.grid(row=0, column=1, padx=5)

        self.complete_button = tk.Button(button_frame, text="Mark/Unmark Complete", command=self.mark_complete)
        self.complete_button.grid(row=0, column=2, padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=0, column=3, padx=5)

        self.task_listbox = tk.Listbox(master, width=60, height=15) # Increased width/height
        self.task_listbox.pack(pady=10)

        # Bind an event to the listbox selection
        self.task_listbox.bind('<<ListboxSelect>>', self.load_selected_task_to_entry)

        # Load tasks when the app starts
        self.load_tasks()
        self.update_task_listbox()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.task_entry.delete(0, tk.END) # Clear the entry field
            self.update_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def update_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            new_task_text = self.task_entry.get().strip()

            if new_task_text:
                # Update the task text in our list
                self.tasks[selected_index]["task"] = new_task_text
                self.task_entry.delete(0, tk.END) # Clear entry after update
                self.update_task_listbox()
                self.save_tasks()
                messagebox.showinfo("Success", "Task updated successfully!")
            else:
                messagebox.showwarning("Warning", "Updated task text cannot be empty!")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to update.")

    def load_selected_task_to_entry(self, event):
        """Loads the text of the selected task into the entry field for editing."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            selected_task_text = self.tasks[selected_index]["task"]
            self.task_entry.delete(0, tk.END) # Clear current entry
            self.task_entry.insert(0, selected_task_text) # Insert selected task text
        except IndexError:
            pass # No item selected, do nothing

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END) # Clear existing entries
        for i, task_info in enumerate(self.tasks):
            display_text = task_info["task"]
            if task_info["completed"]:
                display_text += " (Completed)"
            self.task_listbox.insert(tk.END, display_text)
            if task_info["completed"]:
                self.task_listbox.itemconfig(i, {'fg': 'gray', 'strikeThrough': 1}) # Gray out and strikethrough

    def mark_complete(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            # Toggle the completed status
            self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"]
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark/unmark complete.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
            self.save_tasks()
            self.task_entry.delete(0, tk.END) # Clear entry after deleting
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def save_tasks(self):
        # A simple way to save to a file using JSON for better structure
        import json
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        import json
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = [] # Initialize as empty if file not found or corrupted

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
