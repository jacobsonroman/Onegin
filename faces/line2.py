
# -*- coding: utf-8 -*-
import tkinter as tk
import random
import math

class GoldenRatioWorkshop:
    def __init__(self, master):
        self.master = master
        self.master.title("Golden Ratio Workshop")
        self.master.geometry("800x600")

        self.canvas = tk.Canvas(self.master, width=800, height=550, bg="white")
        self.canvas.pack()

        self.accuracy_button = tk.Button(self.master, text="Check Accuracy", command=self.check_accuracy)
        self.accuracy_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.refresh_button = tk.Button(self.master, text="Refresh Task", command=self.refresh_task)
        self.refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(self.master, text="Next Stage", command=self.next_stage)
        self.next_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.stages = [Stage1(self.canvas), Stage2(self.canvas), Stage3(self.canvas)]
        self.current_stage = 0

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.show_hint)
        self.canvas.bind("<ButtonRelease-3>", self.hide_hint)

        self.refresh_task()

    def refresh_task(self):
        self.canvas.delete("all")
        self.stages[self.current_stage].setup()

    def check_accuracy(self):
        self.stages[self.current_stage].check_accuracy()

    def next_stage(self):
        self.current_stage = (self.current_stage + 1) % len(self.stages)
        self.refresh_task()

    def on_click(self, event):
        self.stages[self.current_stage].on_click(event)

    def on_drag(self, event):
        self.stages[self.current_stage].on_drag(event)

    def on_release(self, event):
        self.stages[self.current_stage].on_release(event)

    def show_hint(self, event):
        self.stages[self.current_stage].show_hint()

    def hide_hint(self, event):
        self.stages[self.current_stage].hide_hint()

class Stage1:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lines = []
        self.colors = ["red", "blue", "green", "orange", "purple"]
        self.hint_lines = []
        self.accuracy_texts = []

    def setup(self):
        self.canvas.delete("all")
        self.lines = []
        self.accuracy_texts = []
        start_x, start_y = 100, 100
        length = random.randint(200, 400)
        self.canvas.create_line(start_x, start_y, start_x + length, start_y, width=2)
        self.canvas.create_text(400, 50, text="Draw 5 lines in golden ratio proportion", font=("Arial", 14))

    def on_click(self, event):
        if len(self.lines) < 5:
            x, y = event.x, event.y
            line = self.canvas.create_line(x, y, x, y, fill=self.colors[len(self.lines)], width=2)
            self.lines.append(line)
            self.accuracy_texts.append(self.canvas.create_text(x, y-15, text="", font=("Arial", 10), fill=self.colors[len(self.lines)-1]))

    def on_drag(self, event):
        if self.lines:
            x, y = event.x, event.y
            x1, y1, _, _ = self.canvas.coords(self.lines[-1])
            self.canvas.coords(self.lines[-1], x1, y1, x, y)
            self.canvas.coords(self.accuracy_texts[-1], (x1 + x) / 2, y1 - 15)

    def on_release(self, event):
        self.check_accuracy()

    def show_hint(self):
        if not self.hint_lines:
            start_x, start_y = 100, 100
            length = self.canvas.coords(self.canvas.find_all()[0])[2] - start_x
            for i in range(5):
                length /= 1.618
                self.hint_lines.append(self.canvas.create_line(start_x, start_y + 30 * (i + 1), 
                                                               start_x + length, start_y + 30 * (i + 1), 
                                                               dash=(5,5), fill="gray"))

    def hide_hint(self):
        for line in self.hint_lines:
            self.canvas.delete(line)
        self.hint_lines = []

    def check_accuracy(self):
        ideal_lengths = [self.canvas.coords(self.canvas.find_all()[0])[2] - 100]
        for _ in range(4):
            ideal_lengths.append(ideal_lengths[-1] / 1.618)

        for i, (line, text) in enumerate(zip(self.lines, self.accuracy_texts)):
            user_length = self.canvas.coords(line)[2] - self.canvas.coords(line)[0]
            accuracy = min(user_length / ideal_lengths[i], ideal_lengths[i] / user_length) * 100
            self.canvas.itemconfig(text, text=f"{accuracy:.1f}%")

