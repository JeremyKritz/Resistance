# player.py
import tkinter as tk
import random
import openai

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def propose_team(self, players, mission_size):
        # This method will randomly select players for the team.
        # Later on, this can be replaced by GPT-3 generated teams.
        return random.sample(players, mission_size)

    def propose_team_with_reasoning(self, players, mission_size):
        # Randomly selects players for the team.
        proposed_team = self.propose_team(players, mission_size)
        
        # Call GPT-3 for reasoning
        # reasoning = interact_with_gpt3(f"Player {self.name} with role {self.role} is proposing a team. What's their reasoning?")
        reasoning = "tbd." # Placeholder
        
        return proposed_team, reasoning

    def vote_on_team(self, proposed_team):
        # This method will randomly return 'approve' or 'reject'
        # Later on, this can be replaced by GPT-3 generated opinions.
        return random.choice(['approve', 'reject'])

    def execute_mission(self):
        # For spies: random chance to sabotage
        # For resistance: always return 'success'
        # This can be enhanced using GPT-3 to make more strategic decisions.
        if self.role == 'spy':
            # decision = interact_with_gpt3(f"Player {self.name} with role {self.role} is on the mission. Do they sabotage or let it succeed?")
            decision = random.choice(['success', 'sabotage']) # Placeholder
        else:
            decision = 'success'
        return decision

    def open_discussion(self, proposed_team):
        # Randomly generate an opinion
        # opinion = interact_with_gpt3(f"Player {self.name} with role {self.role} has been asked about the proposed team {proposed_team}. What's their opinion?")
        opinion = random.choice(['doubt', 'approval', 'neutral']) # Placeholder

        specific_accusation_or_support = None
        if opinion == 'doubt':
            # specific_reaction = interact_with_gpt3(f"Player {self.name} has doubts. Do they accuse anyone specifically from the proposed team {proposed_team}?")
            specific_reaction = {"action": "accuses", "player": random.choice(proposed_team), "reason": "They seem suspicious."} # Placeholder
            specific_accusation_or_support = specific_reaction
        
        return opinion, specific_accusation_or_support

    def respond(self, reactors):
        # Generate a defense/response
        # response = interact_with_gpt3(f"Player {self.name} with role {self.role} has been accused by {reactors}. How do they defend themselves?")
        response = "I have done nothing wrong. Trust me." # Placeholder
        return response
        

    def interact_with_gpt3(self, messages, functions=[]):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        return response








"""
Memory is super vital...

We may want to implement plans...
ie - remind the agent what they had in mind during earlier rounds...

gpt-3.5-turbo-instruct?


"""


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
