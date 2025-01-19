import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '../data')

def main():
    
    # Load ratings
    ratings_df = pd.read_csv(os.path.join(DATA_DIR, 'my_ratings_with_cast.csv'))

    # Select relevant columns
    keep = ['Title', 'Your Rating', 'Title Type', 'IMDb Rating', 'Num Votes', 'Release Date', 'Directors', 'Cast']
    ratings_df = ratings_df[keep]

    # Keep only first listed director
    ratings_df['Directors'] = ratings_df['Directors'].str.split(',').str[0]
    ratings_df.rename(columns={'Directors': 'Director'}, inplace=True)


def long_form(df):
    pass


if __name__ == '__main__':
    main()