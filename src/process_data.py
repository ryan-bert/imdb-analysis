import os
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '../data')
OUTPUT_DIR = os.path.join(CURRENT_DIR, '../output')

def main():

    # Load long-form data
    actors_long = pd.read_csv(os.path.join(DATA_DIR, 'actors_long.csv'))
    
    # Group by Actor and calculate the count of appearances and average IMDb rating
    actor_summary = actors_long.groupby('Actor').agg(
        Appearances=('Actor', 'size'),
        Avg_IMDb_Rating=('IMDb Rating', 'mean'),
        My_Avg_Rating=('Your Rating', 'mean')
    ).reset_index()
    # Sort by Appearances and then by Avg_IMDb_Rating
    actor_summary = actor_summary.sort_values(by=['Appearances', 'My_Avg_Rating'], ascending=[False, False])

    # Rename columns
    actor_summary.rename(columns={'Avg_IMDb_Rating': 'Avg IMDb Rating', 'My_Avg_Rating': 'My Avg Rating'}, inplace=True)

    # Save the actor summary back to a CSV
    summary_csv_path = os.path.join(OUTPUT_DIR, 'actor_summary.csv')
    actor_summary.to_csv(summary_csv_path, index=False)

    # Get my favorite actors
    favorite_actors = actor_summary[(actor_summary['My Avg Rating'] >= 7.5) & (actor_summary['Appearances'] >= 5)]
    favorite_actors = favorite_actors.sort_values(by='My Avg Rating', ascending=False)
    


if __name__ == '__main__':
    main()