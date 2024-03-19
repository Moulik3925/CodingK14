from engine.main import Game
import scriptblue
import scriptred
import sample_scripts.sample1
import sample_scripts.sample2
import sample_scripts.sample3
import neeraje
import V2
import V3_Moulik

if __name__ == "__main__":
    G = Game((40, 40), V3_Moulik , V3_Moulik)
    # G = Game((40, 40), V2, V1)
    G.run_game()
