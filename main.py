from DBWebShop import *
from Guest import *
import cgi
import re

sid_pat = re.compile(r"sid=(\d)")

MAIN_PAGE = "main.html"
CART_PAGE = "cart.html"
ADAPTER = DBWebShop("shop.db")

TABLE_ROW = "<tr>{}</tr>\n"
TABLE_COLUMN = "<td>{}</td>"
IMAGE = """<img src="{}" width="100" height="120">"""

BUTTON_ADD_TO_CART = """<form method="post" action="to_cart">
            <input type="hidden" value = {} name = id>
            <label> Кількість </label><input type="text" value = 0 " name = quantity maxlength = "3" size="4"><br>
            <input type="submit" value="У кошик">
            </form>"""
BUTTON_DELETE_FROM_CART = """<form method="post" action="remove">
            <input type="hidden" value = {} name = id>
            <input type="submit" value="Вилучити з кошика">
            </form>"""
BUTTON_SEARCH_ART = """<form method="post" action="search_art">
            <label> Шукаю актикул: </label><input type="text" name = art_name size="20"><br>
             <input type="submit" value="Пошук">
            </form>"""
BUTTON_SEARCH_CAT = """<form method="post" action="search_cat">
            <label> Шукаю категорію: </label><input type="text" name = cat_name size="20"><br>
            <input type="submit" value="Пошук">
            </form>"""
BUTTON_SHOW_CART = """<form method="post" action="show">
            <input type="submit" value="Мій кошик">
            </form>"""


class MyServer:
    def __init__(self):
        self.commands = {"": self.initialize,
                         "to_cart": self.add_to_cart,
                         "back": self.start,
                         "remove": self.remove,
                         "search_art": self.search_art,
                         "search_cat": self.search_cat,
                         "show": self.show_cart
                         }
        self.guests = {}
        self.last_id = 0

    def __call__(self, environ, start_response):
        """Викликається WSGI-сервером.

           Отримує оточення environ та функцію,
             яку треба викликати у відповідь: start_response.
        Повертає відповідь, яка передається клієнту.
        """
        command = environ.get('PATH_INFO', '').lstrip('/')
        try:
            sid = sid_pat.findall(environ.get("HTTP_COOKIE", ""))[0]
        except:
            sid = 0
        print(command, sid)
        if ".jpg" in command:
            start_response('200 OK', [('Content-Type',
                                       'image/jpg')])
            with open(command, "rb") as f:
                return [f.read()]
        # отримати словник параметрів, переданих з HTTP-запиту
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        err = False
        if command in self.commands:
            # виконати команду та отримати тіло відповіді
            body = self.commands[command](form, sid) if command != "" else self.initialize(start_response)
            if body and command != "":
                start_response('200 OK', [('Content-Type',
                                           'text/html; charset=utf-8')])
            elif body:
                pass
            else:
                # якщо body - порожній рядок, то виникла помилка
                err = True
        else:
            # якщо команда невідома, то виникла помилка
            err = True
        if err:
            start_response('404 NOT FOUND', [('Content-Type',
                                              'text/plain; charset=utf-8')])
            body = 'Сторінку не знайдено'
        return [bytes(body, encoding='utf-8')]

    def initialize(self, start_response):
        self.guests[str(self.last_id)] = Guest(self.last_id)
        start_response('200 OK', [('Content-Type',
                                   'text/html; charset=utf-8'),
                                  ("Set-cookie", f"sid={self.last_id}")])
        self.last_id += 1
        return self.start(None, None)

    def _create_serching_tab(self, str1, str2):
        table = ""
        table += TABLE_ROW.format("    ".join([TABLE_COLUMN.format(st) for st in [str1, str2]]))
        return table

    def _create_table(self, data):
        table = ""
        for row in data:
            table += TABLE_ROW.format("".join([TABLE_COLUMN.format(x) for x in row[:-1]])
                                      + TABLE_COLUMN.format(IMAGE.format(row[-1]))
                                      + TABLE_COLUMN.format(BUTTON_ADD_TO_CART.format(row[0])))
        return table

    def start(self, form, sid):
        """Обробити команду початку роботи (/).
           Спрямувати клієнту сторінку входу до системи.
        """
        with open(MAIN_PAGE, encoding='utf-8') as f:
            # прочитати підготовлений html-файл
            cnt = f.read()
        return cnt.format(self._create_serching_tab(BUTTON_SEARCH_ART, BUTTON_SEARCH_CAT), BUTTON_SHOW_CART,
                          self._create_table(ADAPTER.get_table()))

    def search_art(self, form, sid):
        with open(MAIN_PAGE, encoding='utf-8') as f:
            art_name = form.getfirst("art_name", "")
            cnt = f.read()
        return cnt.format(self._create_serching_tab(BUTTON_SEARCH_ART, BUTTON_SEARCH_CAT), BUTTON_SHOW_CART,
                          self._create_table(ADAPTER.name_search(art_name)))

    def search_cat(self, form, sid):
        with open(MAIN_PAGE, encoding='utf-8') as f:
            cat_name = form.getfirst("cat_name", "")
            cnt = f.read()
        return cnt.format(self._create_serching_tab(BUTTON_SEARCH_ART, BUTTON_SEARCH_CAT), BUTTON_SHOW_CART,
                          self._create_table(ADAPTER.category_search(cat_name)))

    def remove(self, form, sid):
        with open(CART_PAGE, encoding='utf-8') as f:
            cnt = f.read()
            art_id = int(form.getfirst("id", ""))
            self.guests[sid].remove_from_cart(art_id)
        return cnt.format(self._create_cart(self.guests[sid].look_into_cart(), sid),
                          self.guests[sid].get_full_price())

    def add_to_cart(self, form, sid):
        with open(CART_PAGE, encoding='utf-8') as f:
            cnt = f.read()
            art_id = int(form.getfirst("id", ""))
            if form.getfirst("quantity", "").isdigit():
                quantity = int(form.getfirst("quantity", ""))
                if quantity > 0:
                    self.guests[sid].add_to_cart(art_id, *ADAPTER.get_by_id(art_id), quantity)
                    return cnt.format(self._create_cart(self.guests[sid].look_into_cart(), sid),
                                      self.guests[sid].get_full_price())
        return self.start(form, sid)

    def show_cart(self, form, sid):
        with open(CART_PAGE, encoding='utf-8') as f:
            cnt = f.read()
        return cnt.format(self._create_cart(self.guests[sid].look_into_cart(), sid),
                          self.guests[sid].get_full_price())

    def _create_cart(self, cart, sid):
        table = ""
        for art in cart:
            table += TABLE_ROW.format("".join([TABLE_COLUMN.format(x) for x in art])
                                      + TABLE_COLUMN.format(BUTTON_DELETE_FROM_CART.format(art[0])))
        return table


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print('=== Local WSGI webserver ===')
    httpd = make_server('localhost', 8051, MyServer())
    host, port = httpd.server_address
    print(f"http://localhost:{port}")
    print(httpd.socket)
    httpd.serve_forever()
