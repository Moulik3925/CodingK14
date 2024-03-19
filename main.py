from engine.main import Game
import scriptblue
import sample_scripts.sample1
import sample_scripts.sample2
import sample_scripts.sample3
import V3_Rishi
import neeraje
import V2

if __name__ == "__main__":
    G = Game((40, 40), V2, V3_Rishi)
    # G = Game((40, 40), V2, V1)
    G.run_game()
