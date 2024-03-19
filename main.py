from engine.main import Game
import scriptblue
import scriptred
import sample_scripts.sample1
import sample_scripts.sample2
import sample_scripts.sample3
import neeraje
import V2
import V3_Moulik
import V3_Rishi

if __name__ == "__main__":
    player1 = V3_Rishi
    player2 = V3_Moulik
    ML = True
    rate = 10000
    epochs = 20
    size = (40, 40)
    p1Wins = [0, 0, 0, 0]
    p2Wins = [0, 0, 0, 0]
    if (ML):
        # 0 1
        # 3 2
        for epoch in range(epochs//2):
            G = Game(size, player1, player2)
            G.ML = ML
            G.rate = rate
            G.epoch = epoch + 1
            G.run_game()
            mode, winner = G.redMode, G.Win
            if winner == "red" and mode == 0:
                p1Wins[0] += 1
            elif winner == "red" and mode == 1:
                p1Wins[1] += 1
            elif winner == "blue" and mode == 0:
                p2Wins[2] += 1
            elif winner == "blue" and mode == 1:
                p2Wins[3] += 1
        for epoch in range(epochs//2):
            G = Game(size, player2, player1)
            G.ML = ML
            G.rate = rate
            G.epoch = epoch + epochs//2
            G.run_game()
            mode, winner = G.redMode, G.Win
            if winner == "blue" and mode == 0:
                p1Wins[2] += 1
            elif winner == "blue" and mode == 1:
                p1Wins[3] += 1
            elif winner == "red" and mode == 0:
                p2Wins[0] += 1
            elif winner == "red" and mode == 1:
                p2Wins[1] += 1
        print(player1.name, p1Wins, sum(p1Wins))
        print(player2.name, p2Wins, sum(p2Wins))
    else:
        G = Game(size, player1, player2)
        G.run_game()
