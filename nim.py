import copy
import sys
import random
import pygame
from socket import *


class game(object):
    def __init__(self, piles):
        self.piles = piles

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

    def getPilesList(self):
        #print("Piles: ", self.piles)
        return self.piles

def startConnection():
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    clientSock.bind(('', 0))
    clientSock.listen(1)
    PORT = clientSock.getsockname()[1]
    print(f"Waiting for a player to connect at {getLocalIPAddress()}:{PORT}...")
    conn, addr = clientSock.accept()
    print(f"Connected by {addr}")
    return conn

def joinConnection(ip, port):
    peerSock = socket(AF_INET, SOCK_STREAM)
    peerSock.connect((ip, int(port)))
    print(f"Connected to {ip}:{port}")
    return peerSock

def getLine(conn):
    msg = b''
    while True:
        ch = conn.recv(1)
        msg += ch
        if ch == b'\n' or len(ch) == 0:
            break
    return msg.decode().strip()

def recvall(self, conn, msgLength):
    msg = b''
    while len(msg) < msgLength:
        retVal = conn.recv(msgLength - len(msg))
        msg += retVal
        if len(retVal) == 0:
            break    
    return msg

def getLocalIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def sendPilesList(conn, piles, gameOver=False):
    if gameOver:
        conn.send("GAMEOVER\n".encode())
    else:
        conn.send(f"{len(piles)}\n".encode())
        for pile in piles:
            conn.send(f"{pile}\n".encode())

def receivePilesList(conn):
    line = getLine(conn)

    if line == "GAMEOVER":
        return

    lengthPiles = int(line)

    piles = []
    
    for _ in range(lengthPiles):
        pile = int(getLine(conn))
        piles.append(pile)
    
    return piles

def player1(conn, firstMove):
    if firstMove:
        piles = [random.randint(1, 7) for _ in range(3)]
    else:
        piles = receivePilesList(conn)

    if not piles:
        print("Player2 loses! Player1 wins!")
        conn.close()
        return False
        

    print(f"Piles: {piles}")
    nim = game(piles)
    loop = True
    while loop:
        try:
            print(f"Player1's move:")
            pile = int(input("Enter pile number: ")) - 1
            count = int(input("Enter number to remove: "))

            if not nim.legalQ(pile, count):
                raise ValueError("Invalid move!")

            nim.move(1, pile, count)
            updatedPilesList = nim.getPilesList()

            if updatedPilesList == [0, 0, 0]:
                sendPilesList(conn, [], gameOver=True) 

            else:
                sendPilesList(conn, updatedPilesList, gameOver=False)

            loop = False

            if nim.isTerminal(nim.piles, 1)[0]:
                print("Player1 loses! Player2 wins!")
                conn.close()
                return False

        except ValueError as e:
            print(e)
            loop = True
    
    return True

def player2(conn):
    piles = receivePilesList(conn)

    if not piles:
        print("Player1 loses! Player2 wins!")
        conn.close()
        return False

    print(f"Piles: {piles}")
    nim = game(piles)
    loop = True 

    while loop:
        try:
            print(f"Player2's move:")
            pile = int(input("Enter pile number: ")) - 1
            count = int(input("Enter number to remove: "))

            if not nim.legalQ(pile, count):
                raise ValueError("Invalid move!")

            nim.move(2, pile, count)
            updatedPilesList = nim.getPilesList()

            if updatedPilesList == [0, 0, 0]:
                sendPilesList(conn, [], gameOver=True) 

            else:
                sendPilesList(conn, updatedPilesList, gameOver=False)

            loop = False

            if nim.isTerminal(nim.piles, 2)[0]:
                print("Player2 loses! Player1 wins!")
                conn.close()
                return False

        except ValueError as e:
            print(e)
            loop = True
    
    return True

def main():

    if len(sys.argv) == 3: # You are connecting to someone who already has the game started
        ip = sys.argv[1]
        port = sys.argv[2]
        conn = joinConnection(ip, port)

        isPlayer1 = False
        firstMove = False

    else: # The person is starting the connection/ game
        conn = startConnection()

        isPlayer1 = True
        firstMove = True 

    playing = True

    while playing:
        if isPlayer1:
            playing = player1(conn, firstMove)
            firstMove = False # After first move, no need to generate piles again
        else:
            playing = player2(conn)    

    #while True:
    #    pass

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

