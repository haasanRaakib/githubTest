import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unconventional Image Processor")
        self.root.geometry("1000x600")  # Increased size to accommodate both images

        # Image variables
        self.original_image = None
        self.cropped_image = None
        self.display_image = None
        self.selection_rect = None
        self.selection_in_progress = False
        self.mask = None

        # GUI Elements
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=400)
        self.canvas.pack(pady=10)

        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo, state=tk.DISABLED)
        self.undo_button.pack(side=tk.LEFT, padx=10)

        self.redo_button = tk.Button(self.root, text="Redo", command=self.redo, state=tk.DISABLED)
        self.redo_button.pack(side=tk.LEFT, padx=10)

        self.resize_slider = tk.Scale(self.root, from_=10, to=100, orient=tk.HORIZONTAL, label="Resize Quality", command=self.resize_image)
        self.resize_slider.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Mouse bindings for cropping
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)

        # undo/redo history
        self.undo_stack = []
        self.redo_stack = []

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.display_image = self.original_image.copy()
            self.show_image(self.display_image)
            self.save_button.config(state=tk.NORMAL)
            self.undo_button.config(state=tk.NORMAL)
            self.redo_button.config(state=tk.NORMAL)

    def show_image(self, image, save_state=True):
        """Displays an image and saves state for undo/redo."""
        if save_state:
            self.undo_stack.append(self.display_image.copy())  # Save previous state

        self.display_image = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.image = image

        # Enable/disable buttons based on history
        self.undo_button.config(state=tk.NORMAL if self.undo_stack else tk.DISABLED)
        self.redo_button.config(state=tk.NORMAL if self.redo_stack else tk.DISABLED)

    def start_selection(self, event):
        """Start the selection of the cropping area."""
        self.selection_in_progress = True
        self.selection_rect = (event.x, event.y, event.x, event.y)

    def update_selection(self, event):
        """Update the selection area dynamically."""
        if self.selection_in_progress:
            x0, y0, _, _ = self.selection_rect
            self.selection_rect = (x0, y0, event.x, event.y)
            self.draw_selection()

    def end_selection(self, event):
        """End the selection and crop the image."""
        if self.selection_in_progress:
            self.selection_in_progress = False
            self.crop_image()

    def draw_selection(self):
        """Draw the selection rectangle and inverse mask."""
        self.canvas.delete("selection")
        x0, y0, x1, y1 = self.selection_rect
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="selection")

        # Create a mask where the selected area is white, and the rest is black
        mask = np.zeros(self.display_image.shape[:2], dtype=np.uint8)  # Create an empty binary mask (grayscale)
        cv2.rectangle(mask, (x0, y0), (x1, y1), 255, -1)  # Fill the selected area with white (255)

        # Invert the mask to show everything except the selected area
        inverse_mask = cv2.bitwise_not(mask)

        # Show the inverse mask on the image
        inverse_result = cv2.bitwise_and(self.display_image, self.display_image, mask=inverse_mask)
        self.show_image(inverse_result, save_state=False)


    def crop_image(self):
        """Crop the image using the selected rectangle."""
        if self.original_image is None:
            return

        x0, y0, x1, y1 = self.selection_rect

        # Ensure coordinates are within bounds
        x0, x1 = sorted([max(0, x0), min(self.original_image.shape[1], x1)])
        y0, y1 = sorted([max(0, y0), min(self.original_image.shape[0], y1)])

        if x0 < x1 and y0 < y1:  # Valid selection
            self.cropped_image = self.original_image[y0:y1, x0:x1].copy()

            # Show original image alongside cropped image
            self.show_side_by_side()

    def show_side_by_side(self):
        """Show the original and cropped images side by side."""
        original_image_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        cropped_image_rgb = cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB)

        # Convert to ImageTk format
        original_image_pil = Image.fromarray(original_image_rgb)
        cropped_image_pil = Image.fromarray(cropped_image_rgb)

        original_image_tk = ImageTk.PhotoImage(original_image_pil)
        cropped_image_tk = ImageTk.PhotoImage(cropped_image_pil)

        # Clear canvas and display both images side by side
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=original_image_tk)
        self.canvas.create_image(400, 0, anchor=tk.NW, image=cropped_image_tk)

        # Keep references for images to prevent garbage collection
        self.canvas.original_image = original_image_tk
        self.canvas.cropped_image = cropped_image_tk

    def resize_image(self, value):
        if self.cropped_image is None:
            return  # If no cropped image, don't do anything
    
        scale_percent = int(value)  # Convert slider value to percentage
        width = int(self.cropped_image.shape[1] * scale_percent / 100)
        height = int(self.cropped_image.shape[0] * scale_percent / 100)
    
        if width > 0 and height > 0:
            resized = cv2.resize(self.cropped_image, (width, height), interpolation=cv2.INTER_AREA)
            self.show_image(resized, save_state=False)


    def save_image(self):
        """Save the cropped image."""
        if self.cropped_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if file_path:
                cv2.imwrite(file_path, self.cropped_image)
                messagebox.showinfo("Success", "Image saved successfully!")

    def undo(self, event=None):
        """Undo the last change."""
        if self.undo_stack:
            self.redo_stack.append(self.display_image.copy())  # Save current state for redo
            last_image = self.undo_stack.pop()
            self.show_image(last_image, save_state=False)

    def redo(self, event=None):
        """Redo the last undone change."""
        if self.redo_stack:
            self.undo_stack.append(self.display_image.copy())  # Save current state for undo
            last_redo = self.redo_stack.pop()
            self.show_image(last_redo, save_state=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
