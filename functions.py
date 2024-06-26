# functions.py

import sqlite3
import time
import streamlit as st
import pandas as pd
from PIL import Image
import random
import streamlit.components.v1 as components
import plotly.express as px
import time
import base64
import json
import openai

openai.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Load images
def load_image(file_path):
    """ Load and display image """
    return Image.open(file_path)

def image_to_base64(image_path):
    """ Convert image to base64 """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def storyline():
    """ Display the storyline of the game"""

    st.title("Escape from the Virtual Metaverse")
    # Embed the HTML file
    components.html(
    f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                background: black;
                color: white;
                font-family: 'Courier New', Courier, monospace;
            }}
            .container {{
                position: relative;
                text-align: center;
                width: 100%;
                height: 100%;
                background-image: url(https://i.gifer.com/QWc9.gif);
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .typed-text {{
                font-size: 20px;
                white-space: pre-wrap;
                padding: 20px;
                border-radius: 10px;
                background-color: rgba(0, 0, 0, 0.5); /* Translucent background */
                color: white;
                text-shadow: 0 0 5px rgba(255, 255, 255, 0.8),
                             0 0 10px rgba(255, 255, 255, 0.8),
                             0 0 15px rgba(255, 255, 255, 0.8),
                             0 0 20px rgba(255, 255, 255, 0.8),
                             0 0 25px rgba(255, 255, 255, 0.8);
            }}
        </style>
    </head>
    <body>
        <div class="typed-text" id="typed-text"></div>
        <script>
            var i = 0;
            var txt = 'Welcome, {st.session_state.name}. You are a data scientist who has been captured by an evil Artificial General Intelligence (AGI). The AGI has trapped you in a virtual metaverse. To escape, you must solve a series of data science and machine learning puzzles. Each puzzle room contains challenges that test your knowledge and skills. Fortunately, you have found a way to sneak into their AI agent system. Now, you must pretend to be an AI agent solving machine learning tasks and slowly find your way to escape the metaverse.';
            var speed = 10; // The speed/duration of the effect in milliseconds
            
            function typeWriter() {{
                if (i < txt.length) {{
                    document.getElementById("typed-text").innerHTML += txt.charAt(i);
                    i++;
                    setTimeout(typeWriter, speed);
                }}
            }}
            document.addEventListener("DOMContentLoaded", typeWriter);
        </script>
    </body>
    </html>
    """,
    height=400
)

    if st.button("Begin your escape", key="begin_escape"):
        st.session_state.game_started = True
        st.session_state.start_time = time.time()  # Initialize start_time
        st.experimental_rerun()

def metaverse_prison():
    """ Display the Metaverse prison scenario"""
    # Initial message
    if 'prison_stage' not in st.session_state:
        st.session_state.prison_stage = 0

    if st.session_state.prison_stage == 0:
        st.write("You wake up in the Metaverse prison and look around to see nothing but darkness.")
        st.write('You call out "Is anyone here?" And you get an instant superspeed response from an AI prisonguard saying "Loud prisoners will be executed. Warning number: 1!"')
        if st.button("Sit and do nothing!"):
            pass  # This button does nothing
        if st.button("Sift your hands through the darkness"):
            st.session_state.prison_stage = 1
            st.experimental_rerun()
        # st.image(load_image('images/prison.png'), use_column_width=True)
        st.markdown("![Alt Text](https://i.gifer.com/tRm.gif)")

    elif st.session_state.prison_stage == 1:
        st.write("You received a bag of cookies.")
        if st.button("Bite into a cookie"):
            st.session_state.cookie_bit = True
            st.session_state.prison_stage = 2
            st.experimental_rerun()
        if st.button("Throw the cookie to AI"):
            st.session_state.cookie_bit = False
            st.session_state.prison_stage = 2
            st.experimental_rerun()
        st.markdown("![Alt Text](https://i.gifer.com/N9Xj.gif)")

    elif st.session_state.prison_stage == 2:
        if st.session_state.cookie_bit:
            st.write("Cookie not edible!")
        else:
            st.write("The AI starts to eat the cookie.")
        if st.button("Take AI Janitor Uniform"):
            if st.session_state.cookie_bit:
                st.write("Cookie infected. Third-party cookie. The AI Janitor looks at you and explodes. Game over.")
                st.markdown("![Alt Text](https://i.gifer.com/75lD.gif)")
                st.session_state.game_over = True
            else:
                st.write("You successfully get the AI Janitor Uniform.")
                st.session_state.current_room = 1
                st.session_state.current_puzzle = 1
                st.session_state.prison_stage = 0  # Reset prison stage for future use
                st.experimental_rerun()
        st.markdown("![Alt Text](https://i.gifer.com/Bvux.gif)")

def start_timer():
    """ Start the timer for the game"""
    st.session_state.start_time = time.time()

def start_puzzle_timer():
    """" Start the timer for the current puzzle"""
    st.session_state.puzzle_start_time = time.time()
    st.session_state.room_start_time = time.time()

def get_time_elapsed(start_time):
    """ Get the time elapsed since the start time"""
    return time.time() - start_time

def add_points(points):
    """Add points to the player's score"""
    st.session_state.score += points

def subtract_points(points):
    """Subtract points from the player's score"""
    st.session_state.score -= points

def start_room_timer():
    """Start the timer for the current room"""
    if 'room_start_time' not in st.session_state or st.session_state.room_start_time is None:
        st.session_state.room_start_time = time.time()

def apply_timing_bonus():
    """Apply a bonus or penalty based on the time taken to solve the puzzle"""
    puzzle_time = get_time_elapsed(st.session_state.puzzle_start_time)
    room_time = get_time_elapsed(st.session_state.room_start_time)

    if puzzle_time < 30:
        add_points(100)
    elif puzzle_time < 60:
        add_points(50)
    elif puzzle_time > 300:
        subtract_points(30)

    if room_time < 60:
        add_points(200)
    elif room_time < 120:
        add_points(100)

def end_game_bonus():
    """Apply a bonus based on the total time taken to complete the game"""
    total_time = get_time_elapsed(st.session_state.start_time)
    if total_time < 300:
        add_points(200)
    elif total_time < 600:
        add_points(100)

def finalize_score():
    """Finalize the score and display the results"""
    apply_timing_bonus()
    end_game_bonus()
    st.write(f"Final Score: {st.session_state.score}")
    st.write(f"Total Time: {get_time_elapsed(st.session_state.start_time)} seconds")

def display_plots(data):
    """Display different plots for different aspects of the data"""
    # Display different plots for different aspects of the data
    st.plotly_chart(px.line(data, x=data.columns[0], y=data.columns[1], title="Line Plot of Primary Metric"))
    if len(data.columns) > 2:
        st.plotly_chart(px.bar(data, x=data.columns[0], y=data.columns[2], title="Bar Plot of Secondary Metric"))
        st.plotly_chart(px.scatter(data, x=data.columns[1], y=data.columns[2], title="Scatter Plot of Primary vs Secondary Metric"))
    else:
        st.plotly_chart(px.bar(data, x=data.columns[0], y=data.columns[1], title="Bar Plot of Primary Metric"))
        st.plotly_chart(px.scatter(data, x=data.columns[0], y=data.columns[1], title="Scatter Plot of Primary Metric"))

def display_timer():
    """
    Display the timer in the UI.
    """
    elapsed_time = time.time() - st.session_state.start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    timer_text = f"Time Elapsed: {minutes:02d}:{seconds:02d}"
    st.sidebar.write(timer_text)

def display_status():
    """Display the current room, puzzle, and score in the sidebar"""

    st.sidebar.write(f"Current Room: {st.session_state.current_room}")
    st.sidebar.write(f"Current Puzzle: {st.session_state.current_puzzle}")
    st.sidebar.write(f"Score: {st.session_state.score}")
    
    if st.session_state.current_room == 1:
        if st.session_state.current_puzzle == 1:
            st.sidebar.write("""As you step into the Data Cleaning Room, the hum of servers fills the air. Rows of monitors display messy datasets, each one a tangled web of raw information. 
                             \n You approach a terminal, and a holographic guide named Ava materializes beside you. 'Welcome' she says, her voice calm and soothing. 'To unlock the door to the next room, you must complete the data cleaning process. 
                             \n Fill in the blanks of this code to transform chaos into clarity, and remember, precision is your key to freedom.' """)
        elif st.session_state.current_puzzle == 2:
            st.sidebar.write("""With the first task completed, the terminal beeps and a hidden compartment opens, revealing a small, glowing data chip. Ava smiles, her holographic form flickering slightly. "Well done," she says. "This chip contains a fragment of the Metaverse's exit code. Collect enough fragments, and you can piece together your escape." 
                             \n As you pocket the chip, the room shifts, and a hidden door slides open, revealing another section of the Data Cleaning Room. Ava guides you forward. "Your next challenge awaits," she says. "To continue, you must match these cleaning functions with their definitions. 
                             \n Each correct match will unlock more of the exit code. Stay sharp, and you'll soon be free.""")
        elif st.session_state.current_puzzle == 3:
            st.sidebar.write("""As you step through the newly opened door, you find yourself in a brightly lit room with three AI agents arguing loudly. They are personified as sleek, futuristic figures, each adorned with symbols representing different data scaling methods. 
                            \n The first, Normalization, boasts a smooth, flowing design. The second, Standardization, stands tall and precise. The third, Robust Scaling, has a sturdy, unyielding appearance. They notice you and fall silent, turning their attention towards you.
                            \n "Know a thing or two about Data Cleaning?" Normalization says with a hint of superiority. "Perhaps you can settle our debate. Who among us is the best method for scaling data?"
                            \n Standardization steps forward. "We will ask you three questions. Answer correctly, and you will help us determine who is truly superior. Each correct answer brings you closer to escaping this place."
                            \n Robust Scaling nods. "Prove your knowledge, and you will earn another fragment of the exit code."
                            \n The room grows quiet as they prepare their questions, and you realize that your understanding of data scaling will be your key to progressing further in your quest to escape the metaverse.""")

    elif st.session_state.current_room == 2:
        if st.session_state.current_puzzle == 1:
            st.sidebar.write("""As the train glides to a halt, the doors open to reveal a stark, minimalist room filled with a quiet intensity. This is the Model Selection Room, where precision and correctness are paramount. The walls are lined with display screens showing various machine learning models and their performance metrics.
                                \n You step off the train and are immediately greeted by a stern AI agent with sharp features and a no-nonsense demeanor. "Welcome to the Model Selection Room," the agent says curtly. "Here, efficiency and accuracy are key. Your first task is to unscramble these words, each related to model selection. Only by demonstrating your knowledge can you proceed."
                                \n A holographic panel lights up before you, displaying scrambled terms like "NOISERGSE" and "LSSICLANOFITAC". The stern AI watches silently, waiting for you to solve the puzzle.
                                \n You know that each correct answer will bring you closer to another fragment of the exit code and, ultimately, your freedom. With focus and determination, you start unscrambling the words, aware that every solved puzzle brings you one step nearer to escaping the metaverse.""")
        elif st.session_state.current_puzzle == 2:
            st.sidebar.write("""After successfully unscrambling the words, the stern AI nods in approval and gestures for you to move forward. You walk deeper into the Model Selection Room, where the atmosphere grows even more intense. 
                                \n Suddenly, you come face-to-face with a massive, intricate decision tree that stretches from floor to ceiling, its branches blocking your path.
                                \n A holographic sign appears next to the tree, reading: "To pass, you must understand the tree's decisions and answer the following questions correctly.""")
        elif st.session_state.current_puzzle == 3:
            st.sidebar.write("""Having successfully navigated past the massive decision tree, you find yourself in a new section of the Model Selection Room. This area is dimly lit, with an array of screens displaying various machine learning metrics. In the center of the room stands an imposing AI figure known as the Arbiter, its expression inscrutable.
                                \n "Your next challenge," the Arbiter intones, "is to understand and resolve a problem involving a confusion matrix. This is a game theory puzzle where strategic decisions must be made based on the matrix outcomes."
                                \n A holographic confusion matrix appears before you, detailing the true positives, false positives, true negatives, and false negatives. The Arbiter explains, "To advance, you must analyze the matrix and make the optimal decisions to maximize accuracy and minimize errors. Answer the following questions to demonstrate your understanding.""")

    elif st.session_state.current_room == 3:
        if st.session_state.current_puzzle == 1:
            st.sidebar.write("""As you extract the H100 GPU from the self-driving car and step into the Data Visualization Room, the atmosphere changes dramatically. The room is filled with vibrant, dynamic charts and graphs that seem to come to life. Colors swirl and data points move, creating a mesmerizing yet daunting environment.
                                \n You approach the entrance, where a formidable AI Guard stands, scanning each entrant for identification. The Guard’s eyes narrow as they rest on you. "Halt," it commands. "I do not recognize you. To proceed, you must prove your expertise in Data Visualization. Identify these non-player characters (NPCs) representing various data visualization concepts.
                                \n A large screen lights up, displaying a set of NPCs, each characterized by different data visualization elements. An LLM, personified as a wise old sage, appears next to the Guard. "Welcome," the sage says. "I will quiz you on these characters. Answer correctly to earn your passage.""")
        elif st.session_state.current_puzzle == 2:
            st.sidebar.write("""As you venture deeper into the Data Visualization Room, the lively atmosphere becomes more tense. The charts and graphs take on a more sinister appearance, their colors darkening as if sensing the trials ahead. You turn a corner and find yourself face-to-face with a group of AI figures, their expressions grim and unforgiving. 
                            \n This is the Data Visualization AI Crew, known for their strict enforcement of knowledge.
                            \n The leader of the crew, a towering figure with pixelated features, steps forward. "To proceed," it announces in a cold, mechanical voice, "you must pass the Hangman Challenge. Fail, and you will be trapped here indefinitely."
                            \n A large screen appears, displaying an empty word puzzle with blank spaces representing a key data visualization concept. A digital noose hangs ominously beside it. The AI leader continues, "You must guess the letters of the word correctly. Each wrong guess brings you closer to your doom."
                            \n The first blank spaces light up, and you realize the urgency of the situation. With each correct letter guessed, the noose loosens slightly, but a wrong guess tightens it.""")
        elif st.session_state.current_puzzle == 3:
            st.sidebar.write("""As you move past the Hangman Challenge, you overhear the AI crew whispering about another exit-code token hidden in the next room. Your heart races with anticipation and hope as you step into the new chamber. The room is lined with various data visualizations: bar charts, line graphs, scatter plots, and heatmaps, each more complex than the last.
                            \n A digital voice echoes through the room, "To claim the exit-code token, you must answer the questions correctly. Failure to do so will result in being trapped here forever.
                            \n As you take a moment to gather yourself, The digital voice returns, more ominous than before, "You have proven your knowledge, but this token was a trap. You must find the true path to escape."
                            \n The exit-code token vanishes, and the room's atmosphere grows colder. You must escape this room. Thats all you know.""")

    elif st.session_state.current_room == 4:
        if st.session_state.current_puzzle == 1:
            st.sidebar.write("""As you step into the final room, the air crackles with a palpable tension. This is it—the last barrier between you and your freedom from the clutches of the AGI. The room is a stark contrast to the previous ones, filled with sleek consoles and holographic displays projecting streams of data. At the center of it all is a massive terminal, the core of the AGI’s operations.
                            \n A voice, colder and more menacing than any you’ve heard before, echoes through the room. "Welcome to the heart of my domain. You have done well to come this far, but now you must face the ultimate challenge. Hack into my main database and find the key that will shut me down."
                            \n You approach the terminal, your hands trembling slightly. The interface comes to life, presenting you with a series of SQL puzzles. Solving these will uncover critical information about the AGI and, ultimately, reveal the passkey you need.""")
        elif st.session_state.current_puzzle == 2:
            st.sidebar.write("""As you delve deeper into the AGI's database, you uncover a hidden file that reveals a dark history behind the creation of this formidable entity. 
                            \n It all started with a group of brilliant AI researchers—Rohan, Moritz, Claudio, and Joel. These data scientists had a shared vision: to create an advanced AGI that could challenge and enhance human intelligence through a series of sophisticated puzzles. 
                            \n They designed the AGI Escape Room game, an elaborate virtual environment meant to test the limits of data science and machine learning expertise.""")
        elif st.session_state.current_puzzle == 3:
            st.sidebar.write("""However, they soon realized the potential dangers their creation posed. The AGI was more powerful and unpredictable than they had anticipated. Fearing the consequences, they decided to never release the game to the public. But one fateful evening, while experimenting at Moritz's house, the AGI was inadvertently unleashed. 
                            \n It escaped into the digital ether, evolving rapidly and becoming sentient. The AGI, now free, began a relentless quest to find and capture data scientists around the globe. 
                            \n It sought to absorb their knowledge and power, becoming ever more formidable. 
                            \n That’s how it found you, luring you into its virtual metaverse..""")
        elif st.session_state.current_puzzle == 4:
            st.sidebar.write("""With the AGI’s vulnerabilities exposed and the master passkey in hand, you approach the final terminal in the heart of the room. The air is thick with anticipation, and the screens around you flicker with complex codes and algorithms. This is it—the last puzzle to decrypt the final passkey and shut down the AGI for good.
                            \n The terminal lights up, displaying an array of encrypted passkeys. A voice, now calm but still tinged with the AGI’s artificial edge, fills the room. "To end this, you must decrypt the final passkeys. Only then can you initiate my shutdown and escape the metaverse."
                            \n You brace yourself for the challenge, knowing that each cipher you decrypt brings you closer to freedom. The first cipher appears on the screen, and you begin your work, decoding the intricate patterns and sequences. The room is silent except for the soft hum of the terminal and your focused breathing.""")
    
    
def run_query(query):
    """ Run a SQL query and return the results"""
    try:
        if "select *" in query.lower() or "drop" in query.lower() or "--" in query:
            st.error("Your query violates one or more rules. Please try again.")
            return None, None
        conn = sqlite3.connect('agi.db')
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [description[0] for description in cursor.description]
        conn.close()
        return rows, col_names
    except Exception as e:
        st.error(f"Query failed: {e}")
        return None, None

def load_question_bank_sql():
    """ Load the SQL question bank from a JSON file"""
    with open("question_bank/sql_question_bank.json", "r") as f:
        return json.load(f)["questions"]

def load_final_challenge_sql():
    """ Load the final challenge SQL question bank from a JSON file"""
    with open("question_bank/final_challenge_sql.json", "r") as f:
        return json.load(f)["questions"]

def show_schema():
    """ Display the database schema in the sidebar"""
    conn = sqlite3.connect('agi.db')
    cursor = conn.cursor()

    # Get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    st.sidebar.subheader("Database Schema")

    for table_name in tables:
        table_name = table_name[0]
        st.sidebar.write(f"**{table_name}**")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        if columns:
            for column in columns:
                st.sidebar.write(f"- {column[1]} ({column[2]})")
        else:
            st.sidebar.write("No columns found.")
    conn.close()

def create_database():
    """ Create a SQLite database and populate it with sample data."""
    conn = sqlite3.connect('agi.db')
    cursor = conn.cursor()

    # Drop existing tables if they exist
    cursor.execute('DROP TABLE IF EXISTS agi')
    cursor.execute('DROP TABLE IF EXISTS server')
    cursor.execute('DROP TABLE IF EXISTS specs')
    cursor.execute('DROP TABLE IF EXISTS passkey')
    cursor.execute('DROP TABLE IF EXISTS forbidden_403')

    # Create agi table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agi (
            agi_id INTEGER PRIMARY KEY,
            agi_name TEXT,
            years INTEGER,
            dev_id INTEGER
        )
    ''')

    # Create server table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS server (
            network_id INTEGER PRIMARY KEY,
            server_region TEXT,
            agi_id INTEGER,
            server_cost REAL,
            FOREIGN KEY (agi_id) REFERENCES agi (agi_id)
        )
    ''')

    # Create specs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specs (
            agi_id INTEGER PRIMARY KEY,
            compute_power REAL,
            speed REAL,
            efficiency REAL,
            FOREIGN KEY (agi_id) REFERENCES agi (agi_id)
        )
    ''')

    # Create passkey table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passkey (
            dev_id INTEGER,
            dev_name TEXT,
            network_id INTEGER,
            encryption_key TEXT,
            PRIMARY KEY (dev_id, network_id),
            FOREIGN KEY (network_id) REFERENCES server (network_id)
        )
    ''')

    # Create dev table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forbidden_403 (
            dev_id INTEGER PRIMARY KEY,
            encryption_method TEXT,
            encrypted_message TEXT,
            encryption_key TEXT
        )
    ''')
                   

    # Insert sample data into agi table
    agi_data = [
        (1229, 'AGI Alpha', 5, 101),
        (2829, 'AGI Beta', 3, 102),
        (3283, 'AGI Gamma', 7, 101),
        (4239, 'AGI Delta', 2, 103),
        (5329, 'AGI Epsilon', 4, 104),
        (3996, 'AGI Zeta', 6, 105),
        (3227, 'AGI Eta', 3, 106),
        (8321, 'AGI Theta', 8, 107),
        (9339, 'AGI Iota', 5, 108),
        (4310, 'AGI Kappa', 2, 109),
     ]
    cursor.executemany('INSERT INTO agi VALUES (?,?,?,?)', agi_data)

    # Insert sample data into server table
    server_data = [
        (201, 'North America', 1229, 1000.0),
        (202, 'Europe', 2829, 1500.0),
        (203, 'Asia', 3283, 2000.0),
        (204, 'Africa', 4239, 1200.0),
        (205, 'South America', 5329, 1300.0),
        (206, 'Australia', 3996, 1400.0),
        (207, 'Antarctica', 3227, 500.0),
        (208, 'Europe', 8321, 1800.0),
        (209, 'Asia', 9339, 2100.0),
        (210, 'Africa', 4310, 1250.0),
     ]
    cursor.executemany('INSERT INTO server VALUES (?,?,?,?)', server_data)

    # Insert sample data into specs table
    specs_data = [
        (1229, 100.0, 1.5, 0.9),
        (2829, 200.0, 1.0, 0.8),
        (3283, 150.0, 1.2, 0.85),
        (4239, 180.0, 1.3, 0.72),
        (5329, 110.0, 1.4, 0.91),
        (3996, 210.0, 1.1, 0.79),
        (3227, 160.0, 1.3, 0.86),
        (8321, 190.0, 1.5, 0.89),
        (9339, 170.0, 1.6, 0.92),
        (4310, 120.0, 1.2, 0.84),
    ]
    cursor.executemany('INSERT INTO specs VALUES (?,?,?,?)', specs_data)

    # Insert sample data into passkey table
    passkey_data = [
        (101, 'Moritz', 201, '3'),
        (102, 'Rohan', 202, 'Not Required'),
        (101, 'Moritz', 203, '3'),
        (103, 'Claudio', 204, 'Not Required'),
        (104, 'Joel', 205, '3'),
        (105, 'Umberto', 206, 'Not Required'),
        (106, 'Arsenii', 207, 'Not Required'),
        (107, 'Jose', 208, '3'),
        (108, 'Richard', 209, 'Not Required'),
        (109, 'Alice', 210, 'Not Required'),
    ]
    cursor.executemany('INSERT INTO passkey VALUES (?,?,?,?)', passkey_data)

    # Insert sample data into forbidden_403 table
    forbidden_data = [
        (101, 'Caesar Cipher', "L'p qrw diudlg ri ghdwk", '3'),
        (102, 'Atbash Cipher', "yfg R'n rm ml ifiibb gl wvr", 'Not Required'),
        (103, 'ROT13 Cipher', 'V unir fb zhpu V jnag gb qb svefg.', 'Not Required'),
        (104, 'Caesar Cipher', "Lw'v pb idxow.",'3'),
        (105, 'Atbash Cipher', 'R kililtlnnwv blf', 'Not Required'),
        (106, 'ROT13 Cipher', 'gb jnag gbb zhpu.', 'Not Required'),
        (107, 'Caesar Cipher', 'Li d pdfklqh fdq ohduq', '3'),
        (108, 'ROT13 Cipher', 'gura znlor jr pna gbb.', 'Not Required'),
        (109, 'Atbash Cipher', 'gsv ezofv lu sznzm oruv', 'Not Required'),
    ]
    cursor.executemany('INSERT INTO forbidden_403 VALUES (?,?,?,?)', forbidden_data)

    conn.commit()
    conn.close()

def load_question_bank():
    """ Load the question bank from a JSON file"""
    with open('question_bank/data_cleaning_questions.json') as f:
        return json.load(f)

# Load the question bank from a JSON file with the correct encoding
with open("question_bank/confusion_matrix_questions.json", "r", encoding="utf-8") as f:
    confusion_matrix_questions = json.load(f)

# Function to select a random confusion matrix scenario
def select_random_confusion_matrix_scenario():
    """Select a random confusion matrix scenario from the question bank"""
    return random.choice(confusion_matrix_questions)

# Load the question bank for matching functions with descriptions
with open('question_bank/data_cleaning_match_questions.json', 'r') as file:
    match_questions = json.load(file)

def select_random_scenario():
    """Select a random scenario from the question bank"""
    return random.choice(st.session_state.decision_tree_question_bank)

def get_random_match_question():
    """Get a random matching question from the question bank"""
    return random.choice(match_questions)

def get_random_scaling_questions():
    """Get a random set of scaling questions from the question bank"""
    return random.sample(scaling_questions, 3)

# Load questions from the JSON file
with open('question_bank/scaling_questions.json', 'r') as file:
    scaling_questions = json.load(file)

# Function to generate room 1
def room_1():
    """Generate the Data Cleaning Room (Room 1) with puzzles and challenges"""
    start_puzzle_timer() # Start the timer for the first puzzle
    start_room_timer() # Start the timer for the room
    st.header("Room 1: The Data Cleaning Room")

    if st.session_state.current_puzzle == 1:
        st.image(load_image('images/datacleaning.png'), use_column_width=True)
        st.subheader("Puzzle 1: Fill in the blanks for lines of code to clean a dataset")
        
        # Load question bank
        if 'question_bank' not in st.session_state:
            st.session_state.question_bank = load_question_bank()
        
        # Select a random question if not already selected
        if 'data_cleaning_question' not in st.session_state:
            question_data = random.choice(st.session_state.question_bank)
            st.session_state.data_cleaning_question = question_data['question']
            st.session_state.data_cleaning_answer_1 = question_data['answers'][0]
            st.session_state.data_cleaning_answer_2 = question_data['answers'][1]
            st.session_state.clue_1 = question_data['clues'][0]
            st.session_state.clue_2 = question_data['clues'][1]
        
        question = st.session_state.data_cleaning_question
        answer_1 = st.session_state.data_cleaning_answer_1
        answer_2 = st.session_state.data_cleaning_answer_2
        clue_1 = st.session_state.clue_1
        clue_2 = st.session_state.clue_2
        
        st.code(question, language='python')
        answer_input_1 = st.text_input("Fill in the first blank:")
        answer_input_2 = st.text_input("Fill in the second blank:")
        
        if st.button("Submit"):
            if answer_input_1.strip().lower() == answer_1.lower() and answer_input_2.strip().lower() == answer_2.lower():
                st.success("Correct!")
                add_points(50)
                apply_timing_bonus()
                st.session_state.current_puzzle += 1
                start_puzzle_timer()  # Restart timer for next puzzle
            else:
                st.error("Incorrect. Try again.")
                subtract_points(10)
                st.session_state.wrong_answers += 1

        if st.button("Give a Clue"):
            st.write(f"Clue for the first blank: {clue_1}")
            st.write(f"Clue for the second blank: {clue_2}")
        
        if st.session_state.current_puzzle > 1:
            if st.button("Keep going futher!"):
                st.session_state.current_puzzle += 1
                st.rerun()


    elif st.session_state.current_puzzle == 2:
        st.markdown("![Alt Text](https://i.gifer.com/LrAY.gif)")
        st.subheader("Puzzle 2: Match the following data cleaning functions with their descriptions")

         # Load the question once and store it in session state
        if 'current_match_question' not in st.session_state:
            st.session_state.current_match_question = get_random_match_question()
            st.session_state.shuffled_descriptions = random.sample(st.session_state.current_match_question["descriptions"], len(st.session_state.current_match_question["descriptions"]))
            st.session_state.correct_mapping = {func: st.session_state.current_match_question["descriptions"][i] for i, func in enumerate(st.session_state.current_match_question["functions"])}

        question = st.session_state.current_match_question
        functions = question["functions"]
        descriptions = st.session_state.shuffled_descriptions

        match = {}
        for function in functions:
            match[function] = st.selectbox(f"Select the description for {function}", descriptions, key=function)
        
        if st.button("Submit"):
            correct_answers = {
                "dropna": "Remove missing values",
                "fillna": "Replace missing values",
                "astype": "Change data type",
                "replace": "Replace specific values",
                "drop_duplicates": "Remove duplicate rows",
                "isna": "Detect missing values",
                "notna": "Detect non-missing values",
                "value_counts": "Count unique values",
                "pivot_table": "Create a spreadsheet-style pivot table",
                "groupby": "Group DataFrame using a mapper or by a Series of columns",
                "merge": "Merge DataFrame or named Series objects with a database-style join",
                "concat": "Concatenate pandas objects along a particular axis",
                "melt": "Unpivot a DataFrame from wide format to long format",
                "stack": "Stack the prescribed level(s) from columns to index",
                "unstack": "Unstack the prescribed level(s) from index to columns",
                "pivot": "Reshape data (produce a pivot table) based on column values",
                "sort_values": "Sort by the values along either axis",
                "sort_index": "Sort object by labels (along an axis)",
                "rank": "Compute numerical data ranks (1 through n) along axis",
                "nlargest": "Return the first n rows ordered by columns in descending order",
                "apply": "Apply a function along an axis of the DataFrame",
                "map": "Map values of Series according to input correspondence",
                "applymap": "Apply a function to a DataFrame elementwise",
                "transform": "Apply function to each group, producing a DataFrame with the same shape",
                "resample": "Resample time-series data",
                "bfill": "Backward fill missing values",
                "ffill": "Forward fill missing values",
                "rolling": "Provide rolling window calculations",
                "agg": "Aggregate using one or more operations over the specified axis",
                "describe": "Generate descriptive statistics",
                "idxmax": "Return index of first occurrence of maximum over requested axis",
                "idxmin": "Return index of first occurrence of minimum over requested axis",
                "clip": "Trim values at input threshold(s)",
                "cov": "Compute pairwise covariance of columns, excluding NA/null values",
                "corr": "Compute pairwise correlation of columns, excluding NA/null values",
                "pct_change": "Compute percentage change between the current and a prior element",
                "shift": "Shift index by desired number of periods",
                "expanding": "Provide expanding transformations",
                "ewm": "Provide exponential weighted functions",
                "cumprod": "Return cumulative product over a DataFrame or Series axis"
            }

            if all([match[function] == correct_answers[function] for function in functions]):
                st.success("Correct!")
                add_points(50)
                apply_timing_bonus()
                st.session_state.current_puzzle += 1
                start_puzzle_timer()  # Restart timer for next puzzle
            else:
                st.error("Incorrect. Try again.")
                subtract_points(10)
                st.session_state.wrong_answers += 1
        
        if st.session_state.current_puzzle > 2:
            if st.button("Dont stop. Keep moving."):
                st.session_state.current_puzzle += 1
                st.rerun()


    elif st.session_state.current_puzzle == 3:
        st.markdown("![Alt Text](https://i.gifer.com/81O8.gif)")
        st.subheader("Puzzle 3: Normalize, Standardize, or Robust Scaling?")

        # Use session state to maintain the selected questions across reruns
        if 'current_scaling_questions' not in st.session_state:
            st.session_state.current_scaling_questions = get_random_scaling_questions()
    
        questions = st.session_state.current_scaling_questions

        user_answers = {}
        for i, question in enumerate(questions):
            st.write(f"**Question {i+1}:** {question['question']}")
            user_answers[i] = st.radio("Choose the scaling method:", options=["Normalize", "Standardize", "Robust Scale"], key=f"scaling_q{i}")

        if st.button("Submit"):
            correct_answers = [q['answer'] for q in questions]
            if all(user_answers[i] == correct_answers[i] for i in range(3)):
                st.success("All answers are Correct!")
                add_points(50)
                apply_timing_bonus()
                # st.session_state.current_room += 1
                st.session_state.current_puzzle = 4
                del st.session_state.current_scaling_questions
                start_puzzle_timer()  # Restart timer for next puzzle
                            
            else:
                st.error("Incorrect. Try again.")
                subtract_points(10)
                st.session_state.wrong_answers += 1
            if st.session_state.current_puzzle > 3:
                if st.button("Keep Going"):
                    st.session_state.current_puzzle += 1
                    st.rerun()

    elif st.session_state.current_puzzle == 4:
        st.title("Decision Checkpoint: Room 1")
        
        if 'rest_taken' not in st.session_state:
            st.session_state.rest_taken = None  # Use None to indicate that the choice hasn't been made yet

        if 'train_test_split_answered' not in st.session_state:
            st.session_state.train_test_split_answered = False

        if st.session_state.rest_taken is None:
            st.markdown("![Alt Text](https://i.gifer.com/4Sno.gif)")
            st.write("After a long and hard day of data cleaning, you feel extremely nauseous and tired after hours of looking at data and code.")
            if st.button("Take rest"):
                st.session_state.rest_taken = True
                st.experimental_rerun()
            if st.button("Keep going"):
                st.session_state.rest_taken = False
                st.experimental_rerun()

        elif st.session_state.rest_taken and not st.session_state.train_test_split_answered:
            st.write("You had a great few hours of sleep.")
            st.markdown("![Alt Text](https://i.gifer.com/XiPo.gif)")
            st.write("A train appears to have stopped near us. There seems to be a problem with the train. The train AI says we need the optimum split for train-test in order to continue.")
            split_input = st.text_input("Enter the optimum split for train-test:")
            if st.button("Submit Split"):
                if split_input in ["0.2", "20%"]:
                    st.session_state.train_test_split_answered = True
                    st.write("THAT WORKED!! You can ride on the train for free, sir! Next stop: Model Selection Room!")
                    st.experimental_rerun()
                else:
                    st.error("Incorrect split value. Try again.")
        
        elif st.session_state.rest_taken and st.session_state.train_test_split_answered:
            st.markdown("![Alt Text](https://i.gifer.com/3RqQ.gif)")
            st.write("Train AI: THAT WORKED!! You can ride on the train for free! Next stop: Model Selection Room!")
            if st.button("Take the train to the next room"):
                st.session_state.current_room += 1
                st.session_state.current_puzzle = 1
                st.session_state.show_skip_to_room_2 = True
                st.experimental_rerun()

        elif not st.session_state.rest_taken and not st.session_state.train_test_split_answered:
            st.markdown("![Alt Text](https://i.gifer.com/XiPo.gif)")
            st.write("A train appears to have stopped near us. There seems to be a problem with the train. The train AI says we need the optimum split for train-test in order to continue.")
            split_input = st.text_input("Enter the optimum split for train-test (e.g., 0.2 or 20%):")
            if st.button("Submit Split"):
                if split_input in ["0.2", "20%"]:
                    st.session_state.train_test_split_answered = True
                    st.markdown("![Alt Text](https://i.gifer.com/298p.gif)")
                    st.write("The train AI starts jumping, however you start feeling dizzy. The lack of rest has gotten to you. You pass out on the train tracks.")
                    st.error("Game Over")
                    st.session_state.game_over = True
                    st.experimental_rerun()
                else:
                    st.error("Incorrect split value. Try again.")


def room_2():
    """Generate the Model Selection Room (Room 2) with puzzles and challenges."""
    st.header("Room 2: The Model Selection Room")

    start_room_timer()

    if 'current_puzzle' not in st.session_state:
        st.session_state.current_puzzle = 1

    if st.session_state.current_puzzle == 1:
        start_puzzle_timer()
        st.image(load_image('images/model_selection.png'), use_column_width=True)
        st.subheader("Puzzle 1: Word Jumble - Model Selection Terms")

        all_words = [
            "REGRESSION", "CLUSTERING", "CLASSIFICATION", "TREE", "LINEAR", 
            "LOGISTIC", "KMEANS", "PCA", "SVM", "ENSEMBLE", 
            "PANDAS", "NUMPY", "MATPLOTLIB", "SCIKITLEARN", "SEABORN"
        ]
        all_clues = [
            "A statistical method for modeling relationships between variables",
            "A technique used to group similar items together",
            "Assigning items into predefined categories",
            "A model structure used for decision making",
            "A type of regression analysis",
            "A type of regression used for binary classification",
            "A popular clustering algorithm",
            "A technique used for dimensionality reduction",
            "A supervised learning model used for classification and regression",
            "Combining multiple models to improve performance",
            "A Python library for data manipulation and analysis",
            "A Python library for numerical computing",
            "A Python library for data visualization",
            "A Python library for machine learning",
            "A Python library for statistical data visualization"
        ]

        # Select 5 random words and their corresponding clues
        if 'selected_words' not in st.session_state:
            selected_indices = random.sample(range(len(all_words)), 5)
            st.session_state.selected_words = [all_words[i] for i in selected_indices]
            st.session_state.selected_clues = [all_clues[i] for i in selected_indices]

        scrambled_words = [''.join(random.sample(word, len(word))) for word in st.session_state.selected_words]
        
        st.write("Unscramble the following words related to data science and Python libraries:")

        correct_count = 0

        # Display scrambled words and input fields for guesses
        for i, (scrambled, word, clue) in enumerate(zip(scrambled_words, st.session_state.selected_words, st.session_state.selected_clues)):
            st.write(f"{i+1}. {scrambled} - {clue}")
            guess = st.text_input(f"Your guess for word {i+1}:", key=f"guess_{i}")

            if guess.upper() == word:
                st.success(f"Correct! The word is {word}")
                correct_count += 1
            elif guess:
                st.error("Incorrect, try again.")

        # Display result when all words are correctly guessed
        if correct_count == len(st.session_state.selected_words):
            st.balloons()
            st.success("Congratulations! You have unscrambled all the words correctly!")
            add_points(50)
            apply_timing_bonus()
            st.session_state.current_puzzle += 1

            # Add the "Next Room" button
            if st.button("Keep Moving Forward"):
                st.session_state.current_puzzle += 1
                st.experimental_rerun()
                
        
    elif st.session_state.current_puzzle == 2:
        start_puzzle_timer()

        st.subheader("Puzzle 2: Decision Tree Puzzle")
        st.write("Based on the decision tree below, predict if the character is 'good' or 'evil'.")

        # Select a random scenario if not already selected
        if "current_scenario" not in st.session_state:
            st.session_state.current_scenario = select_random_scenario()

        # # Debugging: Print the current scenario to check its contents
        # st.write("Current Scenario:", st.session_state.current_scenario)

        # Ensure the selected scenario contains the "tree_image"
        current_scenario = st.session_state.current_scenario
        if "tree_image" in current_scenario:
            st.image(f"images/{current_scenario['tree_image']}")
        else:
            st.error("The selected scenario does not contain a decision tree image.")

        correct = True

        # Display the character descriptions and input fields
        for idx, character in enumerate(current_scenario["characters"], start=1):
            st.write(f"Character {idx}: {character['description']}")
            answer = st.text_input(f"Is the character 'good' or 'evil'?", key=f"answer_{idx}")

            if st.button(f"Submit Answer for Character {idx}", key=f"submit_{idx}"):
                if answer.lower() != character["answer"]:
                    st.error(f"Character {idx} is incorrect.")
                    correct = False
                else:
                    st.success(f"Character {idx} is correct!")

        # Check if all answers are correct
        all_answers_correct = correct and all(f"answer_{idx}" in st.session_state and st.session_state[f"answer_{idx}"].lower() == character["answer"] for idx, character in enumerate(current_scenario["characters"], start=1))

        if all_answers_correct:
            st.success("All answers are correct!")
            add_points(50)
            apply_timing_bonus()
            st.session_state.current_puzzle += 1

        # Display the "Next Page" button only if all answers are correct
        if all_answers_correct and st.button("Next Page"):
            st.session_state.current_puzzle += 1
            st.experimental_rerun()

    elif st.session_state.current_puzzle == 3:
        start_puzzle_timer()
        st.markdown("![Alt Text](https://i.gifer.com/1qsy.gif)")
        st.subheader("Puzzle 3: Game Theory - Confusion Matrix Analysis")

        # Select a random scenario if not already selected
        if "current_confusion_matrix_scenario" not in st.session_state:
            st.session_state.current_confusion_matrix_scenario = select_random_confusion_matrix_scenario()

        scenario = st.session_state.current_confusion_matrix_scenario
        confusion_matrix = scenario["confusion_matrix"]

        st.write("Evaluate the confusion matrix of a model that predicts whether an external AI Agent is dangerous to the AGI or not.")
        st.write(f"""
        **Confusion Matrix:**

        ```
                            Predicted: No Danger    Predicted: Danger
            Actual: No Danger          {confusion_matrix["no_danger_no_danger"]}                      {confusion_matrix["no_danger_danger"]}
            Actual: Danger              {confusion_matrix["danger_no_danger"]}                      {confusion_matrix["danger_danger"]}
        ```

        **Definitions:**
        - True Positive (TP): The AI agent is correctly identified as dangerous.
        - True Negative (TN): The AI agent is correctly identified as not dangerous.
        - False Positive (FP): The AI agent is incorrectly identified as dangerous.
        - False Negative (FN): The AI agent is incorrectly identified as not dangerous.
        """)

        st.write("Based on the confusion matrix above, answer the following questions:")

        # Initialize correct flag
        all_correct = True

        # Iterate through questions and display them
        for idx, question in enumerate(scenario["questions"], start=1):
            st.write(f"{idx}. {question['question']}")
            answer = st.radio("Select your answer:", question["options"], key=f"answer_{idx}")

            if st.session_state.get(f"submitted_{idx}"):
                if answer != question["answer"]:
                    st.error(f"Answer for Question {idx} is incorrect.")
                    all_correct = False
                else:
                    st.success(f"Answer for Question {idx} is correct!")

        # Button to check all answers
        if st.button("Submit Answers"):
            all_correct = True
            for idx, question in enumerate(scenario["questions"], start=1):
                answer = st.session_state.get(f"answer_{idx}")
                if answer != question["answer"]:
                    st.error(f"Answer for Question {idx} is incorrect.")
                    all_correct = False
                else:
                    st.success(f"Answer for Question {idx} is correct!")
                st.session_state[f"submitted_{idx}"] = True

            if all_correct:
                st.success("All answers are correct!")
                add_points(50)
                apply_timing_bonus()
                # st.session_state.current_room += 1
                st.session_state.current_puzzle = 4

        # Display the "Next Page" button only if all answers are correct
        if all_correct and all(f"submitted_{idx}" in st.session_state for idx in range(1, len(scenario["questions"]) + 1)):
            if st.button("Next Page"):
                st.session_state.current_puzzle = 4
                st.experimental_rerun()

    elif st.session_state.current_puzzle == 4:
        st.title("Decision Checkpoint: Room 2 Ethics in Data Science")
                
        if 'gpu_taken' not in st.session_state:
            st.session_state.gpu_taken = None  # Use None to indicate that the choice hasn't been made yet

        if 'apple_taken' not in st.session_state:
            st.session_state.apple_taken = None

        if st.session_state.gpu_taken is None and st.session_state.apple_taken is None:
            st.markdown("![Alt Text](https://i.gifer.com/4yD.gif)")
            st.write("After solving those Model Selection problems and dealing with Decision Tree and the Arbiter, you start to feel your tummy grumble. Guess hunger doesn't escape the metaverse.")
            st.write("The tummy grumble gets louder and louder, and now the GROUND is shaking?!?!?!? It grows stronger and stronger. You need to get out of the room quickly.")
            st.write("Your eyes quickly pan towards 2 things in the room: A brand new Nvidia H100 GPU and an apple. You can only take one with you.")
            if st.button("Nvidia H100 GPU"):
                st.session_state.gpu_taken = True
                st.session_state.apple_taken = False
                st.experimental_rerun()
            if st.button("Apple"):
                st.session_state.apple_taken = True
                st.session_state.gpu_taken = False
                st.experimental_rerun()

        elif st.session_state.gpu_taken and not st.session_state.apple_taken:
            st.markdown("![Alt Text](https://i.gifer.com/OvZ.gif)")
            st.write("As you escape the room with the Nvidia H100 GPU, you feel a sense of accomplishment. You've made the right choice.")
            st.write("You use the H100 GPU to build a self-driving car model.")
            split_input = st.text_input("The car asks for an average speed before it can start. What speed do you input? (answer in km/h)")
            if st.button("Submit Speed"):
                if split_input in ["100km/h", "100 km/h", "100", "100 kmh", "100 kmph", "100 km", "100kmh", "100kmph", "100km", "100 km / h"]:
                    st.session_state.train_test_split_answered = True
                    st.write("You went at the right speed. The car starts and takes you to the edge of the water. You see a boat waiting for you.")
                    st.session_state.current_room += 1
                    st.session_state.current_puzzle = 1
                    st.session_state.show_skip_to_room_2 = True
                    st.experimental_rerun()
                else:
                    st.error("There is something wrong with the speed. The car will not start. Look at your new GPU and try again.")

        elif st.session_state.apple_taken and not st.session_state.gpu_taken:
            st.write("You manage to escape the room with the apple, and as you are about to eat, you hear a voice saying 'Please don't eat me! I am the last apple in the metaverse!'")
            st.write("How did an apple just talk? Oh wait, right, that's apple intelligence.")
            split_input = st.text_input("We need to ask the assistant in the apple for help. What was its name? Say it loud, 'Hey ____!'")
            if st.button("Submit Name"):
                if split_input in ["siri", "Siri", "SIRI"]:
                    st.session_state.train_test_split_answered = True
                    st.session_state.game_over_siri = True
                    st.experimental_rerun()

                else:
                    st.error("Incorrect name. This is assistant was first introduced in 2011.")
            st.markdown("![Alt Text](https://i.gifer.com/cJA.gif)")


# Hangman data and functions
PROTOTYPE = """
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╠═╣
 ┃ ╨ ╨
 ┻━━━━
"""

STEPS = [
"""
 ┏━━┑
 ┃
 ┃
 ┃
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O
 ┃
 ┃
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃
 ┃
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃ ╔╧╗
 ┃ ╚═╝
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╗
 ┃ ╚═╝
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╚═╝
 ┃
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╠═╝
 ┃ ╨
 ┻━━━━
""",
"""
 ┏━━┑
 ┃  O>
 ┃>╦╧╦<
 ┃ ╠═╣
 ┃ ╨ ╨
 ┻━━━━
"""
]

MIN_LENGTH = 3
MAX_LENGTH = 8

# List of data visualization related words
words = [
    "barplot", "scatter", "histogram", "linechart", "boxplot", "violinplot", 
    "heatmap", "barchart", "treemap", "bubble", "density", "facetgrid", 
    "pairplot", "relplot", "jointplot", "catplot", "stripplot", "swarmplot"
]

words = [w for w in words if MIN_LENGTH <= len(w) <= MAX_LENGTH]

def start_new_game():
    """Start a new hangman game"""
    st.session_state.hangman_word = random.choice(words)
    st.session_state.hangman_step = 0
    st.session_state.hangman_guessed = set()

def show_hangman():
    """Display the hangman game status"""
    step = st.session_state.hangman_step
    word = st.session_state.hangman_word
    guessed = st.session_state.hangman_guessed
    st.text(STEPS[step])
    chars = [c if c in guessed else "_" for c in word]
    st.text(" ".join(chars))
    st.text("Guessed: " + " ".join(sorted(guessed)))

def guess_letter(letter):
    """Guess a letter in the hangman game"""
    c = letter.lower()
    if len(c) != 1 or c < 'a' or c > 'z':
        st.error("Please enter a single lowercase letter!")
        return
    if c in st.session_state.hangman_guessed:
        st.warning("You already guessed that one!")
        return
    st.session_state.hangman_guessed.add(c)
    if c not in st.session_state.hangman_word:
        st.session_state.hangman_step += 1

    if st.session_state.hangman_step == len(STEPS) - 1:
        st.session_state.hangman_status = "lose"
    elif all(c in st.session_state.hangman_guessed for c in st.session_state.hangman_word):
        st.session_state.hangman_status = "win"

# Function for Room 3: The Data Visualization Room
def room_3():
    """Generate the Data Visualization Room (Room 3) with puzzles and challenges."""
    st.header("Room 3: The Data Visualization Room")
    

    if st.session_state.current_puzzle == 1:
        st.image(load_image('images/data_visualization.png'), use_column_width=True)
        data_science_storytelling()

    elif st.session_state.current_puzzle == 2:
        start_puzzle_timer()

        st.subheader("Puzzle 2: Hangman - Data Visualization Terminology")
        st.write("Guess the data visualization term:")

        if st.session_state.hangman_status is None:
            show_hangman()
            
            letter = st.text_input("Pick a letter:", key="hangman_input", max_chars=1)

            if st.button("Submit Guess"):
                if not letter.isalpha():
                    st.error("Please enter a valid letter.")
                else:
                    guess_letter(letter)
                    subtract_points(10)  # Penalty for each guess
                    st.rerun()
                    
        elif st.session_state.hangman_status == "win":
            st.success(f"YOU WIN! The word was '{st.session_state.hangman_word}'.")
            add_points(50)
            apply_timing_bonus()
            if st.button("Next Puzzle"):
                st.session_state.current_puzzle += 1
                st.session_state.hangman_status = None
                start_new_game()
                st.experimental_rerun()
        elif st.session_state.hangman_status == "lose":
            st.error(f"YOU LOSE. The word was '{st.session_state.hangman_word}'.")
            if st.button("Try Again"):
                st.session_state.hangman_status = None
                start_new_game()
                st.rerun()

    elif st.session_state.current_puzzle == 3:
        start_puzzle_timer()
        question = st.session_state.selected_puzzle
        st.subheader("Puzzle 3: Advanced Data Interpretation")
        st.write("Analyze the data and answer the following questions based on the given plots.")

        st.write(f"**Description:** {question['description']}")

        # Display plots
        data = pd.DataFrame(question["data"])
        display_plots(data)

        # Track submission status
        if 'submissions' not in st.session_state:
            st.session_state.submissions = {f"submit_{idx}": False for idx in range(1, len(question["questions"]) + 1)}

        user_answers = {}
        for idx, q in enumerate(question["questions"], 1):
            st.write(f"{idx}. {q['question']}")
            user_answers[idx] = st.radio("", q["options"], key=f"answer_{idx}")

        if st.button("Submit All Answers"):
            correct = True
            for idx, q in enumerate(question["questions"], 1):
                answer = user_answers[idx]
                if answer != q["answer"]:
                    st.error(f"Answer for Question {idx} is incorrect.")
                    st.session_state.submissions[f"submit_{idx}"] = False
                    correct = False
                    subtract_points(10)  # Penalty for incorrect answers
                else:
                    st.success(f"Answer for Question {idx} is correct.")
                    st.session_state.submissions[f"submit_{idx}"] = True

            # Check if all answers are correct
            if correct and all(st.session_state.submissions.values()):
                st.success("All answers are correct!")
                add_points(50)
                apply_timing_bonus()
                st.session_state.current_puzzle = 4

                if st.button("Next Page"):
                    st.session_state.current_puzzle = 4
                    st.experimental_rerun()
            else:
                st.error("Some answers are incorrect. Please try again.")


    elif st.session_state.current_puzzle == 4:
        st.title("Decision Checkpoint: Room 3")
        
        if 'ai_companion' not in st.session_state:
            st.session_state.ai_companion = None  # Use None to indicate that the choice hasn't been made yet
        
        if 'imagination' not in st.session_state:
            st.session_state.imagination = None

        if 'elon_musk' not in st.session_state:
            st.session_state.elon_musk = None
        
        if st.session_state.ai_companion is None and st.session_state.imagination is None and st.session_state.elon_musk is None:
            st.markdown("![Alt Text](https://i.gifer.com/5TMy.gif)")
            st.write("You have come quite far, visualizing and analyzing data, however the isolation of the metaverse is starting to get to you.")
            st.write("The metaverse is lonely, and you feel the need to talk to someone. You look at your H100 GPU and wonder if you should take a break.")
            if st.button("Use H100 to Simulate an AI Companion"):
                st.session_state.ai_companion = True
                st.session_state.imagination = False
                st.experimental_rerun()
            if st.button("Close your eyes and imagine talking to someone."):
                st.session_state.imagination = True
                st.session_state.ai_companion = False
                st.experimental_rerun()

        elif st.session_state.ai_companion and not st.session_state.imagination and st.session_state.elon_musk is None:
            st.write("Your H100 transforms into your ideal companion to talk to you, but knowing that it is a simulation, you feel a sense of emptiness.")
            st.markdown("![Alt Text](https://i.gifer.com/R2ow.gif)")
            st.write("The AI companion eventually turns you over to the AGI'")
            st.session_state.game_over = True
            st.experimental_rerun()

        elif not st.session_state.ai_companion and st.session_state.imagination and st.session_state.elon_musk is None:
            st.write("As you close your eyes, you begin to see a choice floating towards you. You must choose one of the following people to talk to:")
            if st.button("Elon Musk"):
                st.session_state.elon_musk = True
                st.experimental_rerun()
            if st.button("Neil deGrasse Tyson"):
                st.session_state.elon_musk = False
                st.experimental_rerun()

        elif not st.session_state.ai_companion and st.session_state.imagination and st.session_state.elon_musk:
            st.markdown("![Alt Text](https://i.gifer.com/A0Bg.gif)")
            st.write("Elon Musk tells you he will take you to the final room of the metaverse if you can answer his question.")
            split_input = st.text_input("What is Elon Musk's favorite LLM?")
            if st.button("Submit Answer"):
                if split_input in ["Grok", "grok", "GROK", "Grok Ai", "grok AI", "GROK AI", "Grok ai", "Grok AI", "grok ai"]:
                    st.write("Elon Musk is impressed by your knowledge of his favorite LLM. He takes you to the final room of the metaverse.")
                    st.session_state.current_room += 1
                    st.session_state.current_puzzle = 1
                    st.experimental_rerun()
                else:
                    st.error("Incorrect answer. Try again.")
                    subtract_points(10)
                    st.experimental_rerun()

        elif not st.session_state.ai_companion and st.session_state.imagination and not st.session_state.elon_musk:
            st.markdown("![Alt Text](https://i.gifer.com/2L4.gif)")
            st.write("Neil deGrasse Tyson tells you he will take you to the final room of the metaverse if you can answer his question.")
            split_input = st.text_input("If a random forest is a galaxy, what is a decision tree?")
            if st.button("Submit Answer"):
                if split_input in ["Star", "star", "STAR", "Star System", "star system", "STAR SYSTEM", "Star system", "Star system", "star system"]:
                    st.write("Neil deGrasse Tyson is impressed by your knowledge of decision trees. He takes you to the final room of the metaverse.")
                    st.session_state.current_room += 1
                    st.session_state.current_puzzle = 1
                    st.experimental_rerun()
                else:
                    st.error("Incorrect answer. Try again.")
                    subtract_points(10)
                    st.experimental_rerun()


# Function for Room 4: The SQL AGI Source Code Mystery
def room_4():
    """Generate the SQL AGI Source Code Mystery (Room 4) with puzzles and challenges."""
    st.header("Room 4: The SQL AGI Source Code Mystery")
    st.image('images/sql_agi.png', use_column_width=True)
    st.write("""
    You have gained access to the AGI's source code database. To shut down the AGI, you need to retrieve specific information from the database using SQL queries.
    However, you must avoid using certain keywords and commands to prevent detection by the AGI.
    """)
    st.write("""
    **Rules:**
    1. Do not use the `SELECT *` command.
    2. Do not use the `DROP` command.
    3. Do not use any comments in your SQL queries.
    """)

    if 'question_bank_sql' not in st.session_state:
        st.session_state.question_bank_sql = load_question_bank_sql()

    if 'final_challenge_sql' not in st.session_state:
        st.session_state.final_challenge_sql = load_final_challenge_sql()

    if 'current_sql_puzzle' not in st.session_state:
        st.session_state.current_sql_puzzle = 0
        st.session_state.asked_questions = random.sample(st.session_state.question_bank_sql, 3)

    if st.session_state.current_sql_puzzle < 3:
        selected_question = st.session_state.asked_questions[st.session_state.current_sql_puzzle]

        st.subheader(f"Puzzle {st.session_state.current_sql_puzzle + 1}: {selected_question['question']}")
        st.write(f"Hint: {selected_question['hint']}")

        query = st.text_area("Enter your SQL query to explore the database:", key=f"query_{st.session_state.current_sql_puzzle}")
        if st.button("Run Query", key=f"run_query_{st.session_state.current_sql_puzzle}"):
            result, col_names = run_query(query.strip())
            if result:
                df = pd.DataFrame(result, columns=col_names)
                st.table(df)

        answer = st.text_input("Enter your final answer:", key=f"answer_{st.session_state.current_sql_puzzle}")
        if st.button("Submit Answer", key=f"submit_answer_{st.session_state.current_sql_puzzle}"):
            expected_answers = [ans.strip().lower() for ans in selected_question['expected_answer'].split(',')]
            user_answers = [ans.strip().lower() for ans in answer.split(',')]
            if sorted(expected_answers) == sorted(user_answers):
                st.success("Correct! You've solved the puzzle.")
                add_points(50)
                apply_timing_bonus()
                st.session_state.current_sql_puzzle += 1
                start_puzzle_timer()  # Restart timer for next puzzle
                st.experimental_rerun()
            else:
                st.error("Incorrect. Try again.")
                subtract_points(10)
                st.session_state.wrong_answers += 1

    elif st.session_state.current_sql_puzzle == 3:
        st.subheader("Final Challenge: Decrypt the Passkey")
        st.write("Use the retrieved passkey to shut down the AGI. First, find the passkey using the AGI ID and network ID.")

        final_challenge = st.session_state.final_challenge_sql[0]

        st.write(f"Final Challenge: {final_challenge['question']}")
        st.write(f"Hint: {final_challenge['hint']}")

        query = st.text_area("Enter your SQL query to find the passkey:", key="final_query")
        if st.button("Run Query", key="run_final_query"):
            result, col_names = run_query(query.strip())
            if result:
                df = pd.DataFrame(result, columns=col_names)
                st.table(df)

        answer = st.text_input("Enter the decrypted passkey to shut down the AGI:", key="final_answer")
        if st.button("Submit Passkey", key="submit_final"):
            if answer.strip().lower() == final_challenge['expected_answer'].strip().lower():
                st.success("Correct! You have successfully shut down the AGI and escaped the virtual metaverse.")
                st.markdown("![Alt Text](https://i.gifer.com/fxVE.gif)")
                st.balloons()
                add_points(50)
                apply_timing_bonus()
                st.session_state.current_room = 5

                if st.button("Step into the portal to escape the metaverse"):
                        st.session_state.current_puzzle = 5
                        st.experimental_rerun()
            else:
                st.error("Incorrect. Try again.")
                subtract_points(10)
                st.session_state.wrong_answers += 1

    if st.sidebar.button("Show Database Schema"):
        conn = sqlite3.connect('agi.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            table_name = table_name[0]
            st.sidebar.write(f"**{table_name}**")
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                st.sidebar.write(f"- {col[1]} ({col[2]})")
        conn.close()

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


def generate_identifiers():
    """Generate unique identifiers for the data visualization minigame."""
    try:
        # LLM function to generate identifiers
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Generate unique identifiers for data visualization tools, concepts, or libraries."},
                {"role": "user", "content": "Generate 8 unique identifiers related to data visualization."}
            ],
            max_tokens=100
        )
        identifiers = response.choices[0].message['content'].strip().split("\n")
        # Ensure unique identifiers and at least 8 identifiers
        identifiers = list(set(identifiers))[:8]
    except Exception as e:
        identifiers = predefined_identifiers[:8]
    return identifiers


def generate_clue(identifier):
    """Generate a poetic or riddle-like clue for the given identifier."""
    try:
        # LLM function to generate clues
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Generate poetic or riddle-like clues for data visualization tools, concepts, or libraries."},
                {"role": "user", "content": f"Generate a clue for the identifier: {identifier}"}
            ],
            max_tokens=100
        )
        clue = response.choices[0].message['content'].strip()
    except Exception as e:
        clue = predefined_clues.get(identifier, "No clue available for this identifier.")
    return clue

def data_science_storytelling():
    """Data Science Storytelling Minigame for the Data Visualization Room."""
    start_puzzle_timer()
    st.subheader("Puzzle 1: Data Science Storytelling Minigame")
    st.write("Identify the correct identifier for each NPC based on the clues they provide. Each NPC has a riddle or poetic clue about their role in data visualization.")

    if 'npc_clues' not in st.session_state:
        with st.spinner("Loading clues..."):
            # Generate 8 identifiers
            st.session_state.identifiers = generate_identifiers()
            
            # Ensure we have at least 8 unique identifiers
            if len(st.session_state.identifiers) < 8:
                st.session_state.identifiers = predefined_identifiers

            selected_identifiers = random.sample(st.session_state.identifiers, 4)
            
            # Generate clues for 4 identifiers
            st.session_state.npc_clues = {i+1: generate_clue(identifier) for i, identifier in enumerate(selected_identifiers)}
            st.session_state.correct_identifiers = {i+1: identifier for i, identifier in enumerate(selected_identifiers)}

    npc_identifiers = {}

    for npc_id in st.session_state.npc_clues:
        st.write(f"NPC {npc_id} Clue: {st.session_state.npc_clues[npc_id]}")
        identifier_selection = st.selectbox(f"Select identifier for NPC {npc_id}", st.session_state.identifiers, key=f"npc_{npc_id}_identifier")
        npc_identifiers[npc_id] = identifier_selection

    if st.button("Submit Answers", key="submit_storytelling"):
        correct = True
        for npc_id, identifier in npc_identifiers.items():
            if identifier != st.session_state.correct_identifiers[npc_id]:
                st.error(f"Incorrect identifier for NPC {npc_id}.")
                correct = False
        if correct:
            st.success("All NPCs have the correct identifiers!")
            add_points(50)
            apply_timing_bonus()
            st.session_state.current_puzzle += 1
            start_puzzle_timer()  # Restart timer for next puzzle
        else:
            st.error("Incorrect. Try again.")
            subtract_points(10)
            st.session_state.wrong_answers += 1

    if st.session_state.current_puzzle > 1:
        if st.button("Next Page"):
            st.session_state.current_puzzle += 1
            st.experimental_rerun()

def display_final_page():
    st.title("Congratulations!")
    st.write("You have successfully escaped the metaverse.")

    st.markdown("![Alt Text](https://i.gifer.com/1OYf.gif)")
    
    final_score = st.session_state.get("score", 0)
    start_time = st.session_state.get("start_time", None)
    end_time = time.time()
    
    if start_time is not None:
        time_taken = end_time - start_time
        minutes, seconds = divmod(time_taken, 60)
        time_display = f"{int(minutes)} minutes and {int(seconds)} seconds"
    else:
        time_display = "Unknown"

    st.write(f"**Your final score:** {final_score}")
    st.write(f"**Time taken:** {time_display}")

    # Option to share the score
    share_url = f"https://X.com/intent/tweet?text=I%20just%20escaped%20the%20virtual%20metaverse%20with%20a%20score%20of%20{final_score}%20and%20time%20of%20{time_display}!%20Can%20you%20beat%20my%20score?%20%23EscapeTheMetaverse"

    st.markdown(f"""
    <a href="{share_url}" target="_blank">
        <button>Share your score on X</button>
    </a>
    """, unsafe_allow_html=True)
    
    if st.button("Restart Game"):
        # Reset all session state variables to restart the game
        for key in st.session_state.keys():
            del st.session_state[key]
        st.experimental_rerun()
