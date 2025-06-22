import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import os

# --- Define Colors ---
PURPLE_DARK = "#360042"
LIGHT_GREY = "#F0F0F0"
TEXT_COLOR_DARK = "#333333"
TEXT_COLOR_LIGHT = "#FFFFFF"

# New colors for tabs (reused for general styling)
TAB_UNSELECTED_BG = LIGHT_GREY
TAB_UNSELECTED_FG = TEXT_COLOR_DARK

TAB_SELECTED_BG = PURPLE_DARK
TAB_SELECTED_FG = TEXT_COLOR_LIGHT

# --- Function to construct full path for images in Downloads ---
def get_download_image_path(filename):
    home_dir = os.path.expanduser('~')
    downloads_path = os.path.join(home_dir, 'Downloads')
    full_path = os.path.join(downloads_path, filename)
    return full_path

# --- Function to create a rounded rectangle image (retained for other uses if needed) ---
def create_rounded_rectangle(width, height, radius, color):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return ImageTk.PhotoImage(img)

# --- Function to create a standard rectangle image ---
def create_rectangle(width, height, color):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, width, height), fill=color)
    return ImageTk.PhotoImage(img)

# --- Placeholder Functions for Navigation Actions ---
def go_to_home_screen():
    messagebox.showinfo("Navigation", "Navigating to Home screen!")

def go_to_messages_screen():
    messagebox.showinfo("Navigation", "Navigating to Messages screen!")

def go_to_history_screen():
    messagebox.showinfo("Navigation", "Already on History screen!")

# --- Function to load and resize icons for navigation bar ---
def load_and_resize_icon_from_downloads(filename, size=(80, 80)):
    path = get_download_image_path(filename)
    try:
        pil_img = Image.open(path)
        pil_img = pil_img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(pil_img)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Icon '{path}' not found.\nPlease ensure '{filename}' is in your Downloads folder.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Could not load icon '{path}': {e}")
        return None

# --- Main Application Window ---
root = tk.Tk()
root.title("ENNVROOM App - History")
root.geometry("400x700")
root.resizable(False, False)

# --- 1. Top Header Frame (Purple Bar with "History" text) ---
header_frame = tk.Frame(root, bg=PURPLE_DARK, height=80)
header_frame.pack(fill=tk.X, side=tk.TOP)
header_frame.pack_propagate(False)

# "History" Title Label
history_title_label = tk.Label(header_frame, text="History",
                                font=("Lezend Deca", 18, "bold"),
                                fg=TEXT_COLOR_LIGHT, bg=PURPLE_DARK)
history_title_label.pack(expand=True)

# --- 2. Main Content Area Frame (White/Light Grey) ---
content_frame = tk.Frame(root, bg="white")
content_frame.pack(fill=tk.BOTH, expand=True)

# --- Create the light gray rectangle for "Recent" ---
# MODIFIED: Adjusted width and height to match the tab buttons
recent_rect_width = 150
recent_rect_height = 30
tk_recent_rect_img = create_rectangle(recent_rect_width, recent_rect_height, LIGHT_GREY)

# "Recent" label placed within the rectangle image
recent_label_in_rect = tk.Label(content_frame, text="Recent",
                                font=("Lezend Deca", 14, "normal"),
                                fg=TEXT_COLOR_DARK,
                                image=tk_recent_rect_img, # Use the rectangle image
                                compound="center",       # Center text on the image
                                bd=0, relief="flat",     # Remove any default button border
                                highlightthickness=0,    # Remove focus border
                                bg="white")              # Background of the label itself (behind image)
recent_label_in_rect.image = tk_recent_rect_img # Keep a reference to prevent garbage collection
# MODIFIED: Adjusted padx for potentially better centering with the new smaller width
recent_label_in_rect.pack(pady=(20, 0), padx=(20,0), anchor="nw")


# --- 3. Bottom Navigation Bar Frame ---
nav_frame = tk.Frame(root, bg="white", height=70, bd=1, relief=tk.RAISED)
nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
nav_frame.pack_propagate(False)

nav_buttons_container = tk.Frame(nav_frame, bg="white")
nav_buttons_container.pack(expand=True)

def create_nav_button(parent, filename, text, command, is_selected=False):
    tk_icon = load_and_resize_icon_from_downloads(filename, size=(30, 30))
    if tk_icon:
        fg_color = PURPLE_DARK if is_selected else TEXT_COLOR_DARK
        button = tk.Button(parent, image=tk_icon, text=text, compound=tk.TOP,
                           font=("Lezend Deca", 10), fg=fg_color, bg="white",
                           command=command, bd=0, relief=tk.FLAT,
                           activebackground=LIGHT_GREY, activeforeground=PURPLE_DARK,
                           cursor="hand2")
        button.image = tk_icon # Keep a reference
        return button
    return None

home_button = create_nav_button(nav_buttons_container, "home.png", "HOME", go_to_home_screen, is_selected=False)
if home_button:
    home_button.pack(side=tk.LEFT, padx=20)

messages_button = create_nav_button(nav_buttons_container, "message.png", "MESSAGES", go_to_messages_screen, is_selected=False)
if messages_button:
    messages_button.pack(side=tk.LEFT, padx=20)

history_button = create_nav_button(nav_buttons_container, "history.png", "HISTORY", go_to_history_screen, is_selected=True)
if history_button:
    history_button.pack(side=tk.LEFT, padx=20)

# Run the application
root.mainloop()