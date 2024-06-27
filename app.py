# escape_metaverse.py

import streamlit as st
import pandas as pd
import random
import openai
import json
import functions as ff
import time


openai.api_key = "########################################"

# Convert your image and get the base64 string
base64_image = ff.image_to_base64('images/codeescape_logo.png')

# Ensure the session state has the necessary variable
if 'name' not in st.session_state:
    st.session_state.name = "Player"

# Initial state checks
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.intro_shown = False
    st.session_state.intro_screen = False
    st.session_state.current_room = 0  # Start in the Metaverse Prison
    st.session_state.current_puzzle = 1
    st.session_state.score = 0
    st.session_state.name = ""
    st.session_state.show_escape_story = False
    st.session_state.game_over = False
    st.session_state.game_over_siri = False
    st.session_state.cookie_bit = False
    st.session_state.prison_stage = 0
    st.session_state.show_skip_to_room_2 = False
    # st.session_state.selected_puzzle = None


# Prompt user for their name and start the game
if not st.session_state.intro_shown and not st.session_state.intro_screen:
   # Define custom CSS for the text input label
    custom_css = """
        <style>
        .styled-label {
            font-family: 'Courier New', Courier, monospace;
            font-size: 24px;
            font-weight: bold;
            color: white;
            text-shadow: 0 0 5px rgba(255, 255, 255, 0.8),
                        0 0 10px rgba(255, 255, 255, 0.8),
                        0 0 15px rgba(255, 255, 255, 0.8),
                        0 0 20px rgba(255, 255, 255, 0.8),
                        0 0 25px rgba(255, 255, 255, 0.8);
            animation: blinkingText 1.2s infinite;
        }

        @keyframes blinkingText {
            0% { color: white; }
            49% { color: white; }
            60% { color: transparent; }
            99% { color: transparent; }
            100% { color: white; }
        }
        </style>
    """

    # Use st.markdown to inject custom CSS and HTML for the label and input box
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown('<div class="styled-label">Enter your name to start the game:</div>', unsafe_allow_html=True)
    st.session_state.name = st.text_input("", key="name_input")

    
    if st.session_state.name and st.button("Start Game", key="start_game"):
        st.session_state.intro_screen = True
        st.experimental_rerun()
    ff.set_background_image('https://amplify.nabshow.com/wp-content/uploads/sites/12/2022/05/metaverse-ontrack.gif')
    st.image(ff.load_image('images/codeescape_logo.png'), use_column_width=True)

# Show the intro if the name has been entered but the game hasn't started
if st.session_state.intro_screen and not st.session_state.game_started:
    ff.storyline()

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if 'puzzle_start_time' not in st.session_state:
    st.session_state.puzzle_start_time = None

if 'room_start_time' not in st.session_state:
    st.session_state.room_start_time = None

if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = 0

# Load the question bank for matching functions with descriptions
with open('question_bank/data_cleaning_match_questions.json', 'r') as file:
    match_questions = json.load(file)

# Load questions from the JSON file
with open('question_bank/scaling_questions.json', 'r') as file:
    scaling_questions = json.load(file)

# Load the decision tree question bank from a JSON file with the correct encoding
if "decision_tree_question_bank" not in st.session_state:
    with open("question_bank/decision_tree_question_bank.json", "r", encoding="utf-8") as f:
        st.session_state.decision_tree_question_bank = json.load(f)

# Load the question bank from a JSON file with the correct encoding
with open("question_bank/confusion_matrix_questions.json", "r", encoding="utf-8") as f:
    confusion_matrix_questions = json.load(f)

# Load the question bank from JSON
with open("question_bank/question_bank.json", "r") as f:
    question_bank = json.load(f)["questions"]

# Ensure the puzzle is selected only once per session
if 'selected_puzzle' not in st.session_state:
    st.session_state.selected_puzzle = random.choice(question_bank)

# question = st.session_state.selected_puzzle

# Create the database
ff.create_database()