class Stage2:
    def __init__(self, canvas):
        self.canvas = canvas
        self.marks = []
        self.hint_marks = []
        self.accuracy_texts = []

    def setup(self):
        self.canvas.delete("all")
        self.marks = []
        self.accuracy_texts = []
        start_x, start_y = 100, 300
        length = random.randint(400, 600)
        self.canvas.create_line(start_x, start_y, start_x + length, start_y, width=2)
        self.canvas.create_text(400, 50, text="Mark 6 proportional segments on the line", font=("Arial", 14))

    def on_click(self, event):
        x, y = event.x, event.y
        line_coords = self.canvas.coords(self.canvas.find_all()[0])
        if len(self.marks) < 5 and line_coords[0] <= x <= line_coords[2] and abs(y - line_coords[1]) < 10:
            mark = self.canvas.create_line(x, y - 10, x, y + 10, fill="red", width=2)
            self.marks.append(mark)
            self.accuracy_texts.append(self.canvas.create_text(x, y-20, text="", font=("Arial", 10), fill="red"))
            self.check_accuracy()

    def on_drag(self, event):
        pass

    def on_release(self, event):
        pass

    def show_hint(self):
        if not self.hint_marks:
            line_coords = self.canvas.coords(self.canvas.find_all()[0])
            start_x, length = line_coords[0], line_coords[2] - line_coords[0]
            for i in range(1, 6):
                x = start_x + length * (1 - 1 / (1.618 ** i))
                self.hint_marks.append(self.canvas.create_line(x, line_coords[1] - 15, x, line_coords[1] + 15, 
                                                               dash=(5,5), fill="gray"))

    def hide_hint(self):
        for mark in self.hint_marks:
            self.canvas.delete(mark)
        self.hint_marks = []

    def check_accuracy(self):
        line_coords = self.canvas.coords(self.canvas.find_all()[0])
        start_x, length = line_coords[0], line_coords[2] - line_coords[0]

        ideal_positions = [start_x + length * (1 - 1 / (1.618 ** i)) for i in range(1, 6)]
        user_positions = [self.canvas.coords(mark)[0] for mark in self.marks]

        for i, (user_pos, text) in enumerate(zip(user_positions, self.accuracy_texts)):
            accuracy = (1 - abs(user_pos - ideal_positions[i]) / length) * 100
            self.canvas.itemconfig(text, text=f"{accuracy:.1f}%")

class Stage3:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lines = []
        self.arrows = []
        self.colors = ["red", "blue", "green", "orange", "purple"]
        self.selected_line = None
        self.hint_lines = []
        self.accuracy_texts = []

    def setup(self):
        self.canvas.delete("all")
        self.lines = []
        self.arrows = []
        self.accuracy_texts = []
        start_y = 100
        for i in range(5):
            length = random.randint(100, 400)
            line = self.canvas.create_line(100, start_y, 100 + length, start_y, fill=self.colors[i], width=2)
            self.lines.append(line)
            arrow = self.canvas.create_line(100 + length - 10, start_y - 5, 100 + length, start_y, 100 + length - 10, start_y + 5, fill=self.colors[i], width=2)
            self.arrows.append(arrow)
            self.accuracy_texts.append(self.canvas.create_text(100 + length/2, start_y - 15, text="", font=("Arial", 10), fill=self.colors[i]))
            start_y += 60
        self.canvas.create_text(400, 50, text="Adjust lines to golden ratio proportion", font=("Arial", 14))
        self.check_accuracy()

    def on_click(self, event):
        self.selected_line = None
        for line in self.lines:
            coords = self.canvas.coords(line)
            if coords[0] <= event.x <= coords[2] and abs(event.y - coords[1]) < 10:
                self.selected_line = line
                break

    def on_drag(self, event):
        if self.selected_line:
            index = self.lines.index(self.selected_line)
            coords = self.canvas.coords(self.selected_line)
            new_length = max(10, event.x - coords[0])
            self.canvas.coords(self.selected_line, coords[0], coords[1], coords[0] + new_length, coords[3])
            self.canvas.coords(self.arrows[index], coords[0] + new_length - 10, coords[1] - 5, coords[0] + new_length, coords[1], coords[0] + new_length - 10, coords[1] + 5)
            self.canvas.coords(self.accuracy_texts[index], coords[0] + new_length/2, coords[1] - 15)
            self.check_accuracy()

    def on_release(self, event):
        self.selected_line = None

    def show_hint(self):
        if not self.hint_lines:
            start_y = 100
            ideal_length = self.canvas.coords(self.lines[0])[2] - self.canvas.coords(self.lines[0])[0]
            for i in range(5):
                self.hint_lines.append(self.canvas.create_line(100, start_y + 30, 100 + ideal_length, start_y + 30, 
                                                               dash=(5,5), fill="gray"))
                ideal_length /= 1.618
                start_y += 60

    def hide_hint(self):
        for line in self.hint_lines:
            self.canvas.delete(line)
        self.hint_lines = []

    def check_accuracy(self):
        lengths = [self.canvas.coords(line)[2] - self.canvas.coords(line)[0] for line in self.lines]
        ideal_ratio = 1.618
        for i in range(4):
            ratio = lengths[i] / lengths[i+1]
            accuracy = min(ratio / ideal_ratio, ideal_ratio / ratio) * 100
            self.canvas.itemconfig(self.accuracy_texts[i], text=f"{accuracy:.1f}%")
        self.canvas.itemconfig(self.accuracy_texts[4], text="")  # Last line doesn't have a ratio

if __name__ == "__main__":
    root = tk.Tk()
    app = GoldenRatioWorkshop(root)
    root.mainloop()