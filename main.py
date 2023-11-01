import os
from random import random, choice
import textwrap
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw
import requests
import ipdb

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
    
class Imager():
  W = 1024
  H = 768
  d = 2
  tmp_filename = "temp.jpg"
  result_filename = "out.jpg"
  # TODO first grab a link from https://homerize.com/_framegrabs/ then parse <imgs>
  images_url = "http://homerize.com/_framegrabs/%s/"

  def __init__(self):
    pass

  def get_dir(self):
    '''
    Get a random dir from homerize.com
    :returns: string with the dir
    '''
    season = 1 + int(random() * 9)
    chap = 1 + int(random() * 10)

    if chap < 10:
        chap = "0%s" % chap

    return "%sF%s" % (season, chap)

  def get_picture(self):
    '''
    Gets a random image from homerize and saves as the tmp file
    '''
    url = self.images_url % self.get_dir()
    page = requests.get(url)
    print("> URL with images:\n%s\n" % url)
    document = BeautifulSoup(page.content, features="html.parser")
    imgs = document.find_all('img')
    img = choice(imgs)
    print("> Chosen image:\n%s%s\n" % (url, img.attrs['src']))
    req = requests.get("%s%s" % (url, img.attrs['src']), stream=True)

    with open(self.tmp_filename, 'wb') as img_file:
      for chunk in req:
        img_file.write(chunk)

  def write_quote(self, quote):
    '''
    Draws a quote on the temp.jpg image
    '''
    image = Image.open(self.tmp_filename)
    font = ImageFont.truetype('font.ttf', 26)
    big = image.resize((self.W, self.H))
    draw = ImageDraw.Draw(big)
    #import ipdb; ipdb.set_trace()
    draw.text((self.W / 2 + 2, self.H - 2 + 2), quote, font=font, anchor="md", fill=(0 ,0, 0), spacing=15)
    draw.text((self.W / 2, self.H - 2), quote, font=font, anchor="md", fill=(255, 255, 255), spacing=15)
    big.save(self.result_filename, "JPEG")
    os.remove(self.tmp_filename)



if __name__ == '__main__':
  Q = Quoter()
  I = Imager()
  quote = Q.get()
  I.get_picture()
  I.write_quote(quote)
  print("> Done")