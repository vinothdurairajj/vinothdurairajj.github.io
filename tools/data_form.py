import requests

# Define book titles and authors
book1 = {"title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari"}
book2 = {"title": "The Star", "author": "Arthur C. Clarke"}

# Initialize books dictionary
BOOKS = {"books": []}

# Loop over books
for book in [book1, book2]:
    # Use OpenLibrary API to get book cover URL and ISBN
    response = requests.get(f"http://openlibrary.org/search.json?title={book['title']}&author={book['author']}")
    if response.status_code == 200:
        data = response.json()
        if data['numFound'] > 0:
            cover_url = f"http://covers.openlibrary.org/b/isbn/{data['docs'][0]['isbn'][0]}-L.jpg"
            isbn = data['docs'][0]['isbn'][0]
        else:
            cover_url = None
            isbn = None
    else:
        cover_url = None
        isbn = None
    
    # Use Goodreads API to get book genre and Goodreads URL
    response = requests.get(f"https://www.goodreads.com/search/index.xml?key=YOUR_GOODREADS_API_KEY&q={book['title']}")
    if response.status_code == 200:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        work = root.find(".//work")
        goodreads_url = work.find('url').text
        genre = work.find('.//shelf[@name="genres"]/book/@title')
        if genre is not None:
            genre = genre.text
        else:
            genre = None
    else:
        goodreads_url = None
        genre = None

    # Add book information to BOOKS dictionary
    BOOKS["books"].append({
        "title": book['title'],
        "author": book['author'],
        "genre": genre,
        "goodreads": {
            "url": goodreads_url,
            "image": cover_url,
            "genre": genre
        }
    })

print(BOOKS)
