import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import math
import random
from playsound import playsound
from gtts import gTTS
import os


class NeonCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Calculator")
        self.root.geometry("400x600")
        self.root.resizable(True, True)

        self.entry = tk.Entry(root, font=("Helvetica", 20), bd=5, relief=tk.FLAT)
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=(20, 10), sticky="nsew")

        self.buttons = []

        self.generate_buttons()

        self.root.grid_rowconfigure(6, weight=1)

        self.colors = ["#ff0000", "#ff8000", "#ffff00", "#80ff00", "#00ff00", "#00ff80", "#00ffff", "#0080ff",
                       "#0000ff", "#8000ff", "#ff00ff", "#ff0080"]
        self.color_index = 0
        self.change_background_color()

    def generate_buttons(self):
        button_texts = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("/", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("-", 4, 3),
            ("Clear", 5, 0)
        ]

        for (text, row, col) in button_texts:
            btn = tk.Button(self.root, text=text, font=("Helvetica", 20), bd=5, relief=tk.RIDGE,
                            command=lambda t=text: self.on_button_click(t), bg="orange")
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            btn.config(width=4, height=2, borderwidth=0, highlightthickness=0, bd=0, padx=0, pady=0,
                       font=("Helvetica", 16))
            btn.bind("<Enter>", lambda event, btn=btn: self.on_enter(event, btn))
            btn.bind("<Leave>", lambda event, btn=btn: self.on_leave(event, btn))
            self.buttons.append(btn)

    def on_button_click(self, char):
        if char == "=":
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception as e:
                messagebox.showerror("Error", "Invalid input")
        elif char == "Clear":
            self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, char)

    def change_background_color(self):
        # Shift colors
        self.colors.insert(0, self.colors.pop())

        # Update color
        self.root.configure(bg=self.colors[0])

        # Schedule next color change
        self.root.after(100, self.change_background_color)

    def on_enter(self, event, button):
        button.config(bg="dark orange")

    def on_leave(self, event, button):
        button.config(bg="orange")


class GreetingWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome")
        self.root.geometry("400x300")

        self.label = tk.Label(self.root, text="", font=("Helvetica", 20), bg="black", fg="white")
        self.label.pack(fill=tk.BOTH, expand=True)

        self.name_label = tk.Label(self.root, text="Enter your name:", font=("Helvetica", 16), bg="black", fg="white")
        self.name_label.pack(fill=tk.BOTH, expand=True)

        self.name_entry = tk.Entry(self.root, font=("Helvetica", 16))
        self.name_entry.pack(fill=tk.BOTH, expand=True)

        self.open_button = tk.Button(self.root, text="Open Calculator", font=("Helvetica", 16),
                                     command=self.open_calculator)
        self.open_button.pack(fill=tk.BOTH, expand=True)

        # Add animation here
        self.animate_greeting_message()

        self.founder_name = tk.Label(self.root, text="Founder: Arham Farooq", font=("Helvetica", 16), bg="black",
                                     fg="white")
        self.founder_name.pack(fill=tk.BOTH, expand=True)
        self.animate_text_color()

    def animate_greeting_message(self):
        message = "Welcome to Neon Calculator!"
        message_length = len(message)
        frame_width = 20
        frames = []

        for i in range(frame_width):
            frame = " " * i + message
            frames.append(frame)

        for i in range(frame_width - 1, -1, -1):
            frame = " " * i + message
            frames.append(frame)

        def update_frame(index=0):
            self.label.config(text=frames[index])
            index = (index + 1) % len(frames)
            self.root.after(100, update_frame, index)

        update_frame()

    def animate_text_color(self):
        colors = ["#F3EF0F", "#51F30F", "#0FF3D0", "#0FECF3", "#0F99F3", "#F00FF3", "#F30F96", "#F30F46", "#0000CD"]

        def update_color(index=0):
            self.founder_name.config(fg=colors[index])
            index = (index + 1) % len(colors)
            self.root.after(500, update_color, index)

        update_color()

    def open_calculator(self):
        user_name = self.name_entry.get().strip()
        if user_name:
            tts = gTTS(f"Welcome, {user_name}! You will enjoy using the calculator.")
            tts.save("welcome.mp3")
            playsound("welcome.mp3")
            os.remove("welcome.mp3")
            messagebox.showinfo("Welcome", f"Welcome, {user_name}! You will enjoy using the calculator.")
            self.root.destroy()
            root = tk.Tk()
            app = NeonCalculator(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Please enter your name.")


if __name__ == "__main__":
    greeting_root = tk.Tk()
    greeting_app = GreetingWindow(greeting_root)
    greeting_root.mainloop()
