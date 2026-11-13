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

instrumental_challenges = [Challenge("Tubarific", "Write a Sip for Tuba", "instrumental"), Challenge("Sax Attack", "Write a Sip for Saxophone", "instrumental")]
emotional_challenges = [Challenge("Sound of Jealousy", "Write a Sip that sounds jealous", "emotional"), Challenge("Music of Love", "Write a Sip that sounds like its in love", "emotional")]
rhythmic_challenges = [Challenge("Not Half Bad", "Write a Sip using only half notes", "rhythmic"), Challenge("Quartermaster", "Write a Sip using only quarter notes", "rhythmic")]
def get_daily_challenges():
    current_day = time() // 86400  # Get the current day in seconds
    global day_timer, current_intrumental_challenge, current_emotional_challenge, current_rhythmic_challenge  #NO GlOBAL VARIABLES ALLOWED!!!
    if day_timer <= 0:
        day_timer = 86400  # Reset the day timer
        current_intrumental_challenge = random.choice(instrumental_challenges)
        current_emotional_challenge = random.choice(emotional_challenges)
        current_rhythmic_challenge = random.choice(rhythmic_challenges)
    print(current_intrumental_challenge.title, current_emotional_challenge.title, current_rhythmic_challenge.title)

get_daily_challenges()  # Call the function to initialize the challenges