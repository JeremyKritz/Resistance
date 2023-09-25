# player.py
import tkinter as tk
import random
import openai
from constants import *
import json
import re
openai.api_key = '' #HIDE lol

class Player:
    def __init__(self, name, role, fellow_spies=None):
        self.name = name
        self.role = role
        self.fellow_spies = fellow_spies if fellow_spies else []
        self.gui = None 
        self.enableGPT = False


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

        if self.enableGPT:

            gpt_response = self.call_gpt(prompt)  

            parsed_data = json.loads(gpt_response)

            team = parsed_data["team"]
            external_reasoning = parsed_data["external"] 
            
            if self.role == 'spy':
                internal_reasoning = parsed_data["internal"]
                print(f"{self.name} (internal): {internal_reasoning}")

        else:
            team_names = [player.name for player in players]
            team = random.sample(team_names, mission_size)    
            external_reasoning = "Just 'cuz" # Placeholder
            if self.role == 'spy':
                internal_reasoning = "*evil laugh*"

        print("proposed a team")

        self.gui.update_external_dialogue(external_reasoning)
        if self.role == 'spy':
            self.gui.update_internal_dialogue(internal_reasoning)


        return team, external_reasoning
    


    def open_discussion(self, proposed_team, history):

        prompt = (INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
             + DISCUSSION_PROMPT  + FORMAT_PROMPT 
            + ACCUSATION_FIELD + EXTERNAL_DIALOGUE_FIELD 
        )
        if self.role == 'spy':
            prompt = prompt + INTERNAL_DIALOGUE_FIELD

        prompt = prompt + CONCISE_PROMPT
        #print("\n" + prompt + "\n")

        if self.enableGPT:

            gpt_response = self.call_gpt(prompt)  

            parsed_data = json.loads(gpt_response)

            
            external_reasoning = parsed_data["external"] 
            suspected_players = parsed_data.get("suspect", [""])
            if self.role == 'spy':
                internal_reasoning = parsed_data["internal"]
                print(f"{self.name} (internal): {internal_reasoning}")
            

        else:
            external_reasoning = "Idk seems fine" # Placeholder
            suspected_players = random.sample(proposed_team, random.choice([0, 1]))
            if self.role == 'spy':
                internal_reasoning = "I am evil"

        self.gui.update_external_dialogue(external_reasoning)
        if self.role == 'spy':
            self.gui.update_internal_dialogue(internal_reasoning)

        return external_reasoning, suspected_players


    def vote_on_team(self, proposed_team, history):
        
        prompt = (
            INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
            + VOTE_PROMPT + FORMAT_PROMPT
            + VOTE_FIELD
        )

        #print("\n" + prompt + "\n")


        #Im assuming it can get the proposed team from history...
        if self.enableGPT:
            gpt_response = self.call_gpt(prompt)
            parsed_data = json.loads(gpt_response)
            vote = parsed_data["vote"]
        else:
            vote = random.choice(['pass', 'fail']) 
        self.gui.update_vote(vote)
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

        #print("\n" + prompt + "\n")
        if self.enableGPT:
            gpt_response = self.call_gpt(prompt)
            parsed_data = json.loads(gpt_response)

            vote = parsed_data["vote"]
            internal_reasoning = parsed_data["internal"]

            print(internal_reasoning)

        else:
            vote = random.choice(['pass', 'fail']) 

        self.gui.update_vote(vote)
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

        #print("\n" + prompt + "\n")

        if self.enableGPT:
            gpt_response = self.call_gpt(prompt)
            parsed_data = json.loads(gpt_response)

            external_reasoning = parsed_data["external"]
            if self.role == 'spy':
                internal_reasoning = parsed_data["internal"]
                print(f"{self.name} (internal): {internal_reasoning}")

        else:
            external_reasoning = "I have done nothing wrong. Trust me."

        return external_reasoning
            

    def call_gpt(self, prompt):
        print("\n Calling GPT")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = 700
        )
        
        response_text = clean_json(response.choices[0].text.strip())

        try:
            pretty_response = json.loads(response_text)
        except Exception as e:
            print(e)
            print(response)

        token_info = {
            "Prompt Tokens": response.usage["prompt_tokens"],
            "Completion Tokens": response.usage["completion_tokens"],
            "Total Tokens": response.usage["total_tokens"]
        }
            
        print("\nResponse Text:\n", pretty_response)
        print("\nToken Usage:\n", token_info)
        
        #input("\n Press Enter to continue... \n ")
        return response_text
    

def clean_json(text):
    # Convert keys with single quotes to double quotes
    text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\'|\")(\w+)(\'|\")\s*?:", r'\1"\3":', text)

    # Convert keys without quotes to double quotes
    text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\w+)\s*?:", r'\1"\2":', text)

    # Convert values that are not wrapped in quotes but should be (like player names)
    text = re.sub(r":\s*\[([\w\s,]+)\]", lambda match: ': ["' + '", "'.join(match.group(1).split(", ")) + '"]', text)
    
    return text



"""
Memory is super vital...

We may want to implement plans...
ie - remind the agent what they had in mind during earlier rounds...

gpt-3.5-turbo-instruct?

I wonder if i can force them to summarize...   *compression


GPT 3 isnt smart enough not to send 2 spies, but GPT4 is
"""

