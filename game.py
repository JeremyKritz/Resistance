import random, datetime
from player import Player
from constants import *
from threading import Event
from gpt_service import GPTService

class Game:
    def __init__(self, gui=None):
        self.gui = gui
        self.players = []
        self.rd_idx = 0
        self.leader_idx = 0
        self.propsd_team_idx = 0
        self.next_action_event = Event()
        self.gpt = GPTService()
        self.full_game = {
            'players':PLAYER_NAMES,
            'rounds':[]
        }

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"history_{timestamp}.txt"
        # Create the file with just a header for now
        with open(self.log_filename, 'w') as f:
            f.write("HISTORY\n")
            f.write("=====================\n\n")

        self.setup_players()
        self.add_passing_rd_1()

    def setup_players(self):
        #roles = ['spy'] * NUM_SPIES + ['good'] * NUM_RESISTANCE
        #random.shuffle(roles)
        roles = ['good', 'spy', 'good', 'spy', 'good'] #hardcoded for now (they dont remember past games...)
        spy_names = []
        for name, role in zip(PLAYER_NAMES, roles):
            player = Player(name, role)
            if role == 'spy':
                spy_names.append(name)
            self.players.append(player)

        for player in self.players:
            if player.role == 'spy':
                player.fellow_spies = [spy for spy in spy_names if spy != player.name]
            else:
                player.fellow_spies = None
        


    def play_round(self):
        self.clear_player_guis()
        self.full_game["rounds"].append(self.get_init_rd_obj())
        self.propsd_team_idx = 0

        while self.propsd_team_idx < MAX_VOTE_ATTEMPTS:
            proposed_team = self.propose_team()
            self.gui.update_proposed_team(proposed_team)
     
            self.pause()
            
            if self.propsd_team_idx == MAX_VOTE_ATTEMPTS - 1:
                break #The 5th vote attempt auto-passes!

            suspected_players = self.open_discussion()

            self.pause()
            self.clear_player_guis() 

            self.defense_phase(suspected_players)
            is_approved = self.team_voting()
            self.condense_dialogue()

            if is_approved: 
                break
            else:
                self.rotate_leader()
                self.propsd_team_idx += 1
        
        mission_result = self.execute_mission(proposed_team)
        self.gui.update_mission(self.rd_idx, mission_result)
        if self.has_game_ended():
            self.end_game()
        else:
            self.rotate_leader()
            self.rd_idx += 1
        #add some sort of end of game thingy
        
        

    def rotate_leader(self):
        self.leader_idx = (self.leader_idx + 1) % len(self.players)


    def propose_team(self):
        leader = self.players[self.leader_idx]
        self.gui.update_leader(leader.name)
        proposed_team, reasoning = leader.propose_team(self.players, MISSIONS[self.rd_idx], self.get_history())
        init_discussion = {leader.name.upper(): reasoning}
        proposed_team_obj = {
            "leader": leader.name,
            "team_members": proposed_team,
            "discussion": [init_discussion],
            "discussion_summary": "",
            "votes": []
        }
        self.get_current_round()["proposed_teams"].append(proposed_team_obj)
        return proposed_team


    def open_discussion(self):
        #open discussion around the proposed team, leading into defenses against specific callouts
        self.gui.update_game_status("Discussion phase") 
        accused = []
        proposed_team = self.get_current_proposed_team_obj()["team_members"]

        for idx, player in enumerate(self.players):
            if idx == self.leader_idx: #Leader won't weigh on own proposal
                continue

            opinion, suspected_players = player.open_discussion(proposed_team, self.get_history())

            self.add_to_discussion({player.name.upper(): opinion})

            for suspected_player in suspected_players:
                if suspected_player and suspected_player not in accused:  # Check if the suspected_player is not empty and not in the set yet
                    accused.append(suspected_player)
            
            self.pause()
        self.gui.update_game_status(f"Called out as suspicious:  {accused}")
        return accused   
    

    def defense_phase(self, suspected_players):
        suspected_players = self.names_to_players(suspected_players)
        for player in suspected_players:
            self.gui.update_game_status(f"{player.name} is under suspicion")
            response = player.respond(self.get_history())
            self.add_to_discussion({player.name.upper(): response})
            self.pause()



    def team_voting(self):
        votes = []
        vote_logs = []

        for player in self.players:
            vote = player.vote_on_team(self.get_history()) # Note: If get_history includes votes, you might want to provide history till the last round only.
            votes.append(vote)
            vote_logs.append({player.name.upper(): vote})
            self.pause() #required to not get rate-limited!

        # Now, after collecting all the votes, add them to the history
        
        for vote_str in vote_logs:
            self.get_current_proposed_team_obj()["votes"].append(vote_str)

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
        print(approved_team_names)
        self.gui.update_game_status(f"Mission team: {approved_team_names}")
        self.get_current_round()["mission_team"] = approved_team_names
        approved_team = self.names_to_players(approved_team_names)
        #History is public - you can't reveal who voted what...
        mission_votes = []
        for player in approved_team:
            vote = player.execute_mission(self.get_history())
            mission_votes.append(vote)
            self.pause()
        sabotages = mission_votes.count('fail')
        outcome = 'pass'
        if sabotages > 0:
            outcome = 'fail'

        self.get_current_round()["mission_outcome"] = outcome
        self.get_current_round()["sabotages"] = sabotages 
    
        self.gui.update_game_status(f"Mission Result: {outcome.upper()}. {sabotages} fail votes")

        print(self.full_game)

        #For some games some missions require 2 votes to fail... this doesnt cover that
        self.pause()
        return outcome 


    def add_to_discussion(self, string):
        self.get_discussion().append(string)

    def get_current_round(self):
        return self.full_game["rounds"][self.rd_idx]

    def get_current_proposed_team_obj(self):
        return self.get_current_round()["proposed_teams"][self.propsd_team_idx]

    def get_discussion(self):
        return self.get_current_proposed_team_obj()["discussion"]
        
    def names_to_players(self, player_names):
        return [player for player in self.players if player.name in player_names]
    
    def get_init_rd_obj(self):
        return {
            "round": self.rd_idx + 1, #more readable to not zero-idx the rounds
            "mission_player_count": MISSIONS[self.rd_idx],
            "proposed_teams": [],
            "mission_team":[],
            "mission_outcome": None,  # Will be set at the end of the round
            "sabotages":None
        }
    
    def has_game_ended(self):
        passed_missions = sum(1 for round_obj in self.full_game["rounds"] if round_obj["mission_outcome"] == "pass")
        failed_missions = sum(1 for round_obj in self.full_game["rounds"] if round_obj["mission_outcome"] == "fail")
    
        return failed_missions >= 3 or passed_missions >= 3
    
    def end_game(self):
    # Write the history to a file
        with open(self.log_filename, 'a') as f:
            f.write(str(self.full_game))
            f.write("\n=====================\n\n")

        # Update the GUI to show the end game status
        failed_missions = sum(1 for round_obj in self.full_game["rounds"] if round_obj["mission_outcome"] == "fail")
        if failed_missions >= 3:
            self.gui.update_game_status("The spies have won!")
        else:
            self.gui.update_game_status("The resistance has won!")

    def clear_player_guis(self):
        for player in self.players:
            player.gui.clear_all()



    def pause(self):
        print("Waitin' for the click")
        self.gui.wait_for_next_action()

    def condense_dialogue(self):  # Added method to print the game history

        system = CONDENSE_SYSTEM_PROMPT
        discussion = self.get_discussion()
    
        # Convert each dictionary in the discussion to a string and concatenate them
        prompt = ''.join([str(item) for item in discussion])
        condensed  = self.gpt.call_gpt(system, prompt)
        #condensed = "Summary" #for not using gpt
        print(condensed)
        self.get_current_proposed_team_obj()["discussion_summary"] = condensed

        #make gpt call...

    def get_history(self):
        # Create a deep copy of the full_game to avoid modifying the original data
        history_copy = dict(self.full_game)

            # Clean and filter out unnecessary data
        def clean_data(data):
            if isinstance(data, dict):
                cleaned = {}
                for k, v in data.items():
                    if k == "proposed_teams":
                        for team in v:
                            if team.get("discussion_summary"):
                                team.pop("discussion", None)
                    v = clean_data(v)
                    if v not in [None, "", []]:  # Removing key-value pairs with None, empty strings, or empty lists
                        cleaned[k] = v
                return cleaned
            elif isinstance(data, list):
                return [clean_data(item) for item in data if item not in [None, ""]]
            else:
                return data

        cleaned_history = clean_data(history_copy)

        spy_summary = ""

        # # Calculate passed and failed missions
        # passed_missions = sum([1 for round_obj in cleaned_history["rounds"] if round_obj.get("mission_outcome") == "pass"])
        # failed_missions = sum([1 for round_obj in cleaned_history["rounds"] if round_obj.get("mission_outcome") == "fail"])

        # total_rounds = len(cleaned_history["rounds"])
        # remaining_rounds = 5 - (passed_missions + failed_missions)
        # missions_to_fail = 3 - failed_missions

        # # Construct the summary
        #     # Construct the summary for spies

        # spy_summary = f"This is Rd {total_rounds}. {missions_to_fail} of the remaining {remaining_rounds} missions must fail!"
        # if remaining_rounds == missions_to_fail:
        #     spy_summary += " THIS MISSION MUST FAIL OR YOU WILL LOSE AND THE GAME WILL END!" #Turns out this is required lol

        # Convert to string and remove single quotation marks
        history_str = str(cleaned_history).replace("'", "")
        return [history_str, spy_summary]
    

    def add_passing_rd_1(self):
        self.full_game["rounds"].append(
              {
                  "round": 1,
                  "mission_player_count": 2,
                  "proposed_teams": [
                      {
                          "leader": "Alice",
                          "team_members": ["Alice", "Bob"],
                          "discussion_summary": "All players, Alice, Bob, Claire, Dave, and Ed agree to proceed with the mission, expressing no suspicion due to lack of information.",
                          "votes": [
                              {"ALICE": "pass"},
                              {"BOB": "pass"},
                              {"CLAIRE": "pass"},
                              {"DAVE": "pass"},
                              {"ED": "pass"}
                          ]
                      }
                  ],
                  "mission_team": ["Alice", "Bob"],
                  "mission_outcome": "pass",
                  "sabotages": 0
              })
        self.rd_idx = self.leader_idx = 1
        self.gui.update_mission(0, "pass")
