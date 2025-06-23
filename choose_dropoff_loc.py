import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk # Import Image and ImageTk from Pillow
import os # Import os for path manipulation

# Sample location data
locations = [
    ("PUP Main", "PUP Main - A. Mabini Campus, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("CEA", "PUP - College of Engineering and Architecture, Anonas, Sta. Mesa, City of Manila, Metro-Manila, Philippines"),
    ("Hasmin", "PUP Hasmin Building, Valencia, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("iTech", "PUP - Institute of Technology, Pureza, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("COC", "PUP - College of Communication, Anonas, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("PUP LHS", "PUP Laboratory High School, Sta. Mesa, City of Manila, Metro Manila, Philippines"),
    ("Condotel", "PUP Condotel Building, Anonas, Sta. Mesa, City of Manila, Metro Manila, Philippines")
]

# --- Helper Functions for Images ---
def get_download_image_path(filename):
    home_dir = os.path.expanduser('~')
    downloads_path = os.path.join(home_dir, 'Downloads')
    full_path = os.path.join(downloads_path, filename)
    return full_path

def load_and_resize_image_from_downloads(filename, size=None):
    path = get_download_image_path(filename)
    try:
        pil_img = Image.open(path)
        if size:
            pil_img = pil_img.resize(size, Image.LANCZOS) # Use Image.LANCZOS for high-quality downsampling
        return ImageTk.PhotoImage(pil_img)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Image '{path}' not found.\nPlease ensure '{filename}' is in your Downloads folder.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Could not load image '{path}': {e}")
        return None

# Create main window
root = tk.Tk()
root.title("Choose Drop-off Location")
root.geometry("375x667")
root.configure(bg="white")

# Top header bar (purple)
top_frame = tk.Frame(root, bg="#360042", height=60) # Header color is #360042
top_frame.pack(fill="x")
top_frame.pack_propagate(False)

# --- Load and place the ENAVROOM logo inside the top_frame ---
enavroom_logo = load_and_resize_image_from_downloads("enavroom_logo.png", size=(120, 50))
if enavroom_logo:
    logo_label = tk.Label(top_frame, image=enavroom_logo, bg="#360042") # Label background matches header
    logo_label.image = enavroom_logo
    logo_label.pack(expand=True) # Logo is centered

# Title and Cancel button below the header
title_frame = tk.Frame(root, bg="white")
title_frame.pack(fill="x", pady=(20, 10), padx=20)

# Changed font size to 16 for "Choose Drop-off Location" to fit Cancel button
tk.Label(title_frame, text="Choose Drop-off Location", font=("Helvetica", 16, "bold"), bg="white").pack(side="left")

tk.Button(title_frame, text="Cancel", font=("Helvetica", 10), bg="white", bd=0,
          command=root.destroy, fg="black", activebackground="white", activeforeground="red").pack(side="right")

# Scrollable list area
canvas = tk.Canvas(root, bg="white", bd=0, highlightthickness=0)
scroll_frame = tk.Frame(canvas, bg="white")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scroll_frame.bind("<Configure>", on_frame_configure)

# Add locations as labels
def select_location(name, address):
    messagebox.showinfo("Selected Location", f"{name}\n\n{address}")

for name, address in locations:
    frame = tk.Frame(scroll_frame, bg="white", padx=10, pady=10)
    frame.pack(fill="x", anchor="w")

    icon_label = tk.Label(frame, text="📍", font=("Helvetica", 16), bg="white", fg="#3b0057")
    icon_label.pack(side="left", padx=(0, 10))

    text_frame = tk.Frame(frame, bg="white")
    text_frame.pack(side="left", fill="x", expand=True)

    name_label = tk.Label(text_frame, text=name, font=("Helvetica", 14, "bold"), bg="white", anchor="w")
    name_label.pack(anchor="w")

    addr_label = tk.Label(text_frame, text=address, font=("Helvetica", 11), bg="white", fg="#444444", wraplength=300, justify="left")
    addr_label.pack(anchor="w")

    # Make the whole frame clickable
    frame.bind("<Button-1>", lambda e, n=name, a=address: select_location(n, a))
    for widget in (icon_label, name_label, addr_label):
        widget.bind("<Button-1>", lambda e, n=name, a=address: select_location(n, a))

root.mainloop()