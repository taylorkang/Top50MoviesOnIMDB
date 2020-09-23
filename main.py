import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint

headers = {"Accept-Language": "en-US, en;q=0.5"}

#print(soup.prettify())

#initialize empty lists to store data
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

pages = np.arange(1, 1001, 50)

for page in pages:
  page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&start=" + str(page) + "&ref_=adv_nxt", headers=headers)

  soup = BeautifulSoup(page.text, 'html.parser')

  movie_div = soup.find_all('div', class_='lister-item mode-advanced')

  sleep(randint(2,10))

#initiate for loop 
#this tells scraper to iterate through
#every div container stored in movie_div variable
  for container in movie_div:

    #extract movie's title
    name = container.h3.a.text
    titles.append(name)

    #extract year of release
    year = container.h3.find('span', class_='lister-item-year').text
    years.append(year)

    #extract runtime
    runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
    time.append(runtime)

    #extract imdb rating
    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    #extract metascore
    m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
    metascores.append(m_score)

    #extract votes and gross earnings
    nv = container.find_all('span', attrs={'name': 'nv'})

    vote = nv[0].text
    votes.append(vote)

    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)

movies = pd.DataFrame({
  'movie': titles,
  'year': years,
  'timeMin': time,
  'imdb': imdb_ratings,
  'metascore': metascores,
  'votes': votes,
  'us_grossMillions': us_gross,
})

  #print(movies)

  #check data types


  #clean up data

movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].str.extract('(\d)')
movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')

# to see your dataframe
print(movies)

# to see the datatypes of your columns
print(movies.dtypes)

# to see where you're missing data and how much data is missing 
print(movies.isnull().sum())

# to move all your scraped data to a CSV file
movies.to_csv('movies.csv')