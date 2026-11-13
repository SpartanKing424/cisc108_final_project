
from bakery import assert_equal
from dataclasses import dataclass
from drafter import *
from user_info import User, user_database
from notes import real_notes, DEFAULT_NOTE, DEFAULT_INDEX
from comp_challenges import Challenge, get_daily_challenge, instrumental_challenges, emotional_challenges, rhythmic_challenges
from PIL import Image
#go take a look at choosealicense.com

'''
UV HELPFUL COMMANDS
uv run main.py = run the script
uv add (extension) = add an extension to the project
Ctrl + C = stop the server
'''

@dataclass
class Note:       #building block dataclass for music related programs
    pitch: str           
    length: float
    is_rest: bool

#set up reusable rest variables
whole_rest = Note("whole rest", 4, True)
half_rest = Note("half rest", 2, True)
quarter_rest = Note("quarter rest", 1, True)
eighth_rest = Note("eighth rest", .5, True)

@dataclass
class Measure:
    size: int
    beats: list[Note]

@dataclass
class State:
    message: str
    username: str
    password: str
    challenge: Challenge = None
    user_composition: MusicComposition = None

@dataclass
class MusicComposition:        
    length: int #number of measures in the composition
    comp_measures: list[Measure]
    focus_measure: Measure
    focus_measure_num: int
    current_beat: int 

@route
def index(state: State) -> Page:
    '''
    Login/Signup Page
        state(State): either will be the startup state up the updated username + password state 
        if the user signs up
    '''
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
assert_equal(index(State("Welcome to Sips of Ti-Do" + "\n" + "Please log in or sign up.", '', '')), Page(
        State("Welcome to Sips of Ti-Do" + "\n" + "Please log in or sign up.", '', '', None, None),
        [Text("Welcome to Sips of Ti-Do" + "\n" + "Please log in or sign up."),
         "\n",
        "Username:",
        TextBox("username", ''),
        "\n",
        "Password:",
        TextBox("password", ''),
        "\n",
        Button("Login", "login"),
        "\n",
        Button("Sign Up", "sign_up")]) )
@route
def login(state: State, username: str, password: str) -> Page:
    '''
    checks if a users login information matches a registered User from a seperate user database file
        if it does, they proceed to the main menu,
        else they are returned to the login page with an error message 
    state(State): here it just focuses on the current username + password
    username(str): the user's username
    password(str): the user's password
    '''
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
#assert_equal
@route
def sign_up(state: State) -> Page:
    '''
    allows a user to sign up as a new user by inputing a new username and password
        state(State): will be updated with a new message prompting the user to enter 
        a new username and password
    '''
    state.message = "Please type in a username and a strong password!"
    return Page(state, [Text(state.message),
         "\n",
        "Username:",
        TextBox("username", ''),
        "\n",
        "Password:",
        TextBox("password", ''),
        "\n",
        Button("Back", "index"),
        "\n",
        Button("Sign Up", "save_login")])
#assert_equal
@route
def save_login(state: State, username: str, password: str) -> Page:
    '''
    takes the inputed user sign up info and stores it in the user database(temporarily), 
    then the user is sent back to the index/login page
        state(State): will be updated with new user info
        username(str): New user's username that they entered
        password(str): New user's password that they entered

    '''
    state.user = username
    state.password = password
    #add confirm password and astericks
    user_database.append(User(username, password))
    return index(state)
#assert_equal
    


@route
def main_menu(state: State) -> Page:
    '''
    the page where users select what composition challenge they'll do for the day
        state(State): has the saved user info, and will store the TYPE of challenge they select
    '''
    return Page(
        state,
        [Text(state.message),
         "\n",
         "What challenge do you want to sip today?",
         "\n",
         Button("Emotional Challenge", "composition_settings", [Argument("challenge_type", "emotional")]),
         "\n",
         Button("Instrumental Challenge", "composition_settings", [Argument("challenge_type", "instrumental")]),
         "\n",
         Button("Rhythmic Challenge", "composition_settings", [Argument("challenge_type", "rhythmic")])])
