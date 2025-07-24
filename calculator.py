import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, master):
        """
        Initializes the Calculator application.
        :param master: The Tkinter root window.
        """
        self.master = master
        master.title("Simple Python Calculator")
        master.geometry("350x450") # Set a fixed size for the window
        master.resizable(False, False) # Make the window not resizable

        # Configure a modern look for the window
        master.configure(bg="#f0f2f5") # Light gray background

        # Result display
        self.result_var = tk.StringVar()
        self.result_var.set("0") # Initial display value

        self.result_label = tk.Label(
            master,
            textvariable=self.result_var,
            font=("Inter", 36, "bold"), # Larger, bolder font
            bg="#e0e0e0", # Slightly darker gray for display
            fg="#333333", # Dark text
            anchor="e", # Align text to the right
            padx=10,
            pady=10,
            relief="flat", # No border
            bd=0,
            width=12 # Fixed width for consistent look
        )
        self.result_label.pack(pady=20, padx=20, fill="x") # Pack with padding and fill horizontally

        # Input fields
        self.num1_entry = tk.Entry(
            master,
            font=("Inter", 16),
            width=20,
            bd=2,
            relief="solid", # Solid border
            justify="right", # Align text to the right
            bg="white",
            fg="#333333"
        )
        self.num1_entry.insert(0, "0") # Default value
        self.num1_entry.pack(pady=5, padx=20, fill="x")

        self.num2_entry = tk.Entry(
            master,
            font=("Inter", 16),
            width=20,
            bd=2,
            relief="solid",
            justify="right",
            bg="white",
            fg="#333333"
        )
        self.num2_entry.insert(0, "0") # Default value
        self.num2_entry.pack(pady=5, padx=20, fill="x")

        # Buttons frame for operators
        operator_frame = tk.Frame(master, bg="#f0f2f5")
        operator_frame.pack(pady=15)

        # Operator buttons
        button_font = ("Inter", 18, "bold")
        button_bg = "#4CAF50" # Green for operators
        button_fg = "white"
        button_active_bg = "#45a049" # Darker green on hover

        self.add_button = tk.Button(
            operator_frame, text="+", font=button_font, bg=button_bg, fg=button_fg,
            activebackground=button_active_bg, command=lambda: self.calculate('+'),
            width=4, height=2, relief="raised", bd=2, cursor="hand2"
        )
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.subtract_button = tk.Button(
            operator_frame, text="-", font=button_font, bg=button_bg, fg=button_fg,
            activebackground=button_active_bg, command=lambda: self.calculate('-'),
            width=4, height=2, relief="raised", bd=2, cursor="hand2"
        )
        self.subtract_button.grid(row=0, column=1, padx=5, pady=5)

        self.multiply_button = tk.Button(
            operator_frame, text="*", font=button_font, bg=button_bg, fg=button_fg,
            activebackground=button_active_bg, command=lambda: self.calculate('*'),
            width=4, height=2, relief="raised", bd=2, cursor="hand2"
        )
        self.multiply_button.grid(row=0, column=2, padx=5, pady=5)

        self.divide_button = tk.Button(
            operator_frame, text="/", font=button_font, bg=button_bg, fg=button_fg,
            activebackground=button_active_bg, command=lambda: self.calculate('/'),
            width=4, height=2, relief="raised", bd=2, cursor="hand2"
        )
        self.divide_button.grid(row=0, column=3, padx=5, pady=5)

        # Clear button
        self.clear_button = tk.Button(
            master, text="Clear", font=("Inter", 16, "bold"), bg="#f44336", fg="white",
            activebackground="#da190b", command=self.clear_inputs,
            width=10, height=1, relief="raised", bd=2, cursor="hand2"
        )
        self.clear_button.pack(pady=10)

    def calculate(self, operator):
        """
        Performs the arithmetic calculation based on the selected operator.
        :param operator: The arithmetic operator (+, -, *, /).
        """
        try:
            num1_str = self.num1_entry.get()
            num2_str = self.num2_entry.get()

            # Input validation
            if not num1_str or not num2_str:
                messagebox.showwarning("Input Error", "Please enter both numbers.")
                return

            num1 = float(num1_str)
            num2 = float(num2_str)

            result = 0
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    messagebox.showerror("Math Error", "Cannot divide by zero!")
                    self.result_var.set("Error")
                    return
                result = num1 / num2
            
            # Display result, formatted to avoid excessive decimal places
            self.result_var.set(f"{result:.8f}".rstrip('0').rstrip('.'))

        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please enter valid numbers.")
            self.result_var.set("Error")
        except Exception as e:
            messagebox.showerror("An Error Occurred", f"Something went wrong: {e}")
            self.result_var.set("Error")

    def clear_inputs(self):
        """
        Clears the input fields and resets the result display.
        """
        self.num1_entry.delete(0, tk.END)
        self.num1_entry.insert(0, "0") # Reset to 0
        self.num2_entry.delete(0, tk.END)
        self.num2_entry.insert(0, "0") # Reset to 0
        self.result_var.set("0")

# Main part of the script to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
