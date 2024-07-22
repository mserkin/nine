from board import Board
from player import Player


class ComputerPlayer(Player):
    def move(self, board: Board):
        pass

# detect wing
# calc parameters on wing if 9 calc for both wings
# pass to estimation func
# if 9 take max estimation

# parameters:
# - N: next is rival's (1) or mine (0)
# - E: there is separated mine card in wing (1) or no (0)
# - D: distance to last mine
# - R: count of rival's card to last mine
# - C: count of cards to the end of a wing

# 2   3   4   5   6  [7]: N=1, E=0, D=0, R=0, C=5 (-5)
# 2   3   4   5  [6] [7]: N=0, E=0, D=1, R=0, C=5 (0)

# 2  [3]  4  [5]  6  [7]: N=1, E=1, D=4, R=2, C=5 (+4)
# 2  [3] [4]  5   6  [7]: N=1, E=1, D=4, R=2, C=5 (+4)
# 2  [3]  4   5  [6] [7]: N=0, E=1, D=4, R=2, C=5 (+4)
# 2  [3]  4  [5] [6] [7]: N=0, E=1, D=4, R=1, C=5 (+4)
# 2  [3] [4]  5  [6] [7]: N=0, E=1, D=4, R=1, C=5 (+4)

# if E==0:
#   if N==1: e=-C
#   else: e=0
# else:
#   if N==1: e=D+1
#   else: e=D
