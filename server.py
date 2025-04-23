from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

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

# dictionary for dialogues
dialogue_data = {
    "1": {
        "dialogue_id": "1",
        "text": "Oh no!! It’s all over the news. Your neighbor Amy was found dead in the woods.",
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
        "text": "Good news! I happened to meet a hiker passing through the area around the estimated time of Amy’s murder."
    },
    "9": {
        "dialogue_id": "9",
        "text": "I’ve managed to gather some more clues for you. See if you can use them to identify the culprit!"
    },
    "10": {
        "dialogue_id": "10",
        "text": "Try to use as few clues as possible! More importantly, don’t frame the wrong suspect. Your job and reputation are on the line."
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
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/brianna_the_bear.png",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/bear_single.png",
        "family": "bears"
    },
    "2": {
        "suspect_id": "2",
        "name": "Rebecca the Raccoon",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/rebecca_the_raccoon.png",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/raccoon_single.png",
        "family": "small mammals"
    },
    "3": {
        "suspect_id": "3",
        "name": "Emily the Elk",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/emily_the_elk.png",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/elk_single.png",
        "family": "hoofs (large)"
    },
    "4": {
        "suspect_id": "4",
        "name": "Claire the Coyote",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/claire_the_coyote.png",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/coyote_single.png",
        "family": "canines"
    },
    "5": {
        "suspect_id": "5",
        "name": "Ann the Armadillo",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/ann_the_armadillo.png",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/armadillo_single.png",
        "family": "small mammals"
    },
    "6": {
        "suspect_id": "6",
        "name": "Shar the Squirrel",
        "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/shar_the_squirrel.png",
        "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/squirrel_single.png",
        "family": "rodents"
    }
}
# dictionary for clues



# ==================================================================================================================
# ROUTES
# ==================================================================================================================
@app.route('/')
def home():
    return render_template('home.html')   

@app.route('/learn')
def learn():
    return render_template('learn.html')   

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