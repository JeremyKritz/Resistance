# player.py
import tkinter as tk
import random
import openai
from constants import *
import json
openai.api_key = '' #HIDE lol

class Player:
    def __init__(self, name, role, fellow_spies=None):
        self.name = name
        self.role = role
        self.fellow_spies = fellow_spies if fellow_spies else []

    def role_context(self):

        if self.role == 'spy':
            return f"You are {self.name}, you are a spy. Other spies: {self.fellow_spies} "
        return f"You are {self.name}, and in the resistance."
    




    def propose_team(self, players, mission_size, history):
        # Randomly selects players for the team.

        prompt = (INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
             + LEADER_PROMPT + "Mission size:" + str(mission_size) + FORMAT_PROMPT 
            + TEAM_FIELD  + EXTERNAL_DIALOGUE_FIELD 
        )
        if self.role == 'spy':
            prompt = prompt + INTERNAL_DIALOGUE_FIELD
        prompt = prompt + CONCISE_PROMPT
        #print(prompt)

        """
        gpt_response = self.call_gpt(prompt)  

        parsed_data = json.loads(gpt_response)

        team = parsed_data["team"]
        internal_reasoning = parsed_data["internal"] if parsed_data["internal"] else None
        external_reasoning = parsed_data["external"] 
        
        print(internal_reasoning)
        """
        team = random.sample(players, mission_size)    
        external_reasoning = "Just 'cuz" # Placeholder
        
        return team, external_reasoning
    
    def open_discussion(self, proposed_team, history):

        prompt = (INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
             + DISCUSSION_PROMPT  + FORMAT_PROMPT 
            + TEAM_FIELD  + EXTERNAL_DIALOGUE_FIELD 
        )
        if self.role == 'spy':
            prompt = prompt + INTERNAL_DIALOGUE_FIELD

        prompt = prompt + CONCISE_PROMPT
        print(prompt)


        opinion = random.choice(['doubt', 'approval', 'neutral']) # Placeholder

        specific_accusation_or_support = None
        if opinion == 'doubt':
            # specific_reaction = interact_with_gpt3(f"Player {self.name} has doubts. Do they accuse anyone specifically from the proposed team {proposed_team}?")
            specific_reaction = {"action": "accuses", "player": random.choice(proposed_team), "reason": "They seem suspicious."} # Placeholder
            specific_accusation_or_support = specific_reaction
        
        return opinion, specific_accusation_or_support


    def vote_on_team(self, proposed_team):
        # This method will randomly return 'approve' or 'reject'
        # Later on, this can be replaced by GPT-3 generated opinions.
        return random.choice(['pass', 'fail'])

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


    def respond(self, reactors):
        # Generate a defense/response
        # response = interact_with_gpt3(f"Player {self.name} with role {self.role} has been accused by {reactors}. How do they defend themselves?")
        response = "I have done nothing wrong. Trust me." # Placeholder
        return response
        

    def call_gpt(self, prompt):
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = 700
        )
        input("Press Enter to continue...")
        print(response)
        return response.choices[0].text.strip()








"""
Memory is super vital...

We may want to implement plans...
ie - remind the agent what they had in mind during earlier rounds...

gpt-3.5-turbo-instruct?

I wonder if i can force them to summarize...   *compression


GPT 3 isnt smart enough not to send 2 spies, but GPT4 is
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
