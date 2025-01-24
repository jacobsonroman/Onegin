# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        # Папки с изображениями
        self.folders = {
            "hair": "C:\\Users\\JR\\hair",
            "eyes": "C:\\Users\\JR\\eyes",
            "nose": "C:\\Users\\JR\\nose",
            "lips": "C:\\Users\\JR\\lips"
        }

        # Холст
        self.canvas = Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Текущее изображение и позиции
        self.current_images = {folder: [] for folder in self.folders.keys()}
        self.image_positions = {folder: None for folder in self.folders.keys()}
        self.active_folder = "hair"

        # Загрузка изображений
        self.load_images()

        # События
        self.root.bind("<MouseWheel>", self.on_mousewheel)
        self.root.bind("<space>", self.on_space)
        self.canvas.bind("<Configure>", self.on_resize)

    def load_images(self):
        for folder, path in self.folders.items():
            for file in os.listdir(path):
                if file.endswith((".png", ".jpg", ".jpeg")):
                    img_path = os.path.join(path, file)
                    image = Image.open(img_path)
                    photo = ImageTk.PhotoImage(image)
                    item = self.canvas.create_image(0, 0, image=photo, anchor=tk.CENTER)
                    self.current_images[folder].append((image, photo, item))
                    self.canvas.itemconfig(item, state='hidden')

        self.display_current_image()

    def display_current_image(self):
        for folder, images in self.current_images.items():
            for img, photo, item in images:
                self.canvas.itemconfig(item, state='hidden')

        for img, photo, item in self.current_images[self.active_folder]:
            self.canvas.itemconfig(item, state='normal')

        self.update_image_positions()

    def update_image_positions(self):
        hair_position = self.image_positions.get("hair")

        if hair_position is None:
            center_x = self.canvas.winfo_width() // 2
            center_y = self.canvas.winfo_height() // 2
            hair_position = (center_x, center_y)
            self.image_positions["hair"] = hair_position
        else:
            center_x = self.canvas.winfo_width() // 2
            center_y = self.canvas.winfo_height() // 2
            hair_dx = center_x - hair_position[0]
            hair_dy = center_y - hair_position[1]
            self.image_positions["hair"] = (center_x, center_y)

            for folder, pos in self.image_positions.items():
                if folder != "hair" and pos is not None:
                    x, y = pos
                    new_x = x + hair_dx
                    new_y = y + hair_dy
                    self.image_positions[folder] = (new_x, new_y)

        for folder, images in self.current_images.items():
            for img, photo, item in images:
                new_x, new_y = self.image_positions[folder]
                self.canvas.coords(item, new_x, new_y)

    def on_mousewheel(self, event):
        if event.state == 0x0008:  # Alt key is pressed
            self.scale_images(1.1 if event.delta > 0 else 0.9, all_images=True)
        elif event.state == 0x0000:  # No modifier key
            self.scale_images(1.1 if event.delta > 0 else 0.9, all_images=False)

    def on_space(self, event):
        self.active_folder = self.next_folder()
        self.display_current_image()

    def scale_images(self, scale_factor, all_images=False):
        if all_images:
            for folder, images in self.current_images.items():
                self.scale_image_folder(folder, scale_factor)
        else:
            self.scale_image_folder(self.active_folder, scale_factor)

    def scale_image_folder(self, folder, scale_factor):
        for i, (image, photo, item) in enumerate(self.current_images[folder]):
            new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
            resized_image = image.resize(new_size, Image.ANTIALIAS)
            self.current_images[folder][i] = (resized_image, ImageTk.PhotoImage(resized_image), item)
            self.canvas.itemconfig(item, image=self.current_images[folder][i][1])

        self.update_image_positions()

    def on_resize(self, event):
        self.update_image_positions()

    def next_folder(self):
        folders = list(self.folders.keys())
        next_index = (folders.index(self.active_folder) + 1) % len(folders)
        return folders[next_index]

if __name__ == "__main__":
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()