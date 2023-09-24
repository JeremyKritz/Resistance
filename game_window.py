import tkinter as tk
from tkinter import ttk
from player_ui import PlayerUnit  # Import the PlayerUnit class
from game import Game
from constants import TOTAL_PLAYERS, NUM_SPIES, NUM_RESISTANCE, MISSIONS

class GameWindow:
    class MissionElement:
        def __init__(self, parent, x, y):
            self.canvas = parent
            self.x, self.y = x, y
            self.rectangle = self.canvas.create_rectangle(x, y, x+30, y+30, fill='gray')

        def set_outcome(self, outcome):
            self.canvas.itemconfig(self.rectangle, fill='green' if outcome else 'red')

    def __init__(self):
        self.game = Game(gui=self)
        self.root = tk.Tk()
        self.root.title("Resistance Game Visualization")

        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack()


        self.current_mission_index = 0

        # Create Player Elements:
        self.player_units = []
        frame = ttk.Frame(self.canvas)
        frame.pack(side=tk.BOTTOM, fill=tk.X)

        for player in self.game.players:
            player_unit = PlayerUnit(frame, player)
            player_unit.pack(side=tk.LEFT, padx=10, pady=10)
            self.player_units.append(player_unit)
            player.gui = player_unit

        # Create Mission Elements:
        self.mission_elements = []
        for idx, _ in enumerate(MISSIONS):
            self.mission_elements.append(self.MissionElement(self.canvas, 50 + idx*40, 550))

        self.next_action_button = tk.Button(self.root, text="Next Action", command=self.next_action)
        self.next_action_button.pack()
        self.next_action_received = False

        self.start_game_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_game_button.pack()

    def update_mission(self, idx, outcome):
        self.mission_elements[idx].set_outcome(outcome)

    def next_action(self):
        self.next_action_received = True

    def wait_for_next_action(self):
        while not self.next_action_received:
            self.root.update_idletasks()
            self.root.update()

        # Reset the flag for the next input
        self.next_action_received = False

    def update_player_dialogue(self, player_idx, text, internal=False):
        self.player_units[player_idx].update_dialogue(text, internal)

    def update_player_vote(self, player_idx, vote):
        self.player_units[player_idx].update_vote(vote)

    def run(self):
        self.root.mainloop()

    def start_game(self):
        for _ in range(len(MISSIONS)):
            self.game.play_round()
