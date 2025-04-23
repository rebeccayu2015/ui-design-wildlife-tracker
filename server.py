from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import os
import logging
from datetime import datetime

app = Flask(__name__)


# ==================================================================================================================
# JSON DATA
# ==================================================================================================================
# Data for track patterns
pattern_data = {
    "1": {
        "pattern_id": "1",
        "name": "zig-zaggers",
        "print_image": "<insert GitHub link>",
        "animal_gifs": ["<insert GitHub link>", "<insert GitHub link>", "<insert GitHub link>"]
    },
}

# Data for track characteristics
char_data = {
    "1": {
        "char_id": "1",
        "name": "width",
        "description": "<insert text>",
        "char_image": "<insert GitHub link>"
    },
}

# Data for animal groups and their corresponding animal tracks
track_data = {
    "1": {
        "group_id": "1",
        "name": "canines",
        "cover_image": "<insert GitHub link>",
        "description": "<insert text>",
        "animals": {
            "1": {
                "animal_id": "1",
                "name": "wolf",
                "group": "canines",
                "print_image": "<insert GitHub link>",
                "animal_image": "<insert GitHub link>",
                "alt_text": "<insert text>",
                "info": "<insert text>"
            },
            "2": {
                "animal_id": "2",
                "name": "coyote",
                "group": "canines",
                "print_image": "<insert GitHub link>",
                "animal_image": "<insert GitHub link>",
                "alt_text": "<insert text>",
                "info": "<insert text>"
            },
        },
    },
    "2": {
        "group_id": "2",
        "name": "Felines",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {
            "1": {
                "animal_id": "1",
                "name": "cougar",
                "group": "felines",
                "print_image": "<insert GitHub link>",
                "animal_image": "<insert GitHub link>",
                "alt_text": "<insert text>",
                "info": "<insert text>"
            },
            "2": {
                "animal_id": "2",
                "name": "lynx",
                "group": "felines",
                "print_image": "<insert GitHub link>",
                "animal_image": "<insert GitHub link>",
                "alt_text": "<insert text>",
                "info": "<insert text>"
            },
        },
    },
}

# initializing quiz score
quiz_score = 0

# dictionary for dialogues
dialogue_data = {
    "1": {
        "dialogue_id": "1",
        "text": "Oh no!! It's all over the news. Your neighbor Amy was found dead in the woods.",
    },
    "2": {
        "dialogue_id": "2",
        "text": "The only clues are the tracks left by animals passing through the area at the time of her death.",
    },
    "3": {    
        "dialogue_id": "3", 
        "text": "As the only detective on this case, your job is to investigate these tracks and identify the culprit. Good luck!",
    },
    "8": {
        "dialogue_id": "8",
        "text": "Good news! I happened to meet a hiker passing through the area around the estimated time of Amy's murder."
    },
    "9": {
        "dialogue_id": "9",
        "text": "I've managed to gather some more clues for you. See if you can use them to identify the culprit!"
    },
    "10": {
        "dialogue_id": "10",
        "text": "Try to use as few clues as possible! More importantly, don't frame the wrong suspect. Your job and reputation are on the line."
    }
}

# dictionary for tasks
tasks_data = {
    "1": {
        "task_id": "1",
        "text": "Collect evidence from crime scene"
    },
    "2": {
        "task_id": "2",
        "text": "Sort prints into groups"
    },
    "3": {
        "task_id": "3",
        "text": "Match prints to suspects"
    },
    "4": {    
        "task_id": "4", 
        "text": "Identify the culprit"
    }
}

# dictionary for suspects (image, name, track, family)
suspects_data = {
    "1": {
        "suspect_id": "1",
        "name": "Brianna the Bear",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/brianna_the_bear.png?raw=true",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/bear_single.png",
        "family": "bears"
    },
    "2": {
        "suspect_id": "2",
        "name": "Rebecca the Raccoon",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/rebecca_the_raccoon.png?raw=true",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/raccoon_single.png",
        "family": "small mammals"
    },
    "3": {
        "suspect_id": "3",
        "name": "Emily the Elk",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/emily_the_elk.png?raw=true",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/elk_single.png",
        "family": "hoofs (large)"
    },
    "4": {
        "suspect_id": "4",
        "name": "Claire the Coyote",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/claire_the_coyote.png?raw=true",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/coyote_single.png",
        "family": "canines"
    },
    "5": {
        "suspect_id": "5",
        "name": "Ann the Armadillo",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/ann_the_armadillo.png?raw=true",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/armadillo_single.png",
        "family": "small mammals"
    },
    "6": {
        "suspect_id": "6",
        "name": "Shar the Squirrel",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/shar_the_squirrel.png?raw=true",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/squirrel_single.png",
        "family": "rodents"
    }
}
# dictionary for clues
clues_data = {
    "11": {
        "clue_id": "1",
        "text": "The prints were of a larger size."
    },
    "12": {
        "clue_id": "2",
        "text": "The tracks seemed to be of a waddler pattern."
    },
    "13": {
        "clue_id": "3",
        "text": "The print had a wide heel pad."
    },
    "14": {
        "clue_id": "4",
        "text": "The print had claws."
    },
    "15": {
        "clue_id": "5",
        "text": "The print had five rounded toes."
    }
}

