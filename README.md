# 🕹️ Nim Multiplayer (P2P) Game

This project is a two-player, peer-to-peer (P2P) implementation of the classic game **Nim**, built in Python using low-level networking sockets.

Players take turns removing objects from one of several piles. The player forced to remove the last object **loses** the game.

---

## 📦 Features

- 🎮 Two-player Nim gameplay
- 🔗 Peer-to-peer networking using Python sockets (no central server)
- 💡 Player 1 starts the connection, Player 2 joins via IP/port
- 📤 Turn-based game state synchronization via list transmission
- 💻 Terminal-based user input (with future potential for Pygame UI)
- ❌ Graceful exit handling with error messages and keyboard interrupts

---

## 🧠 Game Rules

- The game begins with three piles of objects (each pile has 1–7 objects, randomly generated).
- Players take turns selecting a pile and removing one or more objects.
- The player forced to remove the **last object loses** the game.

---

## 🚀 How to Run

### 🛠️ 1. Clone the Repository

```
git clone https://github.com/jacdylngab/NimGame.git
cd NimGame
```

### 2. Start the Game
🖥️ Player 1 (Host)
Start the game without any arguments. It will wait for Player 2 to connect.
```
python3 nim.py
```
You'll see something like:
```
Waiting for a player to connect at IP:PORT...
```

🧑‍💻 Player 2 (Joiner)
Start the game with Player 1’s IP and port:
```
python3 nim.py <player1-ip> <port>
```
Example:
```
python3 nim.py 192.168.1.4 5555
```
