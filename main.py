from lib.quoter import Quoter
from lib.imager import Imager


if __name__ == '__main__':
  Q = Quoter()
  I = Imager()
  quote = Q.get()
  I.get_picture()
  I.write_quote(quote)
  print("> Done 🤘")