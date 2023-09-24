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

        # gpt_response = self.call_gpt(prompt)  

        # parsed_data = json.loads(gpt_response)

        # team = parsed_data["team"]
        # external_reasoning = parsed_data["external"] 
        
        # if self.role == 'spy':
        #     internal_reasoning = parsed_data["internal"]
        #     print(f"{self.name} (internal): {internal_reasoning}")


        team_names = [player.name for player in players]
        team = random.sample(team_names, mission_size)    
        external_reasoning = "Just 'cuz" # Placeholder

        print("proposed a team")
        self.gui.update_external_dialogue(external_reasoning)
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

        # gpt_response = self.call_gpt(prompt)  

        # parsed_data = json.loads(gpt_response)

        
        # external_reasoning = parsed_data["external"] 
        # suspected_players = parsed_data["suspect"] if parsed_data["suspect"] else [""]
        # if self.role == 'spy':
        #     internal_reasoning = parsed_data["internal"]
        #     print(f"{self.name} (internal): {internal_reasoning}")
        


        external_reasoning = "Idk seems fine" # Placeholder
        suspected_players = random.sample(proposed_team, random.choice([0, 1]))

        self.gui.update_external_dialogue(external_reasoning)

        return external_reasoning, suspected_players


    def vote_on_team(self, proposed_team, history):
        
        prompt = (
            INITIAL_PROMPT + self.role_context() + HISTORY_PROMPT + ",".join(history) + "\n"
            + VOTE_PROMPT + FORMAT_PROMPT
            + VOTE_FIELD
        )

        #print("\n" + prompt + "\n")


        #Im assuming it can get the proposed team from history...
        gpt_response = self.call_gpt(prompt)
        parsed_data = json.loads(gpt_response)
        vote = parsed_data["vote"]

        #vote = random.choice(['pass', 'fail']) 

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

        gpt_response = self.call_gpt(prompt)
        parsed_data = json.loads(gpt_response)

        vote = parsed_data["vote"]
        internal_reasoning = parsed_data["internal"]

        print(internal_reasoning)


        #vote = random.choice(['pass', 'fail']) 

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


        gpt_response = self.call_gpt(prompt)
        parsed_data = json.loads(gpt_response)

        external_reasoning = parsed_data["external"]
        if self.role == 'spy':
            internal_reasoning = parsed_data["internal"]
            print(f"{self.name} (internal): {internal_reasoning}")


        #external_reasoning = "I have done nothing wrong. Trust me."

        return external_reasoning
            

    def call_gpt(self, prompt):
        print("\n Calling GPT")
        #print(prompt)
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens = 700
        )
        
        # Extracting the text and token usage for printing
        response_text = clean_json(response.choices[0].text.strip())

        # Pretty print the response_text (which is a JSON string)
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
        
        input("\n Press Enter to continue... \n ")
        return response_text
    

def clean_json(text):
    """
    Given a starting text from GPT, this function tries to:
    1. Find the start of the JSON structure.
    2. Handle keys with single or no quotes.
    3. Handle values that aren't wrapped in quotes.
    4. Return a cleaner, more predictable JSON structure.
    """
    # Convert keys with single quotes to double quotes
    text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\'|\")(\w+)(\'|\")\s*?:", r'\1"\3":', text)

    # Convert keys without quotes to double quotes
    text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\w+)\s*?:", r'\1"\2":', text)

    # Convert values that are not wrapped in quotes but should be (like player names)
    text = re.sub(r":\s*\[([\w\s,]+)\]", lambda match: ': ["' + '", "'.join(match.group(1).split(", ")) + '"]', text)
    
    return text

# # Test
# text_sample = """
# {
#   "text": " \n\n\nsuspect: [Dave, Ed]\nexternal: \"I have my doubts about Dave and Ed as they seem to be agreeing too easily with the proposed team. Let's watch out for any suspicious behavior during the mission.\"",
# """

# cleaned_text = clean_json(text_sample)
# print(cleaned_text)






"""
Memory is super vital...

We may want to implement plans...
ie - remind the agent what they had in mind during earlier rounds...

gpt-3.5-turbo-instruct?

I wonder if i can force them to summarize...   *compression


GPT 3 isnt smart enough not to send 2 spies, but GPT4 is
"""

