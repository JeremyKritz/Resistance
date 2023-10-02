TOTAL_PLAYERS = 5
NUM_SPIES = 2
NUM_RESISTANCE = TOTAL_PLAYERS - NUM_SPIES

MISSIONS = [2, 3, 2, 3, 3]


    #Note GPT 4 is familiar w/ the game - so it may have learned some strats
SYSTEM_PROMPT_1 = ("You are playing the 5-player game Resistance. 2 spies, 5 rounds." + #consider adding more about team vote
            "Missions fail if any player on it votes 'fail'. " +
            "Mission votes are secret, but the number of fail votes are revealed after the mission." +
            "First team to win 3 rounds wins the game. Num players on each mission - 2, 3, 2, 3, 3. " +
            "Play to win. You dont know these players.")

SYSTEM_PROMPT_2 = "You must respond with JSON format, with all requested keys and no additions or alterations."

SPY_REMINDER = "Blend in, but ensure 3 missions fail."
#Need to say - you're the spy, and the other spy is... - handled in player..py
HISTORY_PROMPT = "Game Progress: "

LEADER_PROMPT = "TASK: Propose a team, explain why."
DISCUSSION_PROMPT = "TASK: Share public thoughts on proposed team. You may choose to throw suspicion on any players. " #Proposed team is in history...
VOTE_PROMPT = "TASK: Submit your vote on the proposed team (This vote is simultaneous and public). (Response must have the vote key)" 
MISSION_PROMPT = "TASK: You are a spy on the mission. Vote to pass or fail. (This vote is secret)."
ACCUSED_PROMPT = "TASK: You have been called out, defend yourself."
NON_REPEAT_PROMPT = "Try not to repeat other players." #Hmm
SPY_INTERNAL_PROMPT = ("Also give internal dialogue - your real plan. " + 
"Remember, you CANNOT allow 3 missions to pass. This includes previous missions in the game history.")

CONCISE_PROMPT = " Brevity is important. Use as few words as possible. "

FORMAT_PROMPT = " KEYS: "
TEAM_FIELD = "team: *(array of strings) names of team members* "
INTERNAL_DIALOGUE_FIELD = "internal: *(string) your plan * "
EXTERNAL_DIALOGUE_FIELD = "external: *(string) what you tell the other players* "
ACCUSATION_FIELD = "suspect: *(array of strings) names of anyone you have specifically accused, can be empty* "
VOTE_FIELD = "vote: *(string) pass or fail* "
CLOSE_PROMPT = "END KEYS.  Remember: JSON, with all given fields in the requested format. "

CONDENSE_SYSTEM_PROMPT = ("You will be provided with a history for the game Resistance. " +
    "Your task is to compress dialogue into as few tokens as possible, while keeping all relevant info. Leave the rest as-is. " +
    "Return the revised history with no commentary")


# PLAYER_DESCRIPTIONS = {
#     'Alice': "Alice is known to be very straightforward and rarely lies. She is a strategist and thinks several steps ahead.",
#     'Bob': "Bob often goes with the flow and is known to be a team player. However, he's also known to change his decisions based on peer pressure.",
#     'Claire': "Claire is analytical and bases her decisions on logic. She rarely lets emotions cloud her judgment.",
#     'Dave': "Dave is unpredictable and can often throw a curveball in the game. His decisions may sometimes seem random, but there's often a deeper strategy behind them.",
#     'Ed': "Ed is trustworthy but can be easily influenced by strong personalities in the group."
# }

"""
We can add some seperate personalities maybe...


"""







