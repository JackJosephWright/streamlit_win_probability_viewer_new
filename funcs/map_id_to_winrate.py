import numpy as np
def map_id_to_winrate(value, id_to_wr_mapping):

    """
    Maps a single card ID to its winrate using the provided dictionary.
    
    Parameters:
        value (int): The card ID to map.
        id_to_wr_mapping (dict): A dictionary mapping card IDs to winrates.
    
    Returns:
        float: The winrate of the card ID, or NaN if not found.
    """
    value = int(value)

    return id_to_wr_mapping.get(value, np.nan)
