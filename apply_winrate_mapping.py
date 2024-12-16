import pandas as pd
import numpy as np

from get_card_columns import get_card_columns
from map_id_to_winrate import map_id_to_winrate


def apply_winrate_mapping(df, id_to_wr_mapping, column_prefix, max_cards):
    """
    Applies map_id_to_winrate to the specified card columns in the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the card ID columns.
        id_to_wr_mapping (dict): A dictionary mapping card IDs to GP WR values.
        column_prefix (str): The prefix for the column names (e.g., 'user_hand').
        max_cards (int): The maximum number of card slots to check for.
    
    Returns:
        pd.DataFrame: The updated DataFrame with card IDs replaced by GP WR values.
    """
    card_columns = get_card_columns(df, column_prefix, max_cards)
    
    for col in card_columns:
        df[col] = df[col].apply(lambda x: map_id_to_winrate(x, id_to_wr_mapping) if pd.notnull(x) else np.nan)
    
    return df