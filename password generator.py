import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import string

class PasswordGeneratorApp:
    def __init__(self, master):
        """
        Initializes the Password Generator application.
        :param master: The Tkinter root window.
        """
        self.master = master
        master.title("Password Generator")
        master.geometry("450x550") # Increased height for better spacing
        master.resizable(False, False) # Make the window not resizable

        # Define a modern color palette
        self.bg_color = "#ECEFF1"      # Light Blue-Gray for background
        self.panel_bg_color = "#FFFFFF" # White for main panel
        self.text_color = "#263238"     # Dark Slate Gray for text
        self.button_color = "#4CAF50"   # Green for generate button
        self.button_active_color = "#66BB6A" # Lighter Green on hover
        self.copy_button_color = "#007BFF" # Blue for copy button
        self.copy_button_active_color = "#0056b3" # Darker blue on hover

        # Configure window background
        master.configure(bg=self.bg_color)

        # Main frame for content
        main_frame = tk.Frame(master, bg=self.panel_bg_color, bd=0, relief="flat")
        main_frame.pack(pady=25, padx=25, fill="both", expand=True)

        # Title Label
        title_label = tk.Label(
            main_frame,
            text="Strong Password Generator",
            font=("Inter", 22, "bold"),
            bg=self.panel_bg_color,
            fg=self.text_color
        )
        title_label.pack(pady=(10, 20))

        # --- Generated Password Display (Moved to top) ---
        self.generated_password_var = tk.StringVar()
        self.generated_password_var.set("Your password will appear here")

        self.password_display_entry = ttk.Entry(
            main_frame,
            textvariable=self.generated_password_var,
            font=("Courier", 16), # Using a monospaced font
            justify="center",
            state="readonly", # Make it read-only
        )
        self.password_display_entry.pack(pady=10, padx=20, fill="x", ipady=5)

        # Copy to Clipboard Button
        copy_button = tk.Button(
            main_frame,
            text="Copy to Clipboard",
            font=("Inter", 12),
            bg=self.copy_button_color,
            fg="white",
            activebackground=self.copy_button_active_color,
            activeforeground="white",
            command=self.copy_to_clipboard,
            relief="flat",
            bd=0,
            cursor="hand2",
            highlightthickness=0,
            padx=10,
            pady=5
        )
        copy_button.pack(pady=(0, 20))


        # --- Settings Frame ---
        settings_frame = tk.Frame(main_frame, bg=self.panel_bg_color)
        settings_frame.pack(pady=10, padx=20, fill="x")


        # Password Length Input
        length_label = tk.Label(
            settings_frame,
            text="Password Length:",
            font=("Inter", 14),
            bg=self.panel_bg_color,
            fg=self.text_color,
            anchor="w"
        )
        length_label.pack(side="left", padx=(0, 10))

        self.length_entry = ttk.Entry(
            settings_frame,
            font=("Inter", 14),
            width=5,
            justify="center"
        )
        self.length_entry.insert(0, "12") # Default length
        self.length_entry.pack(side="right")


        # Complexity Options
        options_frame = tk.LabelFrame(
            main_frame,
            text="Include Characters",
            font=("Inter", 14),
            bg=self.panel_bg_color,
            fg=self.text_color,
            padx=20,
            pady=10
        )
        options_frame.pack(pady=(20, 10), fill="x", padx=20)


        # Checkboxes for character types
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        checkbox_font = ("Inter", 12)
        
        s = ttk.Style()
        s.configure('TCheckbutton', background=self.panel_bg_color, foreground=self.text_color, font=checkbox_font)

        ttk.Checkbutton(
            options_frame, text="Lowercase (a-z)", variable=self.include_lowercase, style='TCheckbutton'
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            options_frame, text="Uppercase (A-Z)", variable=self.include_uppercase, style='TCheckbutton'
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            options_frame, text="Numbers (0-9)", variable=self.include_digits, style='TCheckbutton'
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            options_frame, text="Symbols (!@#$%)", variable=self.include_symbols, style='TCheckbutton'
        ).pack(anchor="w", pady=2)

        # Generate Button
        generate_button = tk.Button(
            main_frame,
            text="Generate Password",
            font=("Inter", 16, "bold"),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_active_color,
            activeforeground="white",
            command=self.generate_password,
            relief="flat",
            bd=0,
            cursor="hand2",
            highlightthickness=0,
            padx=20,
            pady=10
        )
        generate_button.pack(pady=25, fill='x', padx=20)


    def generate_password(self):
        """
        Generates a password based on user-specified length and complexity.
        """
        try:
            length = int(self.length_entry.get())
            if length <= 0:
                messagebox.showwarning("Invalid Length", "Password length must be a positive number.")
                return
            if length > 128: # Prevent excessively long passwords
                messagebox.showwarning("Length Warning", "Password length capped at 128 for practicality.")
                length = 128
                self.length_entry.delete(0, tk.END)
                self.length_entry.insert(0, "128")


            character_pool = ""
            required_characters = [] # To ensure at least one of each selected type

            if self.include_lowercase.get():
                character_pool += string.ascii_lowercase
                required_characters.append(random.choice(string.ascii_lowercase))
            if self.include_uppercase.get():
                character_pool += string.ascii_uppercase
                required_characters.append(random.choice(string.ascii_uppercase))
            if self.include_digits.get():
                character_pool += string.digits
                required_characters.append(random.choice(string.digits))
            if self.include_symbols.get():
                character_pool += string.punctuation
                required_characters.append(random.choice(string.punctuation))

            if not character_pool:
                messagebox.showwarning("Selection Error", "Please select at least one character type.")
                self.generated_password_var.set("No character types selected!")
                return

            # Ensure length is not less than the number of required character types
            if length < len(required_characters):
                length = len(required_characters)
                self.length_entry.delete(0, tk.END)
                self.length_entry.insert(0, str(length))
                messagebox.showwarning("Length Conflict", f"Length adjusted to {length} to include all selected character types.")


            # Generate the rest of the password
            remaining_length = length - len(required_characters)
            
            password_list = required_characters + [random.choice(character_pool) for _ in range(remaining_length)]
            random.shuffle(password_list) # Shuffle to randomize positions

            generated_password = "".join(password_list)
            self.generated_password_var.set(generated_password)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for password length.")
            self.generated_password_var.set("Error: Invalid length")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.generated_password_var.set("Error generating password")

    def copy_to_clipboard(self):
        """
        Copies the generated password to the clipboard.
        """
        password = self.generated_password_var.get()
        if password and password != "Your password will appear here" and not password.startswith("Error"):
            self.master.clipboard_clear()
            self.master.clipboard_append(password)
            messagebox.showinfo("Copied!", "Password copied to clipboard.")
        else:
            messagebox.showwarning("Copy Error", "No valid password to copy.")

# Main part of the script to run the application
if __name__ == "__main__":
    root = tk.Tk()
    # Add font check if possible, otherwise rely on system fonts
    try:
        # This is a simple way to check if a font family is available
        # It's not foolproof but works for common cases.
        from tkinter import font
        font.nametofont("TkDefaultFont").config(family="Inter")
    except tk.TclError:
        print("Inter font not found, using default system font.")

    app = PasswordGeneratorApp(root)
    root.mainloop()
