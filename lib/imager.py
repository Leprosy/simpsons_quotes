import os
import requests
from bs4 import BeautifulSoup
from random import choice
from PIL import Image, ImageFont, ImageDraw

class Imager():
  W = 1024
  H = 768
  d = 2
  tmp_filename = "temp.jpg"
  result_filename = "out.jpg"
  # TODO first grab a link from https://homerize.com/_framegrabs/ then parse <imgs>
  images_url = "http://homerize.com/_framegrabs/"

  def __init__(self):
    pass

  def get_dir(self):
    '''
    Get a random dir from homerize.com
    :returns: string with the dir
    '''
    page = requests.get(self.images_url)
    document = BeautifulSoup(page.content, features="html.parser")
    links = document.find_all('a')[4:]
    return choice(links).text

  def get_picture(self):
    '''
    Gets a random image from homerize and saves as the tmp file
    '''
    url = "%s%s" % (self.images_url, self.get_dir())
    print("> URL with images:\n%s\n" % url)
    page = requests.get(url)
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
    draw.text((self.W / 2 + 2, self.H - 2 + 2), quote, font=font, anchor="md", fill=(0 ,0, 0), spacing=15)
    draw.text((self.W / 2, self.H - 2), quote, font=font, anchor="md", fill=(255, 255, 255), spacing=15)
    big.save(self.result_filename, "JPEG")
    os.remove(self.tmp_filename)