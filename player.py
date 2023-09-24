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
        team_names = [player.name for player in players]
        team = random.sample(team_names, mission_size)    
        external_reasoning = "Just 'cuz" # Placeholder
        
        return team, external_reasoning
    


    def open_discussion(self, proposed_team, history):

        prompt = (INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
             + DISCUSSION_PROMPT  + FORMAT_PROMPT 
            + ACCUSATION_FIELD + EXTERNAL_DIALOGUE_FIELD 
        )
        if self.role == 'spy':
            prompt = prompt + INTERNAL_DIALOGUE_FIELD

        prompt = prompt + CONCISE_PROMPT
        #print(prompt)

        # gpt_response = self.call_gpt(prompt)  

        # parsed_data = json.loads(gpt_response)

        # internal_reasoning = parsed_data["internal"] if parsed_data["internal"] else None
        # external_reasoning = parsed_data["external"] 
        # suspected_players = parsed_data["suspect"] if parsed_data["suspect"] else [""]

        #print(f"{self.name}: {internal_reasoning}")
        


        external_reasoning = "Idk seems fine" # Placeholder
        suspected_players = random.sample(proposed_team, random.choice([0, 1]))

        return external_reasoning, suspected_players


    def vote_on_team(self, proposed_team, history):
        
        prompt = (
            INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
            + VOTE_PROMPT + FORMAT_PROMPT
            + VOTE_FIELD
        )

        """
        #Im assuming it can get the proposed team from history...
        gpt_response = self.call_gpt(prompt)
        parsed_data = json.loads(gpt_response)

        vote = parsed_data["vote"]
        """
        vote = random.choice(['pass', 'fail']) 

        return vote



    def execute_mission(self, history):
        if not self.role == 'spy':
            return "pass"
 
        prompt = (
            INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
            + MISSION_PROMPT + FORMAT_PROMPT
            + VOTE_FIELD
        )
        prompt += INTERNAL_DIALOGUE_FIELD
        prompt += CONCISE_PROMPT
        """
        gpt_response = self.call_gpt(prompt)
        parsed_data = json.loads(gpt_response)

        vote = parsed_data["vote"]
        internal_reasoning = parsed_data["internal"]

        print(internal_reasoning)
        """

        vote = random.choice(['pass', 'fail']) 

        return vote


    def respond(self, history):
        
        prompt = (
            INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
            + ACCUSED_PROMPT + FORMAT_PROMPT
            + EXTERNAL_DIALOGUE_FIELD
        )
        if self.role == 'spy':
            prompt += INTERNAL_DIALOGUE_FIELD
        prompt += CONCISE_PROMPT

        """
        gpt_response = self.call_gpt(prompt)
        parsed_data = json.loads(gpt_response)

        external_reasoning = parsed_data["external"]
        internal_reasoning = parsed_data["internal"] if parsed_data["internal"] else None

        #print(f"{self.name}: {internal_reasoning}")
        """


        external_reasoning = "I have done nothing wrong. Trust me."

        return external_reasoning
            

    def call_gpt(self, prompt):
        print("\n Calling GPT")
        print(prompt)
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = 700
        )
        
        print(response)
        input("\n Press Enter to continue... \n ")
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
