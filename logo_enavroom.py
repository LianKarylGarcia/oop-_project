import tkinter as tk
from tkinter import messagebox
import os # Import os module to handle file paths

def start_action():
    messagebox.showinfo("Start", "Starting the application...")
    # Add your code here for what happens when "Start" is clicked

def exit_action():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Main window setup
root = tk.Tk()
root.title("ENNVROOM")
root.geometry("400x600") # You can adjust the size as needed
root.configure(bg="#360042") # Dark purple background (hex code)

# --- Logo/Title Section ---
# Define the path to your logo image
# IMPORTANT: You MUST change this path to match your actual Downloads folder location
#
# Example for Windows:
# logo_image_path = "C:\\Users\\YourUsername\\Downloads\\enavroom logo.png"
#
# Example for macOS/Linux:
# logo_image_path = "/Users/YourUsername/Downloads/enavroom logo.png"
#
# Replace 'YourUsername' with your actual username.
# If the file extension is different (e.g., .jpg, .gif), adjust it accordingly.

# For demonstration, let's assume a common structure. Please verify this on your system.
# You might need to make this more robust, but this provides the general idea.
# A safer approach for distribution is to place the image in the same directory as the script.

# --- REPLACE THIS LINE WITH YOUR ACTUAL PATH ---
# Assuming a generic path for now, you will need to set this correctly.
# If you are running this from a specific user on your system (e.g., 'user'),
# and the file is in your Downloads, it might look like:
# For Windows:
# logo_image_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'enavroom logo.png')
# For macOS/Linux (this works for both if '~' expands correctly):
logo_image_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'logo.png')

# --- Check if the file exists (optional but good practice) ---
if not os.path.exists(logo_image_path):
    messagebox.showerror("Error", f"Logo image not found at: {logo_image_path}\nPlease check the path and filename.")
    # Fallback to text if image not found
    logo_label = tk.Label(root, text="ENNVROOM", font=("Arial", 48, "bold"), fg="white", bg="#4B0082", borderwidth="0", relief="FLAT")
    logo_label.pack(pady=(100, 50))
else:
    try:
        # Tkinter's PhotoImage supports GIF and PGM/PPM. For PNG/JPG, you might need Pillow (PIL).
        # If your logo is PNG, you'll likely need the Pillow library.
        # Install Pillow: pip install Pillow
        from PIL import Image, ImageTk
        
        # Open the image using Pillow
        pil_image = Image.open(logo_image_path)
        
        # Resize image if needed (optional)
        # pil_image = pil_image.resize((300, 150), Image.LANCZOS) # Adjust size as needed

        logo_image = ImageTk.PhotoImage(pil_image)
        logo_label = tk.Label(root, image=logo_image, bg="#4B0082")
        logo_label.image = logo_image # Keep a reference to prevent garbage collection
        logo_label.pack(pady=(50, 20)) # Adjust padding as needed for the image
    except Exception as e:
        messagebox.showerror("Error", f"Could not load logo image: {e}\nFalling back to text.")
        # Fallback to text if there's an issue loading the image (e.g., wrong format, Pillow not installed)
        logo_label = tk.Label(root, text="ENNVROOM", font=("Arial", 48, "bold"), fg="white", bg="#4B0082")
        logo_label.pack(pady=(100, 50))

# --- Buttons Section ---
# Start Button
start_button = tk.Button(root, text="Start", font=("Arial", 16),
                         command=start_action,
                         bg="white", fg="#4B0082",
                         width=15, height=2,
                         relief="raised", bd=3)
start_button.pack(pady=10) # Padding between logo and button, and between buttons

# Exit Button
exit_button = tk.Button(root, text="Exit", font=("Arial", 16),
                        command=exit_action,
                        bg="white", fg="#4B0082",
                        width=15, height=2,
                        relief="raised", bd=3)
exit_button.pack(pady=10)

# Run the application
root.mainloop()