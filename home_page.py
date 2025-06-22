import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Import Pillow modules
import os # For path handling

# --- Define Colors ---
PURPLE_DARK = "#360042" # This is the purple from your provided code, not the #4B0082 from previous discussions
LIGHT_GREY = "#F0F0F0" # A common light grey, adjust if needed
TEXT_COLOR_DARK = "#333333" # Dark grey for text
TEXT_COLOR_LIGHT = "#FFFFFF" # White for text on dark background

# --- Function to construct full path for images in Downloads ---
def get_download_image_path(filename):
    """Constructs the full path for an image located in the user's Downloads folder."""
    home_dir = os.path.expanduser('~')
    downloads_path = os.path.join(home_dir, 'Downloads')
    full_path = os.path.join(downloads_path, filename)
    return full_path

# --- Placeholder Functions for Actions ---
def on_moto_taxi_click():
    messagebox.showinfo("Service", "Moto Taxi selected!")

def on_car_click():
    messagebox.showinfo("Service", "Car selected!")

def on_home_click():
    messagebox.showinfo("Navigation", "Home button clicked!")

def on_messages_click():
    messagebox.showinfo("Navigation", "Messages button clicked!")

def on_history_click():
    messagebox.showinfo("Navigation", "History button clicked!")

# --- Main Application Window ---
root = tk.Tk()
root.title("ENNVROOM App")
root.geometry("400x700") # Adjusted height to fit content and navigation bar
root.resizable(False, False) # Usually good for mobile-like interfaces

# --- 1. Top Header Frame ---
header_frame = tk.Frame(root, bg=PURPLE_DARK, height=150)
header_frame.pack(fill=tk.X, side=tk.TOP)
header_frame.pack_propagate(False)

# --- Load and place the ENNVROOM Logo ---
logo_image_filename = "enavroom logo.png" # Filename provided by user
logo_image_path = get_download_image_path(logo_image_filename)

try:
    pil_logo_image = Image.open(logo_image_path)
    pil_logo_image = pil_logo_image.resize((250, 100), Image.LANCZOS) # Adjust size as needed
    tk_logo_image = ImageTk.PhotoImage(pil_logo_image)

    # Added bd=0, relief="flat" to remove potential border/outline
    logo_label = tk.Label(header_frame, image=tk_logo_image, bg=PURPLE_DARK, bd=0, relief="flat")
    logo_label.image = tk_logo_image # Keep a reference
    logo_label.pack(pady=20)
except FileNotFoundError:
    messagebox.showerror("Error", f"Logo image '{logo_image_path}' not found.\nPlease check filename and path.")
    logo_label = tk.Label(header_frame, text="ENNVROOM", font=("Arial", 36, "bold"), fg=TEXT_COLOR_LIGHT, bg=PURPLE_DARK, bd=0, relief="flat")
    logo_label.pack(pady=20)
except Exception as e:
    messagebox.showerror("Error", f"Could not load logo image: {e}\nFalling back to text.")
    logo_label = tk.Label(header_frame, text="ENNVROOM", font=("Arial", 36, "bold"), fg=TEXT_COLOR_LIGHT, bg=PURPLE_DARK, bd=0, relief="flat")
    logo_label.pack(pady=20)

# --- 2. Main Content Area Frame ---
content_frame = tk.Frame(root, bg=LIGHT_GREY)
content_frame.pack(fill=tk.BOTH, expand=True)

# --- Service Selection Icons (within content_frame) ---
service_icons_frame = tk.Frame(content_frame, bg="white")
# Using expand=True to center its contents horizontally within the content_frame
service_icons_frame.pack(pady=20, padx=20, fill=tk.X)

# --- Function to load and resize icon from Downloads ---
# Changed default size to (60, 60) for smaller icons
def load_and_resize_icon_from_downloads(filename, size=(60, 60)): # MODIFIED: Smaller default size
    path = get_download_image_path(filename)
    try:
        pil_img = Image.open(path)
        pil_img = pil_img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(pil_img)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Icon '{path}' not found.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Could not load icon '{path}': {e}")
        return None

# Moto Taxi Icon
tk_moto_taxi_icon = load_and_resize_icon_from_downloads("moto taxi.png") # Filename provided
if tk_moto_taxi_icon:
    moto_taxi_label = tk.Label(service_icons_frame, image=tk_moto_taxi_icon, text="Moto Taxi",
                               compound=tk.TOP, font=("Arial", 12), fg=TEXT_COLOR_DARK,
                               bg="white", cursor="hand2")
    moto_taxi_label.image = tk_moto_taxi_icon
    # MODIFIED: Adjusted padx for closer spacing
    moto_taxi_label.pack(side=tk.LEFT, padx=15, pady=10)
    moto_taxi_label.bind("<Button-1>", lambda e: on_moto_taxi_click())

# Car Icon
tk_car_icon = load_and_resize_icon_from_downloads("car.png") # Filename provided
if tk_car_icon:
    car_label = tk.Label(service_icons_frame, image=tk_car_icon, text="Car",
                         compound=tk.TOP, font=("Arial", 12), fg=TEXT_COLOR_DARK,
                         bg="white", cursor="hand2")
    car_label.image = tk_car_icon
    # MODIFIED: Adjusted padx for closer spacing
    car_label.pack(side=tk.LEFT, padx=15, pady=10)
    car_label.bind("<Button-1>", lambda e: on_car_click())

# --- 3. Bottom Navigation Bar Frame ---
nav_frame = tk.Frame(root, bg="white", height=70, bd=1, relief=tk.RAISED)
nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
nav_frame.pack_propagate(False)

# Create a container frame for buttons to easily center them
nav_buttons_container = tk.Frame(nav_frame, bg="white")
nav_buttons_container.pack(expand=True)

# --- Function to create navigation buttons ---
def create_nav_button(parent, filename, text, command):
    tk_icon = load_and_resize_icon_from_downloads(filename, size=(30, 30)) # Smaller icons for nav
    if tk_icon:
        button = tk.Button(parent, image=tk_icon, text=text, compound=tk.TOP,
                           font=("Arial", 10), fg=TEXT_COLOR_DARK, bg="white",
                           command=command, bd=0, relief=tk.FLAT,
                           activebackground=LIGHT_GREY, activeforeground=PURPLE_DARK,
                           cursor="hand2")
        button.image = tk_icon
        return button
    return None

# Home Button
home_button = create_nav_button(nav_buttons_container, "home.png", "HOME", on_home_click) # Filename provided
if home_button:
    home_button.pack(side=tk.LEFT, padx=20)

# Messages Button
messages_button = create_nav_button(nav_buttons_container, "message.png", "MESSAGES", on_messages_click) # Filename provided
if messages_button:
    messages_button.pack(side=tk.LEFT, padx=20)

# History Button
history_button = create_nav_button(nav_buttons_container, "history.png", "HISTORY", on_history_click) # Filename provided
if history_button:
    history_button.pack(side=tk.LEFT, padx=20)

# Run the application
root.mainloop()