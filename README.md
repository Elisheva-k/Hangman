
# 🪢 Hangman Game in Python

Welcome to the **Hangman Game** – a fun and interactive word-guessing game developed in Python. This version includes user registration, authentication, and a scoreboard to track wins.

## 🎮 Features

- 🔤 Classic hangman word guessing gameplay
- 👤 User registration and login system
- 🏆 User win tracking and persistent score saving
- 💾 Local storage using JSON or file-based storage (adjustable)
- 🧼 Clean, readable code written in Python 3

---

## 🚀 Getting Started

### Requirements

- Python 3.x

### Installation

```bash
git clone https://github.com/your-username/hangman-game.git
cd hangman-game
python hangman.py
```

---

## 📁 File Structure

```
hangman-game/
├── hangman.py             # Main game logic
├── auth.py                # User registration & login system
├── users.json             # Stored user credentials & scores
├── words.txt              # Word bank for the game
├── README.md              # This file
```

---

## 📌 Usage

- On start, the user is prompted to login or register.
- After logging in, the game selects a random word.
- Each correct letter reveals its position.
- After 6 incorrect guesses – game over.
- Wins are saved and shown per user.

---

## 💡 Example Gameplay

```
Welcome to Hangman!
1. Login
2. Register
Select option: 1
Username: elisheva
Password: ******

Hello elisheva! Wins: 3

Word: _ _ _ _ _
Guess a letter: a
Good job!

Word: a _ _ _ _
...
```

---

## 🛡️ Security Notes

- Passwords are stored in plain text for simplicity – use `hashlib` for secure applications.
- Files are used instead of databases for easy deployment and learning.

---

## 📜 License

MIT License

---

> Built with ❤️ by Elisheva – for practice, fun, and clean Python learning!
