import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

# --- Color and Font Definitions ---
PURPLE_DARK = "#360042"
HIGHLIGHT_COLOR = "#6A0DAD"
GRAY_LIGHT = "#F0F0F0"
WHITE = "#FFFFFF"
TEXT_COLOR = "#333333"

FONT_TITLE = ("Arial", 16, "bold")
FONT_SUBTITLE = ("Arial", 12, "bold")
FONT_NORMAL = ("Arial", 10)
FONT_PRICE = ("Arial", 14, "bold")
FONT_BUTTON = ("Arial", 14, "bold")

# --- Global variable to hold image references (important for Tkinter) ---
_image_references = {}

# --- Base directory for images (CHANGE THIS TO YOUR ACTUAL DOWNLOADS PATH) ---
# This path needs to be correct for the images to load.
IMAGE_BASE_PATH = "C:/Users/garci/Downloads/" # Ensure this path is accurate

def load_image(filename, size=None):
    """Loads an image from the specified path and resizes it. Returns a PhotoImage object.
       Includes a fallback to a placeholder if the image is not found.
    """
    filepath = os.path.join(IMAGE_BASE_PATH, filename)
    try:
        img = Image.open(filepath)
        if size:
            img = img.resize(size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        # Store a reference to prevent garbage collection
        _image_references[filepath] = photo
        return photo
    except FileNotFoundError:
        print(f"Warning: Image file not found at {filepath}. Using fallback placeholder.")
        if size is None: size = (50, 50)
        placeholder_img = Image.new('RGB', size, (200, 200, 200)) # Grey background
        d = ImageDraw.Draw(placeholder_img)
        try:
            font = ImageFont.truetype("arial.ttf", int(size[1] * 0.3))
        except IOError:
            font = ImageFont.load_default()

        text = filename[0].upper() if filename else "N/A"
        try:
            bbox = d.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            text_width, text_height = d.textsize(text, font=font)
        
        x = (size[0] - text_width) / 2
        y = (size[1] - text_height) / 2
        d.text((x, y), text, fill=(0,0,0), font=font)
        
        photo = ImageTk.PhotoImage(placeholder_img)
        _image_references[filepath + "_fallback"] = photo
        return photo
    except Exception as e:
        print(f"Error loading image {filepath}: {e}. Using fallback placeholder.")
        size = size if size else (50, 50)
        blank_img = Image.new('RGB', size, (200, 200, 200))
        photo = ImageTk.PhotoImage(blank_img)
        _image_references[filepath + "_error_fallback"] = photo
        return photo


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enavroom Booking")
        self.geometry("375x667")
        self.resizable(False, False)
        self.configure(bg=GRAY_LIGHT)

        self.current_selected_vehicle_frame = None
        self.selected_vehicle_type = tk.StringVar(value="")
        self.selected_payment_method = tk.StringVar(value="Cash")

        # --- Top Map Section ---
        map_header_frame = tk.Frame(self, bg=PURPLE_DARK, height=50)
        map_header_frame.pack(fill="x", pady=(0,0))

        map_text_frame = tk.Frame(map_header_frame, bg=PURPLE_DARK)
        map_text_frame.pack(pady=10)

        tk.Label(map_text_frame, text="PUP Main", font=FONT_SUBTITLE, bg=PURPLE_DARK, fg=WHITE).pack(side="left")
        tk.Label(map_text_frame, text=" → ", font=FONT_SUBTITLE, bg=PURPLE_DARK, fg=WHITE).pack(side="left")
        tk.Label(map_text_frame, text="PUP LHS", font=FONT_SUBTITLE, bg=PURPLE_DARK, fg=WHITE).pack(side="left")


        map_image_filename = "main_lhs.png" # Filename for the map image
        map_img = load_image(map_image_filename, (375, 160)) # Resize to fit the UI
        if map_img:
            map_label = tk.Label(self, image=map_img, bg=GRAY_LIGHT)
            map_label.image = map_img
            map_label.pack(fill="x", pady=(0, 0))
        else:
            map_placeholder_label = tk.Label(self, text="Map Placeholder", font=("Arial", 20), bg="lightgray", fg="darkgray")
            map_placeholder_label.pack(fill="both", expand=False)


        # --- Main Content Frame (Scrollable) ---
        canvas = tk.Canvas(self, bg=GRAY_LIGHT, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        self.scrollable_frame = tk.Frame(canvas, bg=GRAY_LIGHT)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # --- Choose your Enavroom Section ---
        tk.Label(self.scrollable_frame, text="Choose your Enavroom", font=FONT_TITLE, bg=GRAY_LIGHT, fg=TEXT_COLOR) \
            .pack(pady=(20, 10))

        self.vehicle_option_frames = []

        # Service Options Data - UPDATED FILENAMES HERE
        service_options = [
            {"icon": "enavroom_price.png", "title": "Enavroom-vroom", "passengers": "1", "description": "Beat the traffic on a motorcycle ride.", "price": "75"},
            {"icon": "car_4.png", "title": "Car (4-seater)", "passengers": "4", "description": "Get around town affordably, up to 4 passengers.", "price": "250"},
            {"icon": "car_6.png", "title": "Car (6-seater)", "passengers": "6", "description": "Roomy and affordable rides for up to six.", "price": "450"},
        ]

        for option_data in service_options:
            frame = self.create_service_option(self.scrollable_frame, **option_data)
            frame.pack(fill="x", padx=20, pady=5)
            self.vehicle_option_frames.append((frame, option_data["title"]))

            frame.bind("<Button-1>", lambda e, f=frame, t=option_data["title"]: self.select_vehicle_option(f, t))
            for widget in frame.winfo_children():
                widget.bind("<Button-1>", lambda e, f=frame, t=option_data["title"]: self.select_vehicle_option(f, t))
                if isinstance(widget, tk.Frame):
                    for child_of_widget in widget.winfo_children():
                        child_of_widget.bind("<Button-1>", lambda e, f=frame, t=option_data["title"]: self.select_vehicle_option(f, t))


        # --- Payment Method Section ---
        payment_frame = tk.Frame(self.scrollable_frame, bg=WHITE, bd=1, relief="solid", padx=10, pady=10)
        payment_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Cash Option - UPDATED FILENAME
        cash_img = load_image("cash.png", (30, 30))
        cash_button_frame = tk.Frame(payment_frame, bg=WHITE)
        cash_button_frame.pack(side="left", expand=True, padx=10)

        if cash_img:
            cash_icon_label = tk.Label(cash_button_frame, image=cash_img, bg=WHITE)
            cash_icon_label.image = cash_img
            cash_icon_label.pack(pady=(0, 5))
        else:
            cash_icon_label = tk.Label(cash_button_frame, text="💵", font=("Arial", 20), bg=WHITE)
            cash_icon_label.pack(pady=(0, 5))

        tk.Label(cash_button_frame, text="Cash", font=FONT_SUBTITLE, bg=WHITE, fg=TEXT_COLOR).pack()
        cash_button_frame.bind("<Button-1>", lambda e: self.select_payment_method("Cash"))
        for widget in cash_button_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: self.select_payment_method("Cash"))


        # Wallet Option - UPDATED FILENAME
        wallet_img = load_image("wallet.png", (30, 30))
        wallet_button_frame = tk.Frame(payment_frame, bg=WHITE)
        wallet_button_frame.pack(side="left", expand=True, padx=10)

        if wallet_img:
            wallet_icon_label = tk.Label(wallet_button_frame, image=wallet_img, bg=WHITE)
            wallet_icon_label.image = wallet_img
            wallet_icon_label.pack(pady=(0, 5))
        else:
            wallet_icon_label = tk.Label(wallet_button_frame, text="👛", font=("Arial", 20), bg=WHITE)
            wallet_icon_label.pack(pady=(0, 5))

        tk.Label(wallet_button_frame, text="Wallet", font=FONT_SUBTITLE, bg=WHITE, fg=TEXT_COLOR).pack()
        wallet_button_frame.bind("<Button-1>", lambda e: self.select_payment_method("Wallet"))
        for widget in wallet_button_frame.winfo_children():
            widget.bind("<Button-1>", lambda e: self.select_payment_method("Wallet"))

        # --- Book Now Button ---
        book_now_button = tk.Button(self.scrollable_frame, text="Book Now", command=self.on_book_now,
                                     font=FONT_BUTTON, bg=PURPLE_DARK, fg=WHITE,
                                     padx=20, pady=15, relief="raised", bd=0, cursor="hand2")
        book_now_button.pack(fill="x", padx=20, pady=(20, 20))

        # Select "Enavroom-vroom" by default
        if self.vehicle_option_frames:
            for frame, title in self.vehicle_option_frames:
                if title == "Enavroom-vroom":
                    self.select_vehicle_option(frame, title)
                    break

    def create_service_option(self, parent, icon, title, passengers, description, price):
        """Creates a clickable service option frame."""
        frame = tk.Frame(parent, bg=WHITE, bd=1, relief="solid",
                         highlightbackground="light grey", highlightthickness=1,
                         padx=10, pady=10)

        icon_size = (40, 40)
        icon_image = load_image(icon, icon_size)
        if icon_image:
            icon_label = tk.Label(frame, image=icon_image, bg=WHITE)
            icon_label.image = icon_image
            icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 10), pady=5, sticky="n")
        else:
            fallback_text = title[0] if title else "?"
            fallback_label = tk.Label(frame, text=fallback_text, font=("Arial", 20, "bold"), bg=WHITE, fg=PURPLE_DARK, width=3, height=2, bd=1, relief="solid")
            fallback_label.grid(row=0, column=0, rowspan=2, padx=(0, 10), pady=5, sticky="n")

        text_frame = tk.Frame(frame, bg=WHITE)
        text_frame.grid(row=0, column=1, rowspan=2, sticky="nw")

        tk.Label(text_frame, text=f"{title}", font=FONT_SUBTITLE, bg=WHITE, fg=TEXT_COLOR, anchor="w").pack(fill="x", expand=True)
        tk.Label(text_frame, text=f"• {passengers} passengers", font=FONT_NORMAL, bg=WHITE, fg="gray", anchor="w").pack(fill="x", expand=True)
        tk.Label(text_frame, text=description, font=FONT_NORMAL, bg=WHITE, fg="gray", anchor="w", wraplength=200, justify="left").pack(fill="x", expand=True)

        tk.Label(frame, text=f"₱{price}", font=FONT_PRICE, bg=WHITE, fg=PURPLE_DARK).grid(row=0, column=2, padx=(10, 0), sticky="ne")

        frame.grid_columnconfigure(1, weight=1)

        return frame

    def select_vehicle_option(self, selected_frame, vehicle_name):
        """Highlights the selected vehicle option and updates the stored value."""
        if self.current_selected_vehicle_frame:
            self.current_selected_vehicle_frame.config(highlightbackground="light grey", highlightthickness=1)

        selected_frame.config(highlightbackground=HIGHLIGHT_COLOR, highlightthickness=2)
        self.current_selected_vehicle_frame = selected_frame
        self.selected_vehicle_type.set(vehicle_name)
        print(f"Selected vehicle: {vehicle_name}")

    def select_payment_method(self, method):
        """Updates the selected payment method."""
        self.selected_payment_method.set(method)
        print(f"Selected payment method: {method}")

    def on_book_now(self):
        selected_vehicle = self.selected_vehicle_type.get()
        selected_payment = self.selected_payment_method.get()

        if not selected_vehicle:
            messagebox.showwarning("Selection Missing", "Please select a vehicle type before booking.")
            return

        confirmation_message = (
            f"Booking Details:\n"
            f"Vehicle: {selected_vehicle}\n"
            f"Payment: {selected_payment}\n"
            f"Confirm your Enavroom booking?"
        )
        if messagebox.askyesno("Confirm Booking", confirmation_message):
            messagebox.showinfo("Success", "Enavroom booked successfully!")
            self.selected_vehicle_type.set("")
            if self.current_selected_vehicle_frame:
                self.current_selected_vehicle_frame.config(highlightbackground="light grey", highlightthickness=1)
                self.current_selected_vehicle_frame = None
            self.selected_payment_method.set("Cash")
        else:
            print("Booking cancelled.")


if __name__ == "__main__":
    app = App()
    app.mainloop()