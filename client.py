from requests import session
from datetime import datetime
from rich.console import Console

console = Console()
session = session()
basic_url = "http://127.0.0.1:5000"

def register(name, password):
    obj = {'name': name, 'password': password}
    response = session.post(f"{basic_url}/register", json=obj)
    if response.status_code == 201:
        console.print("User registered successfully:", style="bold green")
    else:
        console.print("Registration error:", style="bold red")

def login(name, password):
    obj = {'name': name, 'password': password}
    response = session.post(f"{basic_url}/login", json=obj)
    if response.status_code == 200:
        console.print("ברוך שובך", style="bold blue")
    else:
        toRegiste = input("הנך משתמש חדש הקש 1 להרשמה הקש 2 להתנתקות: ")
        if toRegiste == "1":
            register(name, password)
        else:
            stsrt_game()

def stsrt_game():
    name = input("הכניסי שם: ")
    password = input("הכניסי סיסמא: ")
    login(name, password)
    play()

def decorator(func):
    def current_function(*arg, **kwargs):
        response = session.get(f'{basic_url}/check')
        if response.status_code == 200:
            return func(*arg, **kwargs)
        else:
            console.print("משתמש לא מחובר, אנא התחבר", style="bold red")
            stsrt_game()
    return current_function

@decorator
def play():
    option = input("הקש 1 למשחק 2 להיסטוריה 3 להתנתקות: ")
    if option == "2":
        history()
    elif option == "3":
        stsrt_game()
    elif option == "1":
        num = input('הכנס מספר מילה רצויה: ')
        try:
            number = int(num)
            response = session.get(f"{basic_url}/word/{number}")
            if response.status_code == 200:
                word = response.text
                success = 0
                errors = 0
                ansList = []
                current_time = datetime.now()
                time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                word_hide = ''.join([char if char.isspace() else '_' for char in word])
                console.print(word_hide, style="bold yellow")
                while '_' in word_hide and errors < 7:
                    mychar = input("הכנס תו לבדוק אם המילה מכילה אותו: ")
                    while mychar in ansList or mychar.isdigit() or len(mychar) > 1:
                        mychar = input("הכנס תו לבדוק אם המילה מכילה אותו: ")
                    ansList.append(mychar)
                    if mychar in word:
                        for index, char in enumerate(word):
                            if char == mychar:
                                word_hide = word_hide[:index] + mychar + word_hide[index + 1:]
                        console.print(word_hide, style="bold yellow")
                    else:
                        errors += 1
                        console.print(f"נותרו לך {7 - errors} פסילות", style="bold red")
                        response = session.get(f"{basic_url}/error/{int(errors)}")
                        if response.status_code == 200:
                            console.print(response.text)
                        else:
                            console.print(response.status_code)
                if '_' not in word_hide:
                    success = 1
                    console.print("!!!!!כל הכבוד!!!!!!", style="bold green")
                else:
                    success = 0
                    console.print("אויש, לא נורא אולי בפעם הבאה...", style="bold red")

                obj = {'success': success, 'word': word, 'time': time_str}
                response = session.post(f"{basic_url}/end_play", json=obj)
                if response.status_code == 200:
                    console.print(response.text)
                else:
                    console.print(response.status_code)
        except ValueError:
            console.print("שגיאה: נא להזין מספר תקף.", style="bold red")
    else:
        console.print("זה לא תקף, נסה שוב", style="bold red")
    play()

@decorator
def history():
    response = session.get(f"{basic_url}/history")
    if response.status_code == 200:
        console.print(response.text)
    else:
        console.print("שגיאה בקבלת הנתונים", style="bold red")

def main():
    logo = r"""	    _    _
      | |  | |
      | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
      |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \
      | |  | | (_| | | | | (_| | | | | | | (_| | | | |
      |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                           __/ |
                          |___/
    """
    console.print("  hello to our game!!!!!", style="bold magenta")
    console.print(logo)
    stsrt_game()

if __name__ == "__main__":
    main()
