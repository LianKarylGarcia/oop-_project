import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import os

# --- Define Colors ---
PURPLE_DARK = "#360042"
LIGHT_GREY = "#F0F0F0"
TEXT_COLOR_DARK = "#333333"
TEXT_COLOR_LIGHT = "#FFFFFF"

# New colors for tabs
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

# --- Function to create a rounded rectangle image ---
def create_rounded_rectangle(width, height, radius, color):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    return ImageTk.PhotoImage(img)

# --- Function to create a standard rectangle image (for selected state) ---
def create_rectangle(width, height, color):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, width, height), fill=color)
    return ImageTk.PhotoImage(img)


# --- Placeholder Functions for Actions ---
def go_to_home_screen():
    messagebox.showinfo("Navigation", "Navigating to Home screen!")

def go_to_messages_screen():
    messagebox.showinfo("Navigation", "Already on Messages screen!")

def go_to_history_screen():
    messagebox.showinfo("Navigation", "Navigating to History screen!")

# Global references for tab images to prevent garbage collection
tk_chat_img_selected = None
tk_chat_img_unselected = None
tk_notifications_img_selected = None
tk_notifications_img_unselected = None

# Variables to hold button widgets, initialized to None
chats_button = None
notifications_button = None

def update_tab_colors(selected_tab):
    global chats_button, notifications_button, \
           tk_chat_img_selected, tk_chat_img_unselected, \
           tk_notifications_img_selected, tk_notifications_img_unselected

    if chats_button and notifications_button:
        # Set both to their unselected (rounded) state first
        chats_button.config(image=tk_chat_img_unselected, fg=TAB_UNSELECTED_FG)
        chats_button.image = tk_chat_img_unselected
        notifications_button.config(image=tk_notifications_img_unselected, fg=TAB_UNSELECTED_FG)
        notifications_button.image = tk_notifications_img_unselected

        # Then apply selected (non-rounded) state to the specific tab
        if selected_tab == "chats":
            chats_button.config(image=tk_chat_img_selected, fg=TAB_SELECTED_FG)
            chats_button.image = tk_chat_img_selected
        elif selected_tab == "notifications":
            notifications_button.config(image=tk_notifications_img_selected, fg=TAB_SELECTED_FG)
            notifications_button.image = tk_notifications_img_selected

def select_chat_tab():
    update_tab_colors("chats")
    # Logic to show/hide chat content

def select_notifications_tab():
    update_tab_colors("notifications")
    # Logic to show/hide notifications content

# --- Main Application Window ---
root = tk.Tk()
root.title("ENNVROOM App - Notifications") # Changed title for clarity
root.geometry("400x700")
root.resizable(False, False)

# --- 1. Top Header Frame (Purple Bar with "Messages" text ONLY) ---
header_frame = tk.Frame(root, bg=PURPLE_DARK, height=80)
header_frame.pack(fill=tk.X, side=tk.TOP)
header_frame.pack_propagate(False)

# "Messages" Title Label (kept as "Messages" as per assumption)
messages_title_label = tk.Label(header_frame, text="Messages",
                                font=("Lezend Deca", 18, "bold"),
                                fg=TEXT_COLOR_LIGHT, bg=PURPLE_DARK)
messages_title_label.pack(expand=True)

# --- 2. Main Content Area Frame (White/Light Grey) ---
content_frame = tk.Frame(root, bg="white")
content_frame.pack(fill=tk.BOTH, expand=True)

# --- Tabs Selection Frame ---
tab_selection_frame = tk.Frame(content_frame, bg="white")
tab_selection_frame.pack(pady=(10, 10))

# --- Generate Button Images ---
button_width = 150
button_height = 30
corner_radius = 15 # For unselected (rounded) state

# Images for UNSELECTED (rounded) state
tk_chat_img_unselected = create_rounded_rectangle(button_width, button_height, corner_radius, TAB_UNSELECTED_BG)
tk_notifications_img_unselected = create_rounded_rectangle(button_width, button_height, corner_radius, TAB_UNSELECTED_BG)

# Images for SELECTED (non-rounded) state
tk_chat_img_selected = create_rectangle(button_width, button_height, TAB_SELECTED_BG)
tk_notifications_img_selected = create_rectangle(button_width, button_height, TAB_SELECTED_BG)


# Chats Button
chats_button = tk.Button(tab_selection_frame, text="Chats",
                         font=("Lezend Deca", 12, "bold"),
                         image=tk_chat_img_unselected,
                         compound="center",
                         fg=TAB_UNSELECTED_FG,
                         command=select_chat_tab,
                         bd=0, relief="flat",
                         activebackground="white",
                         activeforeground=TAB_SELECTED_FG,
                         cursor="hand2")
chats_button.image = tk_chat_img_unselected
chats_button.pack(side=tk.LEFT, padx=5)

# Notifications Button
notifications_button = tk.Button(tab_selection_frame, text="Notifications",
                                 font=("Lezend Deca", 12, "bold"),
                                 image=tk_notifications_img_unselected,
                                 compound="center",
                                 fg=TAB_UNSELECTED_FG,
                                 command=select_notifications_tab,
                                 bd=0, relief="flat",
                                 activebackground="white",
                                 activeforeground=TAB_SELECTED_FG,
                                 cursor="hand2")
notifications_button.image = tk_notifications_img_unselected
notifications_button.pack(side=tk.LEFT, padx=5)

# MODIFIED: Set "Notifications" as selected initially
root.after(100, lambda: update_tab_colors("notifications"))


# --- Illustration (within content_frame) ---
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

# MODIFIED: Changed illustration filename to "notifications.png"
notifications_illustration_filename = "notifications.png"
tk_notifications_illustration = load_and_resize_icon_from_downloads(notifications_illustration_filename, size=(280, 280))

if tk_notifications_illustration:
    illustration_label = tk.Label(content_frame, image=tk_notifications_illustration, bg="white")
    illustration_label.image = tk_notifications_illustration
    illustration_label.pack(pady=(30, 20), anchor="center")

# No text label as requested

# --- 3. Bottom Navigation Bar Frame ---
nav_frame = tk.Frame(root, bg="white", height=70, bd=1, relief=tk.RAISED)
nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
nav_frame.pack_propagate(False)

nav_buttons_container = tk.Frame(nav_frame, bg="white")
nav_buttons_container.pack(expand=True)

def create_nav_button(parent, filename, text, command):
    tk_icon = load_and_resize_icon_from_downloads(filename, size=(30, 30))
    if tk_icon:
        button = tk.Button(parent, image=tk_icon, text=text, compound=tk.TOP,
                           font=("Lezend Deca", 10), fg=TEXT_COLOR_DARK, bg="white",
                           command=command, bd=0, relief=tk.FLAT,
                           activebackground=LIGHT_GREY, activeforeground=PURPLE_DARK,
                           cursor="hand2")
        button.image = tk_icon
        return button
    return None

home_button = create_nav_button(nav_buttons_container, "home.png", "HOME", go_to_home_screen)
if home_button:
    home_button.pack(side=tk.LEFT, padx=20)

messages_button = create_nav_button(nav_buttons_container, "message.png", "MESSAGES", go_to_messages_screen)
if messages_button:
    messages_button.config(fg=PURPLE_DARK)
    messages_button.pack(side=tk.LEFT, padx=20)

history_button = create_nav_button(nav_buttons_container, "history.png", "HISTORY", go_to_history_screen)
if history_button:
    history_button.pack(side=tk.LEFT, padx=20)

# Run the application
root.mainloop()