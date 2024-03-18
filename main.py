from engine.main import Game
import scriptblue
import sample_scripts.sample1
import sample_scripts.sample2
import sample_scripts.sample3
import Trial

if __name__ == "__main__":
    G = Game((40, 40), Trial, scriptblue)
    G.run_game()