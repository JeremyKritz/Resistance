import openai
import json, re, datetime, time
from constants import *
openai.api_key = '' #HIDE lol

class GPTService:
    def __init__(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"prompt_{timestamp}.txt"
        self.model = "gpt-4-1106-preview"
        self.tokens_used = 0
        self.last_request_time = 0
        # Create the file with just a header for now
        with open(self.log_filename, 'w') as f:
            f.write("Prompts and Responses\n")
            f.write("=====================\n\n")

        print('test')
        print(self.turbo_test())

    def call_gpt(self, system, prompt): # ADD A TIMEOUT...
        print("\n Calling GPT")
        response = openai.ChatCompletion.create(
            model= self.model,
            messages=[
            {
            "role": "system",
            "content": system
            },
            {
            "role": "user",
            "content": prompt
            }
  ],
            max_tokens = 700
            #freq penalty? - idk might kill the json...
        )
        with open(self.log_filename, 'a') as f:
            f.write(f"System Prompt:\n{system}\n\n")
            f.write("\n    ------------\n\n")
            f.write(f"User Prompt:\n{prompt}\n\n")
            f.write("\n    ------------\n\n")
            f.write(f"Response:\n{response}\n")
            f.write("\n==========================\n\n")
            
        
        token_info = {"Prompt Tokens": response.usage["prompt_tokens"], "Completion Tokens": response.usage["completion_tokens"], "Total Tokens": response.usage["total_tokens"]}
        print(token_info)
        

        return response.choices[0].message.content.strip()



    def call_gpt_player(self, system, prompt, max_retries=1): #This one is for json responses
        retries = 0
        while retries <= max_retries: #GPT 3 sometimes (rarely) doesnt return proper format
            if retries > 0:
                time.sleep(15) #long sleep bc rate limit on gpt4, might need to move retries to main call
                prompt = prompt + " Again, ensure the response matches the requested JSON format."
            try:
                response = self.call_gpt(system, prompt)
                clean_json_response = self.clean_json(response)

                pretty_response = json.loads(clean_json_response)
                print("\nResponse Text:\n", pretty_response)
                return clean_json_response
            except Exception as e:
                print(f"Attempt {retries+1} failed:")
                print(e)
                print(response)
                retries += 1
        
        print(f"Failed to get a valid JSON response after {max_retries} attempts.")
        return None

    
    

    def clean_json(self, text):

        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            text = text[start_idx:end_idx+1]
        else:
            text = "{" + text + "}"

        # Convert keys with single quotes to double quotes
        text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\'|\")(\w+)(\'|\")\s*?:", r'\1"\3":', text)

        # Convert keys without quotes to double quotes
        text = re.sub(r"(\s*?{\s*?|\s*?,\s*?)(\w+)\s*?:", r'\1"\2":', text)

        # Convert values that are not wrapped in quotes but should be (like player names)
        text = re.sub(r":\s*\[([\w\s,]+)\]", lambda match: ': ["' + '", "'.join(match.group(1).split(", ")) + '"]', text)
        
        return text
    

    def turbo_test(self):
        system = "You are a highly analytical AI playing the 5-player game Resistance, with 2 spies. Num players on each mission - 2, 3, 2, 3, 3 Its best of 5, so there will be 5 rds max, 3 rds min. You will get game history in JSON You dont know these players Do not refer to yourself in the third-personYou are Ed, in the resistance.Respond with JSON, all requested keys and no additions or alterations. "


        user = """
        Game Summary: 
        {players: [Alice, Bob, Claire, Dave, Ed], rounds: [{round: 1, mission_player_count: 2, proposed_teams: [{leader: Alice, team_members: [Alice, Bob], discussion_summary: All players, Alice, Bob, Claire, Dave, and Ed agree to proceed with the mission, expressing no suspicion due to lack of information., votes: [{ALICE: pass}, {BOB: pass}, {CLAIRE: pass}, {DAVE: pass}, {ED: pass}]}], mission_team: [Alice, Bob], mission_outcome: pass, sabotages: 0}, {round: 2, mission_player_count: 3, proposed_teams: [{leader: Bob, team_members: [Alice, Bob, Claire], discussion_summary: Bob proposes Alice and Claire for the mission due to Alices past success and to gather more info on Claire. Alice and Claire agree with Bobs plan. Dave and Ed express suspicions about Claires quick agreement. Claire reassures her innocence and encourages focusing on uncovering spies. Dave remains suspicious of Claire and also suspects Alice., votes: [{ALICE: pass}, {BOB: pass}, {CLAIRE: pass}, {DAVE: pass}, {ED: pass}]}], mission_team: [Alice, Bob, Claire], mission_outcome: pass, sabotages: 0}, {round: 3, mission_player_count: 2, proposed_teams: [{leader: Claire, team_members: [Alice, Ed], discussion_summary: Claire proposes a team of Alice and Ed for the mission, aiming to gather intel. Alice and Bob support this, but Bob also suspects Dave and Ed could be spies.
        Dave expresses his suspicion of Ed and criticizes Eds eagerness to accept the mission. Ed defends himself, suggesting Daves suspicion of him may be a ploy to sabotage the mission., votes: [{ALICE: pass}, {BOB: pass}, {CLAIRE: pass}, {DAVE: fail}, {ED: pass}]}], mission_team: [Alice, Ed], mission_outcome: fail, sabotages: 1}, {round: 4, mission_player_count: 3, proposed_teams: [{leader: Dave, team_members: [Dave, Ed, Bob], discussion_summary: Dave proposes a team with Bob and Ed. Alice, Bob, Claire, and Ed express doubts on Daves team selection based on past failed missions. All indicate suspicion towards Dave and Ed, and suggest to proceed with caution. They hint at including Alice in the team due to her successful missions. Dave defends his selection, while Ed suggests considering Alice for the next mission and excluding Dave and Bob, suspecting their continuous suspicions as a possible misdirection ploy., votes: [{ALICE: fail}, {BOB: pass}, {CLAIRE: fail}, {DAVE: pass}, {ED: fail}]}, {leader: Ed, team_members: [Ed, Alice, Claire], discussion: [{ED: Given the circumstances, we simply cant afford risks. Alice and Claire have previously been on successful missions. Dave and Bob, your actions and comments have raised some doubts, I am sorry. Lets proceed this way for now and adjust if we need to in the future.},
        {ALICE: Ed, Im unsure of your team selection, considering previous mission failure. It seems like a risk we cannot afford. Perhaps a team revision is needed.}, {BOB: Given the last mission led by Ed failed, we need to reconsider his team selection. Both Alice and Claire have been on successful missions, but Claires decisions were questionable in the past. I believe Dave and Ed might be the spies given their suspicious activity. I suggest we hold off this mission and let the next leader propose a new team.}, {CLAIRE: The score is 2-1, we are close to victory. However, the selection seems risky. Ed, you were part of a failed mission and there is shared suspicion between Dave, Bob, and you which raises doubts. Alice, I trust your judgment as you have been part of all successful missions. I vote for the next player to propose the team, ensuring Alice is part of it.}, {DAVE: Ed, your decisions have been questionable so far. Interestingly, Bob also seemed too quick to jump on this. I would suggest we reconsider and let the next player propose the team, securing Alice as a part of it. She has been on successful missions and her experience can be beneficial for us all.}, {BOB: I have doubts about Eds decisions, including this team selection. He was part of a failed mission earlier, which raises serious concerns.
        I also cannot ignore Daves suspicious behavior and his preference for Ed. I suggest we decline this proposed team and let the next leader propose a new team. Dave and Ed, you both need to provide more convincing arguments for everyones trust.}, {DAVE: As much as the suspicion on me is concerning, I invite you all to look at the broader picture. Agreeably, Alice has had successful missions and is highly trusted. Ed, however, has failed a mission before and his decision-making as leader has also roused suspicion. To keep the game in our favor, I suggest we reflect on these facts and make a wise decision.}]}]}]}
        Your most recent internal thinking: Current score 2-1. If spies win the mission, we lose. Previous mission fails had Dave and Bob pointing fingers at others. Daves team selection received challenges. My suspicion lies on Dave and Bob. Need to propose a team excluding the suspected spies. TASK You have been called out, defend yourself. Give initial thinking first in internal field. Reason through the following before making an action (Be concise. Use few words as possible, no need to repeat prompts): Based on current task, what do you need to make the best decision? Analyze the results of previous results and rounds - what can you determine? Whats the score? If either team gets to 3 they win. What will the score be after this round? If you lose this round, do you lose the game? Does this change priorities? Do you need to adjust your previous thinking based on any new info? Do you have a plan for the next phases / rounds? Analyze the discussions that have occurred, anything convincing, or suspicious?  You are innocent, so half the other players are spies. Who are the 2 you most suspect? Can you craft a specific accusation? Take care to not refer to yourself in third-person. With all this in mind, choose an action. Brevity important. Use few words as possible. Dont waste tokens.
        KEYS: internal: *(string) considerations before the action* external: *(string) what you tell the other players* END KEYS. Remember: JSON, with all given fields in the requested format.
        """

        print(user)

        response = self.call_gpt(system, user)
        print(response)

