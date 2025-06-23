import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import os

# --- Define Colors ---
PURPLE_DARK = "#360042"
LIGHT_GREY_BG = "#F0F0F0"
TEXT_COLOR_DARK = "#333333"
TEXT_COLOR_LIGHT = "#FFFFFF"
CARD_BG_COLOR = "#FFFFFF"

# --- Function to construct full path for images in Downloads ---
def get_download_image_path(filename):
    home_dir = os.path.expanduser('~')
    downloads_path = os.path.join(home_dir, 'Downloads')
    full_path = os.path.join(downloads_path, filename)
    return full_path

# --- Function to create a standard rectangle image (for sharp edges) ---
def create_rectangle(width, height, color):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, width, height), fill=color)
    return ImageTk.PhotoImage(img)

# --- Function to load and resize images (for logo, main illustration, and nav icons) ---
def load_and_resize_image_from_downloads(filename, size=None):
    path = get_download_image_path(filename)
    try:
        pil_img = Image.open(path)
        if size:
            pil_img = pil_img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(pil_img)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Image '{path}' not found.\nPlease ensure '{filename}' is in your Downloads folder.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image '{path}': {e}")
        return None

# --- Placeholder Functions for Navigation Actions ---
def go_to_home_screen():
    messagebox.showinfo("Navigation", "Already on Home screen!")

def go_to_messages_screen():
    messagebox.showinfo("Navigation", "Navigating to Messages screen!")

def go_to_history_screen():
    messagebox.showinfo("Navigation", "Navigating to History screen!")

def book_enavroom():
    messagebox.showinfo("Action", "Booking Enavroom!")

# --- Function to remove the central card ---
def remove_card(card_frame):
    card_frame.destroy()

# --- Main Application Window ---
root = tk.Tk()
root.title("ENAVROOM App - Home") # Title changed to "ENAVROOM"
root.geometry("400x700")
root.resizable(False, False)
root.config(bg=LIGHT_GREY_BG)

# --- 1. Top Header Frame (Purple Bar with ENAVROOM Logo) ---
header_frame = tk.Frame(root, bg=PURPLE_DARK, height=100) # Header height set to 100
header_frame.pack(fill=tk.X, side=tk.TOP)
header_frame.pack_propagate(False)

# Load and place the ENAVROOM logo
enavroom_logo = load_and_resize_image_from_downloads("enavroom_logo.png", size=(200, 80))
if enavroom_logo:
    logo_label = tk.Label(header_frame, image=enavroom_logo, bg=PURPLE_DARK)
    logo_label.image = enavroom_logo
    logo_label.pack(expand=True)

# --- 2. Main Content Area Frame (Background for the card) ---
content_frame = tk.Frame(root, bg=LIGHT_GREY_BG)
content_frame.pack(fill=tk.BOTH, expand=True)

# --- Central White Card Frame ---
card_frame = tk.Frame(content_frame, bg=CARD_BG_COLOR, relief="flat", bd=0)
# Height reduced to 0.75
card_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.75)

# Close button (X) at the top right of the card
close_button = tk.Button(card_frame, text="x", font=("Arial", 14), command=lambda: remove_card(card_frame),
                         bg=CARD_BG_COLOR, fg=TEXT_COLOR_DARK, bd=0, relief="flat",
                         activebackground=CARD_BG_COLOR, activeforeground=TEXT_COLOR_DARK)
close_button.place(relx=0.98, rely=0.02, anchor="ne")

# Main illustration - Loading "enavroom.png"
main_illustration = load_and_resize_image_from_downloads("enavroom.png", size=(250, 180))
if main_illustration:
    illustration_label = tk.Label(card_frame, image=main_illustration, bg=CARD_BG_COLOR)
    illustration_label.image = main_illustration
    illustration_label.pack(pady=(20, 10))

# "Book Enavroom!" button
button_width = 220  # Smaller width
button_height = 45  # Smaller height
tk_book_button_img = create_rectangle(button_width, button_height, PURPLE_DARK) # Using create_rectangle for sharp edges

book_button = tk.Button(card_frame, text="Book Enavroom!", # Button text changed
                        font=("Lezend Deca", 14, "bold"), fg=TEXT_COLOR_LIGHT,
                        image=tk_book_button_img, compound="center",
                        command=book_enavroom, # Command changed
                        bd=0, relief="flat",
                        activebackground=PURPLE_DARK, activeforeground=TEXT_COLOR_LIGHT,
                        cursor="hand2", bg=CARD_BG_COLOR)
book_button.image = tk_book_button_img
book_button.pack(pady=(20, 40))

# --- 3. Bottom Navigation Bar Frame ---
nav_frame = tk.Frame(root, bg="white", height=70, bd=1, relief=tk.RAISED)
nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
nav_frame.pack_propagate(False)

nav_buttons_container = tk.Frame(nav_frame, bg="white")
nav_buttons_container.pack(expand=True)

def create_nav_button(parent, filename, text, command, is_selected=False):
    tk_icon = load_and_resize_image_from_downloads(filename, size=(30, 30))
    if tk_icon:
        fg_color = PURPLE_DARK if is_selected else TEXT_COLOR_DARK
        button = tk.Button(parent, image=tk_icon, text=text, compound=tk.TOP,
                           font=("Lezend Deca", 10), fg=fg_color, bg="white",
                           command=command, bd=0, relief=tk.FLAT,
                           activebackground=LIGHT_GREY_BG, activeforeground=PURPLE_DARK,
                           cursor="hand2")
        button.image = tk_icon
        return button
    return None

home_button = create_nav_button(nav_buttons_container, "home.png", "HOME", go_to_home_screen, is_selected=True)
if home_button:
    home_button.pack(side=tk.LEFT, padx=20)

messages_button = create_nav_button(nav_buttons_container, "message.png", "MESSAGES", go_to_messages_screen, is_selected=False)
if messages_button:
    messages_button.pack(side=tk.LEFT, padx=20)

history_button = create_nav_button(nav_buttons_container, "history.png", "HISTORY", go_to_history_screen, is_selected=False)
if history_button:
    history_button.pack(side=tk.LEFT, padx=20)

# Run the application
root.mainloop()