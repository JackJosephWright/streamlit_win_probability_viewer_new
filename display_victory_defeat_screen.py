def display_victory_defeat_screen(turn_row):
    """
    Displays a stylized Victory/Defeat screen based on the 'won' column.
    - turn_row: Series, the final game state row.
    """
    won = turn_row['won']
    user_life = float(turn_row['user_life'])
    oppo_life = float(turn_row['oppo_life'])
    final_probability = turn_row.get('predict_proba', None)

    # Styling
    result_color = "green" if won else "red"
    result_text = "Victory!" if won else "Defeat!"
    win_prob_text = f"Final Win Probability: {final_probability:.2%}" if final_probability is not None else ""

    # HTML for display
    html = f"""
    <div style="text-align: center; padding: 20px; border: 3px solid {result_color}; border-radius: 10px;">
        <h1 style="color: {result_color}; font-size: 50px; margin-bottom: 20px;">{result_text}</h1>
        <p style="font-size: 24px; margin: 10px 0;">User Life: <b>{user_life}</b></p>
        <p style="font-size: 24px; margin: 10px 0;">Opponent Life: <b>{oppo_life}</b></p>
        <p style="font-size: 20px; margin: 20px 0; color: gray;">{win_prob_text}</p>
    </div>
    """
    return html
