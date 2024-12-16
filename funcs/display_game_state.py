def display_game_state(turn_row):
    """
    Generates an HTML representation of the game state with card names inside boxes for both the opponent and user.
    - turn_row: Series, a single game state row
    """
    # Helper function to create a box for a card
    def card_box(card_name):
        return f"<div class='card-box'>{card_name}</div>"  # Center-align the card name in a box

    # Extract scalar values safely directly from the Series
    html = f"<h2>Turn {turn_row['turn']}</h2>"
    html += f"<p>Predicted Win Probability: {turn_row.get('predict_proba', 'N/A')}</p>"
    
    # Opponent Section
    html += "<h3>Opponent</h3>"
    html += f"<p>Life: {turn_row['oppo_life']}</p>"
    html += "<p>Hand:</p>"
    html += "".join([card_box("???") for _ in range(turn_row['oppo_cards_in_hand'])])
    html += "<p>Lands:</p>"
    html += "".join([card_box("Land") for _ in range(turn_row['oppo_lands_in_play'])])

    # Opponent's Board
    oppo_creature_columns = [col for col in turn_row.index if 'oppo_creature' in col]
    oppo_noncreature_columns = [col for col in turn_row.index if 'oppo_noncreature' in col]
    oppo_creatures = turn_row[oppo_creature_columns].dropna().values
    oppo_noncreatures = turn_row[oppo_noncreature_columns].dropna().values
    html += "<h4>Opponent Board:</h4>"
    html += f"<div>{' '.join([card_box(card) for card in oppo_creatures])}</div>"
    html += f"<div>{' '.join([card_box(card) for card in oppo_noncreatures])}</div>"

    # Separator
    html += "<hr>"

    # User Section
    html += "<h3>User</h3>"
    html += f"<p>Life: {turn_row['user_life']}</p>"
    html += "<p>Lands:</p>"
    html += "".join([card_box("Land") for _ in range(turn_row['user_lands_in_play'])])
    
    user_creature_columns = [col for col in turn_row.index if 'user_creature' in col]
    user_noncreature_columns = [col for col in turn_row.index if 'user_noncreature' in col]
    user_creatures = turn_row[user_creature_columns].dropna().values
    user_noncreatures = turn_row[user_noncreature_columns].dropna().values
    html += "<h4>User Board:</h4>"
    html += f"<div>{' '.join([card_box(card) for card in user_creatures])}</div>"
    html += f"<div>{' '.join([card_box(card) for card in user_noncreatures])}</div>"

    return html
