from engine.main import Game
import scriptblue
import Trial

if __name__ == "__main__":
    G = Game((40, 40), Trial, scriptblue)
    G.run_game()