import pandas as pd

def load_id_to_wr_mappings():
    """
    Loads and prepares a card mapping dictionary (ID → GP WR).
    
    Returns:
        dict: A dictionary mapping card IDs to GP WR.
    """
    cards = pd.read_csv(r'C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\data\cards_data\cards.csv')
    ratings = pd.read_csv(r'C:\Users\Jack Wright\Documents\GitHub\sevLandsPublicData\data\cards_data\card_ratings\dks_card_ratings.csv')
    card_mapping = cards.merge(ratings, left_on='name', right_on='Name')[['id', 'GP WR']]
    # convert 'GP WR' to numeric, remove % and move decimal
    card_mapping['GP WR'] = card_mapping['GP WR'].str.rstrip('%').astype('float') / 100.0
    return card_mapping.set_index('id')['GP WR'].to_dict()