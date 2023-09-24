import random
from player import Player
from constants import TOTAL_PLAYERS, NUM_SPIES, NUM_RESISTANCE, MISSIONS

class Game:
    def __init__(self):
        self.players = []
        self.setup_players()
        self.mission_outcomes = []
        self.current_team = []
        self.current_mission_index = 0
        self.leader_index = 0

    def setup_players(self):
        names = ['Alice', 'Bob', 'Claire', 'Dave', 'Ed'] #Frank, Gary etc
        roles = ['spy'] * NUM_SPIES + ['good'] * NUM_RESISTANCE
        random.shuffle(roles)
        for name, role in zip(names, roles):
            self.players.append(Player(name, role))

        print("\nPlayers and their roles:")
        for player in self.players:
            print(f"{player.name} is a {player.role}")

    def play_round(self):
        MAX_VOTE_ATTEMPTS = 5
        vote_attempts = 0

        while vote_attempts < MAX_VOTE_ATTEMPTS:
            proposed_team, leader_reasoning = self.propose_team_with_reasoning()
            print(f"Reasoning: {leader_reasoning}")
            
            if vote_attempts == MAX_VOTE_ATTEMPTS - 1:  # If this is the 5th vote attempt, auto-approve
                print("The 5th vote attempt auto-passes!")
                break

            # Open Discussion
            accusations = self.open_discussion(proposed_team)

            # Response
            for target, reactors in accusations.items():
                target_player = next(player for player in self.players if player.name == target)
                response = target_player.respond(reactors)
                print(f"{target} responds: {response}")
            
            is_approved = self.team_voting(proposed_team)

            if is_approved:
                break
            else:
                self.rotate_leader()
                vote_attempts += 1

        mission_success = self.execute_mission(proposed_team)
        self.feedback(mission_success)

    def rotate_leader(self):
        # Move to the next leader. If at the end of the player list, loop back to the start.
        self.leader_index = (self.leader_index + 1) % len(self.players)

    def propose_team(self):
        leader = self.players[self.leader_index]
        proposed_team = leader.propose_team(self.players, MISSIONS[self.current_mission_index])
        proposed_team_names = ", ".join(str(player.name) for player in proposed_team)
        print(f"\n {leader.name} has proposed the team: {proposed_team_names}")
        return proposed_team
    

    def team_voting(self, proposed_team):
        votes = [player.vote_on_team(proposed_team) for player in self.players]
        approved = votes.count('approve') > len(self.players) / 2
        if(approved):
            print("\n The team is approved.")
        return approved
    

    def execute_mission(self, approved_team):
        mission_votes = [player.execute_mission() for player in approved_team]
        sabotages = mission_votes.count('sabotage')
        if(sabotages > 0):
            print(f"The mission fails with {sabotages} fail votes \n")
        else:
            print(f"The mission passes! \n")
        return sabotages == 0


    def feedback(self, mission_result):  #RENAME this
        self.mission_outcomes.append(mission_result)
        self.leader_index = (self.leader_index + 1) % TOTAL_PLAYERS
        self.current_mission_index += 1

    def propose_team_with_reasoning(self):
        leader = self.players[self.leader_index]
        proposed_team, reasoning = leader.propose_team_with_reasoning(self.players, MISSIONS[self.current_mission_index])
        proposed_team_names = ", ".join(str(player.name) for player in proposed_team)
        print(f"\n {leader.name} has proposed the team: {proposed_team_names}")
        return proposed_team, reasoning

    def open_discussion(self, proposed_team):
        accusations = {}
        for player in self.players:
            opinion, specific_accusation_or_support = player.open_discussion(proposed_team)
            print(f"{player.name} says: {opinion}")
            
            if specific_accusation_or_support:
                target_player_name = specific_accusation_or_support['player'].name
                print(f"{player.name} {specific_accusation_or_support['action']} {target_player_name}: {specific_accusation_or_support['reason']}")
                
                if specific_accusation_or_support['action'] == 'accuses' and target_player_name not in accusations:
                    accusations[target_player_name] = []
                accusations[target_player_name].append(player.name)
        
        return accusations
