from bs4 import BeautifulSoup
import requests
import os

url = 'https://www.goodreads.com/review/list/86632532-vinoth?shelf=read'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

titles = []
for title_div in soup.find_all('td', {'class': 'field title'}):
    title = title_div.find('a').text.strip()
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
    url = f"https://www.goodreads.com/{url_div.a['href']}"
    urls.append(url)


authors = []
for author_div in soup.find_all('td', {'class': 'field author'}):
    author = author_div.find('a').text.strip()
    authors.append(author)

# asins = []
# for asin_div in soup.find_all('td', {'class': 'field asin'}):
#     asin = asin_div.find('value').text.strip()
#     asins.append(asin)



for i,j,k,l in zip(titles,authors,images,urls):
    print(i,j,k,l)