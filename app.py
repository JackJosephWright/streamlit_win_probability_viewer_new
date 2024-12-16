import streamlit as st
import pandas as pd
import pickle
import random
import os
from display_game_state import display_game_state
from display_victory_defeat_screen import display_victory_defeat_screen
from plot_win_probability import plot_win_probability

# Load model
model_path = os.path.join('models', 'win_probability', 'xgb_win_prob_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Load data
data = pd.read_csv('./data/replay_data_small.csv')

# Import custom functions
from transform_row_to_turns import transform_row_to_turns

def display_game_state_web(turn_row):
    def card_box(card_name):
        return f"<div style='display:inline-block; padding:5px; border:1px solid #ccc; margin:2px;'>{card_name}</div>"
    
    html = f"<h2>Turn {int(turn_row['turn'])}</h2>"  # Ensure 'turn' is an integer
    if 'predict_proba' in turn_row:
        html += f"<p>Predicted Win Probability: {turn_row['predict_proba']:.2%}</p>"

    # Opponent section
    html += f"<p>Opponent Life: {turn_row['oppo_life']}</p>"
    html += "<p>Opponent Hand:</p>"
    html += "".join([card_box("???") for _ in range(int(turn_row['oppo_cards_in_hand']))])  # Convert to int
    html += "<p>Opponent Lands:</p>"
    html += "".join([card_box("Land") for _ in range(int(turn_row['oppo_lands_in_play']))])  # Convert to int
    html += "<p>Opponent Board:</p>"
     # Filter columns matching 'oppo_creature_<n>' and 'oppo_noncreature_<n>'
    oppo_creature_columns = [col for col in turn_row.index if 'oppo_creature' in col]
    oppo_noncreature_columns = [col for col in turn_row.index if 'oppo_non_creature' in col]

    # Extract non-null creature and non-creature names
    oppo_creatures = turn_row[oppo_creature_columns].dropna().values  # Filter out NaN
    oppo_noncreatures = turn_row[oppo_noncreature_columns].dropna().values
  
   
    oppo_board_state =  " ".join([card_box(card) for card in oppo_creatures]) + "  ||  " + " ".join([card_box(card) for card in oppo_noncreatures])
    html += f"<p>{oppo_board_state}</p>"
    # make a cool divider between the opponent and the player
    html += "<hr>"

    user_creature_columns = [col for col in turn_row.index if 'user_creature' in col]
    user_noncreature_columns = [col for col in turn_row.index if 'user_noncreature' in col]

    user_creatures = turn_row[user_creature_columns].dropna().values  # Filter out NaN
    user_noncreatures = turn_row[user_noncreature_columns].dropna().values

    user_board_state = " ".join([card_box(card) for card in user_creatures]) + "  ||  " + " ".join([card_box(card) for card in user_noncreatures])
    html += f"<p>{user_board_state}</p>"
    html += "<p>User Board:</p>"
    html += "".join([card_box("Land") for _ in range(int(turn_row['user_lands_in_play']))])  # Convert to int
    html += "<p>User Lands:</p>"

    user_hand_columns = [col for col in turn_row.index if 'user_hand' in col]
    user_hand = turn_row[user_hand_columns].dropna().values
    html += "".join([card_box(card) for card in user_hand])
    html += "<p>User Hand:</p>"
    # User section
    html += f"<p>User Life: {turn_row['user_life']}</p>"
    
    
    
    return html

# Streamlit UI
st.title("MTG Win Probability Metric")
with st.expander("What is this app about?"):
    st.write("""
        ### Win Probability Calculator Example

        **What this app does:**
        This app demonstrates how win probabilities in Magic: The Gathering (MTG) games can be calculated using machine learning. By analyzing replays from [17Lands](https://www.17lands.com/) (a website that collects data from MTG games), this model estimates your chances of winning based on the current state of the game.

        **How it works:**
        - The app looks at the cards on the board (your "permanents") and in players' hands during each turn of a game.
        - It uses card win rates from 17Lands data as a baseline to estimate how strong each card is. This gives a general sense of how likely a player is to win when certain cards are played.
        - The model has been trained using machine learning, achieving a **74.6% ROC-AUC score**, which means it's pretty good at distinguishing between winning and losing situations.

        **What does ROC-AUC mean?**
        In simple terms, a **74.6% ROC-AUC** score means the model can correctly predict whether you're likely to win or lose about 3 out of 4 times, given the state of the game. It's not perfect, but it’s a solid start for making educated guesses about game outcomes.

        Use the navigation buttons below to explore a game and see the win probabilities evolve turn by turn!
    """)


# Initialize session state for the selected row index
if 'game_row_index' not in st.session_state:
    st.session_state['game_row_index'] = random.randint(0, len(data) - 1)

# Button to show a new game
if st.button("Show New Game"):
    st.session_state['game_row_index'] = random.randint(0, len(data) - 1)
    st.session_state['turn_index'] = 0  # Reset turn index for the new game

# Use the row index from the session state
game_row_index = st.session_state['game_row_index']
raw_game_row = data.iloc[game_row_index]

# Transform the row into a DataFrame for display
df_turn_display = transform_row_to_turns(raw_game_row, display=True, max_cards=20)

# Predict probabilities and append to DataFrame
turn_df_calc = transform_row_to_turns(raw_game_row, display=False, max_cards=20)
turn_df_calc = turn_df_calc.drop(['game_id', 'won'], axis=1)
predict_proba = model.predict_proba(turn_df_calc)
df_turn_display['predict_proba'] = predict_proba[:, 1]

# Initialize session state for the turn index
if 'turn_index' not in st.session_state:
    st.session_state['turn_index'] = 0

# Display the game state for the current turn
current_turn = st.session_state['turn_index']
# Display the game state for the current turn or Victory/Defeat screen
# Ensure the turn index does not exceed the number of turns
# Plot win probability above the game state display
# Plot win probability above the game state display
if st.session_state['turn_index'] > 0:  # Only display if at least one turn is available
    fig = plot_win_probability(df_turn_display, st.session_state['turn_index'] - 1)
    st.pyplot(fig)

# Display the game state or Victory/Defeat screen
if st.session_state['turn_index'] < len(df_turn_display):  # Display regular turns
    current_turn = st.session_state['turn_index']
    turn_html = display_game_state_web(df_turn_display.iloc[current_turn])
    st.markdown(turn_html, unsafe_allow_html=True)
else:  # Display Victory/Defeat screen after the last turn
    final_turn = df_turn_display.iloc[-1]  # Use the last turn to determine the result
    victory_defeat_html = display_victory_defeat_screen(final_turn)
    st.markdown(victory_defeat_html, unsafe_allow_html=True)

# Replay controls
col1, col2 = st.columns([1, 1])

if col2.button('Next Turn') and st.session_state['turn_index'] < len(df_turn_display):
    st.session_state['turn_index'] += 1

if col1.button('Previous Turn') and st.session_state['turn_index'] > 0:
    st.session_state['turn_index'] -= 1

# Display turn navigation status
st.write(f"Turn {current_turn + 1} / {len(df_turn_display)}")
