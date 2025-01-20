import os
import pandas as pd
from plotnine import ggplot, aes, geom_point, geom_bar, scale_x_continuous, ggtitle, xlab, ylab
import matplotlib.pyplot as plt


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '../data')
OUTPUT_DIR = os.path.join(CURRENT_DIR, '../output')

def main():

    # Load long-form data
    actors_long = pd.read_csv(os.path.join(DATA_DIR, 'actors_long.csv'))
    
    # Group by Actor and calculate the count of appearances and average IMDb rating
    actor_summary = actors_long.groupby('Actor').agg(
        Appearances=('Actor', 'size'),
        Avg_IMDb_Rating=('IMDb Rating', lambda x: round(x.mean(), 2)),
        My_Avg_Rating=('Your Rating', lambda x: round(x.mean(), 2))
    ).reset_index()
    # Sort by Appearances and then by Avg_IMDb_Rating
    actor_summary = actor_summary.sort_values(by=['Appearances', 'My_Avg_Rating'], ascending=[False, False])

    # Rename columns
    actor_summary.rename(columns={'Avg_IMDb_Rating': 'Avg IMDb Rating', 'My_Avg_Rating': 'My Avg Rating'}, inplace=True)

    # Save the actor summary back to a CSV
    summary_csv_path = os.path.join(DATA_DIR, 'actor_summary.csv')
    actor_summary.to_csv(summary_csv_path, index=False)

    # Get my favorite actors
    favorite_actors = actor_summary[(actor_summary['My Avg Rating'] >= 8) & (actor_summary['Appearances'] >= 5)]
    favorite_actors = favorite_actors.sort_values(by='My Avg Rating', ascending=False)

    # Create a table from the DataFrame
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    table = ax.table(
        cellText=favorite_actors.values,
        colLabels=favorite_actors.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(favorite_actors.columns))))
    # Save the table as a PNG image
    output_path = os.path.join(OUTPUT_DIR, 'favorite_actors_table.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')

    # Group by Director and Actor to calculate collaborations and ratings
    director_actor_summary = actors_long.groupby(['Director', 'Actor']).agg(
        Collaborations=('Title', 'size'),
        Avg_IMDb_Rating=('IMDb Rating', lambda x: round(x.mean(), 2)),
        My_Avg_Rating=('Your Rating', lambda x: round(x.mean(), 2))
    ).reset_index()
    # Sort by Collaborations and then My_Avg_Rating
    director_actor_summary = director_actor_summary.sort_values(by=['Collaborations', 'My_Avg_Rating'], ascending=[False, False])

    # Rename columns
    director_actor_summary.rename(columns={'Avg_IMDb_Rating': 'Avg IMDb Rating', 'My_Avg_Rating': 'My Avg Rating'}, inplace=True)

    # Create table of top 20 collaborations
    top_collaborations = director_actor_summary.head(20)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    table = ax.table(
        cellText=top_collaborations.values,
        colLabels=top_collaborations.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(top_collaborations.columns))))
    # Save the table as a PNG image
    output_path = os.path.join(OUTPUT_DIR, 'top_collaborations_table.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')

    # Load the original ratings data
    ratings_df = pd.read_csv(os.path.join(DATA_DIR, 'my_ratings.csv'))

    # Calculate difference between IMDb Rating and My Rating
    contoversial_df = ratings_df.copy()
    contoversial_df['Rating Difference'] = (contoversial_df['IMDb Rating'] - contoversial_df['Your Rating']).abs().round(2)
    contoversial_df = contoversial_df.sort_values(by='Rating Difference', ascending=False)
    contoversial_df = contoversial_df[['Title', 'IMDb Rating', 'Your Rating', 'Rating Difference']]

    # Create table of the top 20 controversial ratings
    top_controversial = contoversial_df.head(20)
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    table = ax.table(
        cellText=top_controversial.values,
        colLabels=top_controversial.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(top_controversial.columns))))
    # Save the table as a PNG image
    output_path = os.path.join(OUTPUT_DIR, 'controversial_table.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')

    # Get the release month of each movie
    movie_df = ratings_df[ratings_df['Title Type'] == 'Movie']
    movie_df['Release Date'] = pd.to_datetime(movie_df['Release Date'])
    movie_df["Release Month"] = movie_df['Release Date'].dt.month

    # Get rating month for each title
    ratings_df['Date Rated'] = pd.to_datetime(ratings_df['Date Rated'])
    ratings_df['Rating Month'] = ratings_df['Date Rated'].dt.month

    # Create a histogram of rating months
    rating_month_histogram = (
        ggplot(ratings_df, aes(x='Rating Month')) +
        geom_bar() +
        ggtitle('Frequency of Ratings by Month') +
        xlab('Month') +
        ylab('Number of Ratings') +
        scale_x_continuous(breaks=range(1, 13), labels=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ])
    )
    rating_month_histogram.save(os.path.join(OUTPUT_DIR, 'rating_month_histogram.png'))

    # Create a histogram of release months
    release_month_histogram = (
        ggplot(movie_df, aes(x='Release Month')) +
        geom_bar() +
        ggtitle('Frequency of Movie Releases by Month') +
        xlab('Month') +
        ylab('Number of Movies') +
        scale_x_continuous(breaks=range(1, 13), labels=[
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ])
    )
    release_month_histogram.save(os.path.join(OUTPUT_DIR, 'release_month_histogram.png'))

    # Scatter plot of IMDb Rating vs. My Rating
    ratings_scatterplot = (
        ggplot(ratings_df, aes(x='IMDb Rating', y='Your Rating')) +
        geom_point() +
        ggtitle('IMDb Rating vs. My Rating') +
        xlab('IMDb Rating') + ylab('My Rating')
    )
    ratings_scatterplot.save(os.path.join(OUTPUT_DIR, 'ratings_scatterplot.png'))

    # Scatter plot of IMDb Rating vs. Num Votes
    votes_scatterplot = (
        ggplot(ratings_df, aes(x='Num Votes', y='IMDb Rating')) +
        geom_point() +
        ggtitle('IMDb Rating vs. Num Votes') +
        xlab('Num Votes') + ylab('IMDb Rating')
    )
    votes_scatterplot.save(os.path.join(OUTPUT_DIR, 'votes_scatterplot.png'))

if __name__ == '__main__':
    main()