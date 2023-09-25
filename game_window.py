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
            print("mission element")
            self.canvas.itemconfig(self.rectangle, fill='green' if outcome == 'pass' else 'red')

    def __init__(self):
        self.game = Game(gui=self)
        self.root = tk.Tk()
        self.root.title("Resistance Game Visualization")

        # Status Bar at the top
        self.status_bar = ttk.Label(self.root, text="Game Status: ", font=("Arial", 16, "bold"), relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=10)

        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=150)  # Adjusted height for canvas
        self.canvas.pack(pady=20)  # Separate canvas from status bar and player units

        # Create Player Elements:
        self.player_units = []
        frame = ttk.Frame(self.root)  # frame is packed inside root, not inside canvas
        frame.pack(pady=20)  # Adjust padding for better separation

        for player in self.game.players:
            player_unit = PlayerUnit(frame, player)
            player_unit.pack(side=tk.LEFT, padx=10, pady=10)
            self.player_units.append(player_unit)
            player.gui = player_unit

        # Create Mission Elements:
        self.mission_elements = []
        for idx, _ in enumerate(MISSIONS):
            self.mission_elements.append(self.MissionElement(self.canvas, 50 + idx*40, 50))  # Centered y-coordinate inside canvas

        self.next_action_button = tk.Button(self.root, text="Next Action", command=self.next_action)
        self.next_action_button.pack(pady=10)
        self.next_action_received = False
        self.start_game_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_game_button.pack(pady=10)


    def update_game_status(self, status):
        """ Update the game status on the status bar """
        self.status_bar["text"] = f"Game Status: {status}"

    def update_mission(self, idx, outcome):
        print("hmm")
        self.mission_elements[idx].set_outcome(outcome)

    def next_action(self):
        self.next_action_received = True

    def wait_for_next_action(self):
        while not self.next_action_received:
            self.root.update_idletasks()
            self.root.update()
        self.next_action_received = False


    def run(self):
        self.root.mainloop()

    def start_game(self):
        for _ in range(len(MISSIONS)):
            self.game.play_round()
