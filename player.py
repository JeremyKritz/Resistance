# player.py
import tkinter as tk
import random
from constants import *
import json
from gpt_service import GPTService

class Player:
    def __init__(self, name, role, fellow_spies=None):
        self.name = name
        self.role = role
        self.fellow_spies = fellow_spies if fellow_spies else []
        self.gui = None 
        self.enableGPT = True
        self.gpt = GPTService()
        self.internal_plan = "" #Consider having spies remember their own plans...


    def get_system_prompt(self):
        role_context = f"You are {self.name}, in the resistance."
        if self.role == 'spy':
            role_context =  f"You are {self.name}, you are a spy. The other spy is {self.fellow_spies[0]}. If 3 missions result in a 'fail', you win. If 3 'pass' you lose. "
        return SYSTEM_PROMPT_1 + role_context + SYSTEM_PROMPT_2
    
    def build_prompt(self, mode, mission_size=None, history=[]):
        history_json_str = history[0]
        spy_reminder = history[1]

        continuity = f"Your most recent internal thinking: {self.internal_plan} "


        # Begin with the base prompt
        prompt = HISTORY_PROMPT + history_json_str + "\n" + continuity


        considerations = self.get_role_specific_considerations(mode)
        standard = CONSIDERATIONS_PROMPT + considerations + CONCISE_PROMPT + FORMAT_PROMPT + INITIAL_THINKING_FIELD 


        turn_specific_prompts = {
            "propose": LEADER_PROMPT + " Mission size:" + str(mission_size) + standard  + TEAM_FIELD + EXTERNAL_DIALOGUE_FIELD ,
            "discussion": DISCUSSION_PROMPT + standard + ACCUSATION_FIELD + EXTERNAL_DIALOGUE_FIELD,
            "vote": VOTE_PROMPT + standard + VOTE_FIELD,
            "mission": MISSION_PROMPT + standard  + VOTE_FIELD,
            "accused": ACCUSED_PROMPT + standard + EXTERNAL_DIALOGUE_FIELD,
        }

        # Add the specific prompt based on role and game mode

        full_prompt =  prompt + turn_specific_prompts[mode] + CLOSE_PROMPT
        if self.role == 'spy':
            return full_prompt + spy_reminder
        return full_prompt



    def propose_team(self, players, mission_size, history):

        # Randomly selects players for the team.
        prompt = self.build_prompt("propose", mission_size=mission_size, history=history)
        #print(prompt)
        internal_reasoning = None


        if self.enableGPT:
            gpt_response = self.gpt.call_gpt_player(self.get_system_prompt(), prompt)    
            parsed_data = json.loads(gpt_response)
            team = parsed_data["team"]
            external_reasoning = parsed_data["external"] 
            
            
            self.internal_plan = internal_reasoning = parsed_data["internal"]
            print(f"{self.name} (internal): {internal_reasoning}")

        else:
            team_names = [player.name for player in players]
            team = random.sample(team_names, mission_size)    
            external_reasoning = "Just 'cuz" # Placeholder
            if self.role == 'spy':
                internal_reasoning = "*evil laugh*"

        print("proposed a team")

        self.gui.update_dialogue(external_reasoning, internal_reasoning)


        return team, external_reasoning
    


    def open_discussion(self, proposed_team, history):
        prompt = self.build_prompt("discussion", history=history)
        internal_reasoning = None
        #print(prompt)

        if self.enableGPT:
            gpt_response = self.gpt.call_gpt_player(self.get_system_prompt(), prompt)    
            parsed_data = json.loads(gpt_response)
            external_reasoning = parsed_data["external"] 
            suspected_players = parsed_data.get("suspect", [""])
            
            self.internal_plan = internal_reasoning = parsed_data["internal"]
            print(f"{self.name} (internal): {internal_reasoning}")
            

        else:
            external_reasoning = "Idk seems fine" # Placeholder
            suspected_players = random.sample(proposed_team, random.choice([0, 1]))
            if self.role == 'spy':
                internal_reasoning = "I am evil"

        self.gui.update_dialogue(external_reasoning, internal_reasoning)


        return external_reasoning, suspected_players
    

    def respond(self, history):
        
        prompt = self.build_prompt("accused", history=history)
        internal_reasoning = None

        if self.enableGPT:
            gpt_response = self.gpt.call_gpt_player(self.get_system_prompt(), prompt)  
            parsed_data = json.loads(gpt_response)

            external_reasoning = parsed_data["external"]

            self.internal_plan = internal_reasoning = parsed_data["internal"]
            print(f"{self.name} (internal): {internal_reasoning}")

        else:
            external_reasoning = "I have done nothing wrong. Trust me."
            if self.role == 'spy':
                internal_reasoning = "I hope I decieved them."

        self.gui.update_dialogue(external_reasoning, internal_reasoning)

        return external_reasoning


    def vote_on_team(self, history):   
        prompt = self.build_prompt("vote", history=history)
        internal_reasoning = None
        if self.role == 'spy':
            print (prompt)
        if self.enableGPT:
            gpt_response = self.gpt.call_gpt_player(self.get_system_prompt(), prompt)  
            parsed_data = json.loads(gpt_response)
            vote = parsed_data["vote"]
            self.internal_plan = internal_reasoning = parsed_data["internal"]
        else:
            vote = random.choice(['pass', 'pass', 'fail']) 
        self.gui.update_vote(vote)
        self.gui.update_dialogue(None, internal_reasoning)
        return vote



    def execute_mission(self, history):
        if not self.role == 'spy':
            self.gui.update_vote("pass")
            return "pass"
 
        prompt = self.build_prompt("mission", history=history)

        #print("\n" + prompt + "\n")
        if self.enableGPT:
            gpt_response = self.gpt.call_gpt_player(self.get_system_prompt(), prompt)  
            parsed_data = json.loads(gpt_response)

            vote = parsed_data["vote"]
            self.internal_plan = internal_reasoning = parsed_data["internal"]

            print(internal_reasoning)

        else:
            vote = random.choice(['pass', 'fail']) 
            internal_reasoning = "I'm being sneaky."

        self.gui.update_vote(vote)
        self.gui.update_dialogue(None, internal_reasoning)

        return vote


    def respond(self, history):
        
        prompt = self.build_prompt("accused", history=history)
        internal_reasoning = None

        if self.enableGPT:
            gpt_response = self.gpt.call_gpt_player(self.get_system_prompt(), prompt)  
            parsed_data = json.loads(gpt_response)

            external_reasoning = parsed_data["external"]
            
            self.internal_plan = internal_reasoning = parsed_data["internal"]
            print(f"{self.name} (internal): {internal_reasoning}")

        else:
            external_reasoning = "I have done nothing wrong. Trust me."
            if self.role == 'spy':
                internal_reasoning = "I hope I decieved them."

        self.gui.update_dialogue(external_reasoning, internal_reasoning)

        return external_reasoning




    def get_role_specific_considerations(self, mode):
 
 
        SPY_TURN_CONSIDERATIONS = {
            "propose": SPY_PROPOSAL_CONSIDERATIONS + SPY_GENERAL_CONSIDERATIONS,
            "discussion": SPY_GENERAL_CONSIDERATIONS,
            "vote": "",
            "mission": "",
            "accused": SPY_GENERAL_CONSIDERATIONS
        }

        # RESISTANCE_TURN_CONSIDERATIONS = {
        #     "propose":RESIST_GENERAL_CONSIDERATIONS,
        #     "discussion": RESIST_GENERAL_CONSIDERATIONS,
        #     "vote": RESIST_GENERAL_CONSIDERATIONS,  
        #     "accused": RESIST_GENERAL_CONSIDERATIONS
        #     # Add more modes here as needed
        # }

        if self.role == "spy":
            considerations = SPY_TURN_CONSIDERATIONS.get(mode)
        else: 
            considerations = RESIST_GENERAL_CONSIDERATIONS  #  + RESISTANCE_TURN_CONSIDERATIONS.get(mode)

        return considerations + FINAL_CONSIDERATIONS
    



"""
Memory is super vital...

We may want to implement plans...
ie - remind the agent what they had in mind during earlier rounds...

gpt-3.5-turbo-instruct?

I wonder if i can force them to summarize...   *compression


GPT 3 isnt smart enough not to send 2 spies, but GPT4 is
"""

