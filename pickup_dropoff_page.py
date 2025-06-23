import tkinter as tk
from tkinter import ttk, messagebox

# Create main window
root = tk.Tk()
root.title("Moto Taxi")
root.geometry("375x667")  # iPhone SE-like dimensions

# Colors
bg_color = "white"
highlight_color = "#3b0057"  # Deep purple
light_purple = "#b391c5"

# Set background
root.configure(bg=bg_color)

# Title
title = tk.Label(root, text="Moto Taxi", font=("Helvetica", 24, "bold"), bg=bg_color, anchor="w")
title.pack(pady=(30, 20), padx=30, anchor="w")

# Radio buttons frame
radio_var = tk.StringVar(value="pickup")

frame = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
frame.pack(padx=30, pady=20, fill="x")

def create_radio_option(label_text, search_placeholder, value):
    container = tk.Frame(frame, bg=bg_color, pady=10)
    container.pack(fill="x", padx=10)
    
    radio = tk.Radiobutton(
        container, text=label_text, variable=radio_var, value=value,
        font=("Helvetica", 14), bg=bg_color, activebackground=bg_color,
        highlightthickness=0, selectcolor=highlight_color, fg="black"
    )
    radio.pack(side="top", anchor="w")

    search_label = tk.Label(
        container, text=f"Search {label_text} Location", font=("Helvetica", 14, "bold"),
        fg="black", bg=bg_color
    )
    search_label.pack(anchor="w", padx=20)

create_radio_option("Pickup", "Pickup Location", "pickup")
create_radio_option("Drop-off", "Drop-off Location", "dropoff")

# Bottom buttons
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(side="bottom", pady=30, fill="x", padx=30)

exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 14, "bold"),
                        bg="#d3d3d3", fg="black", width=10, command=root.destroy)
exit_button.pack(side="left", padx=5)

def on_next():
    messagebox.showinfo("Info", f"You selected: {radio_var.get().capitalize()}")

next_button = tk.Button(button_frame, text="Next", font=("Helvetica", 14, "bold"),
                        bg=highlight_color, fg="white", width=10, command=on_next)
next_button.pack(side="right", padx=5)

root.mainloop()