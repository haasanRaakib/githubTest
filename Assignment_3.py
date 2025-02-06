import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import numpy as np

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1200x600")  # Adjust window size to fit all elements

        # Frame for the canvas
        self.canvas_frame = tk.Frame(root, bg="gray")
        self.canvas_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, width=1000, height=400, bg="gray")
        self.canvas.pack()

        # Frame for buttons (horizontal layout)
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, padx=20, pady=10)

        # Load Button
        self.load_button = tk.Button(self.button_frame, text="Load Image", command=self.load_image, width=15)
        self.load_button.grid(row=0, column=0, padx=5)

        # Crop Button
        self.crop_button = tk.Button(self.button_frame, text="Crop Image", command=self.start_crop, width=15)
        self.crop_button.grid(row=0, column=1, padx=5)

        # Undo Button
        self.undo_button = tk.Button(self.button_frame, text="Undo", command=self.undo, width=15)
        self.undo_button.grid(row=0, column=2, padx=5)

        # Redo Button
        self.redo_button = tk.Button(self.button_frame, text="Redo", command=self.redo, width=15)
        self.redo_button.grid(row=0, column=3, padx=5)

        # Save Button
        self.save_button = tk.Button(self.button_frame, text="Save Image", command=self.save_image, width=15)
        self.save_button.grid(row=0, column=4, padx=5)

        # Grayscale Button
        self.grayscale_button = tk.Button(self.button_frame, text="Grayscale", command=self.apply_grayscale, width=15)
        self.grayscale_button.grid(row=0, column=5, padx=5)

        # Blur Button
        self.blur_button = tk.Button(self.button_frame, text="Blur", command=self.apply_blur, width=15)
        self.blur_button.grid(row=0, column=6, padx=5)

        # Edge Detection Button
        self.edge_button = tk.Button(self.button_frame, text="Edge Detection", command=self.apply_edge_detection, width=15)
        self.edge_button.grid(row=0, column=7, padx=5)

        # Initialize slider for resizing the preview of the cropped image
        self.resize_slider = tk.Scale(root, from_=10, to=300, orient="horizontal", label="Resize Preview", length=400)
        self.resize_slider.set(100)  # Default value: 100% scale
        self.resize_slider.pack(padx=20, pady=10)
        self.resize_slider.bind("<Motion>", self.update_preview_size)  # Update preview on slider move

        self.image = None
        self.tk_image = None
        self.cropped_image = None
        self.history = []
        self.future = []

        self.cropping = False
        self.start_x = self.start_y = self.end_x = self.end_y = 0

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.history = [self.image.copy()]
            self.future.clear()
            self.display_image()

    def display_image(self):
        if self.image is not None:
            self.canvas.delete("all")
            image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            image_pil.thumbnail((500, 400))
            self.tk_image = ImageTk.PhotoImage(image_pil)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            if self.cropped_image is not None:
                self.display_cropped_image()

    def display_cropped_image(self):
        cropped_rgb = cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB)
        cropped_pil = Image.fromarray(cropped_rgb)

        # Resize preview based on slider value
        scale_percentage = self.resize_slider.get()
        new_width = int(cropped_pil.width * (scale_percentage / 100))
        new_height = int(cropped_pil.height * (scale_percentage / 100))

        cropped_pil = cropped_pil.resize((new_width, new_height))

        self.tk_cropped_image = ImageTk.PhotoImage(cropped_pil)
        self.canvas.create_image(500, 0, anchor=tk.NW, image=self.tk_cropped_image)

    def start_crop(self):
        if self.image is not None:
            self.cropping = True
        else:
            messagebox.showerror("Error", "Load an image first!")

    def on_press(self, event):
        if self.cropping:
            self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        if self.cropping:
            self.end_x, self.end_y = event.x, event.y
            self.canvas.delete("selection_overlay")
            self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline="red", tags="selection_overlay")

    def on_release(self, event):
        if self.cropping:
            self.end_x, self.end_y = event.x, event.y
            self.crop_selected_area()
            self.cropping = False

    def crop_selected_area(self):
        if self.image is not None and self.start_x != self.end_x and self.start_y != self.end_y:
            x1, x2 = sorted([self.start_x, self.end_x])
            y1, y2 = sorted([self.start_y, self.end_y])
            canvas_width, canvas_height = 500, 400
            image_height, image_width = self.image.shape[:2]
            x_ratio = image_width / canvas_width
            y_ratio = image_height / canvas_height
            x1, x2 = int(x1 * x_ratio), int(x2 * x_ratio)
            y1, y2 = int(y1 * y_ratio), int(y2 * y_ratio)
            if x2 - x1 > 5 and y2 - y1 > 5:
                self.history.append(self.image.copy())  # Add the image to history before cropping
                self.future.clear()  # Clear the redo stack on new modification
                self.cropped_image = self.image[y1:y2, x1:x2]
                self.display_image()
            else:
                messagebox.showerror("Error", "Invalid crop selection! Select a larger area.")

    def update_preview_size(self, event):
        """ Called when the slider is moved to resize the cropped image preview. """
        if self.cropped_image is not None:
            self.display_cropped_image()

    def undo(self):
        # Undo functionality here
        if len(self.history) > 1:
            self.future.append(self.history.pop())  # Push the current image to future
            self.image = self.history[-1].copy()  # Get the previous image from history
            self.cropped_image = None  # Reset cropped image on undo
            self.display_image()
        else:
            messagebox.showinfo("Undo", "No more actions to undo!")

    def redo(self):
        if self.future:
            self.history.append(self.future.pop())  # Push the image from future back to history
            self.image = self.history[-1].copy()  # Get the image to redo
            self.display_image()
        else:
            messagebox.showinfo("Redo", "No actions to redo!")

    def apply_grayscale(self):
        """ Converts the image to grayscale. """
        if self.image is not None:
            self.history.append(self.image.copy())
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            self.display_image()

    def apply_blur(self):
        """ Applies a blur effect to the image. """
        if self.image is not None:
            self.history.append(self.image.copy())
            self.image = cv2.GaussianBlur(self.image, (15, 15), 0)
            self.display_image()

    def apply_edge_detection(self):
        """ Applies edge detection to the image. """
        if self.image is not None:
            self.history.append(self.image.copy())
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.display_image()

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, self.cropped_image if self.cropped_image is not None else self.image)
            messagebox.showinfo("Success", "Image saved successfully!")



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()