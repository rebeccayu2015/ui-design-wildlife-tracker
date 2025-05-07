from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import os
import logging
from datetime import datetime
import random

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
        "name": "Canines",
        "cover_image": "<insert GitHub link>",
        "description": "<insert text>",
        "animals": {
            "1": {
                "animal_id": "1",
                "name": "Wolf",
                "group": "Canines",
                "print_image": "<insert GitHub link>",
                "animal_image": "<insert GitHub link>",
                "alt_text": "<insert text>",
                "info": "<insert text>"
            },
            "2": {
                "animal_id": "2",
                "name": "Coyote",
                "group": "Canines",
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
                "name": "Cougar",
                "group": "Felines",
                "print_image": "<insert GitHub link>",
                "animal_image": "<insert GitHub link>",
                "alt_text": "<insert text>",
                "info": "<insert text>"
            },
            "2": {
                "animal_id": "2",
                "name": "Lynx",
                "group": "Felines",
                "print_image": "<insert GitHub link>",
                "animal_image": "<insert GitHub link>",
                "alt_text": "<insert text>",
                "info": "<insert text>"
            },
        },
    },
    "3": {
        "group_id": "3",
        "name": "Bears",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {

        },
    },
    "4": {
        "group_id": "4",
        "name": "Hoofs (Large)",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {
            
        },
    },
    "5": {
        "group_id": "5",
        "name": "Hoofs (Small)",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {
            
        },
    },
    "6": {
        "group_id": "6",
        "name": "Rodents",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {
            
        },
    },
    "7": {
        "group_id": "7",
        "name": "Small Mammals",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {
            
        },
    },
    "8": {
        "group_id": "8",
        "name": "Reptiles & Amphibians",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {
            
        },
    },
    "9": {
        "group_id": "9",
        "name": "Birds",
        "cover_image": "<insert GitHub link",
        "description": "<insert text>",
        "animals": {
            
        },
    },
}

# initializing quiz score
quiz_score = 0
clues = 1

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
# suspects_data = {
#     "1": {
#         "suspect_id": "1",
#         "name": "Brianna the Bear",
#         "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/brianna_the_bear.png?raw=true",
#         "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/grizzy_bear_track_front.png?raw=true",
#         "family": "bears"
#     },
#     "2": {
#         "suspect_id": "2",
#         "name": "Rebecca the Raccoon",
#         "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/rebecca_the_raccoon.png?raw=true",
#         "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/raccoon_track_front.png?raw=true",
#         "family": "small mammals"
#     },
#     "3": {
#         "suspect_id": "3",
#         "name": "Emily the Elk",
#         "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/emily_the_elk.png?raw=true",
#         "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/elk_track_front.png?raw=true",
#         "family": "hoofs (large)"
#     },
#     "4": {
#         "suspect_id": "4",
#         "name": "Claire the Coyote",
#         "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/claire_the_coyote.png?raw=true",
#         "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/coyote_track_front.png?raw=true",
#         "family": "canines"
#     },
#     "5": {
#         "suspect_id": "5",
#         "name": "Ann the Armadillo",
#         "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/ann_the_armadillo.png?raw=true",
#         "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/armadillo_track_front.png?raw=true",
#         "family": "small mammals"
#     },
#     "6": {
#         "suspect_id": "6",
#         "name": "Shar the Squirrel",
#         "suspect_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/shar_the_squirrel.png?raw=true",
#         "track_image": "https://github.com/rebeccayu2015/ui-design-wildlife-tracker/blob/main/static/images/squirrel_track_front.png?raw=true",
#         "family": "rodents"
#     }
# }

