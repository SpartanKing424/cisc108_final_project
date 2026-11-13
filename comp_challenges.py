from dataclasses import dataclass
import random
from time import time  

current_day = time() // 86400  # Get the current day in seconds
day_timer = 86400 - (time() % 86400)  # Calculate the time remaining in the current day
current_intrumental_challenge = "None"
current_emotional_challenge = "None"
current_rhythmic_challenge = "None"
@dataclass
class Challenge:
    title: str
    description: str
    type: str
    restrictions: str = None  # Optional restrictions for the challenge
#where challenges will be stored
instrumental_challenges = [Challenge("Tubarific", "Write a Sip for Tuba", "instrumental"), Challenge("Sax Attack", "Write a Sip for Saxophone", "instrumental")]
emotional_challenges = [Challenge("Sound of Jealousy", "Write a Sip that sounds jealous", "emotional"), Challenge("Music of Love", "Write a Sip that sounds like its in love", "emotional")]
rhythmic_challenges = [Challenge("Not Half Bad", "Write a Sip using only half notes", "rhythmic"), Challenge("Quartermaster", "Write a Sip using only quarter notes", "rhythmic")]

current_intrumental_challenge = random.choice(instrumental_challenges)
current_emotional_challenge = random.choice(emotional_challenges)
current_rhythmic_challenge = random.choice(rhythmic_challenges)
def get_daily_challenge(instruments: list[Challenge], emotions: list[Challenge], rhythms: list[Challenge], type: str) -> Challenge:
    '''
    gets a daily challenge from the list of the specificied challenge type
        instruments(list[Challenge]): list of potential instrument challenges
        emotions(list[Challenge]): list of potential emotional challenges
        rhymths(list[Challenge]): list of potential rhythmic challenges
        type(str): the actual selected challenge type
    '''
    challenge = "none"
    if type == "instrumental":
        challenge = random.choice(instrumental_challenges)
    elif type == "emotional":
        challenge = random.choice(emotional_challenges)
    elif type == "rhythmic":
       challenge = random.choice(rhythmic_challenges)
    return challenge
#get_daily_challenge is random, so it can't really be unit tested
get_daily_challenge(instrumental_challenges, emotional_challenges, rhythmic_challenges, "emotional")  # Call the function to initialize the challenges