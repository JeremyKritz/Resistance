import random, datetime
from player import Player
from constants import *
from threading import Event
from gpt_service import GPTService

class Game:
    def __init__(self, gui=None):
        self.gui = gui
        self.players = []
        self.prev_rds_history = []  # Added history attribute
        self.curr_rd_history = [] 
        self.full_history = [] 
        self.mission_outcomes = []
        self.current_team = []
        self.current_mission_index = 0
        self.leader_index = 0
        self.next_action_event = Event()
        self.gpt = GPTService()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"history_{timestamp}.txt"
        # Create the file with just a header for now
        with open(self.log_filename, 'w') as f:
            f.write("HISTORY\n")
            f.write("=====================\n\n")

        self.setup_players()
        

    def add_to_history(self, event):  # Added method to log events
        with open(self.log_filename, 'a') as f:
            f.write(f"{event}")
            f.write("\n     ----------\n")
        
        self.curr_rd_history.append(event)
        self.full_history.append(event)

    def setup_players(self):
        names = ['Alice', 'Bob', 'Claire', 'Dave', 'Ed']  # Add more names if needed
        roles = ['spy'] * NUM_SPIES + ['good'] * NUM_RESISTANCE
        random.shuffle(roles)
        spy_names = []
        for name, role in zip(names, roles):
            player = Player(name, role)
            if role == 'spy':
                spy_names.append(name)
            self.players.append(player)

        for player in self.players:
            if player.role == 'spy':
                player.fellow_spies = [spy for spy in spy_names if spy != player.name]
            else:
                player.fellow_spies = None
        # Add to history
        player_names = ", ".join(names)
        self.add_to_history(f"Players: {player_names} (turns rotate based on this order)")



    def play_round(self):
        self.clear_player_guis()
        print(f"\n START ROUND {self.current_mission_index+1} \n")
        self.add_to_history(f"\n ROUND {self.current_mission_index+1}")
        MAX_VOTE_ATTEMPTS = 5
        vote_attempts = 0
        team_string = ""
        while vote_attempts < MAX_VOTE_ATTEMPTS:
            proposed_team, leader_reasoning = self.propose_team_with_reasoning()
            print(f"Reasoning: {leader_reasoning}")
            team_string = ", ".join([player for player in proposed_team])
            
            self.gui.update_proposed_team(proposed_team) #temp
            self.add_to_history("Reasoning: " + leader_reasoning)
            self.gui.update_game_status("A team has been proposed") 
            self.pause()
            
            if vote_attempts == MAX_VOTE_ATTEMPTS - 1:  # If this is the 5th vote attempt, auto-approve
                print("The 5th vote attempt auto-passes!")
                break

            # Open Discussion
            self.gui.update_game_status("Discussion phase") 
            accusations = self.open_discussion(proposed_team)
            print(accusations)
            self.pause()
            self.clear_player_guis() 

            # Response
            for target in accusations:
                for player in self.players: #No real need for efficiency here its 5 players
                    if player.name == target:
                        self.gui.update_game_status(f"{player.name} is under suspicion")
                        response = player.respond(self.get_history())
                        self.add_to_history(f"{player.name} defense: {response}")
                        print(f"{target} responds: {response}")
                        self.pause()
            
            is_approved = self.team_voting(proposed_team)

            if is_approved: 
                break
            else:
                self.rotate_leader()
                vote_attempts += 1
        self.gui.update_game_status("Mission team: " + team_string)
        mission_success = self.execute_mission(proposed_team)
        self.feedback(mission_success)
        self.condense_history()

    def rotate_leader(self):
        self.leader_index = (self.leader_index + 1) % len(self.players)


    def propose_team_with_reasoning(self):
        leader = self.players[self.leader_index]
        self.gui.update_leader(leader.name)
        proposed_team, reasoning = leader.propose_team(self.players, MISSIONS[self.current_mission_index], self.get_history())
        proposed_team_names = ", ".join(str(player) for player in proposed_team)
        print(f"\n {leader.name} has proposed team: {proposed_team_names}")
        self.add_to_history(f"{leader.name} proposed team: {proposed_team_names}") 
        return proposed_team, reasoning

    def open_discussion(self, proposed_team):
        accused = []
        self.add_to_history(f"DISCUSSION PHASE")

        # Loop through all players to gather their opinions on the proposed team
        for index, player in enumerate(self.players):
            if index == self.leader_index: #Leader won't weigh on own proposal now.
                continue
            # Get the player's opinion and list of suspected players
            opinion, suspected_players = player.open_discussion(proposed_team, self.get_history())
            
            self.add_to_history(f"{player.name}: {opinion}")
            print(f"{player.name} says: {opinion}\n")

            for suspected_player in suspected_players:
                if suspected_player and suspected_player not in accused:  # Check if the suspected_player is not empty and not in the set yet
                    accused.append(suspected_player)
                    print(f"{suspected_player} accused")
            
            self.pause()
        self.gui.update_game_status(f"Called out as suspicious:  {suspected_players}")
        return accused   



    def team_voting(self, proposed_team):
        self.add_to_history(f"VOTING PHASE")
        votes = [player.vote_on_team(self.get_history()) for player in self.players]
        for player, vote in zip(self.players, votes):
            self.add_to_history(f"{player.name} voted {vote}")

        approved = votes.count('pass') > len(self.players) / 2
        if(approved):
            self.gui.update_game_status("The team is approved")
            print("\n The team is approved.")
        else:
            self.gui.update_game_status("The proposed team has been voted down.")
        
        self.pause()
        self.clear_player_guis()

        return approved
    

    def execute_mission(self, approved_team_names):
        print("Begin execute mission")
        approved_team = self.names_to_players(approved_team_names)
        #NOTE - history is public - you can't reveal who voted what...
        mission_votes = [player.execute_mission(self.get_history()) for player in approved_team]
        sabotages = mission_votes.count('fail')
        if sabotages > 0:
            self.add_to_history(f"Mission failed: {sabotages} sabotages. Spies win the round.") #Note - some versions don't reveal # of fail votes.
            self.gui.update_game_status(f"The mission fails with {sabotages} fail votes")
            print(f"The mission fails with {sabotages} fail votes \n")
        else:
            self.add_to_history(f"Mission Passes - Resistance wins the round.")
            self.gui.update_game_status(f"The mission has succeeded!")
            print(f"The mission passes! \n")

        #For some games some missions require 2 votes to fail... this doesnt cover that
        self.pause()

        return sabotages == 0


    def feedback(self, mission_result):
        outcome = "pass" if mission_result else "fail"
        self.add_to_history(f"Mission {self.current_mission_index + 1} {outcome}")
        self.mission_outcomes.append(mission_result)
        self.gui.update_mission(self.current_mission_index, outcome)
        self.rotate_leader()
        self.current_mission_index += 1

        if self.current_mission_index == 5:
            print("END")
            self.print_history()

        
    def names_to_players(self, player_names):
        return [player for player in self.players if player.name in player_names]
    
    
    def clear_player_guis(self):
        for player in self.players:
            player.gui.clear_all()


    def print_history(self):  # Added method to print the game history
        for event in self.full_history:
            print(event)

    def pause(self):
        print("Waitin'")
        self.gui.wait_for_next_action()

    def condense_history(self):  # Added method to print the game history

        system = CONDENSE_SYSTEM_PROMPT
        prompt = "  ".join(self.curr_rd_history)
        condensed  = self.gpt.call_gpt(system, prompt)
        self.prev_rds_history.append(condensed)
        self.curr_rd_history = []

        #make gpt call...

    def get_history(self):
        return self.prev_rds_history + self.curr_rd_history
