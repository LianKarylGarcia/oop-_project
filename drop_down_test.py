import tkinter as tk
from tkinter import ttk, messagebox

# --- Location Data ---
locations_data = [
    ("PUP Main", "PUP Main - A. Mabini Campus, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("CEA", "PUP - College of Engineering and Architecture, Anonas, Sta. Mesa, City of Manila, Metro-Manila, Philippines"),
    ("Hasmin", "PUP Hasmin Building, Valencia, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("iTech", "PUP - Institute of Technology, Pureza, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("COC", "PUP - College of Communication, Anonas, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("PUP LHS", "PUP Laboratory High School, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("Condotel", "PUP Condotel Building, Anonas, Sta. Mesa, City of Manila, Metro Manila, Philippines")
]
location_names = [name for name, address in locations_data] # List of just names for combobox

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

# --- Configure ttk style ---
style = ttk.Style()
style.theme_use('default') # Use a default theme as a base

# Style for TRadiobutton (for the radio button indicator and text)
style.configure("TRadiobutton",
                background=bg_color,
                foreground="black",
                font=("Helvetica", 14), # Apply font here for TRadiobutton style
                indicatorbackground=bg_color,
                indicatorforeground=bg_color, # Default indicator color
                borderwidth=0,
                focusthickness=0 # Remove focus border for cleaner look
                )

# Map for TRadiobutton (when selected or active)
style.map("TRadiobutton",
          indicatorbackground=[('selected', highlight_color)], # Indicator color when selected
          indicatorforeground=[('selected', highlight_color)], # Indicator color when selected
          background=[('active', bg_color), ('selected', bg_color)], # Background color of the whole radio button widget
          foreground=[('active', "black"), ('selected', "black")] # Foreground color of the text
          )

# Style for TCombobox
style.configure("TCombobox",
                fieldbackground="white", # Background of the input field
                background=bg_color,     # Background of the dropdown list itself
                foreground="black",
                selectbackground=highlight_color, # Background of selected item in dropdown
                selectforeground="white", # Text color of selected item in dropdown
                bordercolor=highlight_color, # Border color when focused
                lightcolor=highlight_color, # Light border color
                darkcolor=highlight_color,  # Dark border color
                arrowcolor=highlight_color  # Color of the dropdown arrow
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
title = tk.Label(root, text="Moto Taxi", font=("Helvetica", 24, "bold"), bg=bg_color, anchor="w")
title.pack(pady=(30, 20), padx=30, anchor="w")

# Radio buttons frame
radio_var = tk.StringVar(value="pickup")

frame = tk.Frame(root, bg=bg_color, bd=2, relief="groove")
frame.pack(padx=30, pady=20, fill="x")

# StringVars to hold selected locations from comboboxes
pickup_location_var = tk.StringVar(value="Select Pickup Location")
dropoff_location_var = tk.StringVar(value="Select Drop-off Location")

def create_radio_option(label_text, value, location_var):
    container = tk.Frame(frame, bg=bg_color, pady=10)
    container.pack(fill="x", padx=10)

    # Use ttk.Radiobutton and apply style
    radio = ttk.Radiobutton(
        container,
        text=label_text,
        variable=radio_var,
        value=value,
        style="TRadiobutton", # Use the defined style
        command=lambda: location_var.set(location_var.get()) # To ensure variable is set when radio is clicked
    )
    radio.pack(side="top", anchor="w")

    # ttk.Combobox for location selection
    combobox = ttk.Combobox(
        container,
        textvariable=location_var, # Link to the StringVar
        values=location_names,     # Provide the list of location names
        state="readonly",          # Make it read-only so user can only select from dropdown
        font=("Helvetica", 12),    # Apply font directly (ttk.Combobox supports it)
        width=40,                  # Adjust width as needed
        style="TCombobox"          # Apply custom combobox style
    )
    combobox.set(location_var.get()) # Set initial text based on StringVar default value
    combobox.pack(anchor="w", padx=20, pady=(5, 0)) # Add some padding

    # Optional: Bind a click on the combobox to automatically select its radio button
    # This ensures the correct radio button is selected if the user only interacts with the combobox
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
    # Get values directly from the StringVars linked to the comboboxes
    selected_pickup = pickup_location_var.get()
    selected_dropoff = dropoff_location_var.get()

    # Check if a default placeholder text is still present
    if selected_pickup == "Select Pickup Location" or selected_dropoff == "Select Drop-off Location":
        messagebox.showwarning("Incomplete Selection", "Please select both Pickup and Drop-off locations from the dropdowns.")
    else:
        messagebox.showinfo("Confirmation",
                            f"Pickup: {selected_pickup}\n"
                            f"Drop-off: {selected_dropoff}\n"
                            f"Ready to proceed!")

next_button = tk.Button(button_frame, text="Next", font=("Helvetica", 14, "bold"),
                        bg=highlight_color, fg="white", width=10, command=on_next)
next_button.pack(side="right", padx=5)

root.mainloop()