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


# ==================================================================================================================
# ROUTES
# ==================================================================================================================
@app.route('/')
def home():
    return render_template('home.html')   

@app.route('/learn')
def learn():
    return render_template('learn.html')   

@app.route('/quiz/<id>')
def view(id=None):
    if id == '1' or id == '2' or id == '3' or id == '8' or id == '9' or id == '10':
        return render_template('quiz_dialogue.html', dialogue=dialogue_data[])
    else:
        return render_template('quiz.html')

@app.route('/quiz-result')
def quiz_result():
    return render_template('quiz_result.html')


# ==================================================================================================================
# RUN APP
# ==================================================================================================================
if __name__ == '__main__':
   app.run(debug = True, port=5001)