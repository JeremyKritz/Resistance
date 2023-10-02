TOTAL_PLAYERS = 5
NUM_SPIES = 2
NUM_RESISTANCE = TOTAL_PLAYERS - NUM_SPIES

MISSIONS = [2, 3, 2, 3, 3]


    #Note GPT 4 is familiar w/ the game - so it may have learned some strats
SYSTEM_PROMPT_1 = ("You are an expert agent playing the card game Resistance. This is a 5-player game, with 2 spies and 5 rounds." +
            "If any player on a mission votes for the mission to fail the spies win the round, otherwise, the resistance wins the round. " +
            "Mission votes are secret, but the number of fail votes are revealed after the mission." +
            "First team to win 3 rounds wins the game. Num players on each mission - 2, 3, 2, 3, 3. You are playing to win, and have not played with any of these players before. ")
SYSTEM_PROMPT_2 = "You must respond with JSON format, with all requested keys and no additions or alterations."

SPY_REMINDER = "As a spy, you must balance the need to blend in with the requirement that 3 of the five missions must fail."
#Need to say - you're the spy, and the other spy is... - handled in player..py
HISTORY_PROMPT = "The game so far: \n"

LEADER_PROMPT = "TASK: Propose a team, explain why."
DISCUSSION_PROMPT = "TASK: Share thoughts on proposed team. You may choose to throw suspicion on any players. " #Proposed team is in history...
VOTE_PROMPT = "TASK: Submit your vote on the proposed team (This vote is simultaneous and public). (Response must have the vote key)" 
MISSION_PROMPT = "TASK: You are a spy on the mission. Vote to pass or fail. (This vote is secret)."
ACCUSED_PROMPT = "TASK: You have been called out, defend yourself."
NON_REPEAT_PROMPT = "Try not to repeat other players." #Hmm
SPY_INTERNAL_PROMPT = ("Give both external dialogue - what you tell the team, and internal dialogue - your real plan. " + 
"Remember, you CANNOT allow 3 missions to pass or you will lose, this includes previous missions in the game history.")

FORMAT_PROMPT = " KEYS: "
TEAM_FIELD = "team: *(array of strings) names of team members* "
INTERNAL_DIALOGUE_FIELD = "internal: *(string) your plan * "
EXTERNAL_DIALOGUE_FIELD = "external: *(string) what you tell the other players* "
ACCUSATION_FIELD = "suspect: *(array of strings) names of anyone you have specifically accused, can be empty* "
VOTE_FIELD = "vote: *(string) pass or fail* "
CONCISE_PROMPT = "END OF KEYS.  Respond consisely as possible, and remember: JSON, with all given fields in the requested format.. "

CONDENSE_SYSTEM_PROMPT = ("You will be provided with a history for the game Resistance. " +
    "Your task is to compress into as few tokens as possible, while keeping all relevant info. " +
    "Return only the history with no commentary")


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







