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

    # Convert to long-form data
    ratings_df['Cast'] = ratings_df['Cast'].str.split(', ')
    actors_long = ratings_df.explode('Cast').reset_index(drop=True)

    # Rename and reorder columns to make Actor the first column
    actors_long.rename(columns={'Cast': 'Actor'}, inplace=True)
    columns_order = ['Actor'] + [col for col in actors_long.columns if col != 'Actor']
    actors_long = actors_long[columns_order]

    # Save the updated DataFrame back to a CSV
    long_csv_path = os.path.join(DATA_DIR, 'actors_long.csv')
    actors_long.to_csv(long_csv_path, index=False)


if __name__ == '__main__':
    main()