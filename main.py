from engine.main import Game
import scriptblue
import sample_scripts.sample1
import sample_scripts.sample2
import sample_scripts.sample3
import Trial
import neeraje
import Trial_sexy

if __name__ == "__main__":
    # G = Game((40, 40), Trial, neeraje)
    G = Game((40, 40), Trial, Trial_sexy)
    # G = Game((40, 40), Trial_sexy, Trial)
    G.run_game()
