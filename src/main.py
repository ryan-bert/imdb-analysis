import os
import requests
import bs4 as bs
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '../data')

def main():
    # Load ratings
    ratings_df = pd.read_csv(os.path.join(DATA_DIR, 'my_ratings.csv'))

    # No TV Specials
    ratings_df = ratings_df[ratings_df['Title Type'] != 'TV Special']

    # Loop through each row in the DataFrame
    ratings_df['Cast'] = None
    for index, row in ratings_df.iterrows():

        # Get the title ID and title
        title_id = row['Const']
        title = row['Title']

        try:
            # Get the cast for the title
            cast_list = None
            if row['Title Type'] == 'TV Series' or row['Title Type'] == 'TV Mini-Series':
                cast_list = get_series_cast(title_id)
            else:
                cast_list = get_movie_cast(title_id)
            # Convert the cast list to a comma-separated string
            cast_str = ', '.join(cast_list)
            # Add the cast to the "Cast" column
            ratings_df.at[index, 'Cast'] = cast_str
            print(f"Cast for {title}: {cast_str}")

        except Exception as e:
            print(f"Error fetching cast for {title}: {e}")
            ratings_df.at[index, 'Cast'] = "Error fetching cast"

    # Save the updated DataFrame back to a CSV
    updated_csv_path = os.path.join(DATA_DIR, 'my_ratings_with_cast.csv')
    ratings_df.to_csv(updated_csv_path, index=False)
    print(f"Updated ratings saved to {updated_csv_path}")

def get_movie_cast(title_id, size=10):
    # Get the full credits page
    url = f'https://www.imdb.com/title/{title_id}/fullcredits'
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    # Get the table rows
    table = soup.find('table', class_='cast_list')
    odd_table_rows = table.find_all('tr', class_='odd')
    even_table_rows = table.find_all('tr', class_='even')

    # Combine the lists alternately
    table_rows = []
    for even, odd in zip(even_table_rows, odd_table_rows):
        table_rows.append(even)
        table_rows.append(odd)

    # Get the cast
    cast = []
    for row in table_rows[:size]:
        data = row.find_all('td')[1]
        actor = data.find('a').text.strip()
        cast.append(actor)

    return cast

def get_series_cast(title_id, size=10):

    # Get the full credits page
    url = f'https://www.imdb.com/title/{title_id}/fullcredits'
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    # Get the table rows
    table = soup.find('table', class_='cast_list')
    odd_table_rows = table.find_all('tr', class_='odd')
    even_table_rows = table.find_all('tr', class_='even')

    odd_table_rows = [row for i, row in enumerate(odd_table_rows) if i % 2 == 0]
    even_table_rows = [row for i, row in enumerate(even_table_rows) if i % 2 == 0]

    # Combine the lists alternately
    table_rows = []
    for even, odd in zip(even_table_rows, odd_table_rows):
        table_rows.append(even)
        table_rows.append(odd)

    # Get the cast
    cast = []
    for row in table_rows[:size]:
        data = row.find_all('td')[1]
        actor = data.find('a').text.strip()
        cast.append(actor)

    return cast


if __name__ == '__main__':
    main()