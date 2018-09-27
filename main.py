from lxml import html
from random import random
from PIL import Image, ImageDraw, ImageFont
import requests
import textwrap
import shutil
import os


_dbg_flag = True

class Quoter():
    def __init__(self):
        # You can edit this array and add more movies, just search their quotes page from IMDB
        movies = ["http://www.imdb.com/title/tt0120737/quotes", #Lord Of The Rings
                  "http://www.imdb.com/title/tt0121955/quotes", #South Park
                  "http://www.imdb.com/title/tt0068646/quotes", #Godfather
                  "http://www.imdb.com/title/tt0078748/quotes", #Alien
                  "http://www.imdb.com/title/tt0087332/quotes", #Ghostbusters
                  "http://www.imdb.com/title/tt0091763/quotes" #Platoon
                  ]

        movie = int(random() * len(movies))
        print("CHOSEN MOVIE\n%s\n====\n" % movies[movie])
        self.base_url = movies[movie]

    def get(self):
        page = requests.get(self.base_url)
        tree = html.fromstring(page.content)
        quotes = tree.xpath("//div[contains(@class, 'sodatext')]")
        quote = quotes[int(random() * len(quotes))]

        if _dbg_flag:
            print("TEXT\n%s\n====\n" % quote.text_content())

        paras = quote.findall("p")
        parsed_text = ""
        total_lines = 5

        for para in paras:
            if para.find("a") is not None and total_lines > 0:
                character = para.find("a").text_content()
                pre_text = "- %s\n" % (para.text_content()
                                                        .replace("\n", "")
                                                        .replace(character, "")
                                                        .replace(":", ""))

                if _dbg_flag:
                    print("WRAP\n")
                    print(pre_text)
                    print(textwrap.wrap(pre_text, 60))
                    print("====\n")

                for text_line in textwrap.wrap(pre_text, 60):
                    parsed_text += text_line + "\n"
                    total_lines -= 1

        if _dbg_flag:
            print("PARSED TEXT\n%s\n====\n" % parsed_text)

        return parsed_text



class Writer():
    def __init__(self):
        self.img = None
        self.quote = None
        self._quoter = Quoter()

    def get_dir(self):
        #check seasons/chap numbers
        season = 1 + int(random() * 9)
        chap = 1 + int(random() * 10)

        if chap < 10:
            chap = "0%s" % chap

        return "%sF%s" % (season, chap)

    def get_picture(self):
        #try:
        url = "http://homerize.com/_framegrabs/%s/" % self.get_dir()
        page = requests.get(url)
        tree = html.fromstring(page.content)
        links = tree.xpath("//a")
        chosen = links[1 + int(random() * len(links))]
        img = chosen.text_content().replace(" ", "")

        if _dbg_flag:
            print("FETCHING\n%s\n====\n" % (url + img))

        req = requests.get(url + img, stream=True)

        with open("test.jpg", 'wb') as img_file:
            for chunk in req:
                img_file.write(chunk)

        self.img = Image.open("test.jpg")
        self.quote = self._quoter.get()
        #except:
            #raise BaseException("FUCK this url:%s", url)

    def save_picture(self):
        W, H = (1024, 768)
        big = self.img.resize((W, H))
        draw = ImageDraw.Draw(big)
        fnt = ImageFont.truetype('font.ttf', 26)
        w, h = draw.textsize(self.quote, fnt)

        if _dbg_flag:
            print("Size of IMG, size of TXT\n%s %s\n%s %s\n====\n" % (W, H ,w ,h))

        draw.text(( (W-w)/2+2, (H-h-50)+2), self.quote, (0, 0, 0), font=fnt, align="center", spacing=15)
        draw.text(( (W-w)/2, (H-h-50)), self.quote, (255, 255, 255), font=fnt, align="center", spacing=15)
        big.save("out.jpg")
        os.remove("test.jpg")




if __name__ == '__main__':
    W = Writer()
    W.get_picture()
    W.save_picture()
    print("DONE")
