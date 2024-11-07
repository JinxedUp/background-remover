import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from rembg import remove
import io
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import itertools


class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("background remover made by Jinx")
        self.root.geometry("600x550")
        self.root.configure(bg='#1e1e1e')

        self.upload_btn = ttk.Button(root, text="Upload Image", command=self.upload_image, bootstyle="dark-outline",
                                     width=30, padding=10)
        self.upload_btn.pack(pady=20)

        self.image_label = tk.Label(root, text="No Image Uploaded", font=("Arial", 12), bg='#1e1e1e', fg='white')
        self.image_label.pack(pady=10)

        self.loading_label = tk.Label(root, font=("Arial", 14, "italic"), bg='#1e1e1e', fg='#00ff00')

        self.loading_animation = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

        self.made_by_label = tk.Label(root, text="Made by Jinx", font=("Arial", 10, "italic"), bg='#1e1e1e',
                                      fg='#00ff00')
        self.processed_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_label.config(image='', text="Processing...")
            self.loading_label.pack(pady=10)
            self.animate_loading()
            thread = threading.Thread(target=self.process_image, args=(file_path,))
            thread.start()

    def process_image(self, file_path):
        original_image = Image.open(file_path)
        img_bytes = io.BytesIO()
        original_image.save(img_bytes, format='PNG')
        img_no_bg = remove(img_bytes.getvalue())
        self.processed_image = Image.open(io.BytesIO(img_no_bg))
        self.display_image(self.processed_image)
        self.upload_btn.config(text="Save Image", command=self.save_image)

    def display_image(self, img):
        img.thumbnail((400, 300))
        img_tk = ImageTk.PhotoImage(img)
        self.image_label.config(image=img_tk, text='')
        self.image_label.image = img_tk
        self.loading_label.pack_forget()
        self.made_by_label.pack(pady=10)

    def save_image(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Files", "*.png")])
        if save_path:
            self.processed_image.save(save_path)
            messagebox.showinfo("Image Saved", f"Image saved to {save_path}")

    def animate_loading(self):
        self.loading_label.config(text=next(self.loading_animation))
        self.root.after(100, self.animate_loading)


if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = BackgroundRemoverApp(root)
    root.mainloop()
