import requests
import bs4 as bs

def main():
    pass

def get_cast(title_id, size=10):

    # Get the full credits page
    url = f'https://www.imdb.com/title/{title_id}/fullcredits'
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    # Get the table rows
    even_table_rows = soup.find_all('tr', class_='odd')
    odd_table_rows = soup.find_all('tr', class_='even')

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