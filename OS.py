import tkinter as tk
from tkinter import messagebox

# --- Basic "OS" window with taskbar ---

def show_start_menu():
    messagebox.showinfo("Start Menu", "This would open the Start menu.\nYou can add apps or settings here.")

def show_apps():
    messagebox.showinfo("Apps", "This would show available apps.\nAdd your app launcher logic here.")

def exit_os():
    root.destroy()

root = tk.Tk()
root.title("Maxi OS 31.X")
root.geometry("800x600")
root.configure(bg="black")

# Main display area (like a desktop)
main_area = tk.Frame(root, bg="gray20")
main_area.pack(fill=tk.BOTH, expand=True)

# Taskbar at the bottom
taskbar = tk.Frame(root, bg="gray10", height=40)
taskbar.pack(side=tk.BOTTOM, fill=tk.X)

# Add buttons to the taskbar
start_btn = tk.Button(taskbar, text="Start", command=show_start_menu, bg="gray30", fg="white")
apps_btn = tk.Button(taskbar, text="Apps", command=show_apps, bg="gray30", fg="white")
exit_btn = tk.Button(taskbar, text="Exit", command=exit_os, bg="red", fg="white")

start_btn.pack(side=tk.LEFT, padx=(10, 0), pady=5)
apps_btn.pack(side=tk.LEFT, padx=10, pady=5)
exit_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=5)

# You can add more buttons or features as desired

root.mainloop()