import matplotlib.pyplot as plt

# Plot win probabilities up to the current turn
def plot_win_probability(df, current_turn):
    """
    Plots the win probabilities up to the current turn.
    - df: DataFrame containing the game data with 'predict_proba' column.
    - current_turn: Current turn being displayed (int).
    """
    # Extract data up to the current turn
    turns = df['turn'][:current_turn + 1]
    win_probs = df['predict_proba'][:current_turn + 1]
    current_win_prob = win_probs.iloc[-1]  # Get the win probability for the current turn


    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.plot(turns, win_probs, marker='o', linestyle='-', color='blue', label='Win Probability')
    ax.set_title("Win Probability Over Time", fontsize=16)
    ax.set_xlabel("Turn", fontsize=12)
    ax.set_ylabel("Win Probability", fontsize=12)
    ax.set_ylim(0, 1)  # Probabilities range from 0 to 1
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    ax.text(
        0.95, 0.95,  # Position: top-right corner
        f"Current Win Prob: {current_win_prob:.2%}",
        transform=ax.transAxes,  # Use relative coordinates
        fontsize=12,
        color='blue',
        ha='right',  # Align text to the right
        va='top'  # Align text to the top
    )

    return fig
