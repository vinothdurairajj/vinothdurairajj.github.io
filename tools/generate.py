
import json
import os

import PIL
from PIL import Image

import urllib
import urllib.request

#from book_data import BOOKS

IMAGE_WIDTH  = 168
IMAGE_HEIGHT = 248
TEMPLATE =  """"<SEQ_NUM>": {
    "title": "<TITLE>",
    "image": "<GOODREADS_IMAGE_URL>",
    "genre": "<GENRE>"
  }"""



def resize(src_image, dst_image):
    img = Image.open(src_image)
    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), PIL.Image.ANTIALIAS)
    img.save(dst_image)


def _get_filename_from_url(url):

    parse_result = urllib.parse.urlparse(url)
    path, filename = os.path.split(parse_result.path)

    return filename


def download(url, dst_image):
    #image = urllib.URLopener()
    #image.retrieve(url, dst_image)
    urllib.request.urlretrieve(url, dst_image)


def foo(BOOKS):
    #print (json.dumps(BOOKS, indent=4))
    genres = {}
    books = BOOKS.get('books')
    for book in books:
        genre_list = book.get('genre').split(',')
        for genre in genre_list:
              if genre.strip() not in genres.keys():
                  genres[genre.strip()] = [book.get('title')]
              else:
                  genres.get(genre.strip()).append(book.get('title'))

    for genre in genres.keys():
        print ('%s: %d' %(genre, len(genres.get(genre))))
        print ('='*80)
        for title in genres.get(genre):
            print ('%80s' %(title))
        print ('\n')


def generate_html(BOOKS):
    genres = []
    books = BOOKS.get('books')
    for book in books:
        genre_list = book.get('genre').split(',')
        for genre in genre_list:
            genre = genre.strip()
            if genre not in genres:
                genres.append(genre)

    html = '<OPTION value="All">All Genres</OPTION>\n'
    for genre in genres:
        html += '<OPTION value="%s">%s</OPTION>\n' %(genre.replace(" ", ""), genre)

    return html

def generate_js(BOOKS):

    books = BOOKS.get('books')
    count = 0
    js = ""
    for book in books:
        try:
            count += 1
            image = os.path.join('images', _get_filename_from_url(book.get('goodreads').get('image')))
            book_data = TEMPLATE.replace("<TITLE>", book.get('title'))
            book_data = book_data.replace("<SEQ_NUM>", str(count))
            book_data = book_data.replace("<GOODREADS_IMAGE_URL>", image)
            #book_data = book_data.replace("<GOODREADS_IMAGE_URL>", book.get('goodreads').get('image'))
            book_data = book_data.replace("<GENRE>", book.get('genre').replace(" ", ""))
            if book.get('goodreads').get('myreview'):
                book_data = book_data[:-4] + ",\n"
                book_data += '    "review": "%s"' %book.get('goodreads').get('myreview')
                book_data += '\n  }'
            js += book_data
            js += ",\n"
        except:
            print(f"not done js for {book}")
    js = js[:-2]
    js = "var NUM_BOOKS = %d;\nvar BOOKS = {\n%s\n}" %(count, js)

    return js

def resize_book_images(BOOKS):
    if not os.path.exists('original'):
        os.mkdir('original')

    if not os.path.exists('images'):
        os.mkdir('images')

    books = BOOKS.get('books')
    for book in books:
        try:
            image = book.get('goodreads').get('image')
            if not os.path.exists(os.path.join('original', _get_filename_from_url(image))):
                print ('Resizing: %s' %image)
                download(image, os.path.join('original', _get_filename_from_url(image)))
                resize(
                    os.path.join('original', _get_filename_from_url(image)),
                    os.path.join('images', _get_filename_from_url(image))
                    )
        except:
            print(f"not done for book {book}")

def generate_BOOKS():
    from bs4 import BeautifulSoup
    import requests
    import os

    url = 'https://www.goodreads.com/review/list/86632532-vinoth?shelf=read'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    titles = []
    for title_div in soup.find_all('td', {'class': 'field title'}):
        title = title_div.find('a').text.strip().replace('\n', '').replace("'","").replace('"','')
        titles.append(title)

    images = []
    for image_div in soup.find_all('td', {'class': 'field cover'}):
        url,id = os.path.split(image_div.img['src'])
        img1 = os.path.basename(url)
        img2 = id.split('.')[0]
        #image = image_div.img['src']
        imgurl = f"https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/{img1}/{img2}.jpg"
        images.append(imgurl)

    urls = []
    for url_div in soup.find_all('td', {'class': 'field cover'}):
        url = f"https://www.goodreads.com{url_div.a['href']}"
        urls.append(url)

    authors = []
    for author_div in soup.find_all('td', {'class': 'field author'}):
        author = author_div.find('a').text.strip()
        authors.append(author)
    BOOKS = {"books": []}
    for tit,auth,ur,ima in zip(titles,authors,urls,images): 
        book = {
            "title": tit,
            "author": auth,
            "genre": 'PersonalGoal,Read',
            "goodreads": {
                "url": ur,
                "image": ima,
                "myreview":ur,
                "genre": 'PersonalGoal,Read'
            }
        }
        BOOKS["books"].append(book)
        print(BOOKS)
    return BOOKS

def generate_from_widget():
    from bs4 import BeautifulSoup

    # Open the HTML file and create a BeautifulSoup object
    with open('widget.html', encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Find all the book containers
    book_containers = soup.find_all('div', class_='gr_grid_book_container')

    # Loop through the book containers and extract the data
    titles = []
    urls = []
    images = []
    for book in book_containers:
        # Extract the title and href attributes
        title = book.a.get('title').strip().replace('\n', '').replace("'","").replace('"','')
        titles.append(title)
        url = book.a.get('href')
        urls.append(url)
        url,id = os.path.split(book.img.get('src'))
        img1 = os.path.basename(url)
        img2 = id.split('.')[0]
        #image = image_div.img['src']
        imgurl = f"https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/{img1}/{img2}.jpg"
        images.append(imgurl)
    BOOKS = {"books": []}
    for tit,ur,ima in zip(titles,urls,images): 
        book = {
            "title": tit,
            "author": 'NA',
            "genre": 'PersonalGoal,Read',
            "goodreads": {
                "url": ur,
                "image": ima,
                "myreview":ur,
                "genre": 'PersonalGoal,Read'
            }
        }
        BOOKS["books"].append(book)
        print(BOOKS)
    return BOOKS


        
        # Print the data
        #print('Title:', title)
        #print('Href:', href)
        #print('Img:', img)


if '__main__' == __name__:
    #BOOK = generate_BOOKS()
    BOOK = generate_from_widget()
    print(BOOK)
    resize_book_images(BOOK)
    js_data = generate_js(BOOK)
    print(js_data)
    fd = open('js/data.js', 'w', encoding="utf-8")
    fd.write(js_data)
    fd.close()
    #print (generate_html(BOOK))
