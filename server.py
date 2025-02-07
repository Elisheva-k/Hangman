from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS
import json
import os
import random


app = Flask(__name__)
# CORS(app, supports_credentials=True)
supports_credentials=True

class User:
    counter = 1

    def __init__(self, name, password):
        self.name = name
        self.id = User.counter
        User.counter += 1
        self.password = password
        self.sumGames = 0
        self.allWords = []
        self.winners = 0
        self.allGames = []
        self.add_user(name, password)

    def add_user(self, name, password):
        newUser = {
            'id': self.id,
            'name': name,
            'password': password,
            'sumGames': self.sumGames,
            'allWords': self.allWords,
            'winners': self.winners,
            'allGames': self.allGames
        }

        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                users = json.load(file)
        else:
            users = []

        users.append(newUser)

        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)

class Game:
    def __init__(self, time, word, success):
        self.time = time
        self.word = word
        self.success = success

    def to_dict(self):
        return {
            'time': self.time,
            'word': self.word,
            'success': self.success
        }

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    if user_exists(name,password):
        return jsonify({"message": "User already exists"}), 400

    user = User(name=name, password=password)
    response = make_response(jsonify({"message": "User registered successfully", "user_id": user.id}), 201)
    response.set_cookie("user", name, max_age=120, httponly=True, secure=False, samesite='None')
    response.set_cookie("password", password, max_age=120, httponly=True, secure=False, samesite='None')
    return response

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    if user_exists(name, password):
        response = make_response(jsonify({'message': "User logged in successfully"}), 200)
        response.set_cookie("user", name, max_age=120, httponly=True, secure=False, samesite='None')
        response.set_cookie("password", password, max_age=120, httponly=True, secure=False, samesite='None')
        return response
    else:
        return jsonify({"message": "User not found or incorrect password"}), 404

def user_exists(name, password):
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            users = json.load(file)
            for user in users:
                if user['name'] == name and user['password'] == password:
                   return True
    return False

@app.route('/word/<int:num>', methods=['GET'])
def get_word(num):
    user_name = request.cookies.get('user')
    if user_name is None:
        return jsonify({"error": "User not found"}), 403

    with open('words', 'r', encoding='utf-8') as file:
        wordsList = file.read().splitlines()
        random.shuffle(wordsList)
        currentWord = wordsList[num % len(wordsList)]
        return currentWord
@app.route('/history')
def history():
    user_name = request.cookies.get('user')
    user_password = request.cookies.get('password')

    if user_name is None or user_password is None:
        return jsonify({"error": "User not found"}), 403

    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            users = json.load(file)
            for user in users:
                if user['name'] == user_name and user['password'] == user_password:
                    return jsonify({
                        "winners": user["winners"],
                        "words": user["allWords"],
                        "sum_games": user["sumGames"],
                        "all_games": user["allGames"]
                    })


@app.route('/end_play', methods=['POST'])
def end_play():
    user_name = request.cookies.get('user')
    user_password = request.cookies.get('password')

    if user_name is None or user_password is None:
        return jsonify({"error": "User not found"}), 403

    data = request.json
    word = data.get('word')
    success = data.get('success')
    time = data.get('time')
    new_game = Game(time=time, word=word, success=success)

    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            users = json.load(file)
            for user in users:
                if user['name'] == user_name and user['password'] == user_password:
                    if word not in user['allWords']:
                        user['allWords'].append(word)
                    user['sumGames'] += 1
                    user['winners'] += success
                    user['allGames'].append(new_game.to_dict())
                    break
        with open('users.json', 'w') as file:
            json.dump(users, file)

    return jsonify( "Game data updated successfully"), 200
@app.route('/error/<int:num>', methods=['GET'])
def error(num):
   with open('error.txt', 'r', encoding='utf-8') as file:
    errorList = file.read().split(',')
    return errorList[num-1]

@app.route('/check', methods=['GET'])
def check():
    user_name = request.cookies.get('user')
    if user_name is None:
        return jsonify({"error": "User not found"}), 403
    return jsonify({"message": f"Welcome Back, {user_name}!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