#assert_equal

@route 
def composition_settings(state: State, challenge_type: str) -> Page:
    '''
    the page where the specifics of the user's choosen challenge is revealed,
    and also where the user selects how many measures they want to write
        state(State): will save the specific challenge and the number of measures the user wants to write
    '''
    daily_challenge = get_daily_challenge(instrumental_challenges, emotional_challenges, rhythmic_challenges, challenge_type)

    state.user_composition = MusicComposition(0, [Measure(4, [whole_rest])], 1, 1, 1)
    return Page(state, ["Welcome to the " + str(challenge_type) + " challenge!",
                "\n",
                "Your Challenge:" + str(daily_challenge.description),
                "\n",
                "How many measures would you like to sip today?",
                SelectBox("num_measures", [1, 2, 3, 4, 5, 6, 7, 8], 2),
                "\n",
                Button("Let's Sip!", "composition", [Argument("current_measure", 1), Argument("current_beat", 1)])]
                )
#Can't assert_equal for composition_settings() since it involves random elements               
@route
def composition(state: State, num_measures: int, current_measure: int, current_beat: int) -> Page:
    '''
    the central page for composing, will be constantly updated based on user input
        state(State): user info + challenge info
        num_measures(int): total number of measures in the composition
        current_measure(int): which measure we are at in the composition, like an index
        current_beat(int): the current beat the user is working on within the current
        measure, again, like an index for the measure
    '''
    state.user_composition.length = num_measures
    for i in range(num_measures-1):
                print(state.user_composition)
                state.user_composition.comp_measures.append(Measure(4, [whole_rest]))
    focus = state.user_composition.comp_measures[state.user_composition.focus_measure_num]
    focus_note_text = ''
    for beat in focus.beats:
        focus_note_text = focus_note_text + beat.pitch 

    return Page(state, 
                [ "Measure: " + str(current_measure) + "/" + str(num_measures),
                    Picture.from_file("Measure.png").scale(0.25),
                    Text(focus_note_text),
                    Button("Add Note", "add_note"), #does not work yet :(
                    "\n",
                    SelectBox("note_name", ["A", "B", "C", "D", "E", "F"]),
                    SelectBox("octave", [1, 2, 3, 4, 5, 6])])
#assert_equal

@route
def add_note(state: State, note_name: str, octave: str) -> Page: 
#this function is still in progress
    '''
    adds a note to the current measure both visually, and systemically
        state(State): saved challenge settings and restrictions
        note_name(str): Note's letter (A,B,C,D,E,F, OR G)
        octave(str): Note's octave 1-6 (lowest to highest octave)

    '''
    state.user_composition.comp_measures[state.user_composition.focus_measure_num].beats.append(str(note_name + octave))
    if state.user_composition.current_beat + 1 > 4:
        state.user_composition.focus_measure_num += 1
        state.user_composition.current_beat = 1
    else:
        state.user_composition.current_beat += 1
    return composition(state, state.user_composition.length, state.user_composition.focus_measure_num, state.user_composition.current_beat)


   
    
    pass
'''
Functions needed
1. Add_note - when a user adds a note to the staff
2. Play_measure
3. Gen_measures - sets up measures based on user specifications
'''
#stylistic things
set_website_title("Sips of Ti-Do")
set_website_style("latex")
set_site_information(
    author = "Gabriel Young",
    description = "A daily program for writting small 'sips' of music!",
    sources = "Brought to you via Drafter",
    planning = ["CS1 Final Project 0_ Pick a Problem.docx", "CS1 Final Project 1_ Design.docx"],
    links = ["https://github.com/SpartanKing424/cisc108_final_project"]
)
start_server(State("Welcome to Sips of Ti-Do" + "\n" + "Please log in or sign up.", '', ''))