# main.py
from game import Game
from constants import TOTAL_PLAYERS, NUM_SPIES, NUM_RESISTANCE, MISSIONS
from game_window import GameWindow

def main():
    # Create a game instance
    game = Game()
    
    # Initialize the game window with the current game instance
    window = GameWindow(game)
    
    # This will be the main game loop. For the purposes of this example, it'll loop through all the missions.
    for _ in range(len(MISSIONS)):
        game.play_round()
        window.update_mission(game.current_mission_index - 1, game.mission_outcomes[-1])
        
        # This could be a delay or user input for stepping through rounds, but for now, it's just a simple input to progress.
        input("Press Enter to continue to the next round...")

    # Start the main loop for the game window (this will keep the window open)
    window.run()

if __name__ == '__main__':
    main()
