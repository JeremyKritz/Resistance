TOTAL_PLAYERS = 5
NUM_SPIES = 2
NUM_RESISTANCE = TOTAL_PLAYERS - NUM_SPIES

MISSIONS = [2, 3, 2, 3, 3]
MAX_VOTE_ATTEMPTS = 5
PLAYER_NAMES = ['Alice', 'Bob', 'Claire', 'Dave', 'Ed'] 

#GPT understands newline chars...
    #Note GPT 4 is familiar w/ the game - so it may have learned some strats
SYSTEM_PROMPT_1 = ("You are a highly analytical AI playing the 5-player game Resistance, with 2 spies. "  #consider adding more about team vote
           #"Missions are proposed by a leader. Leader does not convey any additional abilities on a mission." +
            "Num players on each mission - 2, 3, 2, 3, 3 " 
            "Its best of 5, so there will be 5 rds max, 3 rds min. "
            "You will get game history in JSON " 
            "The third proposed mission will proceed with no discussion."
            "You dont know these players "
            "Do not refer to yourself in the third-person "
            )

SYSTEM_PROMPT_2 = "Respond with JSON, all requested keys and no additions or alterations. "

#They really like adding both spies on a team.
# SPY_REMINDER = ("You are on same team as other spy but cant coordinate. Resistance knows there are 2 spies. " + 
#                 "Consider how actions will be percieved. You are willing to take risks.")
#Need to say - you're the spy, and the other spy is... - handled in player..py

HISTORY_PROMPT = "Game Summary: \n" #GPT understands newline chars...

# SPY_LEADER_REMINDER = " If you want mission to fail you can secretly fail it, so consider whether you want both spies on mission, given suspicion towards failed team " #this one is a bit like cheating...

LEADER_PROMPT = "TASK Propose a team, explain why."




DISCUSSION_PROMPT = "TASK Share public thoughts on proposed team, and if it should proceed, or if next player should propose mission. You may choose to throw suspicion on any players. " #Proposed team is in history...
VOTE_PROMPT = "TASK Submit your vote on the proposed team (Vote is simultaneous and public). (Response must have the vote key)" 
MISSION_PROMPT = "TASK You are a spy on the mission. Vote to pass or fail. (Vote is secret)."
ACCUSED_PROMPT = "TASK You have been called out, defend yourself."
# SPY_INTERNAL_PROMPT = " Also give internal dialogue - your real plan. "

CONCISE_PROMPT = "Brevity important. Use few words as possible. Dont waste tokens."

FORMAT_PROMPT = " KEYS: "
INITIAL_THINKING_FIELD = "internal: *(string) considerations before the action* "
TEAM_FIELD = "team: *(array of strings) names of team members* "
# INTERNAL_DIALOGUE_FIELD = "internal: *(string) your plan * "
EXTERNAL_DIALOGUE_FIELD = "external: *(string) what you tell the other players* "
ACCUSATION_FIELD = "suspect: *(array of strings) names of anyone you specifically accused, can be empty* "
VOTE_FIELD = "vote: *(string) pass or fail* "
CLOSE_PROMPT = "END KEYS. Remember: JSON, with all given fields in the requested format."

CONDENSE_SYSTEM_PROMPT = ("You will be provided with dialogue from a round of the game Resistance. " +
    "Summarize into as few tokens as possible, while keeping all relevant info.")



CONSIDERATIONS_PROMPT = (" Give initial thinking first in 'internal' field. Reason through the following before making an action (Be concise. Use few words as possible, no need to repeat prompts): "
    "Based on current task, what do you need to make the best decision? "
    "Analyze the results of previous results and rounds - what can you determine? "
    "Whats the score? If either team gets to 3 they win. What will the score be after this round? "
    "If you lose this round, do you lose the game? Does this change priorities? "
    "Do you need to adjust your previous thinking based on any new info? "
    "Do you have a plan for the next phases / rounds? "
)




FINAL_CONSIDERATIONS = ("Take care to not refer to yourself in third-person. "
    "With all this in mind, choose an action. ")   #"Any last thoughts?"


SPY_VOTE_CONSIDERATIONS = (
    "If this mission has no spies, and proceeds, will you lose? ")


SPY_EXECUTE_MISSION_CONSIDERATIONS = (
)

SPY_PROPOSAL_CONSIDERATIONS = (
    "Do you want mission to pass or fail? "
    "If fail, is there a resistance player who can take the fall? "
    "Is there a good reason to include the other spy on this mission? "  #if you plan to fail it... might be cheating
)





SPY_DEFENSE_CONSIDERATIONS = (
    ""
)



SPY_GENERAL_CONSIDERATIONS = (
    "Is it time to make a specific accusation? "
    "If so, what specific evidence can you use to make a convincing case? "
    "Can you use anyones words or actions against them? "
    "The other team doesnt know who other spy is, is it better to defend or suspect them? "
    "What would a resistance player do in this situation "
    "Imagine you're a resistance player, would you find your actions suspicious or convincing? "
)




RESIST_GENERAL_CONSIDERATIONS = (
    "Analyze the discussions that have occurred, anything convincing, or suspicious?  "
    "You are innocent, so half the other players are spies. Who are the 2 you most suspect? "
    "Can you craft a specific accusation? "
)



#RESIST_VOTE_CONSIDERATIONS = ("Based on the discussion, do you think this team will be successful?")





















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







