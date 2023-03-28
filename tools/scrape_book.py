import requests
from bs4 import BeautifulSoup

# define the user profile URL
url = 'https://www.goodreads.com/user/show/86632532-vinoth'

# send a GET request to the URL and get the response object
response = requests.get(url)

# create a BeautifulSoup object from the response content
soup = BeautifulSoup(response.content, 'html.parser')

# find the bookshelf container that contains all the book information
bookshelf_container = soup.find('div', {'class': 'bookshelfContainer'})

# find all the book items inside the bookshelf container
book_items = bookshelf_container.find_all('div', {'class': 'bookalike'})

# loop through each book item and extract the information
for book_item in book_items:
    # extract the book title
    book_title = book_item.find('a', {'class': 'bookTitle'}).text.strip()
    
    # extract the book author
    book_author = book_item.find('a', {'class': 'authorName'}).text.strip()
    
    # extract the book image URL
    book_image_url = book_item.find('img')['src']
    
    # print the extracted information
    print(f'Title: {book_title}')
    print(f'Author: {book_author}')
    print(f'Image URL: {book_image_url}')
    print('-------------------------')




