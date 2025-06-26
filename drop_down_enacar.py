import tkinter as tk
from tkinter import ttk, messagebox

# --- Location Data ---
locations_data = [
    ("PUP Main", "A. Mabini Campus, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("CEA", "PUP - College of Engineering and Architecture, Anonas, Sta. Mesa, City of Manila, Metro-Manila, Philippines"),
    ("Hasmin", "PUP Hasmin Building, Valencia, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("iTech", "PUP - Institute of Technology, Pureza, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("COC", "PUP - College of Communication, Anonas, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("PUP LHS", "PUP Laboratory High School, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("Condotel", "PUP Condotel Building, Anonas, Sta. Mesa, City of Manila, Metro Manila, Philippines")
]

# Create a list where each item is "Short Name - Full Address" for display in combobox
display_names_with_full_address = [f"{name} - {address}" for name, address in locations_data]


# Create main window
root = tk.Tk()
root.title("Enacar") # Changed title to "Enacar"
root.geometry("375x667")  # iPhone SE-like dimensions

# Colors
bg_color = "white"
highlight_color = "#3b0057"  # Deep purple
light_purple = "#b391c5"

# Set background
root.configure(bg=bg_color)

# --- Configure ttk style ---
style = ttk.Style()
style.theme_use('default') # Use a default theme as a base

# Style for TRadiobutton (for the radio button indicator and text)
style.configure("TRadiobutton",
                background=bg_color,
                foreground="black",
                font=("Helvetica", 14),
                indicatorbackground=bg_color,
                indicatorforeground=bg_color,
                borderwidth=0,
                focusthickness=0
                )

# Map for TRadiobutton (when selected or active)
style.map("TRadiobutton",
          indicatorbackground=[('selected', highlight_color)],
          indicatorforeground=[('selected', highlight_color)],
          background=[('active', bg_color), ('selected', bg_color)],
          foreground=[('active', "black"), ('selected', "black")]
          )

# Style for TCombobox
style.configure("TCombobox",
                fieldbackground="white",
                background=bg_color,
                foreground="black",
                selectbackground=highlight_color,
                selectforeground="white",
                bordercolor=highlight_color,
                lightcolor=highlight_color,
                darkcolor=highlight_color,
                arrowcolor=highlight_color
                )

# Map for TCombobox (for dynamic states)
style.map('TCombobox',
          fieldbackground=[('readonly', 'white')],
          background=[('readonly', 'white')],
          foreground=[('readonly', 'black')],
          bordercolor=[('focus', highlight_color)],
          lightcolor=[('focus', highlight_color)],
          darkcolor=[('focus', highlight_color)])


# Title
title = tk.Label(root, text="Enacar", font=("Helvetica", 24, "bold"), bg=bg_color, anchor="w") # Changed title text
title.pack(pady=(30, 20), padx=30, anchor="w")

# Radio buttons frame
radio_var = tk.StringVar(value="pickup")

frame = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
frame.pack(padx=30, pady=20, fill="x")

# StringVars to hold selected locations from comboboxes
pickup_location_var = tk.StringVar(value="Select Pickup Location...")
dropoff_location_var = tk.StringVar(value="Select Drop-off Location...")

def create_radio_option(label_text, value, location_var):
    container = tk.Frame(frame, bg=bg_color, pady=10)
    container.pack(fill="x", padx=10)

    radio = ttk.Radiobutton(
        container,
        text=label_text,
        variable=radio_var,
        value=value,
        style="TRadiobutton",
        command=lambda: radio_var.set(value)
    )
    radio.pack(side="top", anchor="w")

    combobox = ttk.Combobox(
        container,
        textvariable=location_var,
        values=display_names_with_full_address,
        state="readonly",
        font=("Helvetica", 12),
        width=40,
        style="TCombobox"
    )
    combobox.set(location_var.get())
    combobox.pack(anchor="w", padx=20, pady=(5, 0))

    combobox.bind("<<ComboboxSelected>>", lambda event: radio_var.set(value))

# Create Pickup and Drop-off options with comboboxes
create_radio_option("Pickup", "pickup", pickup_location_var)
create_radio_option("Drop-off", "dropoff", dropoff_location_var)


# Bottom buttons
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(side="bottom", pady=30, fill="x", padx=30)

exit_button = tk.Button(button_frame, text="Exit", font=("Helvetica", 14, "bold"),
                        bg="#d3d3d3", fg="black", width=10, command=root.destroy)
exit_button.pack(side="left", padx=5)

def on_next():
    selected_pickup_display = pickup_location_var.get()
    selected_dropoff_display = dropoff_location_var.get()

    if selected_pickup_display == "Select Pickup Location..." or \
       selected_dropoff_display == "Select Drop-off Location...":
        messagebox.showwarning("Incomplete Selection", "Please select both Pickup and Drop-off locations from the dropdowns.")
    else:
        messagebox.showinfo("Enacar Confirmation", # Changed messagebox title
                            f"Enacar Pickup: {selected_pickup_display}\n" # Changed text
                            f"Enacar Drop-off: {selected_dropoff_display}\n" # Changed text
                            f"Ready to proceed with Enacar booking!") # Changed text

next_button = tk.Button(button_frame, text="Next", font=("Helvetica", 14, "bold"),
                        bg=highlight_color, fg="white", width=10, command=on_next)
next_button.pack(side="right", padx=5)

root.mainloop()