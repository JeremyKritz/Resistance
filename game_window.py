# game_window.py
import tkinter as tk
import math
from player import PlayerElement
from constants import TOTAL_PLAYERS, NUM_SPIES, NUM_RESISTANCE, MISSIONS

class GameWindow:
    class MissionElement:
        def __init__(self, parent, x, y):
            self.canvas = parent
            self.x, self.y = x, y
            self.rectangle = self.canvas.create_rectangle(x, y, x+30, y+30, fill='gray')

        def set_outcome(self, outcome):
            self.canvas.itemconfig(self.rectangle, fill='green' if outcome else 'red')

    def __init__(self, game):
        self.root = tk.Tk()
        self.root.title("Resistance Game Visualization")

        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack()

        # Create Player Elements:
        self.player_elements = []
        centerX, centerY = 400, 300
        radius = 200
        angle_diff = 2 * math.pi / len(game.players)
        for player in game.players:
            angle = len(self.player_elements) * angle_diff
            x = centerX + radius * math.cos(angle)
            y = centerY + radius * math.sin(angle)
            self.player_elements.append(PlayerElement(self.canvas, x, y, player))

        # Create Mission Elements:
        self.mission_elements = []
        for idx, _ in enumerate(MISSIONS):
            self.mission_elements.append(self.MissionElement(self.canvas, 50 + idx*40, 550))

    def update_mission(self, idx, outcome):
        self.mission_elements[idx].set_outcome(outcome)

    def run(self):
        self.root.mainloop()
