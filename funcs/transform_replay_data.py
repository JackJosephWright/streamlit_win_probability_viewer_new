from transform_row_to_turns import transform_row_to_turns
import pandas as pd
def transform_replay_data(data, id_to_wr_mapping, max_cards=20):
    """
    Transforms the replay data into a format suitable for modeling.
    
    Parameters:
        data (pd.DataFrame): The replay data to transform.
        id_to_wr_mapping (dict): A dictionary mapping card IDs to GP WR values.
        max_cards (int): Maximum number of slots for cards in hand or on the board.
    
    Returns:
        pd.DataFrame: The transformed replay data with GP WR values and one row per turn.
    """
    # Initialize an empty list to collect all turn DataFrames
    all_turns = []
    
    # Iterate through each row in the data
    for idx, row in data.iterrows():
        # Transform the row into a DataFrame of turns
        turn_df = transform_row_to_turns(row, id_to_wr_mapping, max_cards=max_cards)
        
        # Append the DataFrame to the list
        all_turns.append(turn_df)
    
    # Concatenate all DataFrames into a single DataFrame
    all_turns_df = pd.concat(all_turns, ignore_index=True)
    return all_turns_df