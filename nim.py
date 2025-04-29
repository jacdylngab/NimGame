import copy
import sys
import random
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
    peerSock.settimeout(10) # If you cannot connect in 30 seconds. Close the socket

    try:
        peerSock.connect((ip, int(port)))
        print(f"Connected to {ip}:{port}")
        peerSock.settimeout(None)
        return peerSock
    
    except socket.timeout:
        print(f"Connection attempt timed out after {timeout} seconds.")
        sys.exit(1)

    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)

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

    try:
        while playing:
            if isPlayer1:
                playing = player1(conn, firstMove)
                firstMove = False # After first move, no need to generate piles again
            else:
                playing = player2(conn)

    except Exception as e:
        conn.close()
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Game interrupted. Goodbye!")
        sys.exit(0)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)