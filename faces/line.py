# -*- coding: utf-8 -*-
import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (240, 240, 240)
LINE_COLOR = (0, 0, 0)
BUTTON_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Golden Ratio Trainer")

class Line:
    def __init__(self, start, end, angle):
        self.start = start
        self.end = end
        self.angle = angle
        self.user_divisions = []
        self.correct_divisions = []
        self.is_dragging = False
        self.drag_offset = (0, 0)

    def calculate_correct_divisions(self):
        length = math.hypot(self.end[0] - self.start[0], self.end[1] - self.start[1])
        num_divisions = random.randint(5, 7)
        self.correct_divisions = []
        current_length = length
        for _ in range(num_divisions - 1):
            division_point = current_length / GOLDEN_RATIO
            dx = math.cos(self.angle) * (length - current_length + division_point)
            dy = math.sin(self.angle) * (length - current_length + division_point)
            self.correct_divisions.append((self.start[0] + dx, self.start[1] + dy))
            current_length = division_point

    def draw(self, surface, show_hint):
        pygame.draw.line(surface, LINE_COLOR, self.start, self.end, 2)
        if show_hint:
            for point in self.correct_divisions:
                draw_tick(surface, point, self.angle, (255, 0, 0))
        for point in self.user_divisions:
            draw_tick(surface, point, self.angle, (0, 0, 255))

    def move(self, dx, dy):
        self.start = (self.start[0] + dx, self.start[1] + dy)
        self.end = (self.end[0] + dx, self.end[1] + dy)
        self.correct_divisions = [(x + dx, y + dy) for x, y in self.correct_divisions]
        self.user_divisions = [(x + dx, y + dy) for x, y in self.user_divisions]

    def is_point_on_line(self, point):
        x, y = point
        x1, y1 = self.start
        x2, y2 = self.end
        d1 = math.hypot(x - x1, y - y1)
        d2 = math.hypot(x2 - x, y2 - y)
        line_length = math.hypot(x2 - x1, y2 - y1)
        buffer = 0.1
        return abs(d1 + d2 - line_length) < buffer

def draw_tick(surface, point, angle, color):
    tick_length = 10
    dx = math.sin(angle) * tick_length
    dy = -math.cos(angle) * tick_length
    start = (point[0] - dx, point[1] - dy)
    end = (point[0] + dx, point[1] + dy)
    pygame.draw.line(surface, color, start, end, 2)

def generate_line(attempt):
    margin = 100
    min_length = 200
    max_attempts = 100

    for _ in range(max_attempts):
        if attempt % 3 == 0:
            # Горизонтальные линии
            start = (random.randint(margin, WIDTH - margin - min_length), random.randint(margin, HEIGHT - margin))
            end = (start[0] + random.randint(min_length, min(WIDTH - start[0] - margin, 400)), start[1])
            angle = 0
        elif attempt % 3 == 1:
            # Вертикальные линии
            start = (random.randint(margin, WIDTH - margin), random.randint(margin, HEIGHT - margin - min_length))
            end = (start[0], start[1] + random.randint(min_length, min(HEIGHT - start[1] - margin, 400)))
            angle = math.pi / 2
        else:
            # Диагональные или случайные линии
            start = (random.randint(margin, WIDTH - margin - min_length), random.randint(margin, HEIGHT - margin - min_length))
            angle = random.uniform(0, 2 * math.pi)
            max_length = min(WIDTH - start[0] - margin, HEIGHT - start[1] - margin, 400)
            length = random.randint(min_length, max_length)
            end = (start[0] + length * math.cos(angle), start[1] + length * math.sin(angle))

        if 0 <= start[0] < WIDTH and 0 <= start[1] < HEIGHT and 0 <= end[0] < WIDTH and 0 <= end[1] < HEIGHT:
            line = Line(start, end, angle)
            line.calculate_correct_divisions()
            return line

    raise ValueError("Unable to generate a valid line after maximum attempts")

def draw_button(surface, text, position, size):
    pygame.draw.rect(surface, BUTTON_COLOR, (*position, *size))
    font = pygame.font.Font(None, 24)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(position[0] + size[0] // 2, position[1] + size[1] // 2))
    surface.blit(text_surface, text_rect)

def calculate_accuracy(line):
    if not line.user_divisions:
        return 0

    total_error = 0
    for user_div, correct_div in zip(sorted(line.user_divisions), line.correct_divisions):
        error = math.hypot(user_div[0] - correct_div[0], user_div[1] - correct_div[1])
        total_error += error

    total_length = math.hypot(line.end[0] - line.start[0], line.end[1] - line.start[1])
    accuracy = max(0, (1 - total_error / total_length) * 100)
    return accuracy

def main():
    clock = pygame.time.Clock()
    lines = [generate_line(i) for i in range(3)]
    show_hint = False
    attempt = 0
    user_color = LINE_COLOR
    accuracy_text = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 10 <= x <= 110 and 10 <= y <= 40:  # Show hint button
                    show_hint = True
                elif 120 <= x <= 220 and 10 <= y <= 40:  # Check accuracy button
                    total_accuracy = sum(calculate_accuracy(line) for line in lines) / len(lines)
                    accuracy_text = f"Average Accuracy: {total_accuracy:.2f}%"
                elif 230 <= x <= 330 and 10 <= y <= 40:  # Refresh button
                    lines = [generate_line(attempt + i) for i in range(3)]
                    attempt += 3
                    accuracy_text = ""
                elif 340 <= x <= 440 and 10 <= y <= 40:  # Color picker button
                    user_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                else:
                    for line in lines:
                        if line.is_point_on_line((x, y)):
                            if event.button == 1:  # Left click
                                line.user_divisions.append((x, y))
                            elif event.button == 3:  # Right click
                                line.is_dragging = True
                                line.drag_offset = (x - line.start[0], y - line.start[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    show_hint = False
                elif event.button == 3:  # Right mouse button
                    for line in lines:
                        line.is_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                for line in lines:
                    if line.is_dragging:
                        x, y = event.pos
                        dx = x - line.start[0] - line.drag_offset[0]
                        dy = y - line.start[1] - line.drag_offset[1]
                        line.move(dx, dy)

        screen.fill(BACKGROUND_COLOR)
        for line in lines:
            line.draw(screen, show_hint)
        
        draw_button(screen, "Show Hint", (10, 10), (100, 30))
        draw_button(screen, "Check Accuracy", (120, 10), (100, 30))
        draw_button(screen, "Refresh", (230, 10), (100, 30))
        draw_button(screen, "Change Color", (340, 10), (100, 30))

        if accuracy_text:
            font = pygame.font.Font(None, 24)
            text_surface = font.render(accuracy_text, True, (0, 0, 0))
            screen.blit(text_surface, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()