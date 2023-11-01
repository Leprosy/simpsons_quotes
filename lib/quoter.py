import textwrap
import requests
from random import choice
from bs4 import BeautifulSoup


class Quoter():
  wrap_size = 60
  # You can edit this array and add more movies, just search their quotes page from IMDB
  movies = [
            "tt0120737", #Lord Of The Rings
            "tt0121955", #South Park
            "tt0068646", #Godfather
            "tt0078748", #Alien
            "tt0087332", #Ghostbusters
            "tt0091763" #Platoon
            ]
    
  def __init__(self):
    pass

  def get_movie_url(self):
    '''
    Gets a random IDB page from the list
    '''
    movie = "http://www.imdb.com/title/%s/quotes" % choice(self.movies)
    print("> Chosen movie:\n%s\n" % movie)
    return movie

  def get(self) -> str:
    '''
    Gets a random quote from IMDB a page.
    returns: a string with the quote
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    page = requests.get(self.get_movie_url(), headers=headers)
    document = BeautifulSoup(page.content, features="html.parser")
    quotes = document.find_all('div', {'class', 'ipc-html-content-inner-div'})
    lines = choice(quotes).find_all('li')
    text = ""
    print("> Detected text:")

    for line in lines:
      char = ""
      a = line.find("a")
      print(line.text)

      if a is not None:
        char = "%s:" % a.text
        line = line.text.replace(char, "-")
      else:
        line = line.text

      para = textwrap.wrap(line, self.wrap_size)

      for para_line in para:
        text +=  "%s\n" % para_line

    print("\n> Parsed text:\n%s" % text)
    return text