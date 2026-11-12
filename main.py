
from bakery import assert_equal
from dataclasses import dataclass
from drafter import *
from user_info import User, user_database


#go take a look at choosealicense.com
'''
UV HELPFUL COMMANDS
uv run main.py = run the script
uv add (extension) = add an extension to the project
Ctrl + C = stop the server
'''

@dataclass
class Note:
    pitch: str           
    length: int
    position: int
    is_rest: bool

@dataclass
class Measure:
    size: int
    beats: list[Note]

@dataclass
class State:
    message: str
    username: str
    password: str

@route
def index(state: State) -> Page:
    return Page(
        state,
        [Text(state.message),
         "\n",
        "Username:",
        TextBox("username", ''),
        "\n",
        "Password:",
        TextBox("password", ''),
        "\n",
        Button("Login", "login"),
        "\n",
        Button("Sign Up", "sign_up")])
@route
def login(state: State, username: str, password: str) -> Page:
    is_user = False
    user_number = 0
    for user in user_database:
        user_number += 1
        if user.username == username:
            is_user = True
            break

    if is_user and password == user_database[user_number - 1].password:
        state = State("Login successful!", username, password)
        return main_menu(State("Welcome, " + username + "!", username, password))
    else:
        state = State("Login failed. Please try again.", '', '')
        return index(state)
@route
def sign_up(state: State) -> Page:
    pass


@route
def main_menu(state: State) -> Page:
    return Page(
        state,
        [Text(state.message),
         "\n",
         "What challenge do you want to sip today?",
         "\n",
         Button("Emotional Challenge", "start_challenge", [Argument("start_challenge", "emotional")]),
         "\n",
         Button("Instrumental Challenge", "start_challenge", [Argument("start_challenge", "instrumental")]),
         "\n",
         Button("Rhythmic Challenge", "start_challenge", [Argument("start_challenge", "rhythmic")])])
start_server(State("Welcome to Sips of Ti-Do." + "\n"+ "Please log in or sign up.", '', ''))

@route
def start_challenge(state: State, challenge: str) -> Page:
    pass

'''
Functions needed
1. Add_note - when a user adds a note to the staff
2. Play_measure
3. Gen_measures - sets up measures based on user specifications
'''