suspects_data = {
    "1": {
        "suspect_id": "1",
        "name": "Brianna the Bear",
        "suspect_image": "/static/images/brianna_the_bear.png",
        "track_image": "/static/images/bear_paw.png",
        "family": "bears"
    },
    "2": {
        "suspect_id": "2",
        "name": "Rebecca the Raccoon",
        "suspect_image": "/static/images/rebecca_the_raccoon.png",
        "track_image": "/static/images/raccoon_track_front.png",
        "family": "small mammals"
    },
    "3": {
        "suspect_id": "3",
        "name": "Emily the Elk",
        "suspect_image": "/static/images/emily_the_elk.png",
        "track_image": "/static/images/elk_track_front.png",
        "family": "hoofs (large)"
    },
    "4": {
        "suspect_id": "4",
        "name": "Claire the Coyote",
        "suspect_image": "/static/images/claire_the_coyote.png",
        "track_image": "/static/images/coyote_track_front.png",
        "family": "canines"
    },
    "5": {
        "suspect_id": "5",
        "name": "Ann the Armadillo",
        "suspect_image": "/static/images/ann_the_armadillo.png",
        "track_image": "/static/images/armadillo_track_front.png",
        "family": "small mammals"
    },
    "6": {
        "suspect_id": "6",
        "name": "Shar the Squirrel",
        "suspect_image": "/static/images/shar_the_squirrel.png",
        "track_image": "/static/images/squirrel_track_front.png",
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

# dictionary for score feedback
score_data = {
    "1": {
        "clue_id": "1",
        "text": "Perfect score. You’re a natural!"
    },
    "2": {
        "clue_id": "2",
        "text": "You know your stuff!"
    },
    "3": {
        "clue_id": "3",
        "text": "You’re getting there."
    },
    "4": {
        "clue_id": "4",
        "text": "Your tracking skills might need some work..."
    }
}

# dictionary for sort prints user responses (key = family id)
sort_prints_responses = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": [],
    "9": []
}

# dictionary for match prints user responses (key = suspect id)
match_prints_responses = {
    "1": "",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
    "6": ""
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

#track patterns images and gifs
patterns = [
{
    "name": "Zig-Zaggers",
    "track_img": "images/track_patterns/zig-zaggers.png",
    "animal_imgs": [
        "images/track_patterns/dear.gif",
        "images/track_patterns/fox.gif",
        "images/track_patterns/coyote.gif"
    ]
},
{
    "name": "Leapers/Hoppers",
    "track_img": "images/track_patterns/leapers-hoppers.png",
    "animal_imgs": [
        "images/track_patterns/bunny.gif",
        "images/track_patterns/squirrel.gif",
        "images/track_patterns/frog.gif"
    ]
},
{
    "name": "Bounders",
    "track_img": "images/track_patterns/bounders.png",
    "animal_imgs": [
        "images/track_patterns/otter.gif",
        "images/track_patterns/marten.gif",
        "images/track_patterns/weasel.gif"
    ]
},
{
    "name": "Waddlers",
    "track_img": "images/track_patterns/waddlers.png",
    "animal_imgs": [
        "images/track_patterns/bear.gif",
        "images/track_patterns/penguin.gif",
        "images/track_patterns/porcupine.gif"
    ]
},
]

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
    return render_template('learn/learn.html')   

@app.route('/learn')
def learn():
    record_page_visit()
    return render_template('learn/learn.html')   

@app.route('/learn/track-patterns')
def track_patterns():
    record_page_visit()
    return render_template('learn/track_patterns.html', patterns=patterns)

@app.route('/learn/track-characteristics')
def track_characteristics_page():
    record_page_visit()
    return render_template('learn/track_characteristics.html', characteristics=track_characteristics)

@app.route('/learn/canines')
def learn_canines():
    record_page_visit()
    return render_template('learn/learn_canines.html')   


@app.route('/quiz/<id>')
def view(id=None):
    if id == '1' or id == '2' or id == '3' or id == '8' or id == '9' or id == '10':
        if id == '1':
            global quiz_score
            global clues
            quiz_score = 0
            clues = 1
        return render_template('quiz_dialogue.html', dialogue=dialogue_data[id]['text'], id=int(id))
    if id == '4':
        return render_template('quiz_tasks_suspects.html', tasks=tasks_data, suspects=suspects_data, id=int(id))
    if id == '6':
        return render_template('quiz_sort_prints.html', suspects=suspects_data, tracks=track_data, id=int(id), sort_prints_responses=sort_prints_responses)
    if id == '7':
        order = list(range(1, len(suspects_data)+1))
        random.shuffle(order)
        return render_template('quiz_match_prints.html', suspects=suspects_data, tracks=track_data, id=int(id), match_prints_responses=match_prints_responses, order=order)
    if id == '11':
        return render_template('quiz_clue.html', clues=clues_data, id=int(id), suspects=suspects_data)
    if id == '12':
        return render_template('quiz_identify_culprit.html', suspects=suspects_data, id=int(id))
    else:
        return render_template('quiz.html')

@app.route('/learn/birds')
def learn_birds():
    record_page_visit()
    return render_template('learn_birds.html')

@app.route('/learn/small-mammals')
def learn_small_mammals():
    record_page_visit()
    return render_template('learn_small_mammals.html')

@app.route('/learn/reptiles-amphibians')
def learn_reptiles_amphibians():
    record_page_visit()
    return render_template('learn_reptiles_amphibians.html')

@app.route('/learn/deer')
def learn_deer():
    record_page_visit()
    return render_template('learn_deer.html')

@app.route('/learn/felines')
def learn_felines():
    record_page_visit()
    return render_template('learn_felines.html')

@app.route('/learn/bears')
def learn_bears():
    record_page_visit()
    return render_template('learn_bears.html')

@app.route('/learn/hoofs-large')
def learn_hoofs_large():
    record_page_visit()
    return render_template('learn_hoofs_large.html')

@app.route('/learn/hoofs-small')
def learn_hoofs_small():
    record_page_visit()
    return render_template('learn_hoofs_small.html')

@app.route('/learn/rodents')
def learn_rodents():
    record_page_visit()
    return render_template('learn_rodents.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quiz-result')
def quiz_result():
    feedback = ""
    if quiz_score <= 3:
        feedback = score_data['1']['text']
    elif quiz_score <= 5:
        feedback = score_data['2']['text']
    elif quiz_score <= 7:
        feedback = score_data['3']['text']
    else:
        feedback = score_data['4']['text']

    return render_template('quiz_result.html', suspects=suspects_data, score=quiz_score, feedback=feedback)

# ==================================================================================================================
# AJAX FUNCTIONS
# ==================================================================================================================
@app.route('/record_response', methods=['POST'])
def record_response():
    global quiz_score
    json_data = request.get_json()
    print(json_data)
    answer = json_data['answer']

    if answer == '1':
        quiz_score = 0
    else:
        quiz_score += 3

    return jsonify({"status": "ok"})

@app.route('/clue', methods=['POST'])
def clue():
    global quiz_score
    global clues
    
    clues += 1
    quiz_score += 1

    return jsonify({"status": "ok", "clues": clues, "clues_data": clues_data})

@app.route('/check_sort_prints', methods=['POST'])
def check_sort_prints():
    results = request.get_json()  # a dict: {family_id: [suspect_ids]}
    total_number = 0
    correct_matches = 0

    global quiz_score
    global sort_prints_responses 
    sort_prints_responses = results
    for family_id, suspect_ids in sort_prints_responses.items():
        box_family = track_data[family_id]['name'].lower()
        for suspect_id in suspect_ids:
            suspect_family = suspects_data[suspect_id]['family'].lower()
            total_number += 1
            if box_family == suspect_family:
                correct_matches += 1

    quiz_score += 1

    '''
    results = {}

    for box_id, suspects in assignments.items():
        expected = expected_correlations.get(box_id, set())
        assigned = set(suspects)

        # Compute intersection and status
        matched = assigned & expected
        extra = assigned - expected
        missing = expected - assigned

        results[box_id] = {
            "matched": list(matched),
            "extra": list(extra),
            "missing": list(missing),
        }
    '''
    response = {
        "total_number": total_number,
        "correct_matches": correct_matches
    }

    return jsonify(response)

@app.route('/check_match_prints', methods=['POST'])
def check_match_prints():
    results = request.get_json()  # a dict: {suspect_id: track_id}

    global quiz_score
    global match_prints_responses

    total_number = 0
    correct_matches = 0
    match_prints_responses = results
    for suspect_id, track_id in match_prints_responses.items():
        total_number += 1
        if suspect_id == track_id: # track matches to suspect
            correct_matches += 1

    quiz_score += 1

    response = {
        "total_number": total_number,
        "correct_matches": correct_matches
    }

    return jsonify(response)


# ==================================================================================================================
# RUN APP
# ==================================================================================================================
if __name__ == '__main__':
   app.run(debug = True, port=5001)