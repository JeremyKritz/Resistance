TOTAL_PLAYERS = 5
NUM_SPIES = 2
NUM_RESISTANCE = TOTAL_PLAYERS - NUM_SPIES

MISSIONS = [2, 3, 2, 3, 3]


    #Note GPT 4 is familiar w/ the game - so it may have learned some strats
INITIAL_PROMPT = "You're playing the card game 'The Resistance'."
#Need to say - you're the spy, and the other spy is...
HISTORY_PROMPT = " Game history: \n"

LEADER_PROMPT = "Propose a team, explain why."
DISCUSSION_PROMPT = "Share thoughts on proposed team." #Proposed team is in history...
VOTE_PROMPT = "Vote on proposed team."
MISSION_PROMPT = "You are a spy on the mission. Vote to pass or fail."

FORMAT_PROMPT = " Respond with JSON, with fields:"
TEAM_FIELD = "team: *array of team members* "
INTERNAL_DIALOGUE_FIELD = "internal: *your plan* "
EXTERNAL_DIALOGUE_FIELD = "external: *what you tell the other players* "
ACCUSATION_FIELD = "accuse: *array of names, can be empty* "
VOTE_FIELD = "vote: *yes or no* "
MISSION_FIELD = "vote: *pass or fail* " #No need for good guys to get prompted...
CONCISE_PROMPT = "Be concise."


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







