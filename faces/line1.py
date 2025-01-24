import tkinter as tk
import random
import math

class GoldenRatioTrainer:
    def __init__(self, master):
        self.master = master
        self.master.title("Golden Ratio Trainer")
        self.master.geometry("800x600")

        self.canvas = tk.Canvas(self.master, width=800, height=550, bg="white")
        self.canvas.pack()

        self.instruction = self.canvas.create_text(400, 30, text="Split the line in golden ratio proportion", font=("Arial", 14))

        self.accuracy_button = tk.Button(self.master, text="Check Accuracy", command=self.check_accuracy)
        self.accuracy_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.refresh_button = tk.Button(self.master, text="Refresh Task", command=self.refresh_task)
        self.refresh_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.line = None
        self.user_mark = None
        self.start_point = None
        self.end_point = None
        self.accuracy_text = None
        self.hint_markers = []

        self.refresh_task()

        self.canvas.bind("<Button-1>", self.place_mark)
        self.canvas.bind("<Button-3>", self.show_hint_markers)
        self.canvas.bind("<ButtonRelease-3>", self.hide_hint_markers)

    def refresh_task(self):
        self.canvas.delete("all")
        
        self.instruction = self.canvas.create_text(400, 30, text="Split the line in golden ratio proportion", font=("Arial", 14))
        
        x1, y1 = random.randint(50, 750), random.randint(100, 450)
        x2, y2 = random.randint(50, 750), random.randint(100, 450)
        
        while math.sqrt((x2-x1)**2 + (y2-y1)**2) < 200:
            x2, y2 = random.randint(50, 750), random.randint(100, 450)
        
        self.start_point = (x1, y1)
        self.end_point = (x2, y2)
        
        self.line = self.canvas.create_line(x1, y1, x2, y2, width=2)
        self.user_mark = None
        self.hint_markers = []
        if self.accuracy_text:
            self.canvas.delete(self.accuracy_text)
            self.accuracy_text = None

    def place_mark(self, event):
        if self.user_mark:
            self.canvas.delete(self.user_mark)
        if self.accuracy_text:
            self.canvas.delete(self.accuracy_text)
            self.accuracy_text = None
        
        x, y = event.x, event.y
        self.user_mark = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")

    def check_accuracy(self):
        if not self.user_mark:
            self.show_accuracy("Please place a mark on the line first")
            return

        x, y = self.canvas.coords(self.user_mark)[:2]
        total_length = self.distance(self.start_point, self.end_point)
        segment1 = self.distance(self.start_point, (x, y))
        segment2 = self.distance(self.end_point, (x, y))

        if segment1 > segment2:
            user_ratio = segment1 / segment2
        else:
            user_ratio = segment2 / segment1

        golden_ratio = (1 + math.sqrt(5)) / 2

        accuracy = 100 - abs(user_ratio - golden_ratio) / golden_ratio * 100
        self.show_accuracy(f"Your accuracy: {accuracy:.2f}%")

    def show_accuracy(self, text):
        if self.accuracy_text:
            self.canvas.delete(self.accuracy_text)
        self.accuracy_text = self.canvas.create_text(400, 520, text=text, font=("Arial", 12))

    def show_hint_markers(self, event):
        if self.hint_markers:
            return

        total_length = self.distance(self.start_point, self.end_point)
        golden_ratio = (1 + math.sqrt(5)) / 2
        short_segment = total_length / golden_ratio

        angle = math.atan2(self.end_point[1] - self.start_point[1], self.end_point[0] - self.start_point[0])
        dx = short_segment * math.cos(angle)
        dy = short_segment * math.sin(angle)

        # First marker (from start point)
        marker_point1 = (self.start_point[0] + dx, self.start_point[1] + dy)
        self.hint_markers.append(self.canvas.create_oval(marker_point1[0]-5, marker_point1[1]-5, 
                                                         marker_point1[0]+5, marker_point1[1]+5, 
                                                         fill="green", outline="green"))
        self.hint_markers.append(self.canvas.create_text(marker_point1[0], marker_point1[1]-15, 
                                                         text="Golden Ratio Point", 
                                                         font=("Arial", 10), fill="green"))

        # Second marker (from end point)
        marker_point2 = (self.end_point[0] - dx, self.end_point[1] - dy)
        self.hint_markers.append(self.canvas.create_oval(marker_point2[0]-5, marker_point2[1]-5, 
                                                         marker_point2[0]+5, marker_point2[1]+5, 
                                                         fill="green", outline="green"))
        self.hint_markers.append(self.canvas.create_text(marker_point2[0], marker_point2[1]+15, 
                                                         text="Golden Ratio Point", 
                                                         font=("Arial", 10), fill="green"))

    def hide_hint_markers(self, event):
        for marker in self.hint_markers:
            self.canvas.delete(marker)
        self.hint_markers = []

    @staticmethod
    def distance(p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

if __name__ == "__main__":
    root = tk.Tk()
    app = GoldenRatioTrainer(root)
    root.mainloop()