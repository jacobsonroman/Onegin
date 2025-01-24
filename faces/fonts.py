# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font

class FontViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Font Viewer")

        # ������� ����� ��� ���������� ��������
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # ������� ������ ���������
        self.canvas = tk.Canvas(self.frame, width=800, height=600)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # ��������� ������ ��������� � ����� � ������
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # ������� ����� � ������ ��� ����������� ������
        self.canvas_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor=tk.NW)

        # ���������� ��������� ������� ����
        self.bind("<Configure>", self.on_resize)

        self.fonts = font.families()
        self.font_vars = {}
        self.checkbuttons = []

        # ������� ������� �������
        self.master_var = tk.BooleanVar(value=True)
        self.master_checkbutton = tk.Checkbutton(self.canvas_frame, text="Select all", variable=self.master_var, command=self.toggle_all_fonts)
        self.master_checkbutton.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.create_font_list()
        self.show_all_fonts()

        # ������ ��� ����������� ������ ��������� �������
        self.filter_button = tk.Button(self, text="Selected", command=self.filter_fonts)
        self.filter_button.pack(side=tk.BOTTOM, pady=10)

        # ������ ��� ����������� ���� �������
        self.show_all_button = tk.Button(self, text="Show all", command=self.show_all_fonts)
        self.show_all_button.pack(side=tk.BOTTOM)

    def create_font_list(self):
        y_position = 1
        for font_name in self.fonts:
            var = tk.BooleanVar(value=True)
            self.font_vars[font_name] = var

            # �������� ����� ��� ������� ������
            text_label = tk.Label(self.canvas_frame, text="Onegin.ai", font=(font_name, 32))  # ����������� ������ ������ � 2 ����
            font_name_label = tk.Label(self.canvas_frame, text=font_name, font=("Arial", 12))
            checkbutton = tk.Checkbutton(self.canvas_frame, text="", variable=var, onvalue=True, offvalue=False)

            text_label.grid(row=y_position, column=1, sticky=tk.W, padx=10, pady=5)
            font_name_label.grid(row=y_position, column=2, sticky=tk.W, padx=10, pady=5)
            checkbutton.grid(row=y_position, column=0, padx=10, pady=5)

            self.checkbuttons.append((font_name, text_label, font_name_label, checkbutton))
            y_position += 1  # ��������� �� y

        # ��������� ������� ���������
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_resize(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def filter_fonts(self):
        for font_name, text_label, font_name_label, checkbutton in self.checkbuttons:
            if self.font_vars[font_name].get():
                text_label.grid()
                font_name_label.grid()
                checkbutton.grid()
            else:
                text_label.grid_remove()
                font_name_label.grid_remove()
                checkbutton.grid_remove()

    def show_all_fonts(self):
        for font_name, text_label, font_name_label, checkbutton in self.checkbuttons:
            text_label.grid()
            font_name_label.grid()
            checkbutton.grid()

    def toggle_all_fonts(self):
        all_checked = self.master_var.get()
        for font_name, _, _, checkbutton in self.checkbuttons:
            self.font_vars[font_name].set(all_checked)
        self.filter_fonts()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = FontViewer()
    app.run()