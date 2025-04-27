import copy
import sys
import random
import pygame
from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
clientSock.bind(('', 0))
clientSock.listen(32)

PORT = clientSock.getsockname()[1]

def Connect(peerIP, peerPort):
    peerConn = socket(AF_INET, SOCK_STREAM)
    peerConn.connect((peerIP, int(peerPort)))

def getLocalIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class game(object):
    def __init__(self, piles):
        self.piles = piles
        '''
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Nim Game")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 100, 100)
        self.BLUE = (100, 100, 255)

        self.font = pygame.font.SysFont(None, 48)
        '''
    def move(self, player, pile, count):
        self.piles[pile] -= count

    def availableActions(self, piles):
        actions = []
        for i in range(len(piles)):
            if piles[i] > 0:  # Only consider piles that have objects
                for j in range(1, piles[i] + 1):
                    actions.append((i, j))
        return actions

    def isTerminal(self, piles, current_player):
        if all(pile == 0 for pile in piles):
            if current_player == 1:
                return True, 1
            return True, -1
        else:
            return False, 0

    def legalQ(self, pile, count):
        return 0 <= pile < len(self.piles) and 1 <= count <= self.piles[pile]

    def displayPiles(self):
        print("Piles: ", self.piles)

    '''
    def draw_piles(self, current_player):
        self.screen.fill(self.WHITE)
        pile_positions = [150, 400, 650]  # X-positions for each pile

        for i, count in enumerate(self.piles):
            x = pile_positions[i]
            
            if count == 0:
                continue  # Nothing to draw

            # Calculate starting Y position
            start_y = self.HEIGHT // 2 + 100  # start a bit lower
            
            for j in range(count):
                pygame.draw.circle(self.screen, self.RED, (x, start_y - j * 40), 20)

        # Draw player turn text
        text = self.font.render(f"Player {current_player}'s Turn", True, self.BLACK)
        self.screen.blit(text, (self.WIDTH // 2 - 150, 50))

        pygame.display.flip()
    '''



def main():

    if len(sys.argv) == 3: # You are connecting to someone who already has the game started
        Connect(sys.argv[1], sys.argv[2])
        print(f"Connected to: {sys.argv[1]}, {sys.argv[2]}")

    else:
        print(f"IP : {getLocalIPAddress()} : {PORT}")

    while True:
        pass

    '''
    #pygame.init()

    piles = [random.randint(1, 7) for _ in range(3)]
    nim = game(piles)
    gameOver = False
    players = ["Player1", "Player2"]
    ply = 0  # Player1 goes first, starts as ply 0

    nim.displayPiles()

    while not gameOver:
        loop = True

        if ply % 2 == 0:  # Player1's turn
            while loop:
                try:
                    print(f"{players[0]}'s move:")
                    pile = int(input("Enter pile number: ")) - 1
                    count = int(input("Enter number to remove: "))

                    if not nim.legalQ(pile, count):
                        raise ValueError("Invalid move!")

                    nim.move(1, pile, count)
                    nim.displayPiles()
                    loop = False

                    if nim.isTerminal(nim.piles, 1)[0]:
                        print(f"{players[0]} loses! {players[1]} wins!")
                        sys.exit(0)

                except ValueError as e:
                    print(e)
                    loop = True

        else:  # Player2's turn
            while loop:
                try:
                    print(f"{players[1]}'s move:")
                    pile = int(input("Enter pile number: ")) - 1
                    count = int(input("Enter number to remove: "))

                    if not nim.legalQ(pile, count):
                        raise ValueError("Invalid move!")

                    nim.move(2, pile, count)
                    nim.displayPiles()
                    loop = False

                    if nim.isTerminal(nim.piles, 2)[0]:
                        print(f"{players[1]} loses! {players[0]} wins!")
                        sys.exit(0)

                except ValueError as e:
                    print(e)
                    loop = True

        ply += 1
    '''

if __name__ == "__main__":
    main()