# Initialize Hangman game state
if 'hangman_word' not in st.session_state:
    ff.start_new_game()
if 'hangman_status' not in st.session_state:
    st.session_state.hangman_status = None


# Example predefined identifiers and clues
predefined_identifiers = [
    "TABLEAU", "HEATMAP", "BAR_CHART", "SEABORN", "AXIS", 
    "SCALE", "LEGEND", "MATPLOTLIB", "NETWORK_GRAPH", "PLOTLY"
]

predefined_clues = {
    "TABLEAU": "In vibrant hues and interactive views, I turn data into stories for you.",
    "HEATMAP": "Colors reveal the data's appeal, in a grid where patterns congeal.",
    "BAR_CHART": "Bars rise high to the sky, showing quantities as time goes by.",
    "SEABORN": "Elegant and sleek, my plots speak with a touch unique.",
    "AXIS": "I guide your sight, aligning data just right, from left to right.",
    "SCALE": "From low to high, I quantify, making data points comply.",
    "LEGEND": "In the corner, I reside, explaining colors side by side.",
    "MATPLOTLIB": "Versatile and free, I bring your data to life visually.",
    "NETWORK_GRAPH": "Nodes and edges intertwine, showing connections so divine.",
    "PLOTLY": "Interactive and bold, my plots unfold, stories told."
}

# Function to display the game status and score
# Main game logic
if st.session_state.game_started:
    # Check if the game is over
    if st.session_state.game_over:
        st.title("Game Over")
        st.write("You have failed to escape the metaverse. Please try again. Remember to take rest and trust your imagination.")
        st.markdown("![Alt Text](https://i.gifer.com/y7.gif)")
        if st.button("Restart Game"):
            # Reset all session state variables to restart the game
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()
    elif st.session_state.game_over_siri:
        st.title("Game Over")
        st.write("Hello, How can I help you Today?")
        st.write("BOOOOOOMMMMMM!!!!")
        st.markdown("![Alt Text](https://media.tenor.com/igZCc-gVpjsAAAAj/%D0%B2%D0%B7%D1%80%D1%8B%D0%B2.gif)")
        st.write("Asking Siri to help you caused an explosion. Please try again.")
        if st.button("Restart Game"):
            # Reset all session state variables to restart the game
            for key in st.session_state.keys():
                del st.session_state[key]
            st.experimental_rerun()
    else:
        # Hide the sidebar in Metaverse Prison room
        if st.session_state.current_room == 0:
            st.sidebar.empty()
        else:
             # Add story and game status to the sidebar
            ff.display_status()
            # Add skip buttons in the sidebar with unique keys
            # st.sidebar.title("Debug buttons")
            # if st.sidebar.button("Skip puzzle", key="skip_puzzle"):
            #     st.session_state.current_puzzle += 1
            #     st.experimental_rerun()
            # if st.sidebar.button("Skip sql puzzle", key="skip_sql_puzzle"):
            #     st.session_state.current_sql_puzzle += 1
            #     st.experimental_rerun()
            # if st.sidebar.button("Next room", key="skip_room"):
            #     st.session_state.current_room += 1
            #     st.experimental_rerun()
            # if st.sidebar.button("Go back", key="go_back"):
            #     st.session_state.current_room -= 1
            #     st.experimental_rerun()

        if 'start_time' in st.session_state:
            ff.display_timer()

        # Display the current room
        if st.session_state.current_room == 0:
            ff.metaverse_prison()
        elif st.session_state.current_room == 5:
            ff.display_final_page()  # Add this line to display the final page
        else:
            if st.session_state.current_room == 1:
                ff.room_1()
            elif st.session_state.current_room == 2:
                ff.room_2()
            elif st.session_state.current_room == 3:
                ff.room_3()
            elif st.session_state.current_room == 4:
                ff.room_4()
                if st.session_state.current_puzzle == 5:
                    st.session_state.current_room = 5
                    st.experimental_rerun()
else:
    # Start the game and set the start time
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

