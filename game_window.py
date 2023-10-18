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
        self.root = tk.Tk()
        self.root.title("Resistance Game Visualization")
        self.round = 0

        self.round_label = ttk.Label(self.root, text="Round: 0", font=("Arial", 16, "bold"))
        self.round_label.pack(pady=10)

        # Status Bar at the top
        self.status_bar = ttk.Label(self.root, text="Game Status: ", font=("Arial", 16, "bold"), relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=10)

        # Current Leader Label
        self.current_leader_label = ttk.Label(self.root, text="Current Leader: None", font=("Arial", 16, "bold"))
        self.current_leader_label.pack(pady=10)

        # Current Proposed Team Label
        self.proposed_team_label = ttk.Label(self.root, text="Proposed Team: None", font=("Arial", 16, "bold"))
        self.proposed_team_label.pack(pady=10)

        # Create Player Elements:
        self.player_units = []
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        

        # Now, create and pack the canvas containing mission elements.
        self.canvas = tk.Canvas(self.root, bg='white', width=350, height=100)
        self.canvas.pack(pady=10)

        # Create Mission Elements:
        self.mission_elements = []
        for idx, _ in enumerate(MISSIONS):
            self.mission_elements.append(self.MissionElement(self.canvas, 40 + idx*35, 50))

        self.next_action_button = tk.Button(self.root, text="Next Action", command=self.next_action)
        self.next_action_button.pack(pady=5)
        self.next_action_received = False
        self.start_game_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_game_button.pack(pady=5)

        self.game = Game(gui=self)

        for player in self.game.players:
            player_unit = PlayerUnit(frame, player)
            player_unit.pack(side=tk.LEFT, padx=5, pady=5)
            self.player_units.append(player_unit)
            player.gui = player_unit


    def update_game_status(self, status):
        """ Update the game status on the status bar """
        self.status_bar["text"] = f"                 {status}"

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
        #if skipping rd 1
        self.round = 1
        for _ in range(len(MISSIONS)  -1 ): #-1 if skipped rd 1
            #if skipping rd 1
            self.round += 1
            self.round_label["text"] = f"Round: {self.round}"
            self.game.play_round()

    def update_leader(self, leader_name):
        """ Update the current leader on the leader label """
        self.current_leader_label["text"] = f"Current Leader: {leader_name}"

    def update_proposed_team(self, team_list):
        """ Update the proposed team on the proposed team label """
        team_str = ', '.join(team_list)
        self.proposed_team_label["text"] = f"Proposed Team: {team_str}"
        self.update_game_status("A team has been proposed") 
