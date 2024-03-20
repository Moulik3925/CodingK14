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


def collectibles(G):
    n = G.dim[0]
    arr = G.collectibles

    # rum,gunpowder,wood
    topLeft = [0, 0, 0]
    for i in range(n):
        for j in range(0, n-i):
            if arr[i][j] == -1:
                topLeft[0] += 1
            elif arr[i][j] == -2:
                topLeft[1] += 1
            elif arr[i][j] == -3:
                topLeft[2] += 1
    topRight = [0, 0, 0]
    for i in range(n):
        for j in range(i, n):
            if arr[i][j] == -1:
                topRight[0] += 1
            elif arr[i][j] == -2:
                topRight[1] += 1
            elif arr[i][j] == -3:
                topRight[2] += 1
    bottomLeft = [0, 0, 0]
    for i in range(n):
        for j in range(0, i):
            if arr[i][j] == -1:
                bottomLeft[0] += 1
            elif arr[i][j] == -2:
                bottomLeft[1] += 1
            elif arr[i][j] == -3:
                bottomLeft[2] += 1
    bottomRight = [0, 0, 0]
    for i in range(n):
        for j in range(n-i+1, n):
            if arr[i][j] == -1:
                bottomRight[0] += 1
            elif arr[i][j] == -2:
                bottomRight[1] += 1
            elif arr[i][j] == -3:
                bottomRight[2] += 1
    # mark = {-1: 'R', 0: '_', -2: 'G', -3: 'W'}
    mark = {-1: 'R', 0: '_', -2: '_', -3: '_'}  # if watching only rum
    with open('collectibles.txt', 'w') as f:
        for i in range(n):
            for j in range(n):
                f.write(mark[int(arr[i][j])])
            f.write('\n')
        f.write("topLeft = " + str(topLeft[0]) + ' ' +
                str(topLeft[1]) + ' ' + str(topLeft[2]) + '\n')
        f.write("topRight = " + str(topRight[0]) + ' ' +
                str(topRight[1]) + ' ' + str(topRight[2]) + '\n')
        f.write("bottomLeft = " + str(bottomLeft[0]) + ' ' +
                str(bottomLeft[1]) + ' ' + str(bottomLeft[2]) + '\n')
        f.write("bottomRight = " + str(bottomRight[0]) + ' ' + str(
            bottomRight[1]) + ' ' + str(bottomRight[2]) + '\n')
    return


if __name__ == "__main__":
    player1 = V3_Moulik
    player2 = V3_Rishi
    ML = False
    rate = 100000
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
        collectibles(G)
        G.run_game()
