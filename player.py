# player.py
import tkinter as tk
import random

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def propose_team(self, all_players, mission_size):
        """
        Propose a team of players for the mission.
        Currently, this will select a random set of players, including the player itself.
        """
        return random.sample(all_players, mission_size)

    def vote_on_team(self, proposed_team):
        """
        Decide whether to approve or disapprove of the proposed team.
        Randomly vote 'approve' or 'disapprove'.
        """
        vote = random.choice(['approve', 'disapprove'])
        print(f"{self.name} ({self.role}) has voted: {vote}")
        return vote

    def execute_mission(self):
        """
        Decide how to execute the mission.
        If the player is a spy, they can choose to sabotage or not.
        Resistance players will always vote for success.
        """
        if self.role == 'spy':
            vote = random.choice(['success', 'sabotage'])
            print(f"{self.name} (a spy), has voted: {vote}")
            return vote
        else:
            return 'success'




class PlayerElement:
    #THE GUI part
    def __init__(self, parent, x, y, player):
        self.player = player

        self.canvas = parent
        self.x, self.y = x, y

        self.circle = self.canvas.create_oval(x-20, y-20, x+20, y+20, fill='blue' if self.player.role == "good" else 'red')
        self.label = self.canvas.create_text(x, y, text=self.player.name, fill='white')

    

    def set_active(self, active=True):
        self.canvas.itemconfig(self.circle, outline='yellow' if active else '', width=2)

    def set_vote(self, vote):
        self.player.votes.append(vote)
        self.canvas.create_text(self.x, self.y + 25, text='✔' if vote else '✖', fill='green' if vote else 'red')
