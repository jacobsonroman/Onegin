import tkinter as tk
from tkinter import messagebox
import random

class GoldenRatioTrainer:
    def __init__(self, master):
        self.master = master
        master.title("Тренажер золотого сечения")
        
        self.example_canvas = tk.Canvas(master, width=600, height=200, bg="white")
        self.example_canvas.pack()
        
        self.training_canvas = tk.Canvas(master, width=600, height=200, bg="white")
        self.training_canvas.pack()
        
        self.check_button = tk.Button(master, text="Проверить точность", command=self.check_accuracy)
        self.check_button.pack()
        
        self.clear_button = tk.Button(master, text="Очистить", command=self.clear_training)
        self.clear_button.pack()
        
        self.example_lines = []
        self.training_lines = []
        self.current_line = None
        
        self.generate_example_lines()
        
        self.training_canvas.bind("<Button-1>", self.start_line)
        self.training_canvas.bind("<B1-Motion>", self.draw_line)
        self.training_canvas.bind("<ButtonRelease-1>", self.end_line)
    
    def generate_example_lines(self):
        x1 = random.randint(50, 150)
        for i in range(5):
            length = x1 * (1.618 ** i)
            line = self.example_canvas.create_line(10, 30 + i*40, 10 + length, 30 + i*40, width=2)
            self.example_lines.append(line)
    
    def start_line(self, event):
        self.current_line = self.training_canvas.create_line(event.x, event.y, event.x, event.y)
    
    def draw_line(self, event):
        x, y = self.training_canvas.coords(self.current_line)[:2]
        self.training_canvas.coords(self.current_line, x, y, event.x, event.y)
    
    def end_line(self, event):
        if self.current_line:
            self.training_lines.append(self.current_line)
            self.current_line = None
    
    def clear_training(self):
        for line in self.training_lines:
            self.training_canvas.delete(line)
        self.training_lines = []
    
    def check_accuracy(self):
        if len(self.training_lines) != 5:
            messagebox.showwarning("Предупреждение", "Пожалуйста, нарисуйте 5 линий")
            return
        
        accuracies = []
        for i, (example_line, training_line) in enumerate(zip(self.example_lines, self.training_lines)):
            example_length = self.example_canvas.coords(example_line)[2] - self.example_canvas.coords(example_line)[0]
            training_length = self.training_canvas.coords(training_line)[2] - self.training_canvas.coords(training_line)[0]
            accuracy = min(example_length, training_length) / max(example_length, training_length) * 100
            accuracies.append(accuracy)
            
            # Отображение точности рядом с каждой линией
            self.training_canvas.create_text(
                self.training_canvas.coords(training_line)[2] + 10,
                self.training_canvas.coords(training_line)[1],
                text=f"{accuracy:.1f}%"
            )
        
        average_accuracy = sum(accuracies) / len(accuracies)
        messagebox.showinfo("Результат", f"Средняя точность: {average_accuracy:.1f}%")

def main():
    root = tk.Tk()
    app = GoldenRatioTrainer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
