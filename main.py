from engine.main import Game
import scriptblue
import sample_scripts.sample1
import sample_scripts.sample2
import sample_scripts.sample3
import V1
import neeraje
import V2

if __name__ == "__main__":
    G = Game((40, 40), V1, V2)
    # G = Game((40, 40), V2, V1)
    G.run_game()
