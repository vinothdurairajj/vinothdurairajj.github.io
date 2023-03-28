
import xmltodict
import requests
from bs4 import BeautifulSoup

import json
import os

import PIL
from PIL import Image

import urllib
import urllib.request

AMAZON_ACCESS_KEY_ID = 'AKIAIVBT7KRNVIFWKI6A'
AMAZON_SECRET_KEY = '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'
AMAZON_ASSOC_TAG = 'learninone0f-21'


import requests
import json

def get_book_image(title, author):

# Set up the Amazon API object with your access key and secret key
  import requests

# Enter the book title and author
  #title = 'The Magic of Believing'
  #author = 'Claude M. Bristol'

  # Make a request to the Open Library Search API to get the book details
  response = requests.get(f'http://openlibrary.org/search.json?title={title}&author={author}')

  # Get the JSON response
  data = response.json()

  # Get the first result from the response
  result = data['docs'][0]

  # Get the cover URL and ISBN from the result
  cover_url = f'http://covers.openlibrary.org/b/id/{result["cover_i"]}-L.jpg'
  isbn = result.get('isbn_13', None)

  # Print the cover URL and ISBN
  print(f'Cover URL: {cover_url}')
  print(f'ISBN: {isbn}')
  return cover_url

def get_goodreads_url(title, author):
  import requests
  from bs4 import BeautifulSoup

  #title = "Sapiens: A Brief History of Humankind"
  #author = "Yuval Noah Harari"

  search_url = f"https://www.goodreads.com/search?q={title}+{author}&search_type=books"
  response = requests.get(search_url)

  soup = BeautifulSoup(response.content, "html.parser")
  first_book_link = soup.find("a", class_="bookTitle")["href"]
  book_url = f"https://www.goodreads.com{first_book_link}"

  print(book_url)
  return(book_url)


def get_title_author():
    data = {'Wings of Fire: An Autobiography':'Kalam, A.P.J. Abdul',
'The Millionaire Next Door: The Surprising Secrets of Americas Wealthy':'Stanley, Thomas J.',
'Predictable Revenue: Turn Your Business Into a Sales Machine with the $100 Million Best Practices of Salesforce.com':'Ross, Aaron',
'The Almanack of Naval Ravikant: A Guide to Wealth and Happiness':'Jorgenson, Eric',
'Economics in One Lesson: The Shortest and Surest Way to Understand Basic Economics':'Hazlitt, Henry',
'How to Stop Worrying and Start Living':'Carnegie, Dale',
'The Autobiography of Benjamin Franklin':'Franklin, Benjamin',
'Programming Perl':'Christiansen, Tom',
'You Can Win: A Step by Step Tool for Top Achievers':'Khera, Shiv',
'One Up On Wall Street: How to Use What You Already Know to Make Money in the Market':'Lynch, Peter',
'Shivaji':'Bhagwat, B.R.',
'Basic Economics: A Citizens Guide to the Economy':'Sowell, Thomas',
'The Magic of Believing':'Bristol, Claude M.',
'The Power of Positive Thinking':'Peale, Norman Vincent',
'Think and Grow Rich':'Hill, Napoleon',
'Gandhi: An Autobiography':'Gandhi, Mahatma',
'As a Man Thinketh':'Allen, James',
'The Power of Your Subconscious Mind':'Murphy, Joseph',
'How to Win Friends and Influence People':'Carnegie, Dale',
'The Art of War':'Sun Tzu',
'The Alchemist':'Coelho, Paulo',
'Siddhartha: An Indian Tale':'Hesse, Hermann',
'John C. Maxwells Leadership Series':'Maxwell, John C.',
'The Holy Bible: English Standard Version':'Anonymous',
'Speed Reading: How to Double (or Triple) Your Reading Speed in Just 1 Hour!':'Hammond, Justin',
'Homo Deus: A History of Tomorrow':'Harari, Yuval Noah',
'Communication Skills Training: A Practical Guide to Improving Your Social Intelligence, Presentation, Persuasion and Public Speaking':'Tuhovsky, Ian',
'Massive Life Success: Live a Stress-Free Life and Achieve Your Goals by Dealing with Anxiety, Stress and Fear':'Foroux, Darius',
'How to Avoid Loss and Earn Consistently in the Stock Market: An Easy-To-Understand and Practical Guide for Every Investor':'Paul, Prasenjit',
'Tamil: A Biography':'Shulman, David Dean',
'Self-Discipline: Powerful Techniques from Billionaires, Navy SEALs, Spartans, Olympic Athletes, and Entrepreneurs':'Mann, Dominic',
'The Art Of Saying NO: How To Stand Your Ground, Reclaim Your Time And Energy, And Refuse To Be Taken For Granted':'Zahariades, Damon',
'Think & Trade Like a Champion: The Secrets, Rules & Blunt Truths of a Stock Market Wizard':'Minervini, Mark',
'Elliott Waves Made Simple: Master Elliott Waves Techniques In Less Than 48 Hours':'Sinclair, Steve',
'80/20 Your Life! How To Get More Done With Less Effort And Change Your Life In The Process!':'Zahariades, Damon',
'Master Your Emotions: A Practical Guide to Overcome Negativity and Better Manage Your Feelings(Mastery Series Book 1)':'Meurisse, Thibaut*',
'Atomic Habits: An Easy and Proven Way to Build Good Habits and Break Bad Ones':'Clear, James*',
'Deep Learning With Python: Beginner Guide with TensorFlow, Keras and Pytorch':'Pan, Chao',
'Reflections : Swami Vivekananda':'Vivekananda, Swami',
'Abduls Journey from Zero to Hero in the Share Market':'Kaushik, Mahesh Chandra',
'Price Action Trading Secrets: Trading Strategies, Tools, and Techniques to Help You Become a Consistently Profitable Trader':'Teo, Rayner',
'The Richest Man in Babylon':'Classon, George S.',
'Zero to Billions - The Zerodha Story: An inspiring story on how a startup disrupted the Indian Stock Market':'B, ABHISH'
}
    for title,author in data:
      return {"title":title,"author":author}

