
from bakery import assert_equal
from dataclasses import dataclass
from drafter import *
from user_info import User, user_database
from comp_challenges import Challenge, get_daily_challenges, current_intrumental_challenge, current_emotional_challenge, current_rhythmic_challenge

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

@dataclass
class MusicComposition:
    measures: list[Measure]
    current_measure: int

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
         Button("Emotional Challenge", "composition_settings", [Argument("challenge", "emotional")]),
         "\n",
         Button("Instrumental Challenge", "composition_settings", [Argument("challenge", "instrumental")]),
         "\n",
         Button("Rhythmic Challenge", "composition_settings", [Argument("challenge", "rhythmic")])])


@route 
def composition_settings(state: State, challenge: str) -> Page:
    get_daily_challenges()
    if challenge == "instrumental":
        current_challenge = current_intrumental_challenge
    elif challenge == "emotional":
        current_challenge = current_emotional_challenge
    elif challenge == "rhythmic":
        current_challenge = current_rhythmic_challenge
    return Page(state, ["Welcome to the " + str(challenge) + " challenge!",
                "\n",
                "Your Challenge: Placeholder",
                "\n",
                "How many measures would you like to sip today?",
                SelectBox("num_measures", [1, 2, 3, 4, 5, 6, 7, 8], 2),
                "\n",
                Button("Let's Sip!", "composition", Argument("challenge", challenge))]
                )
                    
@route
def composition(state: State, challenge: str, num_measures: int) -> Page:
    return Page(state,
                [Picture.from_file("Measure.png").scale(0.5)])
    pass
'''
Functions needed
1. Add_note - when a user adds a note to the staff
2. Play_measure
3. Gen_measures - sets up measures based on user specifications
'''
start_server(State("Welcome to Sips of Ti-Do" + "\n" + "Please log in or sign up.", '', ''))