# dictionary for sort prints user responses
sort_prints_responses = {
    "canines": [],
    "felines": [],
    "bears": [],
    "hoofs (large)": [],
    "hoofs (small)": [],
    "rodents": [],
    "small mammals": [],
    "reptiles/amphibians": [],
    "birds": []
}

# dictionary for match prints user responses
match_prints_responses = {
    "Brianna the Bear": "",
    "Rebecca the Raccoon": "",
    "Emily the Elk": "",
    "Claire the Coyote": "",
    "Ann the Armadillo": "",
    "Shar the Squirrel": ""
}

# dictionary for tracking characteristics paws and descriptions
track_characteristics = {
    "width": {
        "title": "Width",
        "description": "The distance from the left side of the print to the right side of the same print.",
        "image": "/static/images/track_characteristics/track_characteristics_width.png"
    },
    "depth": {
        "title": "Depth",
        "description": "How deep the track is pressed into the ground, which can indicate weight and surface.",
        "image": "/static/images/track_characteristics/track_characteristics_depth.png"
    },
    "length": {
        "title": "Length",
        "description": "The distance from the front of the print to the back of the print.",
        "image": "/static/images/track_characteristics/track_characteristics_length.png"
    },
    "stride": {
        "title": "Stride",
        "description": "The measurement from the heel of one print to the heel of the other print on the same side.",
        "image": "/static/images/track_characteristics/track_characteristics_stride.png"
    },
    "number_of_toes": {
        "title": "Number of Toes",
        "description": "Different animal groups have different number of toes.",
        "image": "/static/images/track_characteristics/track_characteristics_num_toes.png"
    },
    "straddle": {
        "title": "Straddle",
        "description": "The width of the track from the outside of the right track to the outside of the left track.",
        "image": "/static/images/track_characteristics/track_characteristics_straddle.png"
    },
    "nails": {
        "title": "Nails",
        "description": "Nails/claws may be retracted or extended depending on animal group and behavior.",
        "image": "/static/images/track_characteristics/track_characteristics_nails.png"
    },
    "front_rear": {
        "title": "Front/Rear",
        "description": "Front and rear paws may have slightly different sizes and shapes, depending on the animal.",
        "image": "/static/images/track_characteristics/track_characteristics_front_rear.png"
    }
}


#user activity logs
activity_logger = logging.getLogger("learn_logger")
activity_logger.setLevel(logging.INFO)

if not os.path.exists("logs"):
    os.makedirs("logs")

file_handler = logging.FileHandler("logs/user_activity.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))

activity_logger.addHandler(file_handler)

def record_page_visit():
    user_ip = request.remote_addr
    path = request.path
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    activity_logger.info(f"[PAGE VISIT] User {user_ip} visited {path} at {timestamp}")


# ==================================================================================================================
# ROUTES
# ==================================================================================================================
@app.route('/')
def home():
    record_page_visit()
    return render_template('home.html')   

@app.route('/learn')
def learn():
    record_page_visit()
    return render_template('learn/learn.html')   

@app.route('/learn/canines')
def learn_canines():
    record_page_visit()
    return render_template('learn/learn_canines.html')   

@app.route('/learn/track-patterns')
def track_patterns_page():
    return render_template('learn/track_patterns.html')

@app.route('/learn/track-characteristics')
def track_characteristics_page():
    record_page_visit()
    return render_template('learn/track_characteristics.html', characteristics=track_characteristics)

@app.route('/learn/birds')
def learn_birds():
    return render_template('learn_birds.html')

@app.route('/learn/small-mammals')
def learn_small_mammals():
    return render_template('learn_small_mammals.html')

@app.route('/learn/reptiles-amphibians')
def learn_reptiles_amphibians():
    return render_template('learn_reptiles_amphibians.html')

@app.route('/learn/deer')
def learn_deer():
    return render_template('learn_deer.html')

@app.route('/learn/felines')
def learn_felines():
    return render_template('learn_felines.html')

@app.route('/learn/bears')
def learn_bears():
    return render_template('learn_bears.html')

@app.route('/learn/hoofs-large')
def learn_hoofs_large():
    return render_template('learn_hoofs_large.html')

@app.route('/learn/hoofs-small')
def learn_hoofs_small():
    return render_template('learn_hoofs_small.html')

@app.route('/learn/rodents')
def learn_rodents():
    return render_template('learn_rodents.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz-result')
def quiz_result():
    return render_template('quiz_result.html')



# ==================================================================================================================
# RUN APP
# ==================================================================================================================
if __name__ == '__main__':
   app.run(debug = True, port=5001)