# title, author = get_title_author()
# print(title, author)
# #book_title, book_author, image_url, associate_link = get_book_info(title, author)
# book_image = get_book_image(title, author)

# print('Book Title:', title)
# print('Book Author:', author)
# print('Book Image URL:', book_image)
#print('Associate Link:', associate_link)

def foo():
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


def generate_html():
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
def _get_filename_from_url(url):

    parse_result = urllib.parse.urlparse(url)
    path, filename = os.path.split(parse_result.path)

    return filename

def generate_js():
    BOOKS = {"books": []}
    TEMPLATE =  """"<SEQ_NUM>": {
    "title": "<TITLE>",
    "image": "<GOODREADS_IMAGE_URL>",
    "genre": "<GENRE>"
    }"""

    for book in get_title_author():
      book_image = get_book_image(book['title'], book['author'])
      goodread_rul = get_goodreads_url(book['title'], book['author'])

    BOOKS["books"].append({
            "title": book['title'],
            "author": book['author'],
            "genre": 'Personal',
            "goodreads": {
                "url": goodread_rul,
                "image": book_image,
                "genre": 'Personal'
            }
        })
    books = BOOKS.get('books')
    count = 0
    js = ""
    for book in books:
        count += 1
        image = os.path.join('images', _get_filename_from_url(book.get('goodreads').get('image')))
        book_data = TEMPLATE.replace("<TITLE>", book.get('title'))
        book_data = book_data.replace("<SEQ_NUM>", str(count))
        book_data = book_data.replace("<GOODREADS_IMAGE_URL>", image)
        book_data = book_data.replace("<GENRE>", book.get('genre').replace(" ", ""))
        if book.get('goodreads').get('myreview'):
            book_data = book_data[:-4] + ",\n"
            book_data += '    "review": "%s"' %book.get('goodreads').get('myreview')
            book_data += '\n  }'
        js += book_data
        js += ",\n"
    js = js[:-2]
    js = "var NUM_BOOKS = %d;\nvar BOOKS = {\n%s\n}" %(count, js)

    return js

if '__main__' == __name__:
    js_data = generate_js()
    fd = open('data.js', 'w')
    fd.write(js_data)
    fd.close